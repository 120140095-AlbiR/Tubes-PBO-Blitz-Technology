import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()

# Mengatur lagu dan suara
pygame.mixer.music.load("assets\sound.mp3")
pygame.mixer.music.play(-1)
zeus_coming_sound = pygame.mixer.Sound("assets\zeuscoming.mp3")

# Mengatur ukuran layar sesuai dengan resolusi layar laptop
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Judul dan ikon
pygame.display.set_caption('Flappy Clash')
icon = pygame.image.load("assets\Blitz.png")
pygame.display.set_icon(icon)

# Gambar background dan objek lainnya
background_image = pygame.image.load("assets/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
bird_image = pygame.image.load("assets\Blitz.png")
bird_image = pygame.transform.scale(bird_image, (60, 50))
zeus_image = pygame.image.load("assets\zeus.png")
zeus_image = pygame.transform.scale(zeus_image, (300, 250))
pipe_image = pygame.image.load("assets\pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (70, screen_height))

# Font
font = pygame.font.Font(None, 36)

# Posisi Pesawat
bird_x = 50
bird_y = 300
bird_y_change = 0

# Ukuran dan kecepatan pipa
pipe_width = 70
pipe_gap = 250
pipe_x_change = -6

# Kecepatan gravitasi dan loncatan Pesawat
gravity = 0.6
jump = -10

# Skor dan nyawa
score = 0
pipes_passed = 0
bird_hp = 100

# Posisi Zeus
zeus_appeared = False
zeus_x = screen_width - 310
zeus_y = -zeus_image.get_height()
zeus_y_change = 3
zeus_hp = 100
zeus_lasers = []
zeus_defeated_count = 0
zeus_appearance_scores = [10, 60, 120, 180]

# Peluru
bullets = []

# Daftar pipa
pipes = []

# Fungsi untuk menampilkan skor
def show_score():
    text = font.render("Score: " + str(score), True, black)
    screen.blit(text, [10, 10])

# Fungsi untuk menggambar pipa
def draw_pipes(pipes):
    for pipe_x, pipe_height, passed in pipes:
        screen.blit(pipe_image, (pipe_x, pipe_height + pipe_gap))
        pipe_top = pygame.transform.flip(pipe_image, False, True)
        screen.blit(pipe_top, (pipe_x, pipe_height - pipe_image.get_height()))

# Fungsi untuk menggambar HP bar
def draw_hp_bar(x, y, hp):
    bar_width = 100
    bar_height = 10
    fill_width = (hp / 100) * bar_width
    fill = pygame.Rect(x, y, fill_width, bar_height)
    border = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(screen, red, fill)
    pygame.draw.rect(screen, black, border, 2)

# Fungsi untuk menggambar HP bar Zeus
def draw_zeus_hp_bar(hp):
    bar_width = 300
    bar_height = 20
    x = (screen_width - bar_width) // 2
    y = 10
    fill_width = (hp / 100) * bar_width
    fill = pygame.Rect(x, y, fill_width, bar_height)
    border = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(screen, red, fill)
    pygame.draw.rect(screen, black, border, 2)

# Fungsi untuk layar awal
def show_start_screen():
    screen.blit(background_image, (0, 0))
    title_font = pygame.font.Font(None, 74)
    text = title_font.render("Flappy Clash", True, black)
    screen.blit(text, [screen_width // 2 - text.get_width() // 2, screen_height // 4])
    prompt_font = pygame.font.Font(None, 50)
    start_text = prompt_font.render("1. Start", True, black)
    exit_text = prompt_font.render("2. Exit", True, black)
    screen.blit(start_text, [screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - 25])
    screen.blit(exit_text, [screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 25])
    pygame.display.update()

# Fungsi untuk menampilkan layar pause
def show_pause_screen():
    screen.fill(white)
    title_font = pygame.font.Font(None, 74)
    text = title_font.render("Paused", True, black)
    screen.blit(text, [screen_width // 2 - text.get_width() // 2, screen_height // 4])
    prompt_font = pygame.font.Font(None, 50)
    resume_text = prompt_font.render("Press P to Resume", True, black)
    exit_text = prompt_font.render("Press Q to Exit", True, black)
    screen.blit(resume_text, [screen_width // 2 - resume_text.get_width() // 2, screen_height // 2])
    screen.blit(exit_text, [screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 50])
    pygame.display.update()

# Fungsi untuk menampilkan layar game over
def show_game_over_screen():
    screen.fill(white)
    title_font = pygame.font.Font(None, 74)
    text = title_font.render("GAME OVER", True, red)
    screen.blit(text, [screen_width // 2 - text.get_width() // 2, screen_height // 4])
    prompt_font = pygame.font.Font(None, 50)
    play_again_text = prompt_font.render("Press R to Play Again", True, black)
    exit_text = prompt_font.render("Press Q to Exit", True, black)
    screen.blit(play_again_text, [screen_width // 2 - play_again_text.get_width() // 2, screen_height // 2])
    screen.blit(exit_text, [screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 50])
    pygame.display.update()

# Fungsi untuk membuat pipa baru
def create_pipes():
    return [(screen_width + i * 300, random.randint(150, 450), False) for i in range(3)]

# Fungsi untuk menangani event
def handle_events():
    global running, bird_y_change, bullets, paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_change = jump
            if event.key == pygame.K_v:
                if zeus_appeared and zeus_y >= screen_height // 2 - 125:
                    bullets.append([bird_x + 50, bird_y + 25])
            if event.key == pygame.K_p:
                paused = True

# Fungsi untuk memperbarui posisi burung
def update_bird():
    global bird_y, bird_y_change, running
    bird_y_change += gravity
    bird_y += bird_y_change
    if bird_y < 0 or bird_y > screen_height - 50 or bird_hp <= 0:
        running = False
        show_game_over_screen()
        wait_for_next()

# Fungsi untuk memperbarui pipa
def update_pipes():
    global pipes, score, pipes_passed, pipe_x_change, running
    pipes = [(pipe_x + pipe_x_change, pipe_height, passed) for pipe_x, pipe_height, passed in pipes]
    pipes = [pipe for pipe in pipes if pipe[0] > -pipe_width]
    if pipes[-1][0] < screen_width - 300:
        pipes.append((screen_width, random.randint(150, 450), False))
    draw_pipes(pipes)
    for pipe_x, pipe_height, passed in pipes:
        if (bird_x + 50 > pipe_x and bird_x < pipe_x + pipe_width and 
            (bird_y < pipe_height or bird_y + 50 > pipe_height + pipe_gap)):
            running = False
            show_game_over_screen()
            wait_for_next()
        if pipe_x + pipe_width < bird_x and not passed:
            pipes[pipes.index((pipe_x, pipe_height, passed))] = (pipe_x, pipe_height, True)
            pipes_passed += 1
            score += 1

# Fungsi untuk memperbarui Zeus
def update_zeus():
    global zeus_appeared, zeus_y, zeus_y_change, zeus_hp, zeus_lasers, zeus_defeated_count, pipe_x_change, zeus_appearance_scores, running, bird_hp
    if score in zeus_appearance_scores and not zeus_appeared:
        zeus_appeared = True
        zeus_appearance_scores.remove(score)
        zeus_y = -zeus_image.get_height()
        zeus_hp = 100 + 50 * zeus_defeated_count
        zeus_coming_sound.play()

    if zeus_appeared:
        if zeus_y < screen_height // 2 - 125:
            zeus_y += zeus_y_change
        screen.blit(zeus_image, (zeus_x, zeus_y))
        if zeus_y >= screen_height // 2 - 125:
            laser_probability = max(1, 60 - zeus_defeated_count * 10)
            if random.randint(1, laser_probability) == 1:
                zeus_lasers.append([zeus_x, zeus_y + 125])
            for laser in zeus_lasers:
                laser[0] -= 15
                draw_lightning(laser[0], laser[1])
                if laser[0] < 0:
                    zeus_lasers.remove(laser)
                if laser[0] < bird_x + 50 and laser[1] > bird_y and laser[1] < bird_y + 50:
                    bird_hp -= 10
                    zeus_lasers.remove(laser)
                    if bird_hp <= 0:
                        running = False
                        show_game_over_screen()
                        wait_for_next()
            draw_zeus_hp_bar(zeus_hp)
        if zeus_hp <= 0:
            zeus_appeared = False
            zeus_defeated_count += 1
            pipe_x_change -= 2

# Fungsi untuk memperbarui peluru
def update_bullets():
    global bullets, zeus_hp
    for bullet in bullets:
        bullet[0] += 10
        pygame.draw.circle(screen, red, bullet, 5)
        if zeus_appeared and bullet[0] > zeus_x and bullet[0] < zeus_x + zeus_image.get_width() and bullet[1] > zeus_y and bullet[1] < zeus_y + zeus_image.get_height():
            zeus_hp -= 10
            bullets.remove(bullet)
    bullets = [bullet for bullet in bullets if bullet[0] < screen_width]

# Fungsi untuk menggambar petir
def draw_lightning(x, y):
    lightning_points = [(x, y), (x - 10, y + 10), (x + 10, y + 20), (x - 10, y + 30), (x + 10, y + 40)]
    pygame.draw.lines(screen, yellow, False, lightning_points, 5)

# Fungsi utama permainan
def main_game():
    global bird_y, bird_y_change, score, zeus_appeared, bullets, pipes, bird_hp, zeus_hp, zeus_lasers, zeus_defeated_count, pipe_x_change, pipes_passed, zeus_appearance_scores
    bird_y = 300
    bird_y_change = 0
    score = 0
    zeus_appeared = False
    bullets = []
    pipes = create_pipes()
    bird_hp = 100
    zeus_hp = 100
    zeus_lasers = []
    pipes_passed = 0
    zeus_defeated_count = 0
    zeus_appearance_scores = [10, 60, 120, 180]
    pipe_x_change = -6
    global running, paused
    running = True
    paused = False

    while running:
        if not paused:
            screen.blit(background_image, (0, 0))
            handle_events()
            update_bird()
            update_pipes()
            update_zeus()
            update_bullets()
            bird_rotated = pygame.transform.rotate(bird_image, 30 if bird_y_change < 0 else -30)
            screen.blit(bird_rotated, (bird_x, bird_y))
            show_score()
            draw_hp_bar(10, 40, bird_hp)
            pause_text = font.render("P for pause", True, black)
            screen.blit(pause_text, [screen_width - pause_text.get_width() - 10, 10])
            pygame.display.update()
            pygame.time.Clock().tick(60)
        else:
            show_pause_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    if event.key == pygame.K_q:
                        running = False

# Fungsi untuk menunggu input pemain setelah game over atau di layar awal
def wait_for_next():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Menampilkan layar awal dan menunggu input pemain
show_start_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                waiting = False
                main_game()
            elif event.key == pygame.K_2:
                waiting = False
                pygame.quit()
                quit()