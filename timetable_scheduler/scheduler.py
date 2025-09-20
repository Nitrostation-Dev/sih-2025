from typing import Dict, List

from timetable_scheduler.utils import print_tables
from .models import Faculty, Batch, Course, Slot


class Scheduler:
    def __init__(self, data: Dict) -> None:
        self.days_per_week = data["daysPerWeek"]
        self.slots_per_day = data["slotsPerDay"]
        self.no_of_free_slot_after_working_slot = data["noOfFreeSlotAfterWorkingSlot"]

        self.courses_by_id_map: Dict[int, Course] = self.create_courses_from_data(data)
        self.batches_by_id_map: Dict[int, Batch] = self.create_batches_from_data(data)
        self.faculties_by_id_map: Dict[int, Faculty] = self.create_faculties_from_data(
            data
        )

        self.faculty_ids_by_course_id_map: Dict[int, List[int]] = (
            self.generate_faculty_by_course_map()
        )

        self.working_days: List[List[Slot]] = self.create_slots()

    def create_slots(self) -> List[List[Slot]]:
        working_days = []
        for day_index in range(self.days_per_week):
            slots: List[Slot] = []
            for slot_index in range(self.slots_per_day):
                slots.append(Slot(slot_index + 1, list(self.batches_by_id_map.keys())))

            working_days.append(slots)

        return working_days

    def exchange_slots(
        self,
        batch_id: int,
        x_day_index: int,
        x_slot_index: int,
        y_day_index: int,
        y_slot_index: int,
    ) -> None:
        x_slot_data = self.working_days[x_day_index][x_slot_index].get_batch_slot_data(
            batch_id
        )
        y_slot_data = self.working_days[y_day_index][y_slot_index].get_batch_slot_data(
            batch_id
        )

        _course_id = x_slot_data.course_id
        _faculty_id = x_slot_data.faculty_id

        x_slot_data.assign_course_faculty(
            y_slot_data.course_id, y_slot_data.faculty_id, force_assign=True
        )
        y_slot_data.assign_course_faculty(_course_id, _faculty_id, force_assign=True)

    def generate_table(self) -> None:
        is_first_batch = True
        for batch_id, batch in self.batches_by_id_map.items():
            for course_id in batch.course_ids:
                course = self.courses_by_id_map[course_id]
                for day in self.working_days:
                    for slot in day:
                        # Assign Courses for first batch
                        if not slot.is_free_slot(batch_id):
                            continue

                        if is_first_batch:
                            if not course.request_slot(batch_id):
                                continue

                            faculty_id = self.faculty_ids_by_course_id_map[course.id][0]

                            batch_data = slot.get_batch_slot_data(batch_id)
                            batch_data.assign_course_faculty(course.id, faculty_id)

                            break
                        else:
                            faculty_id = self.faculty_ids_by_course_id_map[course.id][0]

                            if slot.is_faculty_booked(faculty_id):
                                continue

                            if not course.request_slot(batch_id):
                                continue

                            batch_data = slot.get_batch_slot_data(batch_id)
                            batch_data.assign_course_faculty(course.id, faculty_id)

                            break

            is_first_batch = False

    def are_all_courses_assigned(self) -> bool:
        for course in self.courses_by_id_map.values():
            for batchId in self.batches_by_id_map:
                if course.assigned_slot_countdown_by_batch_ids[batchId] != 0:
                    return False

        return True

    def are_faculties_assigned_to_courses(self, batch_id=-1) -> bool:
        for day in self.working_days:
            for slot in day:
                if batch_id == -1:
                    for batch_id in self.batches_by_id_map.keys():
                        if not slot.get_batch_slot_data(batch_id).is_faculty_assigned():
                            return False

                if (
                    not slot.get_batch_slot_data(batch_id).is_faculty_assigned()
                    and slot.get_batch_slot_data(batch_id).is_course_assigned()
                ):
                    return False

        return True

    def print_tables(self) -> None:
        print_tables(
            self.working_days,
            self.batches_by_id_map,
            self.courses_by_id_map,
            self.faculties_by_id_map,
        )

    def get_course_id(self, course_name: str) -> int:
        for course in self.courses_by_id_map.values():
            if course.name == course_name:
                return course.id

        raise Exception(f"Couldn't Find Course with Name: {course_name}")

    def create_courses_from_data(self, data: Dict) -> Dict[int, Course]:
        courses = {}
        for i in data["courses"]:
            course_cls = Course(
                i,
                data["courses"][i]["name"],
                data["courses"][i]["slotsPerWeek"],
            )
            courses[i] = course_cls

        return courses

    def create_faculties_from_data(self, data: Dict) -> Dict[int, Faculty]:
        teachers = {}
        for i in data["faculties"]:
            teacher_cls = Faculty(
                i,
                data["faculties"][i]["name"],
                self.get_course_id(data["faculties"][i]["course"]),
            )
            teachers[i] = teacher_cls

        return teachers

    def create_batches_from_data(self, data: Dict) -> Dict[int, Batch]:
        batches = {}
        for i in data["batches"]:
            course_ids = []
            for course in data["batches"][i]["courses"]:
                course_ids.append(self.get_course_id(course))

            batch = Batch(i, data["batches"][i]["name"], course_ids)
            batches[i] = batch

        return batches

    def generate_faculty_by_course_map(self) -> Dict[int, List[int]]:
        faculty_by_course_map = {}
        for course in self.courses_by_id_map.values():
            for faculty in self.faculties_by_id_map.values():
                if faculty.course_id == course.id:
                    faculty_by_course_map[course.id] = [faculty.course_id]

        return faculty_by_course_map
