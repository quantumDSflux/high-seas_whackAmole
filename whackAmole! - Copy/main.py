import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
PIPE_SIZE = 100
MOLE_SIZE = 80
PIRANHA_SIZE = 90  # Increased size of Piranha
pipe_image = pygame.image.load("pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (PIPE_SIZE, PIPE_SIZE))
mole_image = pygame.image.load("mole.png")
mole_image = pygame.transform.scale(mole_image, (MOLE_SIZE, MOLE_SIZE))
piranha_image = pygame.image.load("piranha.png")
piranha_image = pygame.transform.scale(piranha_image, (PIRANHA_SIZE, PIRANHA_SIZE))

# Load background image
bg_image = pygame.image.load("bg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  # Scale to fit screen size

# Load scare image
scare_image = pygame.image.load("scare.png")
scare_image = pygame.transform.scale(scare_image, (WIDTH, HEIGHT))  # Scale to fit the screen

# Game settings
GRID_SIZE = 3  # 3x3 grid
GAP = 10
MOLE_LIFETIME = 700  # Milliseconds mole is visible
PIRANHA_LIFETIME = 1000  # Milliseconds Piranha is visible

# Score
score = 0
font = pygame.font.Font(None, 36)

# Pipe positions based on grid size
pipe_positions = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        x = col * (PIPE_SIZE + GAP) + (WIDTH - (GRID_SIZE * (PIPE_SIZE + GAP))) // 2
        y = row * (PIPE_SIZE + GAP) + (HEIGHT - (GRID_SIZE * (PIPE_SIZE + GAP))) // 2
        pipe_positions.append((x, y))

# Initial mole, piranha, and timers with random transition delays
mole_index = random.randint(0, len(pipe_positions) - 1)
piranha_index = random.randint(0, len(pipe_positions) - 1)
mole_start_time = pygame.time.get_ticks() + random.randint(1000, 3000)  # Delay before mole starts
piranha_start_time = pygame.time.get_ticks() + random.randint(3000, 5000)  # Delay before piranha starts
mole_transition_delay = random.randint(1000, 2000)  # Random transition delay for mole
piranha_transition_delay = random.randint(2000, 4000)  # Random transition delay for piranha

# Trick move counter to limit the number of trick-based movements
trick_move_count = 0  # Counter for how many times mole should be moved due to hover tricks

# Game loop
running = True
game_over = False
scare_image_time = 0  # Time to show scare image

while running:
    screen.blit(bg_image, (0, 0))  # Draw the background image first
    
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mole_x, mole_y = pipe_positions[mole_index]
            piranha_x, piranha_y = pipe_positions[piranha_index]
            
            # Check if mole is clicked
            if (mole_x <= mouse_x <= mole_x + MOLE_SIZE and
                mole_y - 40 <= mouse_y <= mole_y + MOLE_SIZE - 40):
                score += 1
                mole_index = random.randint(0, len(pipe_positions) - 1)
                mole_start_time = pygame.time.get_ticks() + random.randint(1000, 3000)  # Reset random delay for mole
                mole_transition_delay = random.randint(1000, 2000)  # Reset random delay for mole

            # Check if piranha is clicked, end game
            elif (piranha_x + 10 <= mouse_x <= piranha_x + PIRANHA_SIZE + 10 and
                  piranha_y - 40 <= mouse_y <= piranha_y + PIRANHA_SIZE - 40):
                # Game over
                game_over = True
                scare_image_time = pygame.time.get_ticks() + 1500  # Wait 1.5 seconds to show scare image

    # Draw pipes
    for pipe_x, pipe_y in pipe_positions:
        screen.blit(pipe_image, (pipe_x, pipe_y))

    # Mole appearance with random transition delay
    current_time = pygame.time.get_ticks()
    if current_time - mole_start_time > mole_transition_delay:
        mole_index = random.randint(0, len(pipe_positions) - 1)
        mole_start_time = current_time + MOLE_LIFETIME  # Set next time mole will disappear
        mole_transition_delay = random.randint(1000, 2000)  # New random delay for next mole appearance

    # Draw mole above the pipe
    mole_x, mole_y = pipe_positions[mole_index]
    screen.blit(mole_image, (mole_x + (PIPE_SIZE - MOLE_SIZE) // 2, mole_y - (MOLE_SIZE // 2)))  # Offset for mole

    # Piranha appearance with random transition delay
    if current_time - piranha_start_time > piranha_transition_delay:
        piranha_index = random.randint(0, len(pipe_positions) - 1)
        piranha_start_time = current_time + PIRANHA_LIFETIME  # Set next time piranha will disappear
        piranha_transition_delay = random.randint(2000, 4000)  # New random delay for next piranha appearance

    # Draw Piranha slightly to the right above the pipe
    piranha_x, piranha_y = pipe_positions[piranha_index]
    screen.blit(piranha_image, (piranha_x + 10 + (PIPE_SIZE - PIRANHA_SIZE) // 2, piranha_y - (PIRANHA_SIZE // 2)))

    # Tricks: Hover effects
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Check if mouse hovers over mole
    mole_x, mole_y = pipe_positions[mole_index]
    if mole_x <= mouse_x <= mole_x + MOLE_SIZE and mole_y - 40 <= mouse_y <= mole_y + MOLE_SIZE - 40:
        # Trick 1: Swap positions of mole and piranha (triggered only 7 times in 10 moves)
        if trick_move_count < 7 and random.random() < 0.1:  # 10% chance to trigger swap, 7 times in 10 moves
            mole_index, piranha_index = piranha_index, mole_index
            trick_move_count += 1  # Increment the trick move count
        
        # Trick 2: Change mole's pipe on hover (triggered only 7 times in 10 moves)
        if trick_move_count < 7 and random.random() < 0.2:  # 20% chance to change pipe
            mole_index = random.randint(0, len(pipe_positions) - 1)
            trick_move_count += 1  # Increment the trick move count
        
    # Reset trick_move_count after every 10 moves
    if trick_move_count >= 7:
        trick_move_count = 0

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Show scare image after 1.5 seconds
    if game_over and current_time > scare_image_time:
        screen.blit(scare_image, (0, 0))  # Display scare image over the whole screen

    # Refresh display
    pygame.display.flip()

    # Control frame rate
    pygame.time.delay(30)  # Small delay to control update frequency

pygame.quit()
