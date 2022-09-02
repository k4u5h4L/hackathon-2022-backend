from enum import Enum

class AssetStatus(Enum):
    IN_USE = "In Use"
    DISCARDED = "Discarded"
    DISPATCHED = "Dispatched"
    IN_STOCK = "In stock"
    IN_REPAIRMENT = "In repairement"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    
