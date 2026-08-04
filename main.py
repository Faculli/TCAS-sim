from services.simulator import Simulator

if __name__ == "__main__":
    sim = Simulator(aircraft_num=2)
    sim.run_cycle(sim_sleep_time=1)