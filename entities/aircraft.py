class Aircraft:
    def __init__(self, callsign, pos, speed, heading, new_altitude):
        self.callsign = callsign
        self.pos = pos
        self.speed = speed
        self.heading = heading

        if new_altitude is None:
            self.new_altitude = self.pos.z
        else:
            self.new_altitude = new_altitude

    #def update_pos(self, delta_time):

    #def change_heading(self, new_heading):

    #def change_altitude(self, new_altitude):