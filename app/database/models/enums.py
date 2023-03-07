from enum import Enum, IntEnum


class Maps(str, Enum):
    Scorch_Gorge = "Scorch Gorge"
    Eeltail_Alley = "Eeltail Alley"


class Modes(IntEnum):
    TW = 0
    SZ = 1
    TC = 2
    RM = 3
    CB = 4
