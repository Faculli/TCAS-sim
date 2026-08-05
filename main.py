import pygame

from services.simulator import Simulator
from view.radar_view import RadarView

if __name__ == "__main__":
    simulator = Simulator(aircraft_num=12)
    view = RadarView(simulator, width=900, height=900)

    running = True
    clock = pygame.time.Clock()

    while running:
        running = view.handle_inputs()
        simulator.step()
        view.render()
        clock.tick(5)

    pygame.quit()

