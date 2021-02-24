import pygame
import time
import random


# Color values
black = (0, 0, 0)
white = (255, 255, 255)
blue = (64, 224, 208)
green = (34, 139, 34)


pygame.init()

surface_width = 800
surface_height = 500
surface = pygame.display.set_mode((surface_width, surface_height))
clock = pygame.time.Clock()

pygame.display.set_caption('Flabby Pird')
img = pygame.image.load('flap.png')
img_width, img_height = img.get_size()


def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(surface, green, [
                     x_block, y_block, block_width, block_height])
    pygame.draw.rect(surface, green, [
                     x_block, y_block + block_height+gap, block_width, surface_height])


def show_score(score):
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render(f'Score: {score}', True, white)
    surface.blit(text, [3, 3])


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            continue
        return event.key
    return None


def make_text_objs(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def msg_surface(msg_large, msg_small):
    text_small = pygame.font.Font('freesansbold.ttf', 20)
    text_large = pygame.font.Font('freesansbold.ttf', 130)

    title_text_surf, title_text_rect = make_text_objs(msg_large, text_large)
    title_text_rect.center = surface_width / 2, surface_height / 2
    surface.blit(title_text_surf, title_text_rect)

    type_text_surf, type_text_rect = make_text_objs(msg_small, text_small)
    type_text_rect.center = surface_width / 2, ((surface_height / 2) + 100)
    surface.blit(type_text_surf, type_text_rect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()


def game_over_(score):
    msg_surface('Game Over', f'Your score is {score}')
    main()


def pause_game():
    msg_surface('Game Paused', 'Press any key to continue')


def bird(x, y, img):
    surface.blit(img, (x, y))


def main():
    x = 150
    y = 200
    y_move = 0
    game_over = False
    game_paused = False

    x_block = surface_width
    y_block = 0
    block_width = 50
    block_height = random.randint(0, surface_height / 2)
    gap = img_height * 5

    # block speeds
    block_move = 5

    score = 0

    while game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True  # Quit game

            if event.type == pygame.KEYDOWN:  # When Up key is pressed
                # if event.key == pygame.K_ESCAPE:
                #     game_paused = True
                if event.key == pygame.K_UP:
                    y_move = -4
                    # game_paused = False

                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:  # When Up key is released
                    y_move = 3

        # game paused
        # if game_paused:
        #     pause_game()

        y += y_move

        surface.fill(blue)
        bird(x, y, img)

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        # game boundaries
        if y > surface_height - img_height or y < 0:
            game_over_(score)

        # see if blocks on screen
        if x_block < (-1 * block_width):
            x_block = surface_width
            block_height = random.randint(0, surface_width / 2)

        # collision detect
        if x + img_width > x_block and x < x_block + block_width:
            if y < block_height or y + img_height > block_height + gap:
                game_over_(score)

        show_score(score)

        # score increase
        if x > x_block + block_width and x < x_block + block_width + img_width / 5:
            score += 1

        pygame.display.update()
        clock.tick(80)


if __name__ == '__main__':
    main()
    pygame.quit()
    quit()
