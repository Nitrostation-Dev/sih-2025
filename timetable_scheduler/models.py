from typing import Dict, List


class Course:
    def __init__(
        self, id: int, name: str, slots_per_week: int
    ) -> None:
        self.id = id
        self.name = name
        self.slots_per_week = slots_per_week

        self.assigned_slot_countdown_by_batch_ids: Dict[int, int] = {}

    def __str__(self) -> str:
        return f"Course( id = {self.id}; name = {self.name}; slots_per_week = {self.slots_per_week}; )"

    def request_slot(self, batch_id: int) -> bool:
        if batch_id not in self.assigned_slot_countdown_by_batch_ids.keys():
            self.assigned_slot_countdown_by_batch_ids[batch_id] = self.slots_per_week - 1
            return True

        if self.assigned_slot_countdown_by_batch_ids[batch_id] == 0:
            return False

        self.assigned_slot_countdown_by_batch_ids[batch_id] -= 1
        return True


class Faculty:
    def __init__(self, id: int, name: str, course_id: int) -> None:
        self.id = id
        self.name = name
        self.course_id = course_id

    def __str__(self) -> str:
        return f"Faculty( id = {self.id}; name = {self.name}; courseId = {self.course_id}; )"


class Batch:
    def __init__(self, id: int, name: str, course_ids: List[int]) -> None:
        self.id = id
        self.name = name
        self.course_ids = course_ids

    def __str__(self) -> str:
        return f"Batch( id = {self.id}; name = {self.name}; )"


class SingleBatchSlotData:
    def __init__(self, batch_id: int) -> None:
        self.course_id = -1
        self.faculty_id = -1
        self.batchId = batch_id

    def assign_course(self, course_id: int) -> None:
        if self.course_id != -1:
            raise ValueError(
                f"Course Already assigned. Course Id to Assign: {course_id}; but already assigned to {self.course_id}"
            )

        self.course_id = course_id

    def assign_faculty(self, faculty_id: int) -> None:
        if self.faculty_id != -1:
            raise ValueError(
                f"Faculty Already assigned. Faculty Id to Assign: {faculty_id}; but already assigned to {self.faculty_id}"
            )

        if self.course_id == -1:
            raise ValueError(
                "Course Not Assigned to Slot, but trying to assign Faculty"
            )

        self.faculty_id = faculty_id

    def assign_course_faculty(
        self, course_id: int, faculty_id: int, force_assign=False
    ) -> None:
        if not force_assign:
            if self.course_id != -1:
                raise ValueError(
                    f"Course Already assigned. Course Id to Assign: {course_id}; but already assigned to {self.course_id}"
                )
            if self.faculty_id != -1:
                raise ValueError(
                    f"Faculty Already assigned. Faculty Id to Assign: {faculty_id}; but already assigned to {self.faculty_id}"
                )

        self.course_id = course_id
        self.faculty_id = faculty_id

    def is_course_assigned(self) -> bool:
        if self.course_id == -1:
            return False

        return True

    def is_faculty_assigned(self) -> bool:
        if self.faculty_id == -1:
            return False

        return True


class Slot:
    def __init__(self, slot_no: int, batch_ids: List[int]) -> None:
        self.slot_no = slot_no

        self.slot_data_by_batch_id_map: Dict[int, SingleBatchSlotData] = {}
        for id in batch_ids:
            self.slot_data_by_batch_id_map[id] = SingleBatchSlotData(id)

    def __str__(self) -> str:
        string = ""
        for batchId, data in self.slot_data_by_batch_id_map.items():
            string += f"\nBatchId: {batchId}; CourseId: {data.course_id}; FacultyId: {data.faculty_id}"

        return string

    def is_free_slot(self, batch_id: int) -> bool:
        return not self.slot_data_by_batch_id_map[batch_id].is_course_assigned()

    def get_batch_slot_data(self, batch_id: int) -> SingleBatchSlotData:
        return self.slot_data_by_batch_id_map[batch_id]

    def is_faculty_booked(self, faculty_id: int) -> bool:
        for data in self.slot_data_by_batch_id_map.values():
            if data.faculty_id == faculty_id:
                return True

        return False
