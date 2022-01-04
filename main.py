from random import randrange

import pygame

RES, SIZE = 800, 50

x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
snake = [(x, y)]

dris = {"W": True, "S": True, "A": True, "D": True}
dx, dy = 0, 0

fps = 10
score = 0
length = 1

# start pygame main window
pygame.init()
# set screen dimensions
sc = pygame.display.set_mode([RES, RES])
# compute how many milliseconds have passed since the previous call
clock = pygame.time.Clock()
# some fonts
font_score = pygame.font.SysFont("Arial", 26, bold=True)
font_end = pygame.font.SysFont("Arial", 66, bold=True)
img = pygame.image.load('3.jpg').convert()



def controller(key, switches):
    global dy, dx, dris

    """ Snake game controller that uses [W, A, S, D] as the keys responsible for the movement

    Args:
        key: pygame keyboard event listener
        switches: initial keyboard switches to control the game
    """
    # preventing our snake from going into opposite direction
    if key[pygame.K_w] and switches["W"]:
        dris = {"W": True, "S": False, "A": True, "D": True}
        dx, dy = 0, -1
    if key[pygame.K_s] and switches["S"]:
        dx, dy = 0, 1
        dris = {"W": False, "S": True, "A": True, "D": True}
    if key[pygame.K_a] and switches["A"]:
        dx, dy = -1, 0
        dris = {"W": True, "S": True, "A": True, "D": False}
    if key[pygame.K_d] and switches["D"]:
        dx, dy = 1, 0
        dris = {"W": True, "S": True, "A": False, "D": True}


while True:
    sc.blit(img, (0, 0))
    score_txt = font_score.render(
        f"score: {score}", True, pygame.Color("green"), pygame.Color("blue")
    )
    # drawing snake
    [
        (pygame.draw.rect(sc, pygame.Color("green"), (i, j, SIZE - 2, SIZE - 2)))
        for i, j in snake
    ]
    pygame.draw.rect(sc, pygame.Color("red"), (*apple, SIZE, SIZE))
    # snake movements
    x += dx * SIZE
    y += dy * SIZE

    # How to make our snake not infinity?
    # There is an answer
    snake.append((x, y))
    snake = snake[-length:]

    # eating apples
    if snake[-1] == apple:
        apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        length += 1
        fps += 0.5
        score += 1

    # end of the game
    if (
        x < 0
        or x > RES - SIZE
        or y < 0
        or y > RES - SIZE
        or len(snake) != len(set(snake))
    ):
        while True:
            render_end = font_end.render("GAME OVER", True, pygame.Color("orange"))
            end_score = font_end.render(
                f"Your Score: {score}", True, pygame.Color("orange")
            )
            sc.blit(render_end, (RES // 2 - 200, RES // 3))
            sc.blit(end_score, (RES // 2 - 200, RES // 3 + 90))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
    # render the score of the player
    sc.blit(score_txt, (0, 0))

    pygame.display.flip()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # control
    key = pygame.key.get_pressed()
    controller(key, dris)

