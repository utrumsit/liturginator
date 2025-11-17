#!/usr/bin/env python3
"""
Gospel Readings Module for Byzantine Lectionary

Determines the Gospel reading for a given date based on the lunar calendar,
fixed feasts, and Lucan Jump rules.
"""

import json
from datetime import datetime, timedelta
from pascha import calculate_pascha

class GospelReader:
    def __init__(self, readings_file='scripture_readings.json'):
        with open(readings_file, 'r') as f:
            self.readings = json.load(f)

    def get_reading(self, date_str):
        """
        Get Gospel reading for the date.
        Returns dict with 'book', 'chapter', 'verses', 'text'.
        """
        dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        year = dt.year
        pascha = calculate_pascha(year)
        pentecost = pascha + timedelta(days=49)

        # Check for fixed feasts first
        month_day = f"{dt.month:02d}-{dt.day:02d}"
        if month_day in self.readings.get('fixed', {}):
            readings = self.readings['fixed'][month_day]
            for r in readings:
                if r['type'] == 'gospel':
                    return r

        # Determine season
        if dt < pascha:
            # Pre-Pascha: Lent or Triodion
            return self._get_lent_reading(dt, pascha)
        elif pascha <= dt < pentecost:
            # Pascha season
            return self._get_pascha_reading(dt, pascha)
        else:
            # Pentecostarion
            return self._get_pentecostarion_reading(dt, pentecost)

    def _get_fixed_feast(self, dt):
        # Now handled in get_reading
        pass

    def _get_lent_reading(self, dt, pascha):
        # Lent readings: special cycle, Lucan Jump
        days_before = (pascha - dt).days
        if 1 <= days_before <= 70:  # Great Lent
            week = (days_before - 1) // 7 + 1
            sunday_readings = self.readings.get('lent', {}).get(str(week), {}).get('sunday', [])
            for r in sunday_readings:
                if r['type'] == 'gospel':
                    return r
        return {"type": "gospel", "book": "Matthew", "chapter": 6, "verses": "14-21", "text": "Default Lent Gospel", "context": "Default"}

    def _get_pascha_reading(self, dt, pascha):
        days_since = (dt - pascha).days
        day_data = self.readings.get('pascha', {}).get(str(days_since), {})
        readings = day_data.get('readings', [])
        for r in readings:
            if r['type'] == 'gospel':
                return r
        return {"type": "gospel", "book": "John", "chapter": 1, "verses": "1-17", "text": "Default Pascha Gospel", "context": "Default"}

    def _get_pentecostarion_reading(self, dt, pentecost):
        days_since = (dt - pentecost).days
        if days_since == 0:
            # Pentecost Sunday
            readings = self.readings.get('pascha', {}).get('49', {}).get('readings', [])
        else:
            weeks_since = (days_since - 1) // 7
            day_of_week = (days_since - 1) % 7
            week_num = weeks_since + 1
            readings = self.readings.get('pentecostarion', {}).get(str(week_num), {}).get(str(day_of_week), {}).get('readings', [])
        for r in readings:
            if r['type'] == 'gospel':
                return r
        return {"type": "gospel", "book": "Matthew", "chapter": 28, "verses": "16-20", "text": "Default Pentecostarion Gospel", "context": "Default"}

# Example usage
if __name__ == '__main__':
    reader = GospelReader()
    reading = reader.get_reading('2023-03-15')
    print(reading)