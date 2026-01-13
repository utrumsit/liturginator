# Vespers Assembly Logic
# This file outlines the structure and conditional logic for assembling Vespers prayers.
# It serves as a guide for implementing the assembly in the main liturginator.py.

import json
import tone
import pascha
from menaion import Menaion
from datetime import datetime
import os
from vespers_prokeimenon import get_vespers_prokeimenon, format_prokeimenon
from vespers_paramia import get_vespers_paramia, format_paramia_output

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

        # 3. Introductory Prayers
        parts.append(self.get_intro_prayers())

        # 4. Psalm 103
        parts.append(self.get_psalm103())

        # 5. Great Litany
        parts.append(self.get_great_litany())

        # 6. Kathisma (if applicable)
        parts.append(self.get_kathisma())

        # 7. Lamplighting Psalms with Stichera
        parts.append(self.get_stichera())

        # 8. O Joyful Light
        parts.append(self.get_o_joyful_light())

        # 9. Prokeimenon
        parts.append(self.get_prokeimenon())

        # 10. Readings (if any)
        parts.append(self.get_readings())

        # 11. Troparion/Theotokion
        parts.append(self.get_troparion_theotokion())

        # 12. Dismissal
        parts.append(self.get_dismissal())

        return '\n\n'.join(parts)

    def get_blessing(self):
        return "Blessed is our God, always, now and ever and forever."

    def get_come_let_us_worship(self):
        return "Come, let us worship our King and God.\nCome, let us worship Christ, our King and God.\nCome, let us worship and bow before the only Lord Jesus Christ, the King and our God."

    def get_intro_prayers(self):
        with open(os.path.join(os.path.dirname(__file__), 'resource', 'introductory_prayers.md'), 'r') as f:
            return f.read()

    def get_psalm103(self):
        with open(os.path.join(os.path.dirname(__file__), 'resource', 'psalm103.md'), 'r') as f:
            return f.read()

    def get_great_litany(self):
        with open(os.path.join(os.path.dirname(__file__), 'resource', 'great_litany.md'), 'r') as f:
            return f.read()

    def get_kathisma(self):
        # Placeholder: implement using kathismata.py
        return "### Kathisma\n\n*Kathisma text goes here.*"

    def get_o_joyful_light(self):
        with open(os.path.join(os.path.dirname(__file__), 'resource', 'o_joyful_light.md'), 'r') as f:
            return f.read()

    def get_psalms(self):
        # Placeholder: Psalm 103 or others
        return "Psalm 103: Bless the Lord, O my soul..."

    def get_prokeimenon(self):
        dt = datetime.strptime(self.date, '%Y-%m-%d').date()
        feast_level = self.feast.get('feast_level', 0) if self.feast else 0
        result = get_vespers_prokeimenon(dt, feast_level)
        return format_prokeimenon(result['data'], result['type'])

    def get_readings(self):
        dt = datetime.strptime(self.date, '%Y-%m-%d').date()
        result = get_vespers_paramia(dt)
        return format_paramia_output(result)

    def get_stichera(self):
        # Load octoechos data
        with open('octoechos_stichera.json', 'r') as f:
            octoechos = json.load(f)
        with open('octoechos_theotokia.json', 'r') as f:
            theotokia = json.load(f)

        # Get day of week
        dt = datetime.strptime(self.date, '%Y-%m-%d').date()
        weekday = dt.weekday()  # 0=mon, 1=tue, ..., 6=sun
        days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        day_name = days[weekday]  # Wait, 0=mon -> monday, but we want sunday for 6
        # Python: 0 mon -> monday, 6 sun -> saturday? No:
        # days[0] = sunday, but weekday 0 = mon, so days[(weekday + 1) % 7]
        day_name = days[(weekday + 1) % 7]  # weekday 0 mon -> 1 monday? Wait
        # To map: sunday = 6, monday=0, etc? No.
        # Better: day_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][weekday]
        day_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][weekday]

        # Get octoechos stichera
        oct_stich = octoechos.get(str(self.tone_num), {}).get(day_name, [])[:3]

        # Get menaion stichera
        men_stich = []
        if self.feast and self.feast.get('vespers', {}).get('stichera_lord_i_cried'):
            men_stich = [s['text'] for s in self.feast['vespers']['stichera_lord_i_cried'][:3]]

        # Combine
        all_stich = oct_stich + men_stich

        # Glory sticheron
        glory_stich = ""
        if self.feast and self.feast.get('vespers', {}).get('glory_sticheron'):
            glory_stich = self.feast['vespers']['glory_sticheron']['text']

        # Theotokion
        theotok = theotokia.get(str(self.tone_num), {}).get('standard', [''])[0]

        # Load base psalms
        resource_dir = os.path.join(os.path.dirname(__file__), 'resource')
        with open(os.path.join(resource_dir, 'lamplighting_psalms.md'), 'r') as f:
            psalms = f.read()

        # Insert stichera
        for i, stich in enumerate(all_stich):
            marker = f"**On {6-i}:**"
            psalms = psalms.replace(marker, f"{stich}\n{marker}", 1)

        # Insert glory
        if glory_stich:
            psalms = psalms.replace("Glory to the Father and to the Son and to the Holy Spirit;", f"{glory_stich}\nGlory to the Father and to the Son and to the Holy Spirit;", 1)

        # Insert theotokion
        if theotok:
            psalms = psalms.replace("Now and ever and unto ages of ages. Amen.", f"{theotok}\nNow and ever and unto ages of ages. Amen.", 1)

        return psalms

    def get_troparion_theotokion(self):
        parts = []
        if self.feast and self.feast.get('troparia'):
            troparion = self.feast['troparia'].get('main', {}).get('text', '')
            if troparion:
                parts.append(f"### Troparion\n\n{troparion}")
        theotok = self.get_theotokion()
        if theotok:
            parts.append(f"### Theotokion\n\n{theotok}")
        return '\n\n'.join(parts) if parts else "### Troparion/Theotokion\n\n*Text here.*"

    def get_theotokion(self):
        with open('octoechos_theotokia.json', 'r') as f:
            theotokia = json.load(f)
        return theotokia.get(str(self.tone_num), {}).get('standard', [''])[0]

    def get_dismissal(self):
        return "Dismissal for Vespers"