# main.py
import pygame
import sys
import traceback
import myplane
import enemy
import bullet

from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("EE551Spring2019 Aircraft War !!!")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def main():

    # Generate our aircraft
    me = myplane.MyPlane(bg_size)
    enemies = pygame.sprite.Group()

    # Generating small enemy aircraft
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # Generating middle enemy aircraft
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # Generating large enemy aircraft
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # Generating bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    clock = pygame.time.Clock()

    # Shot index
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # According score
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # Marks whether to pause the game
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image


    # Bombs that blow up all the planes on the screen
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3


    # Lift our aircraft invincible state timer
    INVINCIBLE_TIME = USEREVENT + 2

    # Number of lives
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # Used to prevent repeated opening of according files
    recorded = False

    # Game ending screen
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # Used to switch pictures
    switch_image = True

    # For delay
    delay = 100

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                       paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False


            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        screen.blit(background, (0, 0))
                
        if life_num and not paused:
            # Detect user's keyboard operations
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # Launch bullet
            if not(delay % 10):
                bullets = bullet1
                bullets[bullet1_index].reset(me.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                
            # Detect if the bullet hits the enemy plane
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            
            # Draw large enemy aircraft
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                else:
                    # Destroy
                    if not(delay % 3):
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            score += 10000
                            each.reset()

            # Draw middle enemy aircraft：
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                else:
                    # Destroy
                    if not(delay % 3):
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # Draw small enemy aircraft：
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # Destroy
                    if not(delay % 3):
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # Check if our plane is hit
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            
            # Draw our aircraft
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # Destroy
                if not(delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # Draw the number of bombs that blow up all the planes on the screen
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # Draw the number of lives
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, \
                                 height-10-life_rect.height))

            # Draw score
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        # Draw the game end screen
        elif life_num == 0:

            if not recorded:
                recorded = True
                # Read history highest score
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # Archive if the player scores higher than the highest score in history
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # Draw the end of the picture
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # Detect user's mouse operation
            # If the user presses the left mouse button
            if pygame.mouse.get_pressed()[0]:
                # Get mouse coordinates
                pos = pygame.mouse.get_pos()
                # If the user clicks "Restart"
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # Call the main function to restart the game
                    main()
                # If the user clicks "Game Over"
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # exit the game
                    pygame.quit()
                    sys.exit()      

        # Draw pause button
        screen.blit(paused_image, paused_rect)

        # Switch picture
        if not(delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()
        clock.tick(60)


# Test Code       
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()