import pygame
from sys import exit
from random import randint

# Class Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5            
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= 2:
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def reset(self):
        self.rect.midbottom = (80,300)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

# Class Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "snail":
            snail_surf1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_surf2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_surf1,snail_surf2]
            y_pos = 300
        elif type == "fly":
            fly_surf1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_surf2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_surf1,fly_surf2]
            y_pos = 180
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(800,1200),y_pos))

    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= 2:
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= i
        self.destroy()

# Class Gameover
class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # player gameover
        self.player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2) #transforming surface
        self.image = self.player_stand
        self.rect = self.player_stand.get_rect(center = (400,200))

# score/time counter
def display_score():
    current_time = pygame.time.get_ticks() - start_time #time in ms   
    score_surf = test_font.render(f' Score: {int(current_time/1000)}',False,"White") # text, anti-aliasing, color
    score_rect = score_surf.get_rect(center = (400,50))  
    screen.blit(score_surf,score_rect)
    return current_time

# collision
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): #sprite destroyed or not
        obstacle_group.empty()
        player.sprite.reset()
        return False
    else:
        return True

# game init
pygame.init() #start engine
screen = pygame.display.set_mode((800,400)) #width and height
pygame.display.set_caption("Apocalyptic Runner") #title
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50) # font type and size
game_active = False
start_time = 0
score = 0
i = 5
maxscore = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

# using sprites
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
gameover = pygame.sprite.GroupSingle()
gameover.add(Gameover())

# background def
sky_surface = pygame.image.load('graphics/sky_2.png').convert()
sky_surface = pygame.transform.rotozoom(sky_surface,0,0.5)
ground_surface = pygame.image.load('graphics/ground.png').convert()

# text gameover
name_gameover = test_font.render('Apocalyptic Runner',False,'White')
name_gameover_rect = name_gameover.get_rect(center = (400,70))
inst_gameover = test_font.render('Press space to start',False,'White')
inst_gameover_rect = inst_gameover.get_rect(center = (400,350))

# timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,300)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,100)

# GAME LOOP
while True:

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:

            if event.type == obstacle_timer:
                i += 1
                prob = randint(0,10)
                if prob > 4:
                    obstacle_group.add(Obstacle('snail'))
                elif prob <= 4:
                    obstacle_group.add(Obstacle('fly'))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    #snail_rect.left = 800
                    start_time = pygame.time.get_ticks()
            
    if game_active:

        # background show
        screen.blit(sky_surface,(0,-150)) # show surface, position
        screen.blit(ground_surface,(0,300)) # order matters, sky is behind, ground is layer 2
        score = display_score()

        # collision:
        game_active = collision_sprite()

        #  sprite draw:
        player.draw(screen) #need surface to draw
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

 
    elif game_active == False:
        screen.fill((65,65,65))
        screen.blit(inst_gameover,inst_gameover_rect)
        gameover.draw(screen)

        if score == 0:
            screen.blit(name_gameover,name_gameover_rect)
        else:

            final_score = test_font.render(f'Pontos: {int(score/1000)}',False,'White')
            final_score_rect = final_score.get_rect(center = (400,70))
            screen.blit(final_score,final_score_rect)
            if score > maxscore:
                maxscore=score  
            max_score = test_font.render(f'Recordista: {int(maxscore/1000)}',False,'White')
            max_score_rect = max_score.get_rect(center = (400,30))
            screen.blit(max_score,max_score_rect)
        player_gravity = 0
        i = 5

    # loop update
    pygame.display.update()
    clock.tick(60) # controlling max fps

#continue at 3:38:00