#!/usr/bin/env python3
import json

readings = {
  "pentecostarion": {
    "29": {
      "0": {
        "title": "Monday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 3,
            "verses": "5-11, 17-19",
            "text": "",
            "context": "Hebrews 3:5-11, 17-19"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 20,
            "verses": "27-44",
            "text": "",
            "context": "Luke 20:27-44"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 4,
            "verses": "1-13",
            "text": "",
            "context": "Hebrews 4:1-13"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 21,
            "verses": "12-19",
            "text": "",
            "context": "Luke 21:12-19"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 5,
            "verses": "11-6:8",
            "text": "",
            "context": "Hebrews 5:11-6:8"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 21,
            "verses": "5-7, 10-11, 20-24",
            "text": "",
            "context": "Luke 21:5-7, 10-11, 20-24"
          }
        ]
      },
      "5": {
        "title": "Saturday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Ephesians",
            "chapter": 2,
            "verses": "11-13",
            "text": "",
            "context": "Ephesians 2:11-13"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 13,
            "verses": "18-29",
            "text": "",
            "context": "Luke 13:18-29"
          }
        ]
      },
      "3": {
        "title": "Thursday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 7,
            "verses": "1-6",
            "text": "",
            "context": "Hebrews 7:1-6"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 21,
            "verses": "28-33",
            "text": "",
            "context": "Luke 21:28-33"
          }
        ]
      },
      "4": {
        "title": "Friday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 7,
            "verses": "18-25",
            "text": "",
            "context": "Hebrews 7:18-25"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 21,
            "verses": "37-22:8",
            "text": "",
            "context": "Luke 21:37-22:8"
          }
        ]
      },
      "5": {
        "title": "Saturday of 29th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Ephesians",
            "chapter": 2,
            "verses": "11-13",
            "text": "",
            "context": "Ephesians 2:11-13"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 13,
            "verses": "18-29",
            "text": "",
            "context": "Luke 13:18-29"
          }
        ]
      },
      "6": {
        "title": "29th Sunday after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Colossians",
            "chapter": 3,
            "verses": "4-11",
            "text": "",
            "context": "Colossians 3:4-11"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 17,
            "verses": "12-19",
            "text": "",
            "context": "Luke 17:12-19"
          }
        ],
        "matins_gospel": {
          "book": "John",
          "chapter": 20,
          "verses": "1-10",
          "text": "",
          "context": "John 20:1-10"
        }
      }
    },
    "30": {
      "0": {
        "title": "Monday of 30th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 8,
            "verses": "7-13",
            "text": "",
            "context": "Hebrews 8:7-13"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 8,
            "verses": "11-21",
            "text": "",
            "context": "Mark 8:11-21"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 30th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 9,
            "verses": "8-10, 15-23",
            "text": "",
            "context": "Hebrews 9:8-10, 15-23"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 8,
            "verses": "22-26",
            "text": "",
            "context": "Mark 8:22-26"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 30th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 10,
            "verses": "1-18",
            "text": "",
            "context": "Hebrews 10:1-18"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 8,
            "verses": "30-34",
            "text": "",
            "context": "Mark 8:30-34"
          }
        ]
      },
      "3": {
        "title": "Thursday of 30th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 10,
            "verses": "35-11:7",
            "text": "",
            "context": "Hebrews 10:35-11:7"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 9,
            "verses": "10-16",
            "text": "",
            "context": "Mark 9:10-16"
          }
        ]
      },
      "4": {
        "title": "Friday of 30th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 11,
            "verses": "8, 11-16",
            "text": "",
            "context": "Hebrews 11:8, 11-16"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 9,
            "verses": "33-41",
            "text": "",
            "context": "Mark 9:33-41"
          }
        ]
      },
      "5": {
        "title": "Saturday of 30th Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Ephesians",
            "chapter": 5,
            "verses": "1-8",
            "text": "",
            "context": "Ephesians 5:1-8"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 14,
            "verses": "1-11",
            "text": "",
            "context": "Luke 14:1-11"
          }
        ]
      },
      "6": {
        "title": "30th Sunday after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Colossians",
            "chapter": 3,
            "verses": "12-16",
            "text": "",
            "context": "Colossians 3:12-16"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 18,
            "verses": "18-27",
            "text": "",
            "context": "Luke 18:18-27"
          }
        ],
        "matins_gospel": {
          "book": "John",
          "chapter": 20,
          "verses": "11-18",
          "text": "",
          "context": "John 20:11-18"
        }
      }
    },
    "31": {
      "0": {
        "title": "Monday of 31st Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 11,
            "verses": "17-23, 27-31",
            "text": "",
            "context": "Hebrews 11:17-23, 27-31"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 9,
            "verses": "42-10:1",
            "text": "",
            "context": "Mark 9:42-10:1"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 31st Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Hebrews",
            "chapter": 12,
            "verses": "25, 26, 13:22-25",
            "text": "",
            "context": "Hebrews 12:25, 26, 13:22-25"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 10,
            "verses": "2-12",
            "text": "",
            "context": "Mark 10:2-12"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 31st Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 1,
            "verses": "1-18",
            "text": "",
            "context": "James 1:1-18"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 10,
            "verses": "11b-16",
            "text": "",
            "context": "Mark 10:11b-16"
          }
        ]
      },
      "3": {
        "title": "Thursday of 31st Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 1,
            "verses": "19-27",
            "text": "",
            "context": "James 1:19-27"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 10,
            "verses": "17-27",
            "text": "",
            "context": "Mark 10:17-27"
          }
        ]
      },
      "4": {
        "title": "Friday of 31st Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 2,
            "verses": "1-13",
            "text": "",
            "context": "James 2:1-13"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 10,
            "verses": "23b-32a",
            "text": "",
            "context": "Mark 10:23b-32a"
          }
        ]
      },
      "5": {
        "title": "Saturday of 31st Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "Colossians",
            "chapter": 1,
            "verses": "3-6",
            "text": "",
            "context": "Colossians 1:3-6"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 16,
            "verses": "10-15",
            "text": "",
            "context": "Luke 16:10-15"
          }
        ]
      },
      "6": {
        "title": "31st Sunday after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Timothy",
            "chapter": 1,
            "verses": "15-17",
            "text": "",
            "context": "1 Timothy 1:15-17"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 18,
            "verses": "35-43",
            "text": "",
            "context": "Luke 18:35-43"
          }
        ],
        "matins_gospel": {
          "book": "John",
          "chapter": 20,
          "verses": "19-31",
          "text": "",
          "context": "John 20:19-31"
        }
      }
    },
    "32": {
      "0": {
        "title": "Monday of 32nd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 2,
            "verses": "14-26",
            "text": "",
            "context": "James 2:14-26"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 10,
            "verses": "46-52",
            "text": "",
            "context": "Mark 10:46-52"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 32nd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 3,
            "verses": "1-10",
            "text": "",
            "context": "James 3:1-10"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 11,
            "verses": "11-23",
            "text": "",
            "context": "Mark 11:11-23"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 32nd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 3,
            "verses": "11-4:6",
            "text": "",
            "context": "James 3:11-4:6"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 11,
            "verses": "22b-26",
            "text": "",
            "context": "Mark 11:22b-26"
          }
        ]
      },
      "3": {
        "title": "Thursday of 32nd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "James",
            "chapter": 4,
            "verses": "7-5:9",
            "text": "",
            "context": "James 4:7-5:9"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 11,
            "verses": "27-33",
            "text": "",
            "context": "Mark 11:27-33"
          }
        ]
      },
      "4": {
        "title": "Friday of 32nd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Peter",
            "chapter": 1,
            "verses": "1-2, 10-12, 2:6-10",
            "text": "",
            "context": "1 Peter 1:1-2, 10-12, 2:6-10"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 12,
            "verses": "1-12",
            "text": "",
            "context": "Mark 12:1-12"
          }
        ]
      },
      "5": {
        "title": "Saturday of 32nd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Thessalonians",
            "chapter": 5,
            "verses": "14-23",
            "text": "",
            "context": "1 Thessalonians 5:14-23"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 17,
            "verses": "3-10",
            "text": "",
            "context": "Luke 17:3-10"
          }
        ]
      },
      "6": {
        "title": "32nd Sunday after Pentecost (Sunday of Zacchaeus)",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Timothy",
            "chapter": 4,
            "verses": "9-15",
            "text": "",
            "context": "1 Timothy 4:9-15"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 19,
            "verses": "1-10",
            "text": "",
            "context": "Luke 19:1-10"
          }
        ],
        "matins_gospel": {
          "book": "John",
          "chapter": 21,
          "verses": "1-14",
          "text": "",
          "context": "John 21:1-14"
        }
      }
    },
    "33": {
      "0": {
        "title": "Monday of 33rd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Peter",
            "chapter": 2,
            "verses": "21b-3:9",
            "text": "",
            "context": "1 Peter 2:21b-3:9"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 12,
            "verses": "13-17",
            "text": "",
            "context": "Mark 12:13-17"
          }
        ]
      },
      "1": {
        "title": "Tuesday of 33rd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Peter",
            "chapter": 3,
            "verses": "10-22",
            "text": "",
            "context": "1 Peter 3:10-22"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 12,
            "verses": "18-27",
            "text": "",
            "context": "Mark 12:18-27"
          }
        ]
      },
      "2": {
        "title": "Wednesday of 33rd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Peter",
            "chapter": 4,
            "verses": "1-11",
            "text": "",
            "context": "1 Peter 4:1-11"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 12,
            "verses": "28-37",
            "text": "",
            "context": "Mark 12:28-37"
          }
        ]
      },
      "3": {
        "title": "Thursday of 33rd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Peter",
            "chapter": 4,
            "verses": "12-5:5",
            "text": "",
            "context": "1 Peter 4:12-5:5"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 12,
            "verses": "38-44",
            "text": "",
            "context": "Mark 12:38-44"
          }
        ]
      },
      "4": {
        "title": "Friday of 33rd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 Peter",
            "chapter": 1,
            "verses": "1-10a",
            "text": "",
            "context": "2 Peter 1:1-10a"
          },
          {
            "type": "gospel",
            "book": "Mark",
            "chapter": 13,
            "verses": "1-8",
            "text": "",
            "context": "Mark 13:1-8"
          }
        ]
      },
      "5": {
        "title": "Saturday of 33rd Week after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "2 Timothy",
            "chapter": 2,
            "verses": "11-19",
            "text": "",
            "context": "2 Timothy 2:11-19"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 18,
            "verses": "2-8a",
            "text": "",
            "context": "Luke 18:2-8a"
          }
        ]
      },
      "6": {
        "title": "33rd Sunday after Pentecost",
        "readings": [
          {
            "type": "epistle",
            "book": "1 Timothy",
            "chapter": 6,
            "verses": "11b-16",
            "text": "",
            "context": "1 Timothy 6:11b-16"
          },
          {
            "type": "gospel",
            "book": "Luke",
            "chapter": 18,
            "verses": "2-8a",
            "text": "",
            "context": "Luke 18:2-8a"
          }
        ],
        "matins_gospel": {
          "book": "John",
          "chapter": 21,
          "verses": "1-14",
          "text": "",
          "context": "John 21:1-14"
        }
      }
    }
  }
}

with open('scripture_readings.json', 'r') as f:
    existing = json.load(f)

existing['pentecostarion'].update(readings['pentecostarion'])

with open('scripture_readings.json', 'w') as f:
    json.dump(existing, f, indent=2)

print('31st week added.')
