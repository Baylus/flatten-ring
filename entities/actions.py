from enum import Enum, auto

class Actions(Enum):
    PLEFT = auto()
    PRIGHT = auto()
    PFORWARD = auto()
    PBACK = auto()
    PTURNL = auto()
    PTURNR = auto()
    PDODGE = auto()
    # PKNOCKED = auto() # Player is knocked down
    PATTACK = auto()
    
    MLEFT = auto()
    MRIGHT = auto()
    MFORWARD = auto()
    MBACK = auto()
    MTURNR = auto()
    MTURNL = auto()
    MRETREAT = auto()
    # Margit Attacks
    MSLASH = auto()
    MREVSLASH = auto()
    MDAGGERS = auto()