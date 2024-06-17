

class Entity:
    name: str
    health: int
    max_health: int
    iframes: int = 0    # Not default, remaining iframes
    velocity: int

    current_action: str # May be used for playbacks or actions that lock you out of others, or are dangerous to opponent
    time_in_action: int # Time remaining while locked in current action, in ticks

    x: int
    y: int
    width: int
    height: int
    angle: int # Where it is currently looking
    turn_speed: int = 30 # How fast the character can rotate, degrees/tick

    image_url: str

    def __init__(self):
        pass

    def busy(self) -> bool:
        return self.time_in_action > 0
