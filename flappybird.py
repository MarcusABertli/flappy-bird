import pygame
from random import randint
pygame.init()
gw, gh = 551, 720
bx,by = 100, 300
v, g  = 0, 0.5
tpx, tpy = 0,-500 
gap = 150
pipe_timer = 0
gnd_x = 0
pipes = []
score = 0
game_over = False
last_score = 0
intro = True
index = 0  
frame = 0 
scr = pygame.display.set_mode((gw, gh))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
bg   = pygame.image.load("background.png")
gnd  = pygame.image.load("ground.png")
bird1 = pygame.image.load("bird_up.png")
bird2 = pygame.image.load("bird_mid.png")
bird3 = pygame.image.load("bird_down.png")
topi = pygame.image.load("pipe_top.png")
bopi = pygame.image.load("pipe_bottom.png")
over = pygame.image.load("game_over.png")
begi = pygame.image.load("start.png")
bird_list = [bird1, bird2, bird3]
running = True 
co = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    frame += 1
    if frame >= 5: 
        index = (index + 1) 
        frame = 0
        if index == 3:
            index = 0
    bird = bird_list[index]
    keys = pygame.key.get_pressed()
    if intro:
        scr.blit(bg, (0,0))
        scr.blit(begi, (184, 120))
        if keys[pygame.K_SPACE]:
            intro = False
    else:
        if pipe_timer <=0:
            tpy = randint(-600, -450)
            bpy = tpy + topi.get_height() + gap
            pipes.append([gw, tpy, "top",False])
            pipes.append([gw, bpy, "bottom",False])
            pipe_timer = 90
        pipe_timer -= 1
        if keys[pygame.K_SPACE]:
            v = -4.5
        v += g
        by += v 
       
        scr.blit(bg, (0, 0))
        new_pipes = []
        bird_rect = bird.get_rect(topleft=(bx, by))
        for p in pipes:
            x, y, kind, passed = p
            if kind == "top": 
                pipe_rect = topi.get_rect(topleft=(x, y))
                scr.blit(topi,(x, y))
            else:
                pipe_rect = bopi.get_rect(topleft=(x, y))
                scr.blit(bopi,(x, y))
                pipe_right = x + bopi.get_width() 
                if pipe_right < bx and not passed and not game_over:
                    score+=1
                    passed = True   
            if bird_rect.colliderect(pipe_rect):          
                game_over = True
                last_score = score
                if last_score > score:
                    last_score = score
            new_pipes.append([x-2, y, kind, passed])
        pipes = new_pipes
        gnd_rect = gnd.get_rect(topleft=(gnd_x, 520)) 
        if bird_rect.colliderect(gnd_rect):
            game_over = True 
            last_score = score
            if last_score > score:
                last_score = score
        if not game_over:
            score_surface = font.render(f"Score: {score}", True, (255,255,255),None)
            scr.blit(score_surface, (20, 20))
            max_score = font.render(f"Max Score: {last_score}", True, (255,255,255),None)
            scr.blit(max_score, (20, 50))
        else: 
            by += 10
            scr.blit(over, (175, 120))
            score_max = font.render(f"Score: {score}", True, (255,255,255),None)
            scr.blit(score_max, (20, 20)) 
            max_score = font.render(f"Max Score: {last_score}", True, (255,255,255),None)
            scr.blit(max_score, (20, 50))
            if keys[pygame.K_r]:
                bx,by = 100, 300
                v, g  = 0, 0.5
                tpx, tpy = 0,-500   # -600
                pipe_timer = 0
                gnd_x = 0
                pipes = []
                score = 0
                game_over = False
                intro = True
    scr.blit(gnd, (gnd_x, 520))
    scr.blit(gnd, (gnd_x + 551, 520))
    scr.blit(bird, (bx, by))
    if gnd_x <= -551:
        gnd_x = 0
    gnd_x -= 2
    pygame.display.flip()
    clock.tick(60)