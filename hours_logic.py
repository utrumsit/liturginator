# Hours Assembly Logic
# This file outlines the structure and conditional logic for assembling Hours prayers.
# It serves as a guide for implementing the assembly in the main liturginator.py.

import json
import tone
import pascha
from menaion import Menaion
from datetime import datetime

class HoursAssembler:
    def __init__(self, date, hour=1):
        self.date = date
        self.hour = hour  # 1, 3, 6, 9
        self.is_lent = pascha.is_lent(date)
        dt = datetime.strptime(date, '%Y-%m-%d').date()
        self.tone_num = tone.get_tone(dt)
        self.men = Menaion()
        self.month = dt.strftime('%B')
        self.day = dt.day
        self.feast = self.men.get_feast(self.month, self.day)

    def assemble(self):
        """
        Assemble the full Hours text based on date and conditions.
        Returns a string of the assembled prayers.
        """
        parts = []

        # 1. Blessing
        parts.append(self.get_blessing())

        # 2. Trisagion
        parts.append(self.get_trisagion())

        # 3. Troparion
        parts.append(self.get_troparion())

        # 4. Theotokion
        parts.append(self.get_theotokion())

        # 5. Dismissal
        parts.append(self.get_dismissal())

        return '\n\n'.join(parts)

    def get_blessing(self):
        return "Blessed is our God, always, now and ever and forever."

    def get_trisagion(self):
        return "Holy God, Holy Mighty, Holy Immortal, have mercy on us."

    def get_troparion(self):
        if self.feast:
            return self.feast.get('troparia', {}).get('troparion', 'Troparion text')
        return "Troparion text"

    def get_theotokion(self):
        with open('theotokia.json', 'r') as f:
            theotokia = json.load(f)
        return theotokia.get(self.tone_num, {}).get('standard', [''])[0]

    def get_dismissal(self):
        return f"Dismissal for {self.hour} Hour"