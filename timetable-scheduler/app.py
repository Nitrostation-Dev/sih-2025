from typing import Dict, List
from tabulate import tabulate

class AssignedClassData:
    def __init__(self, batchId: int) -> None:
        self.courseId = -1
        self.facultyId = -1
        self.batchId = batchId

    def assign_courseId(self, courseId: int) -> None:
        if self.courseId != -1:
            raise ValueError(
                f"Course Already assigned. Course Id to Assign: {courseId}; but already assigned to {self.courseId}"
            )

        self.courseId = courseId

    def assign_facultyId(self, facultyId: int) -> None:
        if self.facultyId != -1:
            raise ValueError(
                f"Faculty Already assigned. Faculty Id to Assign: {facultyId}; but already assigned to {self.facultyId}"
            )

        self.facultyId = facultyId

    def is_course_free(self) -> bool:
        if self.courseId != -1:
            return False

        return True

    def is_faculty_free(self) -> bool:
        if self.facultyId != -1:
            return False

        return True


class Slot:
    def __init__(self, slot_no: int, batchIds: List[int]) -> None:
        self.slot_no = slot_no

        self.batchId_assignedClasses_map: Dict[int, AssignedClassData] = {}
        for id in batchIds:
            self.batchId_assignedClasses_map[id] = AssignedClassData(id)

    def __str__(self) -> str:
        string = ""
        for batchId, data in self.batchId_assignedClasses_map.items():
            string += f"\nBatchId: {batchId}; CourseId: {data.courseId}; FacultyId: {data.facultyId}"

        return string

    def is_free(self, batchId: int) -> bool:
        return self.batchId_assignedClasses_map[batchId].is_course_free()

    def get_data(self, batchId: int) -> AssignedClassData:
        return self.batchId_assignedClasses_map[batchId]

    def is_faculty_free(self, facultyId: int) -> bool:
        for data in self.batchId_assignedClasses_map.values():
            if data.facultyId == facultyId:
                return False

        return True


