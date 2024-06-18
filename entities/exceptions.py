
class GameOver(Exception):
    pass

class CharacterDied(GameOver):
    pass

class TarnishedDied(CharacterDied):
    pass

class MargitDied(CharacterDied):
    pass