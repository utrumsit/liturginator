# Vespers Assembly Logic
# This file outlines the structure and conditional logic for assembling Vespers prayers.
# It serves as a guide for implementing the assembly in the main liturginator.py.

import json
import tone
import pascha
from menaion import Menaion
from datetime import datetime

class VespersAssembler:
    def __init__(self, date):
        self.date = date
        self.is_lent = pascha.is_lent(date)
        dt = datetime.strptime(date, '%Y-%m-%d').date()
        self.tone_num = tone.get_tone(dt)
        self.men = Menaion()
        self.month = dt.strftime('%B')
        self.day = dt.day
        self.feast = self.men.get_feast(self.month, self.day)

    def assemble(self):
        """
        Assemble the full Vespers text based on date and conditions.
        Returns a string of the assembled prayers.
        """
        parts = []

        # 1. Blessing
        parts.append(self.get_blessing())

        # 2. Come, let us worship
        parts.append(self.get_come_let_us_worship())

        # 3. Psalm 103 (or other psalms)
        parts.append(self.get_psalms())

        # 4. Prokeimenon
        parts.append(self.get_prokeimenon())

        # 5. Readings (if any)
        parts.append(self.get_readings())

        # 6. Stichera
        parts.append(self.get_stichera())

        # 7. Troparion
        parts.append(self.get_troparion())

        # 8. Theotokion
        parts.append(self.get_theotokion())

        # 9. Dismissal
        parts.append(self.get_dismissal())

        return '\n\n'.join(parts)

    def get_blessing(self):
        return "Blessed is our God, always, now and ever and forever."

    def get_come_let_us_worship(self):
        return "Come, let us worship our King and God.\nCome, let us worship Christ, our King and God.\nCome, let us worship and bow before the only Lord Jesus Christ, the King and our God."

    def get_psalms(self):
        # Placeholder: Psalm 103 or others
        return "Psalm 103: Bless the Lord, O my soul..."

    def get_prokeimenon(self):
        # Variable by tone or feast
        return f"Prokeimenon for Tone {self.tone_num}"

    def get_readings(self):
        return "Scripture readings for Vespers"

    def get_stichera(self):
        # Variable: stichera for the day
        if self.feast:
            return f"Stichera for {self.feast.get('saints', ['the feast'])}"
        return "Stichera text"

    def get_troparion(self):
        if self.feast:
            return self.feast.get('troparia', {}).get('troparion', 'Troparion text')
        return "Troparion text"

    def get_theotokion(self):
        with open('theotokia.json', 'r') as f:
            theotokia = json.load(f)
        return theotokia.get(self.tone_num, {}).get('standard', [''])[0]

    def get_dismissal(self):
        return "Dismissal for Vespers"