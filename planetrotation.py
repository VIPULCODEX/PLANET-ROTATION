import pygame
import random
import math

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
SPACE_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont("comicsans", 24)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, name, x, y, radius, color, mass, info):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.info = info
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + SCREEN_WIDTH / 2
        y = self.y * self.SCALE + SCREEN_HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = [(p[0] * self.SCALE + SCREEN_WIDTH / 2, p[1] * self.SCALE + SCREEN_HEIGHT / 2) for p in self.orbit]
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{self.name}: {round(self.distance_to_sun / 1000, 1)} km", 1, WHITE)
            win.blit(distance_text, (int(x - distance_text.get_width() / 2), int(y - self.radius - 20)))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

# Function to draw stars in the background
def draw_stars(win):
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(win, WHITE, (x, y), 1)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 30, YELLOW, 1.98892 * 10 ** 30, "The Sun is the star at the center of the Solar System.")
    sun.sun = True

    earth = Planet("Earth", -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24, "Earth is the third planet from the Sun and the only astronomical object known to harbor life.")
    earth.y_vel = 29.783 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23, "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System.")
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23, "Mercury is the smallest and innermost planet in the Solar System.")
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24, "Venus is the second planet from the Sun. It is named after the Roman goddess of love and beauty.")
    venus.y_vel = -35.02 * 1000

    jupiter = Planet("Jupiter", -5.203 * Planet.AU, 0, 20, (255, 150, 150), 1.898 * 10 ** 27, "Jupiter is the fifth planet from the Sun and the largest in the Solar System.")
    jupiter.y_vel = 13.07 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter]

    while run:
        clock.tick(60)
        WIN.fill(SPACE_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw stars in the background
        draw_stars(WIN)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
