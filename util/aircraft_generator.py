import random
from entities.aircraft import Aircraft
from entities.position import Position


class AircraftGenerator:

    AIRLINES = ["AZU", "TAM", "GLO", "AAL", "AFR"]
    ALTITUDES = [range(0, 40000, 1000)]

    @classmethod
    def generate_single(cls) -> Aircraft:
        callsign = f"{random.choice(cls.AIRLINES)}{random.randint(1000, 9999)}"
        pos = Position(
            x = random.uniform(-50, 50),
            y = random.uniform(-50, 50),
            z = random.choice(cls.ALTITUDES)
        )
        heading = random.randint(0, 359)
        speed = random.uniform(100, 450)

        return Aircraft(callsign=callsign, pos=pos, speed=speed, heading=heading)

    @classmethod
    def generate_batch(cls, count: int) -> list[Aircraft]:
        return [cls.generate_single() for _ in range(count)]