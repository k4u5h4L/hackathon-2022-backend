from enum import Enum

class RequestedNeeded(Enum):
    NEW = "New"
    REPAIR = "Repair"
    CHANGE = "Change"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    
