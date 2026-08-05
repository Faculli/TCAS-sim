import math
import pygame

class RadarView:
    def __init__(self, sim, width: int = 1000, height: int = 1000, nm_range: float = 60.0):
        self.sim = sim
        self.width = width
        self.height = height
        self.nm_range = nm_range

        # Define center point (origin = 0.0 NM) on screen center
        self.center_x = width // 2
        self.center_y = height // 2

        # Conversion factor for NM -> pixels
        self.scale = (width // 2) / nm_range

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ATC Radar Console")

        # Menu fonts
        self.font = pygame.font.SysFont("Consolas", 12, bold=True)
        self.title_font = pygame.font.SysFont("Consolas", 14, bold=True)

        # General colors
        self.COLOR_BG = (10, 15, 20)
        self.COLOR_GRID = (20, 45, 35)
        self.COLOR_TEXT_GRID = (40, 90, 70)
        self.COLOR_PLANE_NORMAL = (0, 230, 120)
        self.COLOR_PLANE_CONFLICT = (255, 50, 50)
        self.COLOR_PLANE_COLLISION = (130, 130, 130)
        self.COLOR_DATABLOCK_BG = (15, 25, 30, 180)

    # Conversion from NM to pixels
    def nm_to_pixels(self, x_nm: float, y_nm: float) -> tuple[int, int]:
        px = int(self.center_x + (x_nm * self.scale))
        py = int(self.center_y + (y_nm * self.scale))
        return px, py

    # Draws radar structure
    def _draw_radar_background(self):
        self.screen.fill(self.COLOR_BG)

        # Draws cartesian axis on radar center
        pygame.draw.line(self.screen, self.COLOR_GRID, (self.center_x, 0), (self.center_x, self.height), 1)
        pygame.draw.line(self.screen, self.COLOR_GRID, (0, self.center_y), (self.width, self.center_y), 1)

        # Draws concentric rings every 10 NM
        step_nm = 10.0
        current_nm = step_nm
        while current_nm <= self.nm_range:
            radius_px = int(current_nm * self.scale)
            pygame.draw.circle(self.screen, self.COLOR_GRID, (self.center_x, self.center_y), radius_px, 1)

            # Labels the NM distances
            lbl = self.title_font.render(f"{int(current_nm)}NM", True, self.COLOR_TEXT_GRID)
            self.screen.blit(lbl, (self.center_x + radius_px + 2, self.center_y + 2))

            current_nm += step_nm

    def _draw_aircraft(self, aircraft, color):
        px, py = self.nm_to_pixels(aircraft.pos.x, aircraft.pos.y)

        # Draws aircraft representation
        pygame.draw.circle(self.screen, color, (px, py), 5)
        pygame.draw.circle(self.screen, color, (px, py), 2)

        # Draws vector trajectory
        rad = math.radians(aircraft.heading)
        vector_length = (aircraft.speed / 60.0) * self.scale * 2.0
        end_px = int(px + vector_length * math.sin(rad))
        end_py = int(py - vector_length * math.cos(rad))
        pygame.draw.line(self.screen, color, (px, py), (end_px, end_py), 2)

        # Define symbol based on climb/descend rate
        trend_symbol = "═"
        if aircraft.cd_rate > 0:
            trend_symbol = "▲"
        elif aircraft.cd_rate < 0:
            trend_symbol = "▼"

        # Convert feet (ft) altitude to flight level (FL)
        alt_fl = int(aircraft.pos.z // 100)
        tgt_fl = int(aircraft.new_altitude // 100)

        # Create aircraft data block (callsign, alt(C/D/Level), speed)
        lbl_callsign = f"{aircraft.callsign}"
        lbl_alt = f"FL{alt_fl:03d}{trend_symbol}{tgt_fl:03d}"
        lbl_speed = f"{int(aircraft.speed)}kt {int(aircraft.cd_rate)}ft/m"
        txt_1 = self.font.render(lbl_callsign, True, color)
        txt_2 = self.font.render(lbl_alt, True, color)
        txt_3 = self.font.render(lbl_speed, True, color)
        offset_x = px + 12
        offset_y = py - 18

        # Guideline from aircraft to respective datablock
        pygame.draw.line(self.screen, color, (px, py), (offset_x - 2, offset_y + 10), 1)

        # Renders text on screen
        self.screen.blit(txt_1, (offset_x, offset_y))
        self.screen.blit(txt_2, (offset_x, offset_y + 12))
        self.screen.blit(txt_3, (offset_x, offset_y + 24))

    # Update the screen drawing
    def render(self):
        self._draw_radar_background()

        # Identify aircraft conflicts and collisions
        conflicts = self.sim.radar.detect_conflict(self.sim.aircraft_list)
        conflicting_aircraft = set()
        colliding_aircraft = set()
        for c in conflicts:
            conflicting_aircraft.add(c[0])
            conflicting_aircraft.add(c[1])
            if c[4]:
                colliding_aircraft.add(c[0])
                colliding_aircraft.add(c[1])

        if colliding_aircraft:
            # Collision state: hide all other traffic, draw only the wreckage in gray
            for aircraft in colliding_aircraft:
                self._draw_aircraft(aircraft, self.COLOR_PLANE_COLLISION)
        else:
            # Draws every aircraft (red if in conflict, green otherwise)
            for aircraft in self.sim.aircraft_list:
                color = self.COLOR_PLANE_CONFLICT if aircraft in conflicting_aircraft else self.COLOR_PLANE_NORMAL
                self._draw_aircraft(aircraft, color)

        # Header with simulation general status
        status_text = f"TIME: {self.sim.current_time:.1f}s | TRAFFIC: {len(self.sim.aircraft_list)} | CONFLICTS: {len(conflicts)} | COLLISIONS: {len(colliding_aircraft) // 2}"
        lbl_status = self.title_font.render(status_text, True, (200, 220, 200))
        self.screen.blit(lbl_status, (15, 15))

        pygame.display.flip()

    # Capture Pygame events
    def handle_inputs(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True