from config import parameters as p
import math

class Radar:
    def __init__(self, hor_alert_dist: float = p.MIN_HORIZONTAL_SEPARATION, vert_alert_dist: float = p.MIN_VERTICAL_SEPARATION):
        self.hor_alert_dist = hor_alert_dist
        self.vert_alert_dist = vert_alert_dist

    def calc_horizontal_distance(self, airc1, airc2) -> float:
        return math.sqrt((airc2.pos.x - airc1.pos.x)**2 + (airc2.pos.y - airc1.pos.y)**2)

    def calc_vertical_distance(self, airc1, airc2) -> float:
        return abs(airc2.pos.y - airc1.pos.y)

    def detect_conflict(self, aircraft_list: list) -> list[tuple]:
        conflict = []
        n = len(aircraft_list)

        # Comparison from 1 aircraft to another without repetition
        for i in range(n):
            for j in range(i + 1, n):
                airc1 = aircraft_list[i]
                airc2 = aircraft_list[j]

                h_dist = self.calc_horizontal_distance(airc1, airc2)
                v_dist = self.calc_vertical_distance(airc1, airc2)

                # Aircraft must be close enough for h distance AND unsafe v distance to alert
                if h_dist < self.hor_alert_dist and v_dist < self.vert_alert_dist:
                    conflict.append((airc1, airc2, h_dist, v_dist))

        return conflict

    