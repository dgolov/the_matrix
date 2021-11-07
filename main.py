import pygame
from random import choice, randrange
from screeninfo import get_monitors


class Matrix:
    """ Run the matrix """
    def __init__(self, vision, alpha=None) -> None:
        self.vision = vision
        self.alpha_value = alpha if alpha else 50

    def hello_neo(self) -> None:
        """ RUN """
        self.vision.sound.play()
        while True:
            self.vision.screen.blit(self.vision.surface, (0, 0))
            self.vision.surface.fill(pygame.Color('black'))

            [symbol_column.draw() for symbol_column in self.vision.symbol_columns]

            if not pygame.time.get_ticks() % 20 and self.alpha_value < 150:
                self.alpha_value += 3
                self.vision.surface.set_alpha(self.alpha_value)

            [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
            pygame.display.flip()
            self.vision.clock.tick(60)


class MatrixVision:
    """ Matrix vision """
    def __init__(self):
        monitor = get_monitors()[0]
        pygame.init()

        self.RES = self.WIDTH, self.HEIGHT = monitor.width, monitor.height
        self.FONT_SIZE = 23
        self.screen = pygame.display.set_mode(self.RES)
        self.surface = pygame.Surface(self.RES)
        self.clock = pygame.time.Clock()
        matrix_alphabet = [chr(int('0x30a0', 16) + index) for index in range(96)]
        font = pygame.font.Font('MS_Mincho.ttf', self.FONT_SIZE)
        self.green_alphabet = [font.render(char, True, (0, randrange(160, 256), 0)) for char in matrix_alphabet]
        self.light_green_alphabet = [font.render(char, True, pygame.Color('#e3ffe4')) for char in matrix_alphabet]
        self.symbol_columns = [SymbolColumn(x, randrange(-self.HEIGHT, 0), self)
                               for x in range(0, self.WIDTH, self.FONT_SIZE)]
        self.sound = pygame.mixer.Sound('matrix.mp3')


class Symbol:
    """ Single matrix symbol """
    def __init__(self, x: int, y: int, speed: int, vision) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(vision.green_alphabet)
        self.interval = randrange(5, 30)
        self.vision = vision

    def draw(self, color: str) -> None:
        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(self.vision.green_alphabet if color == 'green' else self.vision.light_green_alphabet)
        self.y = self.y + self.speed if self.y < self.vision.HEIGHT else - self.vision.FONT_SIZE
        self.vision.surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    """ Vertical column of matrix symbols """
    def __init__(self, x: int, y: int, vision) -> None:
        self.column_height = randrange(14, 24)
        self.speed = randrange(2, 6)
        self.symbols = [Symbol(x, i, self.speed, vision)
                        for i in range(y, y - vision.FONT_SIZE * self.column_height, -vision.FONT_SIZE)]

    def draw(self) -> None:
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]


if __name__ == '__main__':

    matrix_vision = MatrixVision()
    matrix = Matrix(vision=matrix_vision, alpha=0)
    matrix.hello_neo()
