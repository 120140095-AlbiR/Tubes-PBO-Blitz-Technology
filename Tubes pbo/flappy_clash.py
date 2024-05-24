import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Mengatur ukuran layar 
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (153, 255, 0)

# Judul dan ikon
pygame.display.set_caption('Flappy Clash')
icon = pygame.image.load("assets/gambar/Blitz.png")
pygame.display.set_icon(icon)

# Gambar background dan objek lainnya
def load_images():
    background_image = pygame.image.load("assets/gambar/background.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    bird_image = pygame.image.load("assets/gambar/Blitz.png")
    bird_image = pygame.transform.scale(bird_image, (60, 50))
    zeus_image = pygame.image.load("assets/gambar/zeus.png")
    zeus_image = pygame.transform.scale(zeus_image, (350, 350))
    pipe_image = pygame.image.load("assets/gambar/pipe.png")
    pipe_image = pygame.transform.scale(pipe_image, (70, screen_height))
    bullet_image = pygame.image.load("assets/gambar/peluru.png")
    bullet_image = pygame.transform.scale(bullet_image, (20, 10))
    zeus_bullet_image = pygame.image.load("assets/gambar/pz.png")
    zeus_bullet_image = pygame.transform.scale(zeus_bullet_image, (30, 30))
    how_to_play_image = pygame.image.load("assets/gambar/how_to_play_screen.png")
    how_to_play_image = pygame.transform.scale(how_to_play_image, (screen_width, screen_height))
    return background_image, bird_image, zeus_image, pipe_image, bullet_image, zeus_bullet_image, how_to_play_image

background_image, bird_image, zeus_image, pipe_image, bullet_image, zeus_bullet_image, how_to_play_image = load_images()

def resize_image(image, new_width, new_height):
    return pygame.transform.smoothscale(image, (new_width, new_height))

# Fungsi untuk memuat dan mengubah ukuran gambar-gambar ikon
def load_image_icon():
    pause_image = pygame.image.load("assets/caption/pause.png")
    paused_image = pygame.image.load("assets/caption/paused.png")
    quit_image = pygame.image.load("assets/caption/quit.png")
    restart_image = pygame.image.load("assets/caption/randex.png")
    gameover_image = pygame.image.load("assets/caption/gameover.png")
    title_image = pygame.image.load("assets/caption/flappy_clash.png")
    start_exit_image = pygame.image.load("assets/caption/awal.png")
    
    pause_image = resize_image(pause_image, 250, 50) 
    paused_image = resize_image(paused_image, 500, 200) 
    quit_image = resize_image(quit_image, 300, 100) 
    restart_image = resize_image(restart_image, 600, 200) 
    gameover_image = resize_image(gameover_image, 1000, 300)
    title_image = pygame.transform.scale(title_image, (1000, 300))
    start_exit_image = pygame.transform.scale(start_exit_image, (600, 300))
    
    return pause_image, paused_image, quit_image, restart_image, gameover_image, title_image, start_exit_image

pause_image, paused_image, quit_image, restart_image, gameover_image, title_image, start_exit_image = load_image_icon()

# Mengatur lagu dan suara
def load_sounds():
    sounds = {
        "music": "assets/audio/sound.mp3",
        "zeus_coming": pygame.mixer.Sound("assets/audio/zeuscoming.mp3"),
        "woosh": pygame.mixer.Sound("assets/audio/woosh.mp3"),
        "gameover": pygame.mixer.Sound("assets/audio/gameover.mp3"),
        "shoot": pygame.mixer.Sound("assets/audio/shoot.mp3"),
        "thunder": pygame.mixer.Sound("assets/audio/thunder.mp3"),
        "ouch": pygame.mixer.Sound("assets/audio/ouch.mp3"),
    }
    return sounds

# Fungsi untuk memainkan suara
def play_sound(sounds, sound_key, loop=-1):
    if sound_key == "music":
        pygame.mixer.music.load(sounds[sound_key])
        pygame.mixer.music.play(loop)
    else:
        sounds[sound_key].play()

sounds = load_sounds()
play_sound(sounds, "music", loop=-1)

# Font
font = pygame.font.Font(None, 36)

# Posisi Pesawat
bird_x = 50
bird_y = 300
bird_y_change = 0

# Ukuran dan kecepatan pipa
pipe_width = 70
pipe_gap = 300
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

# Peluru
bullets = []

# Daftar pipa
pipes = []

# Fungsi untuk menampilkan skor
def show_score():
    text = font.render("SCORE: " + str(score), True, white)
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
def draw_zeus_hp_bar(hp, max_hp):
    bar_width = 300
    bar_height = 20
    x = (screen_width - bar_width) // 2
    y = 10
    fill_width = (hp / max_hp) * bar_width
    fill = pygame.Rect(x, y, fill_width, bar_height)
    border = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(screen, yellow, fill)
    pygame.draw.rect(screen, black, border, 2)

# Fungsi untuk layar awal
def show_start_screen():
    screen.blit(background_image, (0, 0))
    title_x = (screen_width - title_image.get_width()) // 2
    title_y = screen_height // 18
    screen.blit(title_image, (title_x, title_y))
    
    start_exit_x = (screen_width - start_exit_image.get_width()) // 2
    start_exit_y = screen_height // 2.2
    screen.blit(start_exit_image, (start_exit_x, start_exit_y))
    
    pygame.display.update()

# Fungsi untuk menampilkan layar how to play
def show_how_to_play_screen():
    screen.blit(how_to_play_image, (0, 0))
    pygame.display.update()

# Fungsi untuk menampilkan layar pause
def show_pause_screen():
    screen.blit(paused_image, [screen_width // 2 - paused_image.get_width() // 2, screen_height // 4.25])
    pygame.display.update()

# Fungsi untuk menampilkan layar game over
def show_game_over_screen():
    play_sound(sounds, "gameover")
    screen.fill(black)
    go_x = (screen_width - gameover_image.get_width()) // 2
    go_y = screen_height // 10
    screen.blit(gameover_image, (go_x, go_y))
    randex_x = (screen_width - restart_image.get_width()) // 2
    randex_y = screen_height // 1.85
    screen.blit(restart_image, (randex_x, randex_y))
    pygame.display.update()
    pygame.mixer.music.stop()

# Fungsi untuk membuat pipa baru
def create_pipes():
    return [(screen_width + i * 300, random.randint(150, 450), False) for i in range(3)]

def handle_events():
    global running, bird_y_change, bullets, paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_change = jump
                play_sound(sounds, "woosh")
            if event.key == pygame.K_v:
                if zeus_appeared and zeus_y >= screen_height // 2 - 125:
                    bullets.append([bird_x + 50, bird_y + 25])
                    play_sound(sounds, "shoot")
            if event.key == pygame.K_p:
                paused = True

# Fungsi untuk memperbarui posisi burung
def update_bird():
    global bird_y, bird_y_change, running
    bird_y_change += gravity
    bird_y += bird_y_change
    if bird_y < -50 or bird_y > screen_height:
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
    global zeus_appeared, zeus_y, zeus_y_change, zeus_hp, zeus_lasers, zeus_defeated_count, pipe_x_change, zeus_appearance_scores, running, bird_hp, score

    if score in zeus_appearance_scores and not zeus_appeared:
        zeus_appeared = True
        zeus_appearance_scores.remove(score)
        zeus_y = -zeus_image.get_height()
        zeus_hp = 100 + 50 * zeus_defeated_count
        play_sound(sounds, "zeus_coming", loop=-1)

    if zeus_appeared:
        if zeus_y < screen_height // 2 - 125:
            zeus_y += zeus_y_change
        elif zeus_hp <= 0:
            zeus_y += 10

        screen.blit(zeus_image, (zeus_x, zeus_y))

        if zeus_y >= screen_height // 2 - 125 and zeus_hp > 0:
            laser_probability = max(1, 60 - zeus_defeated_count * 10)
            if random.randint(1, laser_probability) == 1:
                zeus_lasers.append([zeus_x, zeus_y + 125])
                play_sound(sounds, "thunder", loop=-1)

            lasers_to_remove = []

            for laser in zeus_lasers:
                laser[0] -= 15
                screen.blit(zeus_bullet_image, laser)
                if laser[0] < 0:
                    lasers_to_remove.append(laser)
                elif laser[0] < bird_x + 50 and laser[1] > bird_y and laser[1] < bird_y + 50:
                    bird_hp -= 10
                    lasers_to_remove.append(laser)
                    if bird_hp <= 0:
                        running = False
                        show_game_over_screen()
                        wait_for_next()

            for laser in lasers_to_remove:
                zeus_lasers.remove(laser)

            draw_zeus_hp_bar(zeus_hp, 100 + 50 * zeus_defeated_count)

        if zeus_hp <= 0 and zeus_y > screen_height:
            zeus_appeared = False
            zeus_defeated_count += 1
            pipe_x_change -= 2

def update_bullets():
    global bullets, zeus_hp
    for bullet in bullets:
        bullet[0] += 10
        screen.blit(bullet_image, bullet)
        if zeus_appeared and bullet[0] > zeus_x and bullet[0] < zeus_x + zeus_image.get_width() and bullet[1] > zeus_y and bullet[1] < zeus_y + zeus_image.get_height():
            zeus_hp -= 10
            play_sound(sounds, "ouch")
            bullets.remove(bullet)
    bullets = [bullet for bullet in bullets if bullet[0] < screen_width]

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
    zeus_appearance_scores = [10, 60, 110, 160, 210, 250]
    pipe_x_change = -6
    global running, paused
    running = True
    paused = False
    clock = pygame.time.Clock()

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
            screen.blit(pause_image, [screen_width - pause_image.get_width() - 10, 10])
            pygame.display.update()
            clock.tick(60)  # Batasi FPS ke 60
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
                    pygame.mixer.music.play(-1)
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
            elif event.key == pygame.K_3:
                waiting = False
                show_how_to_play_screen()
                how_to_play_waiting = True
                while how_to_play_waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            how_to_play_waiting = False
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                how_to_play_waiting = False
                                show_start_screen()
                                waiting = True