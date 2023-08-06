import pygame

class Buttons:
    def __init__(self, x_pos, y_pos, text_input, button_rect, font):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.button_rect = button_rect
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.button_rect.center))
        self.surface = pygame.Surface(self.button_rect.size, pygame.SRCALPHA) 
        self.color = (100, 80, 90, 128)  # Set the color with transparency
        
    def draw(self, screen): 
        pygame.draw.rect(self.surface, self.color, (0, 0, *self.button_rect.size))  
        screen.blit(self.surface, self.button_rect)  
        screen.blit(self.text, self.text_rect)
    
    def decrease_radius(self, added_radius):
        if added_radius > 1:
            return added_radius - 1
        else:
            return added_radius

    def increase_radius(self, added_radius):
        return added_radius + 1

    def decrease_mass(self, added_mass):
        if added_mass > 1:
            return added_mass - 1
        else:
            return added_mass

    def increase_mass(self, added_mass):
        return added_mass + 1

    def decrease_velocity_x(self, added_velocity, add_button_statement_put):
        added_velocity.x -= 0.05
        return added_velocity

    def increase_velocity_x(self, added_velocity, add_button_statement_put):
        added_velocity.x += 0.05
        return added_velocity

    def decrease_velocity_y(self, added_velocity, add_button_statement_put):
        added_velocity.y -= 0.05
        return added_velocity

    def increase_velocity_y(self, added_velocity, add_button_statement_put):
        added_velocity.y += 0.05
        return added_velocity

    def reset_particles(self, num_particles, particles, reset_button_statement, hide_button):
        if not hide_button:    
            num_particles = 0
            particles = []
        reset_button_statement = False
        return num_particles, particles, reset_button_statement

    def reset_scale(self, scale, reset_scale_button_statement, hide_button):
        if not hide_button:    
            scale = 1.0
            reset_scale_button_statement = False
        return scale, reset_scale_button_statement 
    
    def reset_vel(self, vel, reset_button_statement):
        vel = pygame.Vector2(0, 0)
        reset_button_statement = False
        return vel, reset_button_statement
   
    def change_text(self, text_input, font):
        self.text_input = text_input
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=self.button_rect.center)
