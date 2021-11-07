import numpy as np
import pygame
import pygame.camera
import time

from random import choice, randrange
from settings import ALPHABET, FONT_SIZE, RES, WIDTH, HEIGHT


class MatrixVision:
    """ Matrix camera image """
    def __init__(self, app) -> None:
        self.app = app
        self.SIZE = self.ROWS, self.COLS = HEIGHT // FONT_SIZE, WIDTH // FONT_SIZE
        self.matrix = np.random.choice(ALPHABET, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(1, 500, size=self.SIZE)
        self.rendered_chars = self.get_rendered_chars()
        self.image = None

    @staticmethod
    def get_frame():
        """ Get pixels from camera image """
        image = matrix.camera.get_image()
        image = pygame.transform.scale(image, RES)
        pixel_array = pygame.pixelarray.PixelArray(image)
        return pixel_array

    def get_rendered_chars(self) -> dict:
        char_colors = [(0, green, 0) for green in range(256)]
        rendered_chars = {}
        for char in ALPHABET:
            rendered_char = {(char, color): self.app.font.render(char, True, color) for color in char_colors}
            rendered_chars.update(rendered_char)
        return rendered_chars

    def run(self) -> None:
        frames = pygame.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.draw()

    def shift_column(self, frames) -> None:
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    def change_chars(self, frames) -> None:
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(ALPHABET, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    def draw(self) -> None:
        self.image = self.get_frame()
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * FONT_SIZE, y * FONT_SIZE
                    _, red, green, blue = pygame.Color(self.image[pos])
                    if red and green and blue:
                        color = (red + green + blue) // 3
                        color = 220 if 160 < color < 220 else color
                        char = self.rendered_chars[(char, (0, color, 0))]
                        char.set_alpha(color + 60)
                        self.app.surface.blit(char, pos)


class Matrix:
    """ Matrix """
    def __init__(self, alpha=None) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(RES)
        self.surface = pygame.Surface(RES)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('MS_Mincho.ttf', FONT_SIZE)
        self.green_alphabet = [self.font.render(char, True, (0, randrange(160, 256), 0)) for char in ALPHABET]
        self.light_green_alphabet = [self.font.render(char, True, pygame.Color('#e3ffe4')) for char in ALPHABET]
        self.symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0), self) for x in range(0, WIDTH, FONT_SIZE)]
        self.alpha_value = alpha if alpha else 50
        self.sound = pygame.mixer.Sound('matrix.mp3')
        self.camera = None
        self.run_camera = False
        self.vision = MatrixVision(self)

    def draw(self) -> None:
        if not self.run_camera:
            self.screen.blit(self.surface, (0, 0))
            self.surface.fill(pygame.Color('black'))
        else:
            self.surface.fill(pygame.Color('black'))
            self.vision.run()
            self.screen.blit(self.surface, (0, 0))

    def hello_neo(self) -> None:
        """ RUN THE MATRIX """
        self.sound.play()
        pygame.camera.init()
        self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])

        while True:
            if not self.run_camera and pygame.key.get_pressed()[pygame.K_SPACE]:
                self.run_camera = True
                self.camera.start()
            elif self.run_camera and pygame.key.get_pressed()[pygame.K_SPACE]:
                self.run_camera = False
                self.camera.stop()
                time.sleep(0.1)

            self.draw()

            if not self.run_camera:
                [symbol_column.draw() for symbol_column in self.symbol_columns]
                if not pygame.time.get_ticks() % 20 and self.alpha_value < 150:
                    self.alpha_value += 3
                    self.surface.set_alpha(self.alpha_value)

            [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
            pygame.display.flip()
            self.clock.tick(60)


class Symbol:
    """ Single matrix symbol """
    def __init__(self, x: int, y: int, speed: int, app) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(app.green_alphabet)
        self.interval = randrange(5, 30)
        self.vision = app

    def draw(self, color: str) -> None:
        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(self.vision.green_alphabet if color == 'green' else self.vision.light_green_alphabet)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        self.vision.surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    """ Vertical column of matrix symbols """
    def __init__(self, x: int, y: int, app) -> None:
        self.column_height = randrange(14, 24)
        self.speed = randrange(2, 6)
        self.symbols = [Symbol(x, i, self.speed, app) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self) -> None:
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]


if __name__ == '__main__':
    matrix = Matrix(alpha=0)
    matrix.hello_neo()
