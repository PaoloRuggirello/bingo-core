from enum import Enum


# number related to prize is the number of extracted numbers needed in a row card (o entire card for TOMBOLA)
class Prize(Enum):
    AMBO = 2
    TERNA = 3
    QUATERNA = 4
    CINQUINA = 5
    TOMBOLA = 15

    @staticmethod
    def list():
        return list(map(lambda p: p.value, Prize))
