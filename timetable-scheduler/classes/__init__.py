class Course:
    def __init__(self, id: int, name: str, slots_per_week: int) -> None:
        self.id = id
        self.name = name
        self.slots_per_week = slots_per_week

    def __str__(self) -> str:
        return f"Course ( id = {self.id}; name = {self.name}; slots_per_week = {self.slots_per_week}; )"


class Faculty:
    def __init__(self, id: int, name: str, courseId: int) -> None:
        self.id = id
        self.name = name
        self.courseId = courseId

    def __str__(self) -> str:
        return f"Faculty ( id = {self.id}; name = {self.name}; courseId = {self.courseId}; )"


class Batch:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return f"Batch ( id = {self.id}; name = {self.name}; )"
