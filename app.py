import copy
from board import boards  # Import the boards module containing game levels
import pygame  # Import the pygame module for game development
import math  # Import the math module for mathematical operations

# Initialize pygame
pygame.init()

# Set up the screen dimensions
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Create a game screen
timer = pygame.time.Clock()  # Initialize a clock for controlling the frame rate
fps = 60  # Frames per second
font = pygame.font.Font('freesansbold.ttf', 20)  # Font for displaying text
level = copy.deepcopy(boards)  # Deep copy of the game levels
color = 'blue'  # Color for the game elements
PI = math.pi  # Pi constant from the math module

# Load player images and scale them
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

# Load ghost images and scale them
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))

# Player initial position and direction
player_x = 450
player_y = 663
direction = 0

# Ghosts' initial positions and directions
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2

# Game state variables
counter = 0
flicker = False
# Directions allowed for turning: Right, Left, Up, Down
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2  # Player movement speed
score = 0  # Player score
powerup = False  # Power-up state
power_counter = 0  # Counter for power-up duration
eaten_ghost = [False, False, False, False]  # Eaten state for each ghost
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]  # Targets for ghosts
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False  # Player moving state
ghost_speeds = [2, 2, 2, 2]  # Ghosts' movement speeds
startup_counter = 0  # Startup counter
lives = 3  # Player lives
game_over = False  # Game over state
game_won = False  # Game won state

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        # Initialize ghost attributes
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()  # Check possible turns and box status
        self.rect = self.draw()  # Draw the ghost and get its rectangle

    def draw(self):
        # Draw the ghost image based on its state
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        
        # Create a rectangle around the ghost for collision detection
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # Check for possible directions the ghost can turn
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            # If ghost is outside the main area, allow all turns
            self.turns[0] = True
            self.turns[1] = True

        # Check if the ghost is in the box
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        
        return self.turns, self.in_box


    def move_clyde(self):
        # Move Clyde based on his current direction and proximity to the target.
        # Clyde changes direction to pursue the target whenever advantageous.
        
        # Move right (direction 0)
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                # Move right if the target is to the right and the turn is allowed
                self.x_pos += self.speed
            elif not self.turns[0]:
                # Check vertical and left directions if right turn is not allowed
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
            elif self.turns[0]:
                # Continue moving right if right turn is allowed
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
                    
        # Move left (direction 1)
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3  # Turn down
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                # Check vertical and right directions if left turn is not allowed
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed

        # Move up (direction 2)
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1  # Turn left
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Check horizontal and down directions if up turn is not allowed
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed

        # Move down (direction 3)
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                # Check horizontal and up directions if down turn is not allowed
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed

        # Handle wrapping around the screen
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
            
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # Move Blinky based on his current direction and proximity to the target.
        # Blinky changes direction when colliding with walls, otherwise continues straight.
        
        # Move right (direction 0)
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                # Check vertical and left directions if right turn is not allowed
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed

        # Move left (direction 1)
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                # Check vertical and right directions if left turn is not allowed
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed

        # Move up (direction 2)
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Check horizontal and down directions if up turn is not allowed
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3  # Turn down
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed

        # Move down (direction 3)
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                # Check horizontal and up directions if down turn is not allowed
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2  # Turn up
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0  # Turn right
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Turn left
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed

        # Handle wrapping around the screen
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
            
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # Inky turns up or down at any point to pursue, but left and right only on collision
        
        # Move right (direction 0)
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                self.x_pos += self.speed
            elif not self.turns[0]:  # Cannot turn right, check other directions
                if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:  # Default to turn down if possible
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:  # Default to turn up if possible
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:  # Default to turn left if possible
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:  # Continue moving right if possible
                if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed

        # Move left (direction 1)
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                self.x_pos -= self.speed
            elif not self.turns[1]:  # Cannot turn left, check other directions
                if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:  # Default to turn down if possible
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:  # Default to turn up if possible
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:  # Default to turn right if possible
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:  # Continue moving left if possible
                if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed

        # Move up (direction 2)
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:  # Cannot turn up, check other directions
                if self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:  # Default to turn left if possible
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:  # Default to turn down if possible
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:  # Default to turn right if possible
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:  # Continue moving up if possible
                self.y_pos -= self.speed

        # Move down (direction 3)
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                self.y_pos += self.speed
            elif not self.turns[3]:  # Cannot turn down, check other directions
                if self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:  # Default to turn up if possible
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:  # Default to turn left if possible
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:  # Default to turn right if possible
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:  # Continue moving down if possible
                self.y_pos += self.speed

        # Handle wrapping around the screen
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # Pinky is going to turn left or right whenever advantageous, but only up or down on collision
        
        # Move right (direction 0)
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                self.x_pos += self.speed
            elif not self.turns[0]:  # Cannot turn right, check other directions
                if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:  # Default to turn down if possible
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:  # Default to turn up if possible
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:  # Default to turn left if possible
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:  # Continue moving right if possible
                self.x_pos += self.speed

        # Move left (direction 1)
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                self.x_pos -= self.speed
            elif not self.turns[1]:  # Cannot turn left, check other directions
                if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:  # Default to turn down if possible
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:  # Default to turn up if possible
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:  # Default to turn right if possible
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:  # Continue moving left if possible
                self.x_pos -= self.speed

        # Move up (direction 2)
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                self.y_pos -= self.speed
            elif not self.turns[2]:  # Cannot turn up, check other directions
                if self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:  # Default to turn left if possible
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:  # Default to turn down if possible
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:  # Default to turn right if possible
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:  # Continue moving up if possible
                self.y_pos -= self.speed

        # Move down (direction 3)
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:  # Target is below and can turn down
                self.y_pos += self.speed
            elif not self.turns[3]:  # Cannot turn down, check other directions
                if self.target[0] > self.x_pos and self.turns[0]:  # Target is to the right and can turn right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # Target is to the left and can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # Target is above and can turn up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:  # Default to turn up if possible
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:  # Default to turn left if possible
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:  # Default to turn right if possible
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:  # Continue moving down if possible
                self.y_pos += self.speed

        # Handle wrapping around the screen
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count, eaten_ghosts):#to see with what i made collision
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:#if the collision was the small circles
            level[center_y // num1][center_x // num2] = 0#turn them black
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:#if the collision was the big circles
            level[center_y // num1][center_x // num2] = 0#turn them black
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

#creating the board from the numbers
def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

#drawing players
def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):#check if i can move
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:#if my direction is up or down
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3: #check if down is available by the level (board numbers 0,1,2)
                    turns[3] = True #turn down
                if level[(centery - num3) // num1][centerx // num2] < 3:#check if up is available
                    turns[2] = True #turn up
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:#check if righ is available
                    turns[1] = True #turn righ
                if level[centery // num1][(centerx + num2) // num2] < 3:#check if left is available
                    turns[0] = True #turn left
        if direction == 0 or direction == 1:#if my direction is right or left
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):#how the player is moving by the variable speed i gave
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):#see the target of the ghosts
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:#if player is powerup
        if not blinky.dead and not eaten_ghost[0]:#if ghost is not dead and the ghost is not eaten
            blink_target = (runaway_x, runaway_y)#ghost should run away
        elif not blinky.dead and eaten_ghost[0]:#if ghost is eaten
            if 340 < blink_x < 560 and 340 < blink_y < 500:#and it is in the box
                blink_target = (400, 100)#the target is to go out from the box
            else:
                blink_target = (player_x, player_y)#if it is not in the box the target is the player
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:#if ghost inside the box
                blink_target = (400, 100)#the target is to go out of the box
            else:#if it is not in the box
                blink_target = (player_x, player_y)#the target is to go to the player
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')#first
    draw_board()#drawing the board
    center_x = player_x + 23#initializig positions
    center_y = player_y + 24#initializing positions
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)#put circle on the player to see when collide
    draw_player()#drawing the player
    #creating the ghosts
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                  clyde_box, 3)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    if not powerup:#if the player power is down
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):#if player circle collide with the ghost
            if lives > 0:#if life is not 0 reset everything and subtract the life
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:#else gameover
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:#if power is up and we collide with the ghost
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:#when i press the keyboard
            if event.key == pygame.K_RIGHT:#if to the right
                direction_command = 0
            if event.key == pygame.K_LEFT:#left
                direction_command = 1
            if event.key == pygame.K_UP:#up
                direction_command = 2
            if event.key == pygame.K_DOWN:#down
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):#if i pressed space when the game is over or won it will reset
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:#if i leaved the keyboard
            if event.key == pygame.K_RIGHT and direction_command == 0:#if it is to the right keep it
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:#if it is to the left keep it
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:#if it is to the up keep it
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:#if it is to the down keep it
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:#if iam going right and i can go right
        direction = 0
    if direction_command == 1 and turns_allowed[1]:#if iam going left and i can go left
        direction = 1
    if direction_command == 2 and turns_allowed[2]:#if iam going up and i can go up
        direction = 2
    if direction_command == 3 and turns_allowed[3]:#if iam going down and i can go down
        direction = 3

    if player_x > 900:#if the player reach the boundries of the game 
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky.in_box and blinky_dead:#if ghosts are in the box and they was dead ,make dead false
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()
