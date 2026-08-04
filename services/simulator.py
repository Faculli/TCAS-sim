import time

from entities import aircraft
from entities.radar import Radar
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

    # Test feature to verify aircraft attributes
    def print_aircraft_status(self):
        print(f"\n--- AIRCRAFT STATUS (TIME: {self.current_time:.1f}s) ---")
        for aircraft in self.aircraft_list:
            pos = aircraft.pos
            print(
                f"[{aircraft.callsign}] "
                f"Pos: (X: {pos.x:6.2f} NM, Y: {pos.y:6.2f} NM, Z: {pos.z:7.1f} ft) | "
                f"Tgt Z: {aircraft.new_altitude:7.1f} ft | "
                f"Spd: {aircraft.speed:5.1f} kt | "
                f"Hdg: {aircraft.heading:3.0f}° | "
                f"CD_Rate: {aircraft.cd_rate:6.1f} ft/min"
            )
        print("-" * 75)

    # Every updated time the sim will run a verification for conflicts and solve them
    def step(self):
        for aircraft in self.aircraft_list:
            aircraft.update_pos(self.update_time)

        self.print_aircraft_status()

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


