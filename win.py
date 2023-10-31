import pygame
import numpy as np

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
window_width = 800
window_height = 600

# Tạo cửa sổ pygame
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('BS Matrix Visualization')

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)

# Hàm để vẽ ma trận BS và các thông tin liên quan
def draw_bs_matrix(bs_matrix, bs_loads):
    screen.fill(white)  # Xóa màn hình

    # Vẽ ma trận BS
    for y, row in enumerate(bs_matrix):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, black, (x * 40, y * 40, 40, 40))

    # Hiển thị thông tin BS Loads
    font = pygame.font.Font(None, 36)
    for y, row in enumerate(bs_loads):
        for x, load in enumerate(row):
            text = font.render(f'{load:.2f}', True, black)
            screen.blit(text, (x * 40, (y + 5) * 40))

    pygame.display.flip()  # Cập nhật màn hình

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dữ liệu ma trận BS và BS Loads từ dữ liệu bạn đã cung cấp
    bs_matrix1 = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 1]])
    bs_matrix2 = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 1]])
    bs_loads1 = np.array([[0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.125, 0.1], [0.1, 0.1, 0.125, 0.0, 0.125], [0.1, 0.1, 0.1, 0.125, 0.1]])
    bs_loads2 = np.array([[0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.125, 0.1, 0.125, 0.1], [0.125, 0.0, 0.15, 0.0, 0.125], [0.1, 0.125, 0.1, 0.125, 0.1]])

    # Vẽ ma trận BS và BS Loads
    draw_bs_matrix(bs_matrix1, bs_loads1)
    pygame.time.delay(2000)  # Hiển thị trong 2 giây
    draw_bs_matrix(bs_matrix2, bs_loads2)
    pygame.time.delay(2000)  # Hiển thị trong 2 giây

pygame.quit()  # Kết thúc pygame
