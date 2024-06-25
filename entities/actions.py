from enum import IntEnum, Enum, auto

class Actions(IntEnum):
    PLEFT = auto()
    PRIGHT = auto()
    PFORWARD = auto()
    PBACK = auto()
    PTURNL = auto()
    PTURNR = auto()     # 6
    PDODGE = auto()     # 7
    # PKNOCKED = auto() # Player is knocked down
    PATTACK = auto() # 8
    
    MLEFT = auto() # DO NOT REORGANIZE THIS. THIS IS BEING USED TO SIGNAL THE START OF THE MARGIT ACTIONS
    MRIGHT = auto()     # 10
    MFORWARD = auto()   # 11
    MBACK = auto()      # 12
    MTURNL = auto()     # 13
    MTURNR = auto()     # 14
    MRETREAT = auto()   # 15
    # Margit Attacks
    MSLASH = auto()     # 16
    MREVSLASH = auto()  # 17
    MDAGGERS = auto()   # 18

class ActionType(Enum):
    ATTACK = auto()
    DODGE = auto()
    MOVEMENT = auto()

def get_action_type(action: Actions) -> ActionType:
    """Determines what kind of action is given

    Args:
        action (Actions): _description_

    Returns:
        ActionType: _description_
    """
    attacks = [
        Actions.PATTACK,
        Actions.MSLASH,
        Actions.MREVSLASH,
        Actions.MDAGGERS,
    ]
    if action in attacks:
        return ActionType.ATTACK

    dodges = [
        Actions.PDODGE,
        Actions.MRETREAT,
    ]
    if action in dodges:
        return ActionType.DODGE
    
    # If we didnt match any of the previous types, it must be movement
    return ActionType.MOVEMENT


def get_primary_action(action_list: list[Actions]) -> Actions:
    """Determine what the primary action is based on the actions list provided

    Used to determine if the 

    Args:
        action_list (list[Actions]): _description_

    Returns:
        Actions: _description_
    """
    if not action_list:
        # print("We were given a bad list with no actions")
        return None

    for action in TARNISHED_ACTION_PRIORITY:
        if action in action_list:
            return action
    for action in MARGIT_MOVE_PRIORITY:
        if action in action_list:
            return action
    
    raise Exception(f"WE FOUND A LIST WITH UNEXPECTED ACTIONS: {str(action_list)}")


TARNISHED_ACTION_PRIORITY = [
    Actions.PATTACK,
    Actions.PDODGE,
    Actions.PLEFT,
    Actions.PRIGHT,
    Actions.PFORWARD,
    Actions.PBACK,
    Actions.PTURNL,
    Actions.PTURNR,
]

MARGIT_MOVE_PRIORITY = [
    Actions.MSLASH,
    Actions.MREVSLASH,
    Actions.MDAGGERS,
    Actions.MRETREAT,
    Actions.MLEFT,
    Actions.MRIGHT,
    Actions.MFORWARD,
    Actions.MBACK,
    Actions.MTURNL,
    Actions.MTURNR,
]