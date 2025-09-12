from typing import Dict, List

from timetable_scheduler.utils import print_tables
from .models import Faculty, Batch, Course, Slot


class Scheduler:
    def __init__(self, data: Dict) -> None:
        self.days_per_week = data["daysPerWeek"]
        self.slots_per_day = data["slotsPerDay"]
        self.no_of_free_slot_after_working_slot = data["noOfFreeSlotAfterWorkingSlot"]

        self.batches_by_id_map: Dict[int, Batch] = self.create_batches_from_data(data)
        self.courses_by_id_map: Dict[int, Course] = self.create_courses_from_data(data)
        self.faculties_by_id_map: Dict[int, Faculty] = self.create_faculties_from_data(
            data
        )

        self.faculty_ids_by_course_id_map: Dict[int, List[int]] = (
            self.generate_faculty_by_course_map()
        )

        # print("Slots Per Day: ", self.slots_per_day)
        # print("Days Per Week: ", self.days_per_week)
        # print(
        #     "No Of Free Slot After Working Slot",
        #     self.no_of_free_slot_after_working_slot,
        # )

        # print("\nCourses:")
        # [print(key, ":", value, ";", end="") for key, value in self.courses_by_id_map.items()]
        # print("\n\nFaculties")
        # [print(key, ":", value, ";", end="") for key, value in self.faculties_by_id_map.items()]
        # print("\n\nBatches")
        # [print(key, ":", value, ";", end="") for key, value in self.batches_by_id_map.items()]
        # print()
        # print()

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
        # 1. Pick a Batch to work with
        # 2. Fill the Batch Slots with Courses
        # 3. Pick Faculty for Each Course
        def assign_courses_per_day(
            self: Scheduler, batch_id: int, course_id: int
        ) -> None:
            for dayIndex, day in enumerate(self.working_days):
                for slotIndex, slot in enumerate(day):
                    if not slot.is_free_slot(batch_id):
                        continue

                    if not course.request_slot(batch_id):
                        return

                    slot.get_batch_slot_data(batch_id).assign_course(course_id)
                    break

        def assign_faculty(self: Scheduler) -> None:
            for batch_id in self.batches_by_id_map.keys():
                for day_index, day in enumerate(self.working_days):
                    for slot_index, slot in enumerate(day):
                        if slot.is_free_slot(batch_id):
                            continue

                        batch_data = slot.get_batch_slot_data(batch_id)
                        faculty_id = self.faculty_ids_by_course_id_map[
                            batch_data.course_id
                        ][0]

                        if slot.is_faculty_booked(faculty_id):
                            continue

                        batch_data.assign_faculty(faculty_id)

        def find_and_exchange_double_booked_slot_per_day(self: Scheduler) -> None:
            for day_index, day in enumerate(self.working_days):
                for slot_index, slot in enumerate(day):
                    for batch_id in self.batches_by_id_map.keys():
                        if self.are_faculties_assigned_to_courses(batch_id):
                            continue

                        batch_data = slot.get_batch_slot_data(batch_id)

                        if not slot.is_free_slot(
                            batch_id
                        ) and not batch_data.is_faculty_assigned():
                            # First Find if any free Slots available to exchange with
                            for check_slot_index, check_slot in enumerate(day):
                                if check_slot_index == slot_index:
                                    continue

                                if not check_slot.is_free_slot(batch_id):
                                    continue
                                
                                print("BOIII", batch_id, day_index, slot_index, check_slot_index)
                                self.exchange_slots(
                                    batch_id,
                                    day_index,
                                    slot_index,
                                    day_index,
                                    check_slot_index,
                                )
                                return

                            # Now Check for any suitable slots that are already assigned to exchange with
                            for check_slot_index, check_slot in enumerate(day):
                                if check_slot_index == slot_index:
                                    continue

                                if check_slot.is_free_slot(batch_id):
                                    continue

                                # TODO:
                                
                                # print("BOIII", batch_id, day_index, slot_index, check_slot_index)
                                # self.exchange_slots(
                                #     batch_id,
                                #     day_index,
                                #     slot_index,
                                #     day_index,
                                #     check_slot_index,
                                # )
                                # return


        # def assign_faculty(self: App, batchId: int):
        #     for dayNo, day in self.working_days.items():
        #         for slotNo, slot in enumerate(day):
        #             if slot.is_free(batchId):
        #                 continue
        #
        #             data = slot.get_data(batchId)
        #             facultyId = self.faculty_ids_by_course_id_map[data.courseId][0]
        #             # Since We are working with contraint that only one faculty per course
        #
        #             if slot.is_faculty_free(facultyId):
        #                 data.assign_facultyId(facultyId)
        #                 continue
        #
        #             for check_slotNo, check_slot in enumerate(day):
        #                 if check_slotNo == slotNo:
        #                     continue
        #
        #                 if check_slot.is_free(batchId):
        #                     self.exchange_slots(
        #                         batchId, dayNo, slotNo, dayNo, check_slotNo
        #                     )
        #                 else:
        #                     if check_slot.get_data(batchId).is_faculty_free():
        #                         facultyIdToAssign = self.faculty_ids_by_course_id_map[
        #                             check_slot.get_data(batchId).courseId
        #                         ][0]
        #                         if slot.is_faculty_free(
        #                             facultyIdToAssign
        #                         ) and check_slot.is_faculty_free(facultyId):
        #                             check_slot.get_data(batchId).assign_facultyId(
        #                                 facultyIdToAssign
        #                             )
        #                             self.exchange_slots(
        #                                 batchId, dayNo, slotNo, dayNo, check_slotNo
        #                             )
        #
        #                     elif check_slot.is_faculty_free(
        #                         facultyId
        #                     ) and slot.is_faculty_free(
        #                         check_slot.get_data(batchId).facultyId
        #                     ):
        #                         self.exchange_slots(
        #                             batchId, dayNo, slotNo, dayNo, check_slotNo
        #                         )

        # Fill Batch Slots with Courses
        for batchId in self.batches_by_id_map:
            for courseId, course in self.courses_by_id_map.items():
                assign_courses_per_day(self, batchId, courseId)

        assign_faculty(self)
        counter = 5
        while not self.are_faculties_assigned_to_courses() and counter != 0:
            find_and_exchange_double_booked_slot_per_day(self)
            assign_faculty(self)

        # # Assign Faculty
        # for batchId in self.batches:
        #     assign_faculty(self, batchId)
        #
        # for id in self.batches:
        #     while self.is_all_faculty_assigned(id):
        #         for batchId in self.batches:
        #             assign_faculty(self, batchId)

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
                
                if not slot.get_batch_slot_data(batch_id).is_faculty_assigned() and slot.get_batch_slot_data(batch_id).is_course_assigned():
                    return False

        return True

    def print_tables(self) -> None:
        print_tables(
            self.working_days,
            self.batches_by_id_map,
            self.courses_by_id_map,
            self.faculties_by_id_map,
        )

    # TODO
    # def print_slots_table(self) -> None:
    #     for batchId in self.batches_by_id_map:
    #         batch_table = []
    #         for dayNo, day in self.working_days.items():
    #             day_slots = []
    #             for slotNo, slot in enumerate(day):
    #                 if slot.is_free(batchId):
    #                     day_slots.append("-")
    #                     continue
    #
    #                 text = ""
    #                 text += f"Course: {self.courses_by_id_map[slot.get_data(batchId).courseId].name}"
    #
    #                 if slot.get_data(batchId).facultyId == -1:
    #                     day_slots.append(text)
    #                     continue
    #
    #                 text += f"    Faculty: {self.faculties_by_id_map[slot.get_data(batchId).facultyId].name}"
    #                 day_slots.append(text)
    #
    #             batch_table.append(day_slots)
    #
    #         print("For Batch: ", self.batches_by_id_map[batchId].name)
    #         print(
    #             tabulate(
    #                 batch_table,
    #                 headers=[str(i + 1) for i in range(self.slots_per_day)],
    #                 tablefmt="github",
    #             )
    #         )
    #         print()

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
                list(self.batches_by_id_map.keys()),
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
        for i, name in enumerate(data["batches"]):
            batch = Batch(i, name)
            batches[i] = batch

        return batches

    def generate_faculty_by_course_map(self) -> Dict[int, List[int]]:
        faculty_by_course_map = {}
        for course in self.courses_by_id_map.values():
            for faculty in self.faculties_by_id_map.values():
                if faculty.course_id == course.id:
                    faculty_by_course_map[course.id] = [faculty.course_id]

        return faculty_by_course_map