class App:
    def __init__(self, data: Dict) -> None:
        self.slots_per_day = data["slotsPerDay"]
        self.days_per_week = data["daysPerWeek"]
        self.no_of_free_slot_after_working_slot = data["noOfFreeSlotAfterWorkingSlot"]

        self.batches: Dict[int, classes.Batch] = self.get_classes_from_data(data)
        self.courses: Dict[int, classes.Course] = self.get_courses_from_data(data)
        self.faculties: Dict[int, classes.Faculty] = self.get_teachers_from_data(data)

        self.course_faculty_map: Dict[int, List[int]] = (
            self.generate_course_teachers_map()
        )

        print("Slots Per Day: ", self.slots_per_day)
        print("Days Per Week: ", self.days_per_week)
        print(
            "No Of Free Slot After Working Slot",
            self.no_of_free_slot_after_working_slot,
        )

        print("\nCourses:")
        [print(key, ":", value, ";", end="") for key, value in self.courses.items()]
        print("\n\nFaculties")
        [print(key, ":", value, ";", end="") for key, value in self.faculties.items()]
        print("\n\nBatches")
        [print(key, ":", value, ";", end="") for key, value in self.batches.items()]
        print()
        print()

        self.working_days: Dict[int, List[Slot]] = {}
        self.create_free_slots()

    def create_free_slots(self) -> None:
        for dayNo in range(self.days_per_week):
            slots: List[Slot] = []
            for slotNo in range(self.slots_per_day):
                slots.append(Slot(slotNo + 1, list(self.batches.keys())))

            self.working_days[dayNo] = slots

    def exchange_slots(
        self, batchId: int, x_dayNo: int, x_slotNo: int, y_dayNo: int, y_slotNo: int
    ) -> None:
        _courseId = self.working_days[x_dayNo][x_slotNo].get_data(batchId).courseId
        _facultyId = self.working_days[x_dayNo][x_slotNo].get_data(batchId).facultyId

        self.working_days[x_dayNo][x_slotNo].batchId_assignedClasses_map[
            batchId
        ].courseId = (self.working_days[y_dayNo][y_slotNo].get_data(batchId).courseId)
        self.working_days[x_dayNo][x_slotNo].batchId_assignedClasses_map[
            batchId
        ].facultyId = (self.working_days[y_dayNo][y_slotNo].get_data(batchId).facultyId)

        self.working_days[y_dayNo][y_slotNo].batchId_assignedClasses_map[
            batchId
        ].courseId = _courseId
        self.working_days[y_dayNo][y_slotNo].batchId_assignedClasses_map[
            batchId
        ].facultyId = _facultyId

    def generate_table(self) -> None:
        # 1. Pick a Batch to work with
        # 2. Fill the Batch Slots with Courses
        # 3. Pick Faculty for Each Course
        def fill_single_slot_per_day(
            self, batchId: int, courseId: int, course: classes.Course
        ):
            for dayIndex, day in self.working_days.items():
                for slotIndex, slot in enumerate(day):
                    if not slot.is_free(batchId):
                        continue

                    if not course.request_slot(batchId):
                        return

                    slot.get_data(batchId).assign_courseId(courseId)
                    # print("Assigned Course")
                    break

        def assign_faculty(self: App, batchId: int):
            for dayNo, day in self.working_days.items():
                for slotNo, slot in enumerate(day):
                    if slot.is_free(batchId):
                        continue

                    data = slot.get_data(batchId)
                    facultyId = self.course_faculty_map[data.courseId][0]
                    # Since We are working with contraint that only one faculty per course

                    if slot.is_faculty_free(facultyId):
                        data.assign_facultyId(facultyId)
                        continue

                    for check_slotNo, check_slot in enumerate(day):
                        if check_slotNo == slotNo:
                            continue

                        if check_slot.is_free(batchId):
                            self.exchange_slots(
                                batchId, dayNo, slotNo, dayNo, check_slotNo
                            )
                        else:
                            if check_slot.get_data(batchId).is_faculty_free():
                                facultyIdToAssign = self.course_faculty_map[
                                    check_slot.get_data(batchId).courseId
                                ][0]
                                if slot.is_faculty_free(
                                    facultyIdToAssign
                                ) and check_slot.is_faculty_free(facultyId):
                                    check_slot.get_data(batchId).assign_facultyId(
                                        facultyIdToAssign
                                    )
                                    self.exchange_slots(
                                        batchId, dayNo, slotNo, dayNo, check_slotNo
                                    )

                            elif check_slot.is_faculty_free(
                                facultyId
                            ) and slot.is_faculty_free(
                                check_slot.get_data(batchId).facultyId
                            ):
                                self.exchange_slots(
                                    batchId, dayNo, slotNo, dayNo, check_slotNo
                                )

        # Fill Batch Slots with Courses
        while not self.is_all_courses_filled():
            for batchId in self.batches:
                for courseId, course in self.courses.items():
                    fill_single_slot_per_day(self, batchId, courseId, course)

        # # Assign Faculty
        # for batchId in self.batches:
        #     assign_faculty(self, batchId)
        #
        # for id in self.batches:
        #     while self.is_all_faculty_assigned(id):
        #         for batchId in self.batches:
        #             assign_faculty(self, batchId)

    def is_all_courses_filled(self) -> bool:
        for course in self.courses.values():
            for batchId in self.batches:
                if course.batchIds_slotsTrack_map[batchId]["slotsNeeded"] != 0:
                    return False

        return True

    def is_all_faculty_assigned(self, batchId: int) -> bool:
        for day in self.working_days.values():
            for slot in day:
                if slot.get_data(batchId).is_faculty_free():
                    return False

        return True

    # TODO
    def print_slots_table(self) -> None:
        for batchId in self.batches:
            batch_table = []
            for dayNo, day in self.working_days.items():
                day_slots = []
                for slotNo, slot in enumerate(day):
                    if slot.is_free(batchId):
                        day_slots.append("-")
                        continue

                    text = ""
                    text += (
                        f"Course: {self.courses[slot.get_data(batchId).courseId].name}"
                    )

                    if slot.get_data(batchId).facultyId == -1:
                        day_slots.append(text)
                        continue

                    text += f"    Faculty: {self.faculties[slot.get_data(batchId).facultyId].name}"
                    day_slots.append(text)

                batch_table.append(day_slots)

            print("For Batch: ", self.batches[batchId].name)
            print(
                tabulate(
                    batch_table,
                    headers=[str(i + 1) for i in range(self.slots_per_day)],
                    tablefmt="github",
                )
            )
            print()

    def get_course_id(self, name: str):
        for course in self.courses.values():
            if course.name == name:
                return course.id

        raise IndexError(f"course not found with name '{name}'")

    def get_courses_from_data(self, data: Dict) -> Dict[int, classes.Course]:
        courses = {}
        for i in data["courses"]:
            course_cls = classes.Course(
                i,
                data["courses"][i]["name"],
                data["courses"][i]["slotsPerWeek"],
                list(self.batches.keys()),
            )
            courses[i] = course_cls

        return courses

    def get_teachers_from_data(self, data: Dict) -> Dict[int, classes.Faculty]:
        teachers = {}
        for i in data["faculties"]:
            teacher_cls = classes.Faculty(
                i,
                data["faculties"][i]["name"],
                self.get_course_id(data["faculties"][i]["course"]),
            )
            teachers[i] = teacher_cls

        return teachers

    def get_classes_from_data(self, data: Dict) -> Dict[int, classes.Batch]:
        batches = {}
        for i, name in enumerate(data["batches"]):
            batch = classes.Batch(i, name)
            batches[i] = batch

        return batches

    def generate_course_teachers_map(self) -> Dict[int, List[int]]:
        course_teacher_map = {}
        for course in self.courses.values():
            for teacher in self.faculties.values():
                if teacher.courseId == course.id:
                    course_teacher_map[course.id] = [teacher.courseId]

        return course_teacher_map


if __name__ == "__main__":
    data = {
        "slotsPerDay": 8,
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
            2: {
                "name": "23CHY",
                "slotsPerWeek": 4,
            },
        },
        "batches": [
            "ELC-A",
            "ELC-B",
            "ELC-C",
            "ELC-D",
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
            2: {
                "name": "TeacherName3",
                "course": "23CHY",
            },
        },
    }

    app = App(data)
    app.generate_table()
    print("=============================================================")
    app.print_slots_table()
