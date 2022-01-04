from enum import Enum

# number related to prize is the number of True needed in card


class Prize(Enum):
    AMBO = 2
    TERNO = 3
    QUATERNA = 4
    CINQUINA = 5
    TOMBOLA = 15

    @staticmethod
    def list():
        return list(map(lambda p: p.value, Prize))
