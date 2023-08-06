import pygame
import math
from collections import deque

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.particles = []
        self.is_divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def insert(self, particle):
        if not self.boundary.collidepoint(particle.position.x, particle.position.y):
            return False

        if len(self.particles) < self.capacity:
            self.particles.append(particle)
            return True

        if not self.is_divided:
            self.subdivide()

        if self.northwest.insert(particle):
            return True
        if self.northeast.insert(particle):
            return True
        if self.southwest.insert(particle):
            return True
        if self.southeast.insert(particle):
            return True

    def subdivide(self):
        x, y, w, h = self.boundary
        nw_boundary = pygame.Rect(int(x), int(y), int(w / 2), int(h / 2))
        ne_boundary = pygame.Rect(int(x + w / 2), int(y), int(w / 2), int(h / 2))
        sw_boundary = pygame.Rect(int(x), int(y + h / 2), int(w / 2), int(h / 2))
        se_boundary = pygame.Rect(int(x + w / 2), int(y + h / 2), int(w / 2), int(h / 2))

        self.northwest = QuadTree(nw_boundary, self.capacity)
        self.northeast = QuadTree(ne_boundary, self.capacity)
        self.southwest = QuadTree(sw_boundary, self.capacity)
        self.southeast = QuadTree(se_boundary, self.capacity)

        self.is_divided = True
    
    def calculate_forces(self, particle, G):
        for other_particle in self.particles:
            if particle != other_particle:
                dx = abs(particle.position.x - other_particle.position.x)
                dy = abs(particle.position.y - other_particle.position.y)

                if dx < particle.radius or dy < particle.radius:
                    continue
                else:
                    try:
                        r_squared = dx**2 + dy**2
                        r = math.sqrt(r_squared)
                        a = G * other_particle.mass / r_squared
                        theta = math.asin(dy / r)

                        if particle.position.y > other_particle.position.y:
                            sin_theta = -math.sin(theta)
                        else:
                            sin_theta = math.sin(theta)

                        if particle.position.x > other_particle.position.x:
                            cos_theta = -math.cos(theta)
                        else:
                            cos_theta = math.cos(theta)

                        particle.apply_force(pygame.Vector2(cos_theta * a, sin_theta * a))
                    except ZeroDivisionError:
                        pass

        if self.is_divided:
            if self.northwest.boundary.colliderect(pygame.Rect(int(particle.position.x), int(particle.position.y), 1, 1)):
                self.northwest.calculate_forces(particle, G)
            if self.northeast.boundary.colliderect(pygame.Rect(int(particle.position.x), int(particle.position.y), 1, 1)):
                self.northeast.calculate_forces(particle, G)
            if self.southwest.boundary.colliderect(pygame.Rect(int(particle.position.x), int(particle.position.y), 1, 1)):
                self.southwest.calculate_forces(particle, G)
            if self.southeast.boundary.colliderect(pygame.Rect(int(particle.position.x), int(particle.position.y), 1, 1)):
                self.southeast.calculate_forces(particle, G)
class Particles:
    def __init__(self, x, y, mass, color, radius, velocity):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.color = color
        self.stats_text = None
        self.selected = None
        self.path = deque(maxlen=100)  # Maximum length of the path

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def update(self):
        self.position += self.velocity
        self.path.append(self.position.copy())  # Add current position to the path

    def draw_scaled(self, mouse_x, mouse_y, scale, width, height, screen, font):
        scaled_x = int(mouse_x + (self.position.x - mouse_x) * scale)
        scaled_y = int(mouse_y + (self.position.y - mouse_y) * scale)
        circle_center = (scaled_x, scaled_y)
        radius_scaled = int(self.radius * scale)

        # Draw the particle if it is within the screen boundaries
        if 0 < scaled_y < height and 0 < scaled_x < width:
            pygame.draw.circle(screen, self.color, circle_center, radius_scaled)

        # Render and position the statistics text
        if self.selected:
            text_y = scaled_y + radius_scaled + 10
            stats_lines = [
                f"Mass: {self.mass}",
                f"Radius: {self.radius}",
                f"Velocity: {round(self.velocity.x, 2), round(self.velocity.y, 2)}"
            ]
            line_height = 20
            stats_surfaces = [font.render(line, True, (255, 255, 255)) for line in stats_lines]

            for i, stats_text in enumerate(stats_surfaces):
                stats_text_rect = stats_text.get_rect(center=(scaled_x, text_y + i * line_height))
                screen.blit(stats_text, stats_text_rect)
                        # Add the current position to the path (unscaled)
            self.path.append(self.position.copy())

            # Scale the path coordinates
            scaled_path = [(int(mouse_x + (pos.x - mouse_x) * scale), int(mouse_y + (pos.y - mouse_y) * scale))
                        for pos in self.path]

            # Draw the path if it has at least two points
            if len(scaled_path) >= 16:
                pygame.draw.lines(screen, self.color, False, scaled_path)

    def is_clicked(self, mouse_pos):
        squared_distance = self.position.distance_squared_to(pygame.Vector2(*mouse_pos))
        return squared_distance <= self.radius**2