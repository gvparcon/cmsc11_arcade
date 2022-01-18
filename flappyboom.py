import pygame, sys, random

from pygame.time import set_timer

def flappymain():

    #-----------------------------------------GAME FUNCTIONS-----------------------------------------
    #For floor animation
    def repeat_floor():
        screen.blit(floor_image, (floor_position, 580))
        screen.blit(floor_image, (floor_position  + 1120, 580))

    #For creating blocks
    def create_block():
        block_position = random.choice(block_height)
        lower_block = block_image.get_rect(midtop = (1170, block_position))
        upper_block = block_image.get_rect(midbottom = (1170, block_position -200))
        return upper_block, lower_block

    #Move block positions
    def move_block(blocks):
        for block in blocks:
            block.centerx -= 5
        return blocks

    #Displays Blocks
    def display_block(blocks):
        for block in blocks:
            if block.bottom >= 630:
                screen.blit(block_image, block)
            else:
                upper_block = pygame.transform.flip(block_image, False, True)
                screen. blit(upper_block, block)

    #cheks for collisions
    def collision(blocks):
        global pass_pipe
        for block in blocks:
            if char_rect.colliderect(block):
                pass_pipe = True
                return False
        if char_rect.top <= -100 or char_rect.bottom >= 900:
            pass_pipe = True
            return False
        return True

    #The scoreboard
    def scoreboard(game_status,score):
        if game_status == 'playing':
            score_text = text.render(str(int((score))), True, (255, 255, 255))
            score_rect = score_text.get_rect(center = (560, 60))
            screen.blit(score_text, score_rect)

        if game_status == 'game_over':
            game_over_text = text.render(f'GAME OVER', True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center = (560, 60))
            screen.blit(game_over_text, game_over_rect)

            game_over_instruction_text = text.render(f'ESC TO EXIT', True, (255, 255, 255))
            game_over_instruction = game_over_instruction_text.get_rect(center = (560, 100))
            screen.blit(game_over_instruction_text, game_over_instruction)

            score_text = text.render(f'Score: {int(score)}', True, (255, 255, 255))
            score_rect = score_text.get_rect(center = (560, 510))
            screen.blit(score_text, score_rect)

            high_score_text = text.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center = (560, 550))
            screen.blit(high_score_text, high_score_rect)
    
    #GameExit
    def gameexit(running, score):
        runexit = True
        while runexit:
            scoreboard('game_over', score)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running == False
                        runexit = False
            pygame.display.update()      

    #for checking score    
    def check_score(score, high_score):
        if score > high_score:
            high_score = score
        return high_score

    #adds score
    def add_score(score,pass_pipe):
        if block_list:       
            for block in block_list:
                if 95 < block.centerx < 105 and pass_pipe:
                    score += 1
                    pass_pipe = False
                if block.centerx < 0:
                    pass_pipe = True
        return score, pass_pipe
    
    #pause function
    def pause():
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        paused = False     

    #-----------------------------------------GAME INITIALIZATIONS-----------------------------------------

    pygame.init()
    pygame.display.set_caption('Flappy Bat')
    screen = pygame.display.set_mode((1120, 630))
    clock = pygame.time.Clock()
    text = pygame.font.Font('flappy_resources/04B_19.ttf',40)

    #-----------------------------------------GAME VARIABLES-----------------------------------------

    gravity = 0.25
    char_motion = 0
    active = True
    score = 0
    high_score = 0
    pass_pipe = True

    #-----------------------------------------GAME RESOURCES-----------------------------------------

    #background image
    bg_image = pygame.image.load('flappy_resources/background.jpg').convert()

    #floor image
    floor_image = pygame.image.load('flappy_resources/floor.png').convert_alpha()
    floor_position = 0

    #character image
    char_image = pygame.image.load('flappy_resources/bat.png').convert_alpha()
    char_image = pygame.transform.scale(char_image,  (80, 80))
    char_rect = char_image.get_rect(center = (200, 315))

    #block image
    block_image = pygame.image.load('flappy_resources/pipe.png').convert()
    block_image = pygame.transform.scale2x(block_image)
    block_list = []
    SPAWNBLOCK = pygame.USEREVENT
    pygame.time.set_timer(SPAWNBLOCK, 1500)
    block_height = [230, 300, 400, 500, 550]

    #-----------------------------------------MAIN GAME LOOP-----------------------------------------
    running = True
    while running:
        #for loop
        for interaction in pygame.event.get():
            if interaction.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #if space is pressed
            if interaction.type == pygame.KEYDOWN: 
                if interaction.key == pygame.K_SPACE:
                    char_motion = 0                     
                    char_motion -= 7
                if interaction.key == pygame.K_SPACE and active == False:
                    active == True
                    block_list.clear()
                    char_rect.center =  (100, 315)
                    char_motion =  0
                    score = 0
                if interaction.key == pygame.K_RETURN:
                    pause()

            if interaction.type == SPAWNBLOCK:
                block_list.extend(create_block())

        screen.blit(bg_image,(0, 0))
        
        if active:
            #Character
            char_motion += gravity
            char_rect.centery += char_motion
            screen.blit(char_image, char_rect)
            active = collision(block_list)

            #Block
            block_list = move_block(block_list)
            display_block(block_list)

            #Score
            score, pass_pipe = add_score(score,pass_pipe)
            scoreboard('playing',score)

        else:
            high_score = check_score(score, high_score)
            
            running = gameexit(running,score)
            # running = False
            
        #Floor
        floor_position -= 2
        repeat_floor()
        if floor_position <= -1120:
            floor_position = 0
    
        pygame.display.update()
        clock.tick(120) 


#flappymain()