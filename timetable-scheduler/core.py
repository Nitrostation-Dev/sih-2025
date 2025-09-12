from typing import Dict, List


class Course:
    def __init__(
        self, id: int, name: str, slots_per_week: int, batchIds: List[int]
    ) -> None:
        self.id = id
        self.name = name
        self.slots_per_week = slots_per_week

        self.batchIds_slotsTrack_map: Dict[int, Dict[str, int]] = {}
        for id in batchIds:
            self.batchIds_slotsTrack_map[id] = {
                "slotsNeeded": slots_per_week,
                "slotsRequired": slots_per_week,
            }

        print(
            "Created Course: ",
            name,
            " ; with slots tracker: ",
            self.batchIds_slotsTrack_map,
        )

    def __str__(self) -> str:
        return f"Course ( id = {self.id}; name = {self.name}; slots_per_week = {self.slots_per_week}; )"

    def request_slot(self, batchId: int) -> bool:
        if batchId not in self.batchIds_slotsTrack_map.keys():
            raise IndexError("Batch Id Not Found")

        if self.batchIds_slotsTrack_map[batchId]["slotsNeeded"] == 0:
            return False

        self.batchIds_slotsTrack_map[batchId]["slotsNeeded"] -= 1
        return True


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
