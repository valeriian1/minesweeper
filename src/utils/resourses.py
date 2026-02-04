
# import pygame
# import os

# class ResourceManager:
#     def __init__(self):
#         # Словник для зберігання завантажених зображень (поле images: dict)
#         self.images = {}

#     def load_assets(self):
#         """
#         Завантажує всі необхідні картинки з папки assets.
#         Цей метод викликається один раз на початку гри.
#         """
#         # Шлях до папки з картинками (припускаємо, що вона в корені проєкту)
#         assets_path = os.path.join('assets', 'sprites')
        
#         # Список назв файлів, які нам потрібні
#         # Ви можете додати сюди свої назви файлів
#         image_names = [
#             'closed', 'empty', 'mine', 'mine_exploded', 'flag',
#             '1', '2', '3', '4', '5', '6', '7', '8'
#         ]

#         for name in image_names:
#             file_path = os.path.join(assets_path, f"{name}.png")
#             try:
#                 # Завантажуємо картинку
#                 img = pygame.image.load(file_path).convert_alpha()
                
#                 # Масштабуємо картинку під розмір клітинки (наприклад, 32x32)
#                 # Розмір можна винести в constants.py
#                 img = pygame.transform.scale(img, (32, 32))
                
#                 self.images[name] = img
#             except pygame.error:
#                 print(f"Помилка: Не вдалося завантажити файл {file_path}")
#                 # Створюємо порожню поверхню, щоб програма не "впала", якщо картинки немає
#                 self.images[name] = pygame.Surface((32, 32))

#     def get_image(self, name):
#         """Повертає зображення за його назвою."""
#         return self.images.get(name)
