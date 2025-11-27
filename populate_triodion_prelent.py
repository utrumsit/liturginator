#!/usr/bin/env python3
import json

data = {
  "triodion": {
    "publican_pharisee": {
      "title": "Sunday of the Publican and the Pharisee",
      "readings": [
        {
          "type": "epistle",
          "book": "2 Timothy",
          "chapter": 3,
          "verses": "10-15",
          "text": "",
          "context": "2 Timothy 3:10-15"
        },
        {
          "type": "gospel",
          "book": "Luke",
          "chapter": 18,
          "verses": "10-14",
          "text": "",
          "context": "Luke 18:10-14"
        }
      ]
    },
    "34": {
      "0": {
        "title": "Monday of 34th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 Peter",
            "chapter": 1,
            "verses": "20-2:9",
            "text": "",
            "context": "2 Peter 1:20-2:9"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 13,
            "verses": "9-13",
            "text": "",
            "context": "Mark 13:9-13"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 34th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 Peter",
            "chapter": 2,
            "verses": "9-22",
            "text": "",
            "context": "2 Peter 2:9-22"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 13,
            "verses": "14-23",
            "text": "",
            "context": "Mark 13:14-23"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 34th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 Peter",
            "chapter": 3,
            "verses": "1-18",
            "text": "",
            "context": "2 Peter 3:1-18"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 13,
            "verses": "24-31",
            "text": "",
            "context": "Mark 13:24-31"
          }
        ]
      },
      "3": {
        "title": "Thursday of 34th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 John",
            "chapter": 1,
            "verses": "8-2:6",
            "text": "",
            "context": "1 John 1:8-2:6"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 13,
            "verses": "31-14:2",
            "text": "",
            "context": "Mark 13:31-14:2"
          }
        ]
      },
      "4": {
        "title": "Friday of 34th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 John",
            "chapter": 2,
            "verses": "7-17",
            "text": "",
            "context": "1 John 2:7-17"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 14,
            "verses": "3-9",
            "text": "",
            "context": "Mark 14:3-9"
          }
        ]
      },
      "5": {
        "title": "Saturday of 34th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 Timothy",
            "chapter": 3,
            "verses": "1-9",
            "text": "",
            "context": "2 Timothy 3:1-9"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 20,
            "verses": "46-21:4",
            "text": "",
            "context": "Luke 20:46-21:4"
          }
        ]
      },
      "6": {
        "title": "Sunday of the Prodigal Son",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Corinthians",
            "chapter": 6,
            "verses": "12-20",
            "text": "",
            "context": "1 Corinthians 6:12-20"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 15,
            "verses": "11-32",
            "text": "",
            "context": "Luke 15:11-32"
          }
        ]
      }
    },
    "35": {
      "0": {
        "title": "Monday of 35th Week after Pentecost (Meatfare Week)",
        "readings": [
          {
            "type": "epistle",
            "book": "1 John",
            "chapter": 2,
            "verses": "18-3:10a",
            "text": "",
            "context": "1 John 2:18-3:10a"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 11,
            "verses": "1-11",
            "text": "",
            "context": "Mark 11:1-11"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 35th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 John",
            "chapter": 3,
            "verses": "10b-20",
            "text": "",
            "context": "1 John 3:10b-20"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 14,
            "verses": "10-42",
            "text": "",
            "context": "Mark 14:10-42"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 35th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 John",
            "chapter": 3,
            "verses": "21-4:6",
            "text": "",
            "context": "1 John 3:21-4:6"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 14,
            "verses": "43-15:1",
            "text": "",
            "context": "Mark 14:43-15:1"
          }
        ]
      },
      "3": {
        "title": "Thursday of 35th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 John",
            "chapter": 4,
            "verses": "20-5:21",
            "text": "",
            "context": "1 John 4:20-5:21"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 15,
            "verses": "1-15",
            "text": "",
            "context": "Mark 15:1-15"
          }
        ]
      },
      "4": {
        "title": "Friday of 35th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 John",
            "chapter": 1,
            "verses": "1-13",
            "text": "",
            "context": "2 John 1:1-13"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 15,
            "verses": "22, 25, 33-41",
            "text": "",
            "context": "Mark 15:22, 25, 33-41"
          }
        ]
      },
      "5": {
        "title": "Meatfare Saturday: Saturday of Souls",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Corinthians",
            "chapter": 10,
            "verses": "23-28",
            "text": "",
            "context": "1 Corinthians 10:23-28"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 21,
            "verses": "8-9, 25-27, 33-36",
            "text": "",
            "context": "Luke 21:8-9, 25-27, 33-36"
          },
          {
            "type": "epistle",
            "book": "1 Thessalonians",
            "chapter": 4,
            "verses": "13-17",
            "text": "",
            "context": "1 Thessalonians 4:13-17"
          },
          {
            "type": "gospel",
            "book": "John",
            "chapter": 5,
            "verses": "24-30",
            "text": "",
            "context": "John 5:24-30"
          }
        ]
      },
      "6": {
        "title": "Meatfare Sunday: The Sunday of the Last Judgment",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Corinthians",
            "chapter": 8,
            "verses": "8-9:2",
            "text": "",
            "context": "1 Corinthians 8:8-9:2"
          },
          {
            "type": "gospel",
            "book": "Matthew",
            "chapter": 25,
            "verses": "31-46",
            "text": "",
            "context": "Matthew 25:31-46"
          }
        ]
      }
    },
    "36": {
      "0": {
        "title": "Monday of 36th Week after Pentecost (Cheesefare Week)",
        "readings": [
          {
            "type": "epistle",
            "book": "3 John",
            "chapter": 1,
            "verses": "1-15",
            "text": "",
            "context": "3 John 1:1-15"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 19,
            "verses": "29-40; 22:7-39",
            "text": "",
            "context": "Luke 19:29-40; 22:7-39"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 36th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Jude",
            "chapter": 1,
            "verses": "1-10",
            "text": "",
            "context": "Jude 1-10"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 22,
            "verses": "39-42, 45b-23:1",
            "text": "",
            "context": "Luke 22:39-42, 45b-23:1"
          }
        ]
      },
      "2": {
        "title": "Wednesday of Cheesefare Week",
        "readings": [
          {
            "type": "other",
            "book": "Joel",
            "chapter": 2,
            "verses": "12-26",
            "text": "",
            "context": "Joel 2:12-26 Sixth Hour"
          }
        ],
        "vespers_paramia": [
          {
            "book": "Joel",
            "chapter": 4,
            "verses": "12-21 (or 3:12-21)",
            "text": "",
            "context": "Joel 4:12-21 (or 3:12-21)"
          }
        ]
      },
      "3": {
        "title": "Thursday of Cheesefare Week",
        "readings": [
          {
            "type": "epistle",
            "book": "Jude",
            "chapter": 1,
            "verses": "11-25",
            "text": "",
            "context": "Jude 1:11-25"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 23,
            "verses": "1-34, 44-56",
            "text": "",
            "context": "Luke 23:1-34, 44-56"
          }
        ]
      },
      "4": {
        "title": "Friday of Cheesefare Week",
        "readings": [
          {
            "type": "other",
            "book": "Zechariah",
            "chapter": 8,
            "verses": "7-17",
            "text": "",
            "context": "Zechariah 8:7-17 Sixth Hour"
          }
        ],
        "vespers_paramia": [
          {
            "book": "Zechariah",
            "chapter": 8,
            "verses": "19-23",
            "text": "",
            "context": "Zechariah 8:19-23"
          }
        ]
      },
      "5": {
        "title": "Cheesefare Saturday: Commemoration of Holy Ascetics",
        "readings": [
          {
            "type": "epistle",
            "book": "Romans",
            "chapter": 14,
            "verses": "19-23;16:25-27",
            "text": "",
            "context": "Romans 14:19-23;16:25-27"
          },
          {
            "type": "gospel",
            "book": "Matthew",
            "chapter": 6,
            "verses": "1-13",
            "text": "",
            "context": "Matthew 6:1-13"
          },
          {
            "type": "epistle",
            "book": "Galatians",
            "chapter": 5,
            "verses": "22-6:2",
            "text": "",
            "context": "Galatians 5:22-6:2"
          },
          {
            "type": "gospel",
            "book": "Matthew",
            "chapter": 11,
            "verses": "27-30",
            "text": "",
            "context": "Matthew 11:27-30"
          }
        ]
      },
      "6": {
        "title": "Cheesefare Sunday: The Sunday of Forgiveness",
        "readings": [
          {
            "type": "epistle",
            "book": "Romans",
            "chapter": 13,
            "verses": "11b-14:4",
            "text": "",
            "context": "Romans 13:11b-14:4"
          },
          {
            "type": "gospel",
            "book": "Matthew",
            "chapter": 6,
            "verses": "14-21",
            "text": "",
            "context": "Matthew 6:14-21"
          }
        ]
      }
    }
  }
}

try:
    with open('scripture_readings.json', 'r') as f:
        existing = json.load(f)
except:
    existing = {}

if 'triodion' not in existing:
    existing['triodion'] = {}

for key, value in data['triodion'].items():
    existing['triodion'][key] = value

with open('scripture_readings.json', 'w') as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)

print('Pre-Lent Triodion populated.')
