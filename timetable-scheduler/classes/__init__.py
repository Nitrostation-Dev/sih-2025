class Course:
    def __init__(self, id: int, name: str, slots_per_week: int) -> None:
        self.id = id
        self.name = name
        self.slots_per_week = slots_per_week


class Teacher:
    def __init__(self, id: int, name: str, courseId: int) -> None:
        self.id = id
        self.name = name
        self.courseId = courseId


class Class:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
