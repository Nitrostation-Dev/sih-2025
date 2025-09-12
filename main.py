from typing import Dict, List

from timetable_scheduler.scheduler import Scheduler

data = {
    "slotsPerDay": 2,
    "daysPerWeek": 5,
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
    },
    "batches": [
        "ELC-A",
        "ELC-B",
    ],
    "faculties": {
        0: {
            "name": "TeacherName1",
            "course": "23MAT",
        },
        1: {
            "name": "TeacherName2",
            "course": "23MEE",
        },
    },
}

if __name__ == "__main__":
    scheduler = Scheduler(data)
    scheduler.generate_table()
    scheduler.print_tables()
