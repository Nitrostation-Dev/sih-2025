from typing import Dict, List

from timetable_scheduler.scheduler import Scheduler

data = {
    "slotsPerDay": 6,
    "daysPerWeek": 6,
    "noOfFreeSlotAfterWorkingSlot": 1,
    "courses": {
        0: {
            "name": "23MAT",
            "slotsPerWeek": 5,
        },
        1: {
            "name": "23MEE",
            "slotsPerWeek": 3,
        },
        2: {
            "name": "23CHY",
            "slotsPerWeek": 5,
        },
    },
    # "batches": [
    #     "ELC-A",
    #     "ELC-B",
    #     "ELC-C",
    # ],
    "batches": {
        0: {"name": "ELC-A", "courses": ["23MAT", "23MEE", "23CHY"]},
        1: {"name": "ELC-B", "courses": ["23MAT", "23MEE"]},
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
    },
}

if __name__ == "__main__":
    scheduler = Scheduler(data)
    scheduler.generate_table()
    scheduler.print_tables()
