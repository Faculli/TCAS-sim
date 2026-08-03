import random
from entities.aircraft import Aircraft


class AircraftGenerator:

    AIRLINES = ["AZU", "TAM", "GLO", "AAL", "AFR"]
    ALTITUDES = [range(0, 40000, 1000)]

    @staticmethod
    def generate_single():
        callsign = f"{random.choice(AircraftGenerator.AIRLINES)}{random.randint(1000, 9999)}"
        x = random.uniform(-50, 50)
        y = random.uniform(-50, 50)
        altitude = random.choice(AircraftGenerator.ALTITUDES)
        heading = random.randint(0, 359)
        speed = random.uniform(100, 450)

        return Aircraft(callsign, x, y, altitude, heading, speed)

    @staticmethod
    def generate_batch(count: int):
        return [AircraftGenerator.generate_single() for _ in range(count)]