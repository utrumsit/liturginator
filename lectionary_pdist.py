#!/usr/bin/env python3
"""
Lectionary based on pascha distance (pdist) using orthocal's algorithm.

Algorithm credit: orthocal-python by Brian Glass
https://github.com/brianglass/orthocal-python

This implementation uses orthocal's reading schedule but fetches text from RSV.
"""

import json
import datetime
from pascha import calculate_pascha

try:
    from rsv_extractor import RSVExtractor
    RSV_AVAILABLE = True
except ImportError:
    RSV_AVAILABLE = False

class LectionaryPdist:
    """Lectionary using pascha distance for lookups."""
    
    def __init__(self, readings_file='orthocal_complete_lectionary.json', rsv_xml_path=None):
        with open(readings_file, 'r') as f:
            data = json.load(f)
            # Convert string keys to integers for paschal cycle
            self.paschal_cycle = {int(k): v for k, v in data.get('paschal_cycle', {}).items()}
            self.fixed_feasts = data.get('fixed_feasts', {})
        
        # Initialize RSV extractor if requested and available
        self.rsv_extractor = None
        if rsv_xml_path and RSV_AVAILABLE:
            self.rsv_extractor = RSVExtractor(rsv_xml_path)
        elif rsv_xml_path:
            print("Warning: RSV extraction requested but rsv_extractor module not available")
    
    def get_readings(self, date):
        """
        Get readings for a given date.
        
        Args:
            date: datetime.date object
            
        Returns:
            dict with 'title', 'epistle', 'gospel'
        """
        # Calculate pascha distance
        year = date.year
        pascha = calculate_pascha(year)
        
        # Adjust for liturgical year (before Pascha = previous year)
        if date < pascha:
            pascha = calculate_pascha(year - 1)
        
        pdist = (date - pascha).days
        
        # Calculate key dates for this liturgical year
        liturgical_year = pascha.year
        key_dates = self._calculate_key_dates(liturgical_year, pascha)
        
        # Get adjusted pdists for epistle and gospel
        epistle_pdist = self._get_epistle_pdist(pdist, key_dates)
        gospel_pdist = self._get_gospel_pdist(pdist, date, key_dates, pascha)
        
        # Check for fixed feast
        date_key = f"{date.month:02d}-{date.day:02d}"
        feast_info = self.fixed_feasts.get(date_key, {})
        feast_level = feast_info.get('feast_level', 0)
        feast_name = feast_info.get('feast_name', '')
        
        # Get daily cycle readings (always available)
        daily_epistle = None
        daily_gospel = None
        if epistle_pdist is not None and epistle_pdist in self.paschal_cycle:
            daily_epistle = self.paschal_cycle[epistle_pdist].get('epistle')
        if gospel_pdist is not None and gospel_pdist in self.paschal_cycle:
            daily_gospel = self.paschal_cycle[gospel_pdist].get('gospel')
        
        # Get saint/feast readings if available
        saint_epistle = None
        saint_gospel = None
        if feast_info.get('readings'):
            for reading in feast_info['readings']:
                if reading['type'] == 'epistle' and not saint_epistle:
                    saint_epistle = reading.copy()
                elif reading['type'] == 'gospel' and not saint_gospel:
                    saint_gospel = reading.copy()
        
        # Determine primary readings based on feast level
        # Level >= 6: Major feasts completely replace daily cycle
        # Level 4-5: Saints' feasts - show both
        # Level < 2: Minor commemorations - daily cycle primary
        if feast_level >= 6:
            # Major feast only
            epistle = saint_epistle
            gospel = saint_gospel
        elif feast_level >= 2:
            # Show both daily and saint readings (primary = daily)
            epistle = daily_epistle
            gospel = daily_gospel
        else:
            # Daily cycle only
            epistle = daily_epistle
            gospel = daily_gospel
        
        # Add RSV text if extractor is available
        if self.rsv_extractor:
            # Add to primary readings
            if epistle and epistle.get('display'):
                rsv_text = self.rsv_extractor.extract_text(epistle['display'])
                if rsv_text:
                    epistle['rsv_text'] = rsv_text
            if gospel and gospel.get('display'):
                rsv_text = self.rsv_extractor.extract_text(gospel['display'])
                if rsv_text:
                    gospel['rsv_text'] = rsv_text
            
            # Add to saint readings
            if saint_epistle and saint_epistle.get('display'):
                rsv_text = self.rsv_extractor.extract_text(saint_epistle['display'])
                if rsv_text:
                    saint_epistle['rsv_text'] = rsv_text
            if saint_gospel and saint_gospel.get('display'):
                rsv_text = self.rsv_extractor.extract_text(saint_gospel['display'])
                if rsv_text:
                    saint_gospel['rsv_text'] = rsv_text
            
            # Add to daily readings (if different from primary)
            if daily_epistle and daily_epistle.get('display'):
                rsv_text = self.rsv_extractor.extract_text(daily_epistle['display'])
                if rsv_text:
                    daily_epistle['rsv_text'] = rsv_text
            if daily_gospel and daily_gospel.get('display'):
                rsv_text = self.rsv_extractor.extract_text(daily_gospel['display'])
                if rsv_text:
                    daily_gospel['rsv_text'] = rsv_text
        
        # Generate title
        title = self._generate_title(pdist, date, key_dates)
        
        result = {
            'title': title,
            'pdist': pdist,
            'epistle_pdist': epistle_pdist,
            'gospel_pdist': gospel_pdist,
            'epistle': epistle,
            'gospel': gospel,
        }
        
        # Add feast information if present
        if feast_name:
            result['feast_name'] = feast_name
            result['feast_level'] = feast_level
        
        # Add saint readings if different from primary
        if feast_level >= 2 and feast_level < 6:
            # Both daily and saint readings available
            result['saint_epistle'] = saint_epistle
            result['saint_gospel'] = saint_gospel
            result['daily_epistle'] = daily_epistle
            result['daily_gospel'] = daily_gospel
        
        return result
    
    def _calculate_key_dates(self, year, pascha):
        """Calculate key liturgical dates for the year."""
        
        # Exaltation of the Cross (September 14)
        exaltation = datetime.date(year, 9, 14)
        exaltation_pdist = (exaltation - pascha).days
        
        # Sunday after Exaltation
        weekday_exalt = exaltation_pdist % 7  # 0=Sunday
        sun_after_elevation = exaltation_pdist + 7 - weekday_exalt
        
        # Nativity (December 25)
        nativity = datetime.date(year, 12, 25)
        nativity_pdist = (nativity - pascha).days
        
        # Theophany (January 6, next year)
        theophany = datetime.date(year + 1, 1, 6)
        theophany_pdist = (theophany - pascha).days
        weekday_theo = theophany_pdist % 7
        sat_before_theophany = theophany_pdist - (weekday_theo + 1) % 7 - 1
        sun_after_theophany = theophany_pdist + 7 - weekday_theo
        
        # Forefathers Sunday
        weekday_nat = nativity_pdist % 7
        forefathers = nativity_pdist - 14 + ((7 - weekday_nat) % 7)
        
        # First Sunday of Luke
        first_sun_luke = sun_after_elevation + 7
        
        # Lukan Jump calculation
        eighteenth_monday = 50 + 7*17  # Pentecost Monday + 17 weeks
        mon_after_elevation = sun_after_elevation + 1
        lukan_jump = eighteenth_monday - mon_after_elevation
        
        return {
            'sun_after_elevation': sun_after_elevation,
            'sat_before_theophany': sat_before_theophany,
            'sun_after_theophany': sun_after_theophany,
            'forefathers': forefathers,
            'first_sun_luke': first_sun_luke,
            'lukan_jump': lukan_jump,
            'nativity': nativity_pdist,
            'theophany': theophany_pdist,
        }
    
    def _get_epistle_pdist(self, pdist, key_dates):
        """
        Get adjusted pdist for epistle lookup.
        Epistles mostly follow the paschal cycle without the lukan jump.
        """
        # TODO: Handle end-of-year wraparound (pdist > ~320)
        # For now, just return the actual pdist
        return pdist
    
    def _get_gospel_pdist(self, pdist, date, key_dates, pascha):
        """
        Get adjusted pdist for gospel lookup.
        This is where the Lukan Jump magic happens.
        """
        # Step 1: Special case - 11th Sunday of Luke = Forefathers
        weekday = pdist % 7
        if pdist == key_dates['first_sun_luke'] + 10*7:
            return key_dates['forefathers'] + key_dates['lukan_jump']
        
        # Step 2: Sundays after Theophany use "reserve" gospels
        # (Skipping this for now - requires calculating reserves)
        
        # Step 3: After Saturday before Theophany - jump to next year
        if pdist > key_dates['sat_before_theophany']:
            next_pascha = calculate_pascha(pascha.year + 1)
            return (date - next_pascha).days
        
        # Step 4: After Sunday after Exaltation - apply Lukan Jump
        if pdist > key_dates['sun_after_elevation']:
            return pdist + key_dates['lukan_jump']
        
        # Step 5: Default - no adjustment
        return pdist
    
    def _generate_title(self, pdist, date, key_dates):
        """Generate a human-readable title for the day."""
        weekday = pdist % 7
        weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        if pdist == 0:
            return "Great and Holy Pascha"
        elif pdist == 49:
            return "Pentecost"
        elif 0 < pdist < 50:
            week = pdist // 7 + 1
            return f"{weekday_names[weekday]} of the {self._ordinal(week)} week of Pascha"
        elif pdist >= 50:
            week = (pdist - 50) // 7 + 1
            return f"{weekday_names[weekday]} of the {self._ordinal(week)} week after Pentecost"
        else:
            week = abs(pdist) // 7 + 1
            return f"{weekday_names[weekday]} of the {self._ordinal(week)} week before Pascha"
    
    def _ordinal(self, n):
        """Convert number to ordinal (1st, 2nd, 3rd, etc.)"""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"


def main():
    """Command-line interface."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python lectionary_pdist.py YYYY-MM-DD [--rsv]")
        print("  --rsv: Include RSV text extraction from rsv.xml")
        sys.exit(1)
    
    date_str = sys.argv[1]
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Check for --rsv flag
    use_rsv = '--rsv' in sys.argv
    rsv_path = 'rsv.xml' if use_rsv else None
    
    lect = LectionaryPdist(rsv_xml_path=rsv_path)
    result = lect.get_readings(date)
    
    print(json.dumps(result, indent=2, default=str))


if __name__ == '__main__':
    main()
