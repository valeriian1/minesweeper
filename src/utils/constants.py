import os

# Базовий шлях до ресурсів
ASSETS_DIR = "assets"
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")

# Підпапки
BOARD_SPRITES = os.path.join(SPRITES_DIR, "board sprites")
HEADER_SPRITES = os.path.join(SPRITES_DIR, "header sprites")
ENDSCREEN_SPRITES = os.path.join(SPRITES_DIR, "endscreen sprites")

# Кольори та візуальні параметри
BG_COLOR = (255, 255, 255)

# Закрита клітинка (напівпрозора маска)
CLOSED_CELL_COLOR = (55, 50, 200)
CLOSED_CELL_ALPHA = 110

# Оверлей кінця гри (затемнення)
OVERLAY_COLOR = (0, 0, 0)
OVERLAY_ALPHA = 180

# Анімація — інтервал зміни кадрів (мс)
ANIM_INTERVAL_HEADER = 400
ANIM_INTERVAL_ENDSCREEN = 500

# Хедер-дисплей — ширина однієї цифри
DIGIT_WIDTH = 19

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