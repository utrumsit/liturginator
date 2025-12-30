#!/usr/bin/env python3
"""
COMPLETE Byzantine Catholic Lectionary Generator - orthocal logic ported
Forefathers, Sunday before Nativity, Theophany afterfeasts, ALL FIXED
"""
import json
import datetime
from pascha import calculate_pascha

try:
    from rsv_extractor import RSVExtractor
    RSV_AVAILABLE = True
except ImportError:
    RSV_AVAILABLE = False

FLOAT_FEASTS = {
    1007: "Sunday before Exaltation",  # Galatians 6.11-18 | John 3.13-17
    1009: "Sunday after Exaltation",   # Galatians 2.16-20 | Mark 8.34-9.1
    1010: "Forefathers Sunday",        # Colossians 3.4-11 | Luke 14.16-24
    1012: "Sunday before Nativity",    # Hebrews 11.9-10,17-23,32-40 | Matthew 1.1-25
    1020: "Sunday after Nativity",     # Galatians 1.11-19 | Matthew 2.13-23
    1024: "Sunday before Theophany",   # 2 Timothy 4.5-8 | Mark 1.1-8
    1030: "Sunday after Theophany",    # Ephesians 4.7-13 | Matthew 4.12-17
}

class LectionaryPdist:
    def __init__(self, readings_file='orthocal_complete_lectionary.json', rsv_xml_path=None):
        with open(readings_file, 'r') as f:
            data = json.load(f)
            self.paschal_cycle = {int(k): v for k, v in data.get('paschal_cycle', {}).items()}
            self.fixed_feasts = data.get('fixed_feasts', {})
        
        self.rsv_extractor = None
        if rsv_xml_path and RSV_AVAILABLE:
            self.rsv_extractor = RSVExtractor(rsv_xml_path)
    
    def get_readings(self, date_obj):
        year = date_obj.year
        pascha = calculate_pascha(year)
        
        if date_obj < pascha:
            pascha = calculate_pascha(year - 1)
        
        pdist = (date_obj - pascha).days
        key_dates = self._calculate_key_dates(pascha.year, pascha)
        
        epistle_pdist = self._get_epistle_pdist(pdist, key_dates)
        gospel_pdist = self._get_gospel_pdist(pdist, date_obj, key_dates, pascha)
        
        date_key = f"{date_obj.month:02d}-{date_obj.day:02d}"
        feast_info = self.fixed_feasts.get(date_key, {})
        feast_level = feast_info.get('feast_level', 0)
        feast_name = feast_info.get('feast_name', '')
        
        # Check for floating feast override
        float_feast = None
        if date_obj.weekday() == 6:  # Sunday
            days_to_nativity = (date_obj.replace(month=12, day=25) - date_obj).days
            if 11 <= days_to_nativity <= 17:  # Forefathers range
                float_feast = 1010
            elif date_obj.month == 12 and 18 <= date_obj.day <= 24:  # Sunday before Nativity
                float_feast = 1012
            elif date_obj.month == 12 and date_obj.day >= 26:  # Sunday after Nativity
                float_feast = 1020
            elif date_obj.month == 1 and date_obj.day <= 5:  # Sunday before Theophany
                float_feast = 1024
            elif date_obj.month == 1 and date_obj.day >= 7:  # Sunday after Theophany
                float_feast = 1030
        
        if float_feast:
            cycle = self.paschal_cycle.get(float_feast, {})
            daily_epistle = cycle.get('epistle')
            daily_gospel = cycle.get('gospel')
            feast_name = FLOAT_FEASTS.get(float_feast, feast_name)
            feast_level = max(feast_level, 4)
        else:
            daily_epistle = self.paschal_cycle.get(epistle_pdist, {}).get('epistle') if epistle_pdist else None
            daily_gospel = self.paschal_cycle.get(gospel_pdist, {}).get('gospel') if gospel_pdist else None
        
        # Saint readings from fixed feast
        saint_epistle = None
        saint_gospel = None
        if feast_info.get('readings'):
            for reading in feast_info['readings']:
                if reading['type'] == 'epistle' and not saint_epistle:
                    saint_epistle = reading.copy()
                elif reading['type'] == 'gospel' and not saint_gospel:
                    saint_gospel = reading.copy()
        
        # Determine primary readings
        if feast_level >= 6:
            epistle = saint_epistle
            gospel = saint_gospel
        elif feast_level >= 2:
            epistle = daily_epistle
            gospel = daily_gospel
        else:
            epistle = daily_epistle
            gospel = daily_gospel
        
        # Add RSV text
        if self.rsv_extractor:
            for reading in [epistle, gospel, saint_epistle, saint_gospel, daily_epistle, daily_gospel]:
                if reading and reading.get('display'):
                    rsv_text = self.rsv_extractor.extract_text(reading['display'])
                    if rsv_text:
                        reading['rsv_text'] = rsv_text
        
        result = {
            'title': self._generate_title(pdist, date_obj, key_dates, feast_name),
            'pdist': pdist,
            'epistle_pdist': epistle_pdist,
            'gospel_pdist': gospel_pdist,
            'epistle': epistle,
            'gospel': gospel,
        }
        
        if feast_name:
            result['feast_name'] = feast_name
            result['feast_level'] = feast_level
        
        if feast_level >= 2 and feast_level < 6:
            result['saint_epistle'] = saint_epistle
            result['saint_gospel'] = saint_gospel
            result['daily_epistle'] = daily_epistle
            result['daily_gospel'] = daily_gospel
        
        return result
    
    def _calculate_key_dates(self, year, pascha):
        exaltation = datetime.date(year, 9, 14)
        exaltation_pdist = (exaltation - pascha).days
        sun_after_elevation = exaltation_pdist + 7 - (exaltation_pdist % 7)
        
        nativity = datetime.date(year, 12, 25)
        nativity_pdist = (nativity - pascha).days
        
        return {
            'sun_after_elevation': sun_after_elevation,
            'nativity': nativity_pdist,
        }
    
    def _get_epistle_pdist(self, pdist, key_dates):
        return pdist
    
    def _get_gospel_pdist(self, pdist, date_obj, key_dates, pascha):
        if pdist > key_dates['sun_after_elevation']:
            # Lukan jump: align gospel readings so Luke starts on Monday after
            # the Sunday after Elevation. The 18th Monday after Pentecost
            # (pdist 169) must fall on that day.
            # Formula: (49 + 1 + 7*17) - (sun_after_elevation + 1) = 168 - sun_after_elevation
            lukan_jump = 168 - key_dates['sun_after_elevation']
            return pdist + lukan_jump
        return pdist
    
    def _generate_title(self, pdist, date_obj, key_dates, feast_name):
        weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        weekday = pdist % 7
        
        if feast_name:
            return feast_name
        
        days_to_nativity = (date_obj.replace(month=12, day=25) - date_obj).days
        if 11 <= days_to_nativity <= 17 and date_obj.weekday() == 6:
            return "Forefathers Sunday"
        if date_obj.month == 12 and 18 <= date_obj.day <= 24:
            return f"Forefeast of the Nativity ({25 - date_obj.day} days)"
        
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
        if 10 <= (n % 100) <= 20:
            return f"{n}th"
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"
