#!/usr/bin/env python3
"""
Populate scripture_readings.json with the 29th Sunday after Pentecost.
"""

import json

def main():
    readings = {
        'pentecostarion': {
            '3': {  # Luke cycle
                '6': [  # 6th Sunday of Luke
                    {
                        'type': 'epistle',
                        'book': '2 Corinthians',
                        'chapter': 9,
                        'verses': '6-11',
                        'text': 'The point is this: he who sows sparingly will also reap sparingly, and he who sows bountifully will also reap bountifully. Each one must do as he has made up his mind, not reluctantly or under compulsion, for God loves a cheerful giver. And God is able to provide you with every blessing in abundance, so that you may always have enough of everything and may provide in abundance for every good work. As it is written, "He scatters abroad, he gives to the poor; his righteousness endures for ever." He who supplies seed to the sower and bread for food will supply and multiply your resources and increase the harvest of your righteousness. You will be enriched in every way for great generosity, which through us will produce thanksgiving to God;',
                        'context': '2 Corinthians 9:6-11'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Luke',
                        'chapter': 16,
                        'verses': '19-31',
                        'text': 'There was a rich man, who was clothed in purple and fine linen and who feasted sumptuously every day. And at his gate lay a poor man named Laz\'arus, full of sores, who desired to be fed with what fell from the rich man\'s table; moreover the dogs came and licked his sores. The poor man died and was carried by the angels to Abraham\'s bosom. The rich man also died and was buried; and in Hades, being in torment, he lifted up his eyes, and saw Abraham far off and Laz\'arus in his bosom. And he called out, "Father Abraham, have mercy upon me, and send Laz\'arus to dip the end of his finger in water and cool my tongue; for I am in anguish in this flame." But Abraham said, "Son, remember that you in your lifetime received your good things, and Laz\'arus in like manner evil things; but now he is comforted here, and you are in anguish. And besides all this, between us and you a great chasm has been fixed, in order that those who would pass from here to you may not be able, and none may cross from there to us." And he said, "Then I beg you, father, to send him to my father\'s house, for I have five brothers, so that he may warn them, lest they also come into this place of torment." But Abraham said, "They have Moses and the prophets; let them hear them." And he said, "No, father Abraham; but if some one goes to them from the dead, they will repent." He said to them, "If they do not hear Moses and the prophets, neither will they be convinced if some one should rise from the dead."',
                        'context': 'Luke 16:19-31'
                    }
                ]
            }
        }
    }
    # Load existing and merge
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'pentecostarion' not in existing:
        existing['pentecostarion'] = {}
    existing['pentecostarion'].update(readings['pentecostarion'])
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()