import pygame, random

pygame.init()

#Set display surface
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = 1

score = 0
player_lives = PLAYER_STARTING_LIVES
MAX_GAME_TIME = 30  

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1,1])
clown_dy = random.choice([-1,1])

#Set Colors
BLUE = (1,175,209)
YELLOW = (248,231,28)

#Set fonts
font = pygame.font.Font("/Users/sammymylove/Desktop/Pygame/Catch_the_clown/Franxurter.ttf", 32)

#Set text
title_text = font.render("Catch the Clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (100,10)

score_text = font.render("Score:" + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH -50, 10)

lives_text = font.render("Lives:" + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH -50, 50)

gameover_text = font.render("GAMEOVER", True, YELLOW, BLUE)
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Click anywhere to play again" , True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set sounds and music
click_sound = pygame.mixer.Sound("/Users/sammymylove/Desktop/Pygame/Catch_the_clown/click_sound.wav")
miss_sound = pygame.mixer.Sound("/Users/sammymylove/Desktop/Pygame/Catch_the_clown/miss_sound.wav")
pygame.mixer.music.load("/Users/sammymylove/Desktop/Pygame/Catch_the_clown/back_music.wav")

#Set images
back_image = pygame.image.load("/Users/sammymylove/Desktop/Pygame/Catch_the_clown/back.png")
back_rect = back_image.get_rect()
back_rect.topleft = (0,0)

clown_image = pygame.image.load("/Users/sammymylove/Desktop/Pygame/Catch_the_clown/clown.png")
clown_rect = clown_image.get_rect()
clown_rect.centerx = (WINDOW_HEIGHT//2)
clown_rect.centery = (WINDOW_WIDTH//2)

#Loop
start_time = pygame.time.get_ticks()
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    #Check if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #A click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            #The clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                #Move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
                while(previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
            #We missed the clown
            else:
                miss_sound.play()
                player_lives -= 1

    #Move the clown
    clown_rect.x += clown_dx*clown_velocity
    clown_rect.y += clown_dy*clown_velocity

    #Bounce the clown off the edges of the display
    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx = -1*clown_dx
    if clown_rect.top <= 0 or clown_rect.bottom >= WINDOW_HEIGHT:
        clown_dy = -1*clown_dy

    # Update game state
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, MAX_GAME_TIME - elapsed_time // 1000)
    remaining_time_text = font.render(str(remaining_time), True, YELLOW)

    #Update HUD
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)
    timer_text = font.render("Time: " + str(remaining_time), True, YELLOW)
    timer_rect = timer_text.get_rect()
    timer_rect.bottomright = (WINDOW_WIDTH -50, 590)


    #Gameover
    if remaining_time == 0 or player_lives == 0:
        display_surface.blit(gameover_text,gameover_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()

     #Pause the game until the player clicks then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #The player wants to play again.
                start_time = pygame.time.get_ticks()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    remaining_time = MAX_GAME_TIME 

                    clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                    running = True
                #The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    #Blit background
    display_surface.blit(back_image, back_rect)

    #Blit HUD 
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(lives_text,lives_rect)
    display_surface.blit(timer_text, timer_rect)

    #Blit assets to screen
    display_surface.blit(clown_image,clown_rect)
 
    #Update display and tick the clock 
    pygame.display.update()
    clock.tick(FPS)


#End the game
pygame.quit()