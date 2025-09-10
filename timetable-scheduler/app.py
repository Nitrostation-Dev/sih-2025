from typing import Dict, List
import classes


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

    def is_free_course(self) -> bool:
        if self.courseId != -1:
            return False

        return True

    def is_free_faculty(self) -> bool:
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
        return self.batchId_assignedClasses_map[batchId].is_free_course()


class App:
    def __init__(self, data: Dict) -> None:
        self.slots_per_day = data["slotsPerDay"]
        self.days_per_week = data["daysPerWeek"]
        self.no_of_free_slot_after_working_slot = data["noOfFreeSlotAfterWorkingSlot"]

        self.batches: Dict[int, classes.Batch] = self.get_classes_from_data(data)
        self.courses: Dict[int, classes.Course] = self.get_courses_from_data(data)
        self.faculties: Dict[int, classes.Faculty] = self.get_teachers_from_data(data)

        self.course_faculty_map = self.generate_course_teachers_map()

        print("Slots Per Day: ", self.slots_per_day)
        print("Days Per Week: ", self.days_per_week)
        print("No Of Free Slot After Working Slot", self.no_of_free_slot_after_working_slot)
        
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
        self.print_slots_table()

    def create_free_slots(self) -> None:
        for dayNo in range(self.days_per_week):
            slots: List[Slot] = []
            for slotNo in range(self.slots_per_day):
                slots.append(Slot(slotNo + 1, list(self.batches.keys())))

            self.working_days[dayNo] = slots

    def generate_table(self) -> None:
        # 1. Pick a Batch to work with
        # 2. Fill the Batch Slots with Courses
        # 3. Pick Faculty for Each Course

        def fill_single_slot_per_day(self, batchId: int, courseId: int, course: classes.Course):
            for dayIndex, day in self.working_days.items():
                for slotIndex, slot in enumerate(day):
                    if not slot.is_free(batchId):
                        continue

                    if not course.request_slot(batchId):
                        return
                    
                    slot.batchId_assignedClasses_map[batchId].assign_courseId(
                        courseId
                    )
                    print("Assigned Course")
                    break

        for batchId in self.batches:
            for courseId, course in self.courses.items():
                print("Working With", courseId)
                fill_single_slot_per_day(self, batchId, courseId, course)

    # TODO
    def print_slots_table(self) -> None:
        for day_i, day in self.working_days.items():
            for slot_no, slot in enumerate(day):
                print("Day: ", day_i)
                print("Slot No: ", slot_no)
                print("Slot: \n", slot, sep="")
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
    app.generate_table()
    print("=============================================================")
    app.print_slots_table()
