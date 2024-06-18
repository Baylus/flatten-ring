from enum import IntEnum, auto

class Actions(IntEnum):
    PLEFT = auto()
    PRIGHT = auto()
    PFORWARD = auto()
    PBACK = auto()
    PTURNL = auto()
    PTURNR = auto()
    PDODGE = auto()
    # PKNOCKED = auto() # Player is knocked down
    PATTACK = auto()
    
    MLEFT = auto() # DO NOT REORGANIZE THIS. THIS IS BEING USED TO SIGNAL THE START OF THE MARGIT ACTIONS
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