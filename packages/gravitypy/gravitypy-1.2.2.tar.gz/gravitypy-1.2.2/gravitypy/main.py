import pygame
import random
import math
import os
from pygame.locals import *
from .button.button import Buttons
from .particle.particle import Particles, QuadTree

def main():
    pygame.init()
    pygame.display.set_caption("GravityPy")
    
    current_file = __file__
    current_dir = os.path.dirname(current_file)
    font_file = os.path.join(current_dir, 'resources', 'fonts', 'minecraft_font.ttf')
    font_size = 16
    FONT = pygame.font.Font(font_file, font_size)

    WIDTH, HEIGHT = 1200, 700
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    G = 1
    SCALE = 1.0
    PARTICLES = []
    ADDED_RADIUS = 5
    ADDED_MASS = 5
    ADDED_VELOCITY = pygame.Vector2(0, 0)
    NUM_PARTICLES = 250
    ADDED_COLOR = (255,255,255)
    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
    
    # Initialize states  
    states = {
        'increase_radius':          False,
        'decrease_radius':          False,
        'increase_mass':            False,
        'decrease_mass':            False,
        'increase_velocity_x':      False,
        'decrease_velocity_x':      False,
        'increase_velocity_y':      False,
        'decrease_velocity_y':      False,
        'add_particle':             False,
        'add_particle_put':         False,
        'reset_particles':          False,
        'reset_scale':              False,
        'reset_vel':                False,
        'move_particles':           False,
        'pause':                    False,
        'hide_button':              False


    }
    
    # Initialize Buttons
    buttons = {
        'button_increase_r':  Buttons(50,50,"Increse R", pygame.Rect(50,50,120,25), FONT),
        'button_decrease_r':  Buttons(150,50,"Decrese R", pygame.Rect(50,85,120,25), FONT),
        'button_increase_m':  Buttons(250,50,"Increse M", pygame.Rect(200,50,120,25), FONT),
        'button_decrease_m':  Buttons(350,50,"Decrese M", pygame.Rect(200,85,120,25), FONT),
        'button_increase_vx': Buttons(250,50,"+ Vx", pygame.Rect(350,50,50,25), FONT),
        'button_decrease_vx': Buttons(350,50,"- Vx", pygame.Rect(350,85,50,25), FONT),
        'button_increase_vy': Buttons(250,50,"+ Vy", pygame.Rect(410,50,50,25), FONT),
        'button_decrease_vy': Buttons(350,50,"- Vy", pygame.Rect(410,85,50,25), FONT),
        'button_res_vel':     Buttons(350,50,"Res vel", pygame.Rect(480,50,50,60), FONT),
        'add_button':         Buttons(350,50,"Add particle", pygame.Rect(550,50,140,60), FONT),
        'reset_button':       Buttons(350,50,"Reset Praticles", pygame.Rect(850,50,160,25), FONT),
        'reset_scale_button': Buttons(350,50,"Reset scale", pygame.Rect(1050,50,120,25), FONT),
        'hide_button':        Buttons(350,50,"Hide buttons", pygame.Rect(1030,650,150,25), FONT)       
    }
      
    # Generate random particlesbutton
    for i in range(NUM_PARTICLES):
        if i == 0:
            x = WIDTH // 2
            y = HEIGHT// 2
            mass = 10000
            radius = random.randint(10, 10)
            PARTICLES.append(Particles(x, y, mass, (189, 255, 20) , radius, pygame.Vector2(0, 0)))
        else:
            x =  i*3
            y = 100 
            mass = int(random.uniform(1, 10))
            radius = int(random.randint(1, 3))
            PARTICLES.append(Particles(x, y, mass, (255,255,255), radius, pygame.Vector2(2.0, 0)))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Left click
                if event.button == 1: 
                    if buttons['button_increase_r'].button_rect.collidepoint(event.pos):
                        states['increase_radius'] = True

                    elif buttons['button_decrease_r'].button_rect.collidepoint(event.pos):
                        states['decrease_radius'] = True

                    elif buttons['button_increase_m'].button_rect.collidepoint(event.pos):
                        states['increase_mass'] = True

                    elif buttons['button_decrease_m'].button_rect.collidepoint(event.pos):
                        states['decrease_mass'] = True

                    elif buttons['button_increase_vx'].button_rect.collidepoint(event.pos):
                        states['increase_velocity_x'] = True

                    elif buttons['button_decrease_vx'].button_rect.collidepoint(event.pos):
                        states['decrease_velocity_x'] = True

                    elif buttons['button_increase_vy'].button_rect.collidepoint(event.pos):
                        states['increase_velocity_y'] = True

                    elif buttons['button_decrease_vy'].button_rect.collidepoint(event.pos):
                        states['decrease_velocity_y'] = True

                    elif buttons['add_button'].button_rect.collidepoint(event.pos):
                        states['add_particle'] = True

                    elif states['add_particle']:
                        states['add_particle_put'] = True

                    elif buttons['reset_button'].button_rect.collidepoint(event.pos):
                        states['reset_particles'] = True

                    elif buttons['reset_scale_button'].button_rect.collidepoint(event.pos):
                        states['reset_scale'] = True

                    elif buttons['hide_button'].button_rect.collidepoint(event.pos):
                        states['hide_button'] = not states['hide_button']
                    
                    elif buttons['button_res_vel'].button_rect.collidepoint(event.pos):
                        states['reset_vel'] = not states['reset_vel']
                    
                    for particle in PARTICLES:
                        scaled_x = int(MOUSE_X + (particle.position.x - MOUSE_X) * SCALE)
                        scaled_y = int(MOUSE_Y + (particle.position.y - MOUSE_Y) * SCALE)
                        distance = math.sqrt((event.pos[0] - scaled_x)**2 + (event.pos[1] - scaled_y)**2)
                        if distance <= particle.radius * SCALE:
                            particle.selected = not particle.selected
                
                # Right click
                if event.button == 3: 
                    if states['add_particle']:
                        states['add_particle'] = False
                
                # Scroll Up
                elif event.button == 4:  
                    SCALE += 0.1
                    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
                
                # Scroll Down 
                elif event.button == 5:  
                    if SCALE - 0.1 > 0:
                        SCALE -= 0.1
                        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Reset button states
                    states['increase_radius']     = False
                    states['decrease_radius']     = False
                    states['increase_mass']       = False
                    states['decrease_mass']       = False
                    states['increase_velocity_x'] = False
                    states['decrease_velocity_x'] = False
                    states['increase_velocity_y'] = False
                    states['decrease_velocity_y'] = False
                    states['add_button']          = False
                    states['reset_partilces']     = False
                    states['reset_scale']         = False
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    states['move_particles'] = True
                    move_direction = pygame.Vector2(5/SCALE, 0)

                elif event.key == pygame.K_RIGHT:
                    states['move_particles'] = True
                    move_direction = pygame.Vector2(-5/SCALE, 0)

                elif event.key == pygame.K_UP:
                    states['move_particles'] = True
                    move_direction = pygame.Vector2(0, 5/SCALE)

                elif event.key == pygame.K_DOWN:
                    states['move_particles'] = True
                    move_direction = pygame.Vector2(0, -5/SCALE)

                elif event.key == pygame.K_SPACE:
                    states['pause'] = not states['pause']
            
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    states['move_particles'] = False

        SCREEN.fill((9, 20, 20))
        
        text_data = {
            'text_radius': {
                'text': FONT.render(f'Radius: {ADDED_RADIUS}', True, (240, 240, 240)),
                'position': (50, 20)
            },
            'text_mass': {
                'text': FONT.render(f'Mass: {ADDED_MASS}', True, (240, 240, 240)),
                'position': (200, 20)
            },
            'text_velocity': {
                'text': FONT.render(f'Velocity: {ADDED_VELOCITY}', True, (240, 240, 240)),
                'position': (350, 20)
            },
            'text_num_particles': {
                'text': FONT.render(f'Number of particles: {NUM_PARTICLES}', True, (240, 240, 240)),
                'position': (950, 0)
            },
            'text_scale': {
                'text': FONT.render(f'Scale: {int(SCALE * 100)}%', True, (240, 240, 240)),
                'position': (950, 20)
            },
            'text_info': {
                'text': FONT.render('Move camera with arrow keys, pause with a space', True, (240, 240, 240)),
                'position': (700, 85)
            },
            'text_fps': {
                'text': FONT.render("FPS: {:.2f}".format(CLOCK.get_fps()), True, (255, 255, 255)),
                'position': (1070, 20)
            }
        }

        if states['increase_radius']:
            ADDED_RADIUS = buttons['button_increase_r'].increase_radius(ADDED_RADIUS)
        elif states['decrease_radius']:
            ADDED_RADIUS = buttons['button_decrease_r'].decrease_radius(ADDED_RADIUS)
        elif states['increase_mass']:
            ADDED_MASS = buttons['button_increase_m'].increase_mass(ADDED_MASS)
        elif states['decrease_mass']:
            ADDED_MASS = buttons['button_decrease_m'].decrease_mass(ADDED_MASS)
        elif states['increase_velocity_x']:
            ADDED_VELOCITY = buttons['button_increase_vx'].increase_velocity_x(ADDED_VELOCITY, states['add_particle'])
        elif states['decrease_velocity_x']:
            ADDED_VELOCITY = buttons['button_decrease_vx'].decrease_velocity_x(ADDED_VELOCITY, states['add_particle'])
        elif states['increase_velocity_y']:
            ADDED_VELOCITY = buttons['button_increase_vy'].increase_velocity_y(ADDED_VELOCITY, states['add_particle'])
        elif states['decrease_velocity_y']:
            ADDED_VELOCITY = buttons['button_decrease_vx'].decrease_velocity_y(ADDED_VELOCITY, states['add_particle'])
        elif states['reset_particles']:
            NUM_PARTICLES, PARTICLES, states['reset_particles'] = buttons['reset_button'].reset_particles(NUM_PARTICLES, PARTICLES, states['reset_particles'], states['hide_button'])
        elif states['reset_scale']:
            SCALE, states['reset_scale'] = buttons['reset_scale_button'].reset_scale(SCALE, states['reset_scale'], states['hide_button'])
        elif states['reset_vel']:
            ADDED_VELOCITY, states['reset_vel'] = buttons['button_res_vel'].reset_vel(ADDED_VELOCITY, states['reset_vel'])
        
        # Hide or unhide buttons 
        if states['hide_button']:
            for button_name, button in buttons.items():
                if button_name == 'hide_button':
                    button.change_text('unhide buttons', FONT)
                    button.draw(SCREEN) 
            for data in text_data.values():
                data.pop('text', None)
        else:
            for button_name, button in buttons.items():
                if button_name == 'hide_button':
                    button.change_text('hide buttons', FONT)
                button.draw(SCREEN)
            for key, data in text_data.items():
                SCREEN.blit(data['text'], data['position'])


        if states['add_particle']:
            actual_mouse_x, actuale_mouse_y = pygame.mouse.get_pos()
            scaled_mouse_x = int(MOUSE_X + (actual_mouse_x - MOUSE_X) * SCALE)
            scaled_mouse_y = int(MOUSE_Y + (actuale_mouse_y - MOUSE_Y) * SCALE)
            circle_center = (scaled_mouse_x, scaled_mouse_y)
            circle_radius = int(ADDED_RADIUS * SCALE)
            if 0 < scaled_mouse_y < HEIGHT and 0 < scaled_mouse_x < WIDTH: 
                pygame.draw.circle(
                    SCREEN, 
                    ADDED_COLOR, 
                    circle_center, 
                    circle_radius
                    )

        if states['add_particle_put']:
            particle_velocity = ADDED_VELOCITY.copy()
            PARTICLES.append(
                Particles(
                    actual_mouse_x,
                    actuale_mouse_y,
                    ADDED_MASS,
                    ADDED_COLOR ,
                    ADDED_RADIUS,
                    particle_velocity
                )
            )
            states['add_particle_put'] = False
            # Change color of the next particle
            ADDED_COLOR  = (255,255,255)
            NUM_PARTICLES += 1

        # Sort in case bigger particles do not cover smaller ones 
        PARTICLES = sorted(PARTICLES, key=lambda x: x.radius, reverse=True)
        
        boundary = pygame.Rect(0, 0, WIDTH, HEIGHT)
        capacity = 4  
        quadtree = QuadTree(boundary, capacity)

        for particle in PARTICLES:
            quadtree.insert(particle)

        for particle in PARTICLES:
            if states['move_particles']:
                particle.position += move_direction * SCALE
            elif not states['pause']:
                particle.update()
                quadtree.calculate_forces(particle, G)
            particle.draw_scaled(MOUSE_X, MOUSE_Y, SCALE, WIDTH, HEIGHT, SCREEN, FONT)

        pygame.display.update()
        CLOCK.tick(60)
    pygame.quit()
