from typing import Dict, List
from tabulate import tabulate

from timetable_scheduler.models import Course, Faculty, Slot, Batch

days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def print_tables(
    working_days: List[List[Slot]],

    batch_by_ids_map: Dict[int, Batch],
    course_by_id_map: Dict[int, Course],
    faculty_by_id_map: Dict[int, Faculty],
):
    for batch_id, batch in batch_by_ids_map.items():
        batch_table = []
        for day_index, day in enumerate(working_days):
            day_slots = [days[day_index]]
            for slot in day:
                if slot.is_free_slot(batch_id):
                    day_slots.append("-")
                    continue

                batch_data = slot.get_batch_slot_data(batch_id)

                text = f"Course: {course_by_id_map[batch_data.course_id].name}"
                if batch_data.is_faculty_assigned():
                    text += f"; Faculty: {faculty_by_id_map[batch_data.faculty_id].name}"

                day_slots.append(text)

            batch_table.append(day_slots)

        print(f"Batch: {batch.name}")
        print(
            tabulate(
                batch_table,
                headers=[str(i + 1) for i in range(len(working_days[0]))],
                tablefmt="github",
            )
        )
