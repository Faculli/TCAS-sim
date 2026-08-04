import random
from entities.aircraft import Aircraft
from entities.position import Position


class AircraftGenerator:

    AIRLINES = ["AZU", "TAM", "GLO", "AAL", "AFR"]
    ALTITUDES = list(range(400, 40000, 1000))
    CD_RATE = [rate for rate in range(-2500, 2500, 500) if rate != 0]

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
        cd_rate = random.choice(cls.CD_RATE)

        return Aircraft(callsign=callsign, pos=pos, speed=speed, heading=heading, cd_rate=cd_rate)

    @classmethod
    def generate_batch(cls, count: int) -> list[Aircraft]:
        return [cls.generate_single() for _ in range(count)]