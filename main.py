import pygame
from random import choice, randrange
from screeninfo import get_monitors


class Symbol:
    """ Single matrix symbol
    """
    def __init__(self, x: int, y: int, speed: int) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_alphabet)
        self.interval = randrange(5, 30)

    def draw(self, color: str) -> None:
        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_alphabet if color == 'green' else light_green_alphabet)
        self.y = self.y + self.speed if self.y < HEIGHT else - FONT_SIZE
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    """ Vertical column of matrix symbols
    """
    def __init__(self, x: int, y: int) -> None:
        self.column_height = randrange(14, 24)
        self.speed = randrange(2, 6)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self) -> None:
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]


monitor = get_monitors()[0]
RES = WIDTH, HEIGHT = monitor.width, monitor.height

FONT_SIZE = 23
alpha_value = 50

pygame.init()
screen = pygame.display.set_mode(RES)
surface = pygame.Surface(RES)
surface.set_alpha(alpha_value)
clock = pygame.time.Clock()

matrix_alphabet = [chr(int('0x30a0', 16) + index) for index in range(96)]
font = pygame.font.Font('MS_Mincho.ttf', FONT_SIZE)
green_alphabet = [font.render(char, True, (0, randrange(160, 256), 0)) for char in matrix_alphabet]
light_green_alphabet = [font.render(char, True, pygame.Color('#e3ffe4')) for char in matrix_alphabet]
symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]

sound = pygame.mixer.Sound('matrix.mp3')


def hello_neo(alpha: int = alpha_value) -> None:
    """ Start matrix
    """
    global alpha_value

    if alpha_value != alpha:
        alpha_value = alpha

    sound.play()
    while True:
        screen.blit(surface, (0, 0))
        surface.fill(pygame.Color('black'))

        [symbol_column.draw() for symbol_column in symbol_columns]

        if not pygame.time.get_ticks() % 20 and alpha_value < 150:
            alpha_value += 3
            surface.set_alpha(alpha_value)

        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    hello_neo(alpha=0)
