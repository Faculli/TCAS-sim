import math

class Aircraft:
    def __init__(self, callsign: str, pos, speed: float, heading: float, new_altitude: float = None, cd_rate: float = 0.0):
        self.callsign = callsign
        self.pos = pos
        self.speed = speed
        self.heading = heading
        self.cd_rate = cd_rate

        if new_altitude is None:
            self.new_altitude = self.pos.z
        else:
            self.new_altitude = new_altitude

    def update_pos(self, delta_time):
        # Converts from knots -> NM/s
        speed_conversion = self.speed / 3600

        # New positions x and y based on time and speed
        self.pos.x += speed_conversion * delta_time * math.sin(math.radians(self.heading))
        self.pos.y += speed_conversion * delta_time * math.cos(math.radians(self.heading))

        # Climb / descent rate conversion from ft/min -> ft/s
        cd_rate_sec = abs(self.cd_rate) / 60.0

        # New position z if new_altitude != pos.z
        if self.new_altitude > self.pos.z:
            self.pos.z = min(self.pos.z + (cd_rate_sec * delta_time), self.new_altitude)
        elif self.new_altitude < self.pos.z:
            self.pos.z = max(self.pos.z - (cd_rate_sec * delta_time), self.new_altitude)
        else:
            self.cd_rate = 0.0

    #def change_heading(self, new_heading):

    #def change_altitude(self, new_altitude):