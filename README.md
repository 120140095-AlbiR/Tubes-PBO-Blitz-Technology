import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Judul dan ikon
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('flappy.png')  
pygame.display.set_icon(icon)

# Gambar burung
bird = pygame.image.load('flappy.png') 
bird = pygame.transform.scale(bird, (60, 50))

# Gambar Zeus
zeus = pygame.image.load('zeus.png')  
zeus = pygame.transform.scale(zeus, (70, 70))

#gambar kayu/batu
obstacle_image = pygame.image.load('obstacle.png')  
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

# Posisi burung
bird_x = 50
bird_y = 300
bird_y_change = 0

# Gambar pipa
pipe_width = 70
pipe_height = random.randint(150, 450)
pipe_color = green
pipe_x_change = -4
pipe_x = screen_width

# Kecepatan gravitasi dan loncatan burung
gravity = 0.5
jump = -5

# Skor
score = 0
font = pygame.font.Font(None, 36)

# Posisi Zeus
zeus_appeared = False
zeus_x = screen_width // 2 - 35
zeus_y = -70
zeus_y_change = 3 

# Peluru
bullets = []

# Obstacle
obstacles = []

# Fungsi untuk menampilkan skor
def show_score():
    text = font.render("Score: " + str(score), True, black)
    screen.blit(text, [10, 10])

# Fungsi untuk menggambar pipa
def draw_pipe(pipe_x, pipe_height):
    pygame.draw.rect(screen, pipe_color, [pipe_x, 0, pipe_width, pipe_height])
    pygame.draw.rect(screen, pipe_color, [pipe_x, pipe_height + 200, pipe_width, screen_height - pipe_height - 200])

# Fungsi untuk layar awal
def show_start_screen():
    screen.fill(white)
    title_font = pygame.font.Font(None, 74)
    text = title_font.render("Flappy Bird", True, black)
    screen.blit(text, [screen_width // 2 - text.get_width() // 2, screen_height // 4])

    prompt_font = pygame.font.Font(None, 36)
    prompt_text = prompt_font.render("Press Any Key to Start", True, black)
    screen.blit(prompt_text, [screen_width // 2 - prompt_text.get_width() // 2, screen_height // 2])

    pygame.display.update()

# Fungsi utama permainan
def main_game():
    global bird_y, bird_y_change, pipe_x, pipe_height, score, zeus_appeared, bullets
    bird_y = 300
    bird_y_change = 0
    pipe_x = screen_width
    pipe_height = random.randint(150, 450)
    score = 0
    zeus_appeared = False
    bullets = []
    obstacles = []
    zeus_y = -70
    running = True

    while running:
        # Latar belakang
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = jump
                if event.key == pygame.K_v and zeus_appeared:
                    bullets.append([bird_x + 50, bird_y + 25])

        bird_y_change += gravity
        bird_y += bird_y_change

        if bird_y < 0:
            bird_y = 0
        elif bird_y > screen_height - 50:
            bird_y = screen_height - 50

        pipe_x += pipe_x_change

        if pipe_x < -pipe_width:
            pipe_x = screen_width
            pipe_height = random.randint(150, 450)
            score += 1

        draw_pipe(pipe_x, pipe_height)

        screen.blit(bird, (bird_x, bird_y))

        # Tampilkan Zeus jika skor mencapai 5
        if score >= 5 and not zeus_appeared:
            zeus_appeared = True

        if zeus_appeared:
            zeus_y += zeus_y_change
            screen.blit(zeus, (zeus_x, zeus_y))
            if zeus_y > screen_height:
                zeus_y = -70

        # Update dan gambar peluru
        for bullet in bullets:
            bullet[0] += 10
            pygame.draw.circle(screen, red, bullet, 5)

        # Hapus peluru yang keluar dari layar
        bullets = [bullet for bullet in bullets if bullet[0] < screen_width]

        show_score()

        # Check collision between bullets and obstacles
        for bullet in bullets:
            for obstacle in obstacles:
                if obstacle[0] < bullet[0] < obstacle[0] + 50 and obstacle[1] < bullet[1] < obstacle[1] + 50:
                    bullets.remove(bullet)
                    obstacles.remove(obstacle)
                    break
                
        # Check for collision
        if (bird_x + 50 > pipe_x and bird_x < pipe_x + pipe_width and (bird_y < pipe_height or bird_y + 50 > pipe_height + 200)):
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(30)

# Main loop
show_start_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            waiting = False
            main_game()

pygame.quit()
