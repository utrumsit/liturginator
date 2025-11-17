#!/usr/bin/env python3
"""
Epistle Readings Module for Byzantine Lectionary

Determines the Epistle reading for a given date.
"""

import json
from datetime import datetime, timedelta
from pascha import calculate_pascha

class EpistleReader:
    def __init__(self, readings_file='scripture_readings.json'):
        with open(readings_file, 'r', encoding='utf-8') as f:
            self.readings = json.load(f)

    def get_reading(self, date_str):
        """
        Get Epistle reading for the date.
        Similar logic to GospelReader.
        """
        dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        year = dt.year
        pascha = calculate_pascha(year)
        pentecost = pascha + timedelta(days=49)

        # Fixed feasts
        month_day = f"{dt.month:02d}-{dt.day:02d}"
        if month_day in self.readings.get('fixed', {}):
            readings = self.readings['fixed'][month_day]
            for r in readings:
                if r['type'] == 'epistle':
                    return r

        # Seasons
        if dt < pascha:
            return self._get_lent_reading(dt, pascha)
        elif pascha <= dt < pentecost:
            return self._get_pascha_reading(dt, pascha)
        else:
            return self._get_pentecostarion_reading(dt, pentecost)

    def _get_fixed_feast(self, dt):
        # Handled in get_reading
        pass

    def _get_lent_reading(self, dt, pascha):
        days_before = (pascha - dt).days
        if 1 <= days_before <= 70:
            week = (days_before - 1) // 7 + 1
            sunday_readings = self.readings.get('lent', {}).get(str(week), {}).get('sunday', [])
            for r in sunday_readings:
                if r['type'] == 'epistle':
                    return r
        return {"type": "epistle", "book": "Romans", "chapter": 13, "verses": "11b-14:4", "text": "Default Lent Epistle", "context": "Default"}

    def _get_pascha_reading(self, dt, pascha):
        days_since = (dt - pascha).days
        day_data = self.readings.get('pascha', {}).get(str(days_since), {})
        readings = day_data.get('readings', [])
        for r in readings:
            if r['type'] == 'epistle':
                return r
        return {"type": "epistle", "book": "Acts", "chapter": 1, "verses": "1-8", "text": "Default Pascha Epistle", "context": "Default"}

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
            if r['type'] == 'epistle':
                return r
        return {"type": "epistle", "book": "Hebrews", "chapter": 11, "verses": "33-12:2a", "text": "Default Pentecostarion Epistle", "context": "Default"}

# Example usage
if __name__ == '__main__':
    reader = EpistleReader()
    reading = reader.get_reading('2023-03-15')
    print(reading)