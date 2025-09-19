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
        # 3: {
        #     "name": "23CHYA",
        #     "slotsPerWeek": 1,
        # },
        # 4: {
        #     "name": "23CHYB",
        #     "slotsPerWeek": 3,
        # },
        # 5: {
        #     "name": "23CHYC",
        #     "slotsPerWeek": 2,
        # },
    },
    "batches": [
        "ELC-A",
        "ELC-B",
        "ELC-C",
    ],
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
        # 3: {
        #     "name": "teaiasoeitnarst",
        #     "course": "23CHYA",
        # },
        # 4: {
        #     "name": "teachernamiarsnoten3",
        #     "course": "23CHYB",
        # },
        # 5: {
        #     "name": "teachermgtmg3",
        #     "course": "23CHYC",
        # },
    },
}

if __name__ == "__main__":
    scheduler = Scheduler(data)
    scheduler.generate_table()
    scheduler.print_tables()
