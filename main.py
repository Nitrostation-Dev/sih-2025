from typing import Dict, List

from timetable_scheduler.scheduler import Scheduler

data = {
    "slotsPerDay": 6,
    "daysPerWeek": 6,
    "noOfFreeSlotAfterWorkingSlot": 1,
    "courses": {
        0: {
            "name": "23MAT",
            "slotsPerWeek": 8,
        },
        1: {
            "name": "23MEE",
            "slotsPerWeek": 3,
        },
        2: {
            "name": "23CHY",
            "slotsPerWeek": 5,
        },
        3: {
            "name": "23ABC",
            "slotsPerWeek": 4,
        },
    },
    "batches": {
        0: {"name": "ELC-A", "courses": ["23MAT", "23MEE", "23CHY"]},
        1: {"name": "ELC-B", "courses": ["23MAT", "23MEE"]},
        2: {"name": "ELC-C", "courses": ["23MAT", "23MEE"]},
        3: {"name": "ELC-D", "courses": ["23MAT"]},
        4: {"name": "ELC-E", "courses": ["23MAT", "23MEE", "23ABC"]},
    },
    "faculties": {
        0: {
            "name": "TeacherName1",
            "course": "23MAT",
        },
        1: {
            "name": "teachername2",
            "course": "23MEE",
        },
        2: {
            "name": "teachername3",
            "course": "23CHY",
        },
        3: {
            "name": "teachername7",
            "course": "23ABC",
        },
    },
}

if __name__ == "__main__":
    scheduler = Scheduler(data)
    scheduler.generate_table()
    scheduler.print_tables()
