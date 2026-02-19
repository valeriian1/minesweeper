import os

# Базовий шлях до ресурсів
ASSETS_DIR = "assets"
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")

# Підпапки
BOARD_SPRITES = os.path.join(SPRITES_DIR, "board sprites")
HEADER_SPRITES = os.path.join(SPRITES_DIR, "header sprites")
ENDSCREEN_SPRITES = os.path.join(SPRITES_DIR, "endscreen sprites")

# Кольори (якщо знадобляться)
BG_COLOR = (255, 255, 255)

# Налаштування рівнів складності
DIFFICULTIES = {
    "easy": {
        "rows": 9,
        "cols": 9,
        "mines": 10,
        "cell_size": 40
    },
    "normal": {
        "rows": 16,
        "cols": 16,
        "mines": 40,
        "cell_size": 30
    },
    "hard": {
        "rows": 22,
        "cols": 22,
        "mines": 99,
        "cell_size": 25
    }
}

HEADER_HEIGHT = 80