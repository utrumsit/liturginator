# Matins Assembly Logic
# This file outlines the structure and conditional logic for assembling Matins prayers.
# It serves as a guide for implementing the assembly in the main liturginator.py.

class MatinsAssembler:
    def __init__(self, date, is_lent=False):
        self.date = date
        self.is_lent = is_lent  # True if Great Forty Day Fast

    def assemble(self):
        """
        Assemble the full Matins text based on date and conditions.
        Returns a string of the assembled prayers.
        """
        parts = []

        # 1. Blessing (from introductory_prayers.md or similar)
        parts.append(self.get_blessing())

        # 2. Royal Service (conditional)
        if self.is_lent:
            parts.append(self.get_introductory_prayers())
        parts.append(self.get_royal_service())

        # 3. Hexapsalm (constant)
        parts.append(self.get_hexapsalm())

        # 4. The Lord is God (constant)
        parts.append(self.get_the_lord_is_god())

        # 5. Hymn of Light (variable by tone)
        parts.append(self.get_hymn_of_light(self.get_tone()))

        # 6. Exapostilarion (variable)
        parts.append(self.get_exapostilarion())

        # 7. Scripture Readings (variable)
        parts.append(self.get_scripture_readings())

        # 8. Canon (variable)
        parts.append(self.get_canon())

        # 9. Praises (constant)
        parts.append(self.get_praises())

        # 10. Dismissal (constant)
        parts.append(self.get_dismissal())

        return '\n\n'.join(parts)

    def get_blessing(self):
        # Load from introductory_prayers.md or hardcoded
        return "Blessed is our God, always, now and ever and forever."

    def get_introductory_prayers(self):
        # Load from introductory_prayers.md
        with open('resource/introductory_prayers.md', 'r') as f:
            return f.read()

    def get_royal_service(self):
        # Load from royal_service.md
        with open('resource/matins/royal_service.md', 'r') as f:
            return f.read()

    def get_the_lord_is_god(self):
        # Load from theLordisGod.md
        with open('resource/matins/theLordisGod.md', 'r') as f:
            return f.read()

    def get_hexapsalm(self):
        # Load from hexapsalm_matins.md
        with open('resource/matins/hexapsalm_matins.md', 'r') as f:
            return f.read()

    def get_tone(self):
        # Determine tone based on date (placeholder)
        return 1  # Example

    def get_hymn_of_light(self, tone):
        # Load or generate based on tone
        # Placeholder: return hymn for tone
        hymns = {
            1: "Send light, O Lord...",
            # etc.
        }
        return hymns.get(tone, "Hymn of Light")

    def get_exapostilarion(self):
        # Variable: select based on day
        return "Exapostilarion text"

    def get_scripture_readings(self):
        # Variable: prokeimenon, readings
        return "Scripture readings"

    def get_canon(self):
        # Variable: ode-based hymns
        return "Canon text"

    def get_praises(self):
        # Load from praises_matins.md
        with open('resource/matins/praises_matins.md', 'r') as f:
            return f.read()

    def get_dismissal(self):
        # Load from dismissal_matins.md
        with open('resource/matins/dismissal_matins.md', 'r') as f:
            return f.read()

# Example usage:
# assembler = MatinsAssembler(date='2023-03-15', is_lent=True)
# matins_text = assembler.assemble()
# print(matins_text)