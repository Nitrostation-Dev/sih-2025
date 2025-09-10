from typing import Dict, List
import classes


class AssignedClassData:
    # def __init__(self, courseId: int, teacherId: int, clsId: int) -> None:
    #     self.courseId = courseId
    #     self.teacherId = teacherId
    #     self.clsId = clsId
    #
    def __init__(self, batchId: int) -> None:
        self.courseId = -1
        self.facultyId = -1
        self.batchId = -1

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

    def assign_batchId(self, batchId: int) -> None:
        if self.batchId != -1:
            raise ValueError(
                f"Batch Already assigned. Batch Id to Assign: {batchId}; but already assigned to {self.batchId}"
            )

        self.batchId = batchId


class Slot:
    def __init__(self, slot_no: int, batchIds: List[int]) -> None:
        self.slot_no = slot_no

        self.assignedClasses: List[AssignedClassData] = [
            AssignedClassData(id) for id in batchIds
        ]


class App:
    def __init__(self, data: Dict) -> None:
        self.slots_per_day = data["slotsPerDay"]
        self.days_per_week = data["daysPerWeek"]
        self.no_of_free_slot_after_working_slot = data["noOfFreeSlotAfterWorkingSlot"]

        self.courses: Dict[int, classes.Course] = self.get_courses_from_data(data)
        self.faculties: Dict[int, classes.Faculty] = self.get_teachers_from_data(data)
        self.batches: Dict[int, classes.Batch] = self.get_classes_from_data(data)

        self.course_faculty_map = self.generate_course_teachers_map()

        print(self.slots_per_day)
        print(self.days_per_week)
        print(self.no_of_free_slot_after_working_slot)

        [print(key, ":", value, ";", end="") for key, value in self.courses.items()]
        print()
        [print(key, ":", value, ";", end="") for key, value in self.faculties.items()]
        print()
        [print(key, ":", value, ";", end="") for key, value in self.batches.items()]
        print()

        self.working_days: Dict[int, List[Slot]] = {}
        self.create_free_slots()
        print(self.working_days)

    def create_free_slots(self) -> None:
        for dayNo in range(self.days_per_week):
            slots: List[Slot] = []
            for slotNo in range(self.slots_per_day):
                slots.append(Slot(slotNo + 1, list(self.batches.keys())))

            self.working_days[dayNo] = slots

    def generate_table(self) -> None:
        pass

    def get_course_id(self, name: str):
        for course in self.courses.values():
            if course.name == name:
                return course.id

        raise IndexError(f"course not found with name '{name}'")

    def get_courses_from_data(self, data: Dict) -> Dict[int, classes.Course]:
        courses = {}
        for i in data["courses"]:
            course_cls = classes.Course(
                i, data["courses"][i]["name"], data["courses"][i]["slotsPerWeek"]
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
                    course_teacher_map[course.id] = teacher.courseId

        return course_teacher_map


if __name__ == "__main__":
    data = {
        "slotsPerDay": 2,
        "daysPerWeek": 5,
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

    app = App(data)
