import time

from entities import aircraft
from services.radar import Radar
from util.aircraft_generator import AircraftGenerator
from config import parameters as p
from services.tcas_control import TCASControl

class Simulator:
    def __init__(self, update_time: float = p.UPDATE_TIME, aircraft_num: int = 5):
        self.update_time = update_time # How many seconds between simulation updates (defined in parameters)
        self.current_time = 0.0

        self.aircraft_list = AircraftGenerator.generate_batch(aircraft_num)
        self.radar = Radar()
        self.tcas = TCASControl()

    # Every updated time the sim will run a verification for conflicts and solve them
    def step(self):
        for aircraft in self.aircraft_list:
            aircraft.update_pos(self.update_time)

        conflicts = self.radar.detect_conflict(self.aircraft_list)

        if conflicts:
            print(f"\n[TIME {self.current_time:.1f}s] CONFLICT(S) DETECTED(S): {len(conflicts)}")

            for conflict in conflicts:
                airc1, airc2, h_dist, v_dist = conflict
                print(f"  -> {airc1.callsign} <-> {airc2.callsign} | Dist H: {h_dist:.2f} NM | Dist V: {v_dist:.0f} ft")

            self.tcas.process_conflict(conflicts)

        self.current_time += self.update_time

    # Simulation ini
    def run_cycle(self, total_time: float = p.TOTAL_TIME, sim_sleep_time: float = 0.5):
        print(f"BEGINING SIMULATOR - TOTAL AIRCRAFTS LOADED: {len(self.aircraft_list)}")

        while self.current_time < total_time:
            self.step()

            if sim_sleep_time > 0:
                time.sleep(sim_sleep_time)

        print(f"\nSIMULATOR TERMINATED")


