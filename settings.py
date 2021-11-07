import numpy as np

from screeninfo import get_monitors


monitor = get_monitors()[0]

FONT_SIZE = 23
RES = WIDTH, HEIGHT = monitor.width, monitor.height
ALPHABET = np.array([chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for _ in range(10)])
