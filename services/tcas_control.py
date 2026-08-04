from config import parameters as p

class TCASControl:
    # The separation itself will be only vertical
    def __init__(self, separation_alt: float = p.MIN_VERTICAL_SEPARATION, default_cd_rate: float = 1500):
        self.separation_alt = separation_alt
        self.default_cd_rate = default_cd_rate

    def reroute_suggestion(self, airc1, airc2):
        # Decides witch aircraft will climb or descend based on their relative pos
        if airc1.pos.z < airc2.pos.z:
            climbing_airc = airc2
            descending_airc = airc1
        else:
            climbing_airc = airc1
            descending_airc = airc2

        # Apply the new route only if the aircraft is not climbing/descending already
        if climbing_airc.new_altitude == climbing_airc.pos.z:
            climbing_airc.new_altitude = climbing_airc.pos.z + self.separation_alt
            climbing_airc.cd_rate = self.default_cd_rate

        if descending_airc.new_altitude == climbing_airc.pos.z:
            descending_airc.new_altitude = max(0.0, descending_airc.pos.z - self.separation_alt)
            descending_airc.cd_rate = -self.default_cd_rate

    # Order the planes from conflict list to reroute
    def process_conflict(self, conflict_list: list):
        for conflict in conflict_list:
            airc1, airc2 = conflict[0], conflict[1]
            self.reroute_suggestion(airc1, airc2)