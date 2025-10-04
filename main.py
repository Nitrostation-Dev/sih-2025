from typing import Dict, List
from timetable_scheduler.utils import parse_json

from timetable_scheduler.scheduler import Scheduler

if __name__ == "__main__":
    data = parse_json("data.json")

    scheduler = Scheduler(data)
    scheduler.generate_table_soft()
    scheduler.print_tables()
