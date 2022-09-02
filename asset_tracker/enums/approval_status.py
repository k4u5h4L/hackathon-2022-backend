from enum import Enum

class ApprovalStatus(Enum):
    PENDING = "Pending"
    DENIED = "Denied"
    APPROVED = "Approved"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    
