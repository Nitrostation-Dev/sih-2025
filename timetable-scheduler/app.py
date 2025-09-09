from typing import Dict
import classes


class App:
    def __init__(self, data: Dict) -> None:
        self.slots_per_day = data["slotsPerDay"]
        self.days_per_week = data["daysPerWeek"]
        self.no_of_free_slot_after_working_slot = data["noOfFreeSlotAfterWorkingSlot"]

        self.courses = self.get_courses_from_data(data)
        self.teachers = self.get_teachers_from_data(data)
        self.classes = self.get_classes_from_data(data)

        print(self.slots_per_day)
        print(self.days_per_week)
        print(self.no_of_free_slot_after_working_slot)

    def get_courses_from_data(self, data: Dict) -> Dict[int, classes.Course]:
        courses = {}
        for i in data["courses"]:
            course_cls = classes.Course(
                i, data["courses"][i]["name"], data["courses"][i]["slotsPerWeek"]
            )
            courses[i] = course_cls

        return courses

    def get_course_id(self, name: str):
        for course in self.courses.values():
            if course.name == name:
                return course.id

        raise IndexError(f"course not found with name '{name}'")

    def get_teachers_from_data(self, data: Dict) -> Dict[int, classes.Teacher]:
        teachers = {}
        for i in data["teachers"]:
            teacher_cls = classes.Teacher(
                i,
                data["teachers"][i]["name"],
                self.get_course_id(data["teachers"][i]["course"]),
            )
            teachers[i] = teacher_cls

        return teachers

    def get_classes_from_data(self, data: Dict) -> Dict[int, classes.Class]:
        clss = {}
        for i, name in enumerate(data["classes"]):
            cls = classes.Class(i, name)
            clss[i] = cls

        return clss


if __name__ == "__main__":
    data = {
        "slotsPerDay": 8,
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
        "classes": [
            "ELC-A",
            "ELC-B",
        ],
        "teachers": {
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
