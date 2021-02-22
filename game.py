import pygame
import random
import os
import sys
import sqlite3

JUMP_POWER = 10
GRAVITY = 0.35

G_SKINS = ['knight.png', 'smurf.png', 'fairy.png', 'cowboy.png', 'harry.png', 'hero.png']
B_SKINS = ['ghost.png', 'witch.png', 'skeleton.png', 'elf.png', 'plague.png', 'stone_man.png']
BG = ['mountains.jpg', 'stones.jpg', 'city.jpg', 'forest.jpg']

BACKGROUND = BG[0]
PLAYER = G_SKINS[0]
OPPONENT = B_SKINS[0]

LEVEL = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('game_data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Pause(pygame.sprite.Sprite):
    im = load_image('pause.jpeg')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)

        self.image = Pause.im
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def game_over(match_score):
    clock = pygame.time.Clock()

    color = pygame.Color((46, 26, 14))
    font = pygame.font.Font(None, 100)

    BackGround = Background('game_over.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    g_over = True
    while g_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 108 < x < 584 and 312 < y < 438:
                    g_over = False
                    game()
                if 695 < x < 1167 and 312 < y < 438:
                    global LEVEL
                    if LEVEL < 6:
                        LEVEL += 1
                    else:
                        LEVEL = 1
                    g_over = False
                    game()
                if 400 < x < 875 and 512 < y < 638:
                    g_over = False
                    LEVEL = 0
                    main_menu()

        score_surface = font.render(str(match_score), True, color)
        screen.blit(score_surface, (612, 195))

        pygame.display.update()
        clock.tick(60)


def game_over_friendly_match(winner):
    global user_name, opponent_name
    if winner == 1:
        winner = opponent_name
    else:
        winner = user_name

    clock = pygame.time.Clock()

    BackGround = Background('game_over_f.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    color = pygame.Color((46, 26, 14))
    font = pygame.font.Font(None, 100)

    g_over = True
    while g_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 400 < x < 884 and 304 < y < 433:
                    g_over = False
                    friendly_match()
                if 40 < x < 884 and 507 < y < 635:
                    g_over = False
                    LEVEL = 0
                    main_menu()

        winner_surface = font.render(winner, True, color)
        screen.blit(winner_surface, (433, 198))

        pygame.display.update()
        clock.tick(60)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 400
    BAR_HEIGHT = 40
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (61, 143, 71), fill_rect)
    pygame.draw.rect(surf, (46, 26, 14), outline_rect, 4)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Completed(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(completed_levels)
        image = load_image('completed.png')

        self.image = image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (333, 197))
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Opponent(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, level):
        super().__init__(opponent_group)
        global OPPONENT, B_SKINS
        if LEVEL == 1:
            OPPONENT = B_SKINS[0]
            self.speed = 2
            self.strength = 10
        elif LEVEL == 2:
            OPPONENT = B_SKINS[1]
            self.speed = 3
            self.strength = 15
        elif LEVEL == 3:
            OPPONENT = B_SKINS[2]
            self.speed = 4
            self.strength = 20
        elif LEVEL == 4:
            OPPONENT = B_SKINS[3]
            self.speed = 5
            self.strength = 25
        elif LEVEL == 5:
            OPPONENT = B_SKINS[4]
            self.speed = 6
            self.strength = 30
        elif LEVEL == 6:
            OPPONENT = B_SKINS[5]
            self.speed = 7
            self.strength = 35

        opponent_image = load_image(OPPONENT)

        self.image = opponent_image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.n = 0
        self.hp = 100
        self.game = True

        self.mask = pygame.mask.from_surface(self.image)

        self.move = 0

    def continue_game(self):
        self.game = True
        player.game = True

    def stop(self):
        self.move = 0
        self.game = False
        player.game = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.hp <= 0:
            self.game = False
            player.game = False
            global score
            score += player.hp * LEVEL
            if str(LEVEL) not in completed:
                completed.append(str(LEVEL))
                cursor.execute(f"INSERT INTO levels VALUES (?, ?)", (user_id, LEVEL))
            cursor.execute(f"UPDATE users set score = {score} WHERE id = {user_id}")
            data_base.commit()
            game_over(player.hp * LEVEL)
        if self.move == 0 and self.game:
            self.move = -self.speed
        if pygame.sprite.collide_mask(self, player) and self.game:
            if self.n % 60 == 0:
                player.yvel = -10
                player.onGround = False
                player.hp -= self.strength
            self.n += 1

        if self.rect.x < 100:
            self.move = self.speed

        if self.rect.x > 1100:
            self.move = -self.speed

        if not self.game:
            self.move = 0

        self.rect.x += self.move


class Friend(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(friend_group)
        friend_image = load_image(OPPONENT)
        self.image = friend_image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.move = 0
        self.speed = 5
        self.yvel = 0
        self.onGround = True
        self.hp = 100
        self.game = True

        self.mask = pygame.mask.from_surface(self.image)

    def continue_game(self):
        self.game = True
        player.game = True

    def stop(self):
        self.move = 0
        player.move = 0
        self.game = False
        player.game = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, left, right, up):
        if self.hp <= 0:
            self.game = False
            player.game = False
            game_over_friendly_match(0)
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
                self.onGround = False
        if left and self.rect.x > 0:
            self.move = -self.speed
        elif left and self.rect.x <= 0:
            self.move = 0

        if right and self.rect.x < 1100:
            self.move = self.speed
        elif right and self.rect.x >= 1100:
            self.move = 0

        if not (left or right):
            self.move = 0

        if not self.onGround:
            self.yvel += GRAVITY

        if self.yvel > 10:
            self.onGround = True

        if self.onGround:
            self.rect.y = 370

        if not self.game:
            self.move = 0
            self.yvel = 0

        self.rect.y += self.yvel
        self.rect.x += self.move


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        player_image = load_image(PLAYER)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.move = 0
        self.speed = 5
        self.yvel = 0
        self.onGround = True
        self.hp = 100
        self.game = True

        self.mask = pygame.mask.from_surface(self.image)

    def continue_game(self):
        self.game = True
        opponent.game = True

    def stop(self):
        self.move = 0
        self.game = False
        opponent.game = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, left, right, up):
        if self.hp <= 0:
            if friendly_m:
                self.game = False
                friend.game = False
                game_over_friendly_match(1)
            else:
                self.game = False
                opponent.game = False
                game_over(0)
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
                self.onGround = False
        if left and self.rect.x > 0:
            self.move = -self.speed
        elif left and self.rect.x <= 0:
            self.move = 0

        if right and self.rect.x < 1100:
            self.move = self.speed
        elif right and self.rect.x >= 1100:
            self.move = 0

        if not (left or right):
            self.move = 0

        if not self.onGround:
            self.yvel += GRAVITY

        if self.yvel > 10:
            self.onGround = True

        if self.onGround:
            self.rect.y = 470

        if not self.game:
            self.move = 0
            self.yvel = 0

        self.rect.y += self.yvel
        self.rect.x += self.move


def pause_func():
    clock = pygame.time.Clock()

    BackGround = Background('pause_window.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    global friendly_m

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 200 < x < 1095 and 217 < y < 351:
                    pause = False
                    if friendly_m:
                        friend.continue_game()
                    else:
                        player.continue_game()
                        opponent.continue_game()
                elif 200 < x < 1095 and 430 < y < 566:
                    pause = False
                    global LEVEL
                    LEVEL = 0
                    main_menu()
        pygame.display.update()
        clock.tick(60)


def username_taken():
    clock = pygame.time.Clock()

    BackGround = Background('username_taken.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 959 < x < 1030 and 129 < y < 196:
                    active = False
        pygame.display.update()
        clock.tick(60)


def wrong_password():
    clock = pygame.time.Clock()

    BackGround = Background('wrong_password.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 959 < x < 1030 and 129 < y < 196:
                    active = False
        pygame.display.update()
        clock.tick(60)


def log_up(username, password):
    if len(password) < 6:
        return False

    cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")

    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", (username, password, 0))
        cursor.execute(f"SELECT id FROM users WHERE username = '{username}'")
        global user_id
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO levels VALUES (?, ?)", (user_id, 0))
        data_base.commit()
        return True
    else:
        username_taken()
        return False


def log_in(username, password):
    password_flag = 0

    if username == '':
        return False
    if password == '':
        return False

    usernames = [username[0] for username in cursor.execute("SELECT username FROM users")]
    if username not in usernames:
        return False
    else:
        for username_password in cursor.execute("SELECT username, password FROM users"):
            if username == username_password[0] and password != username_password[1]:
                wrong_password()
                password_flag = 1
            elif username == username_password[0] and password == username_password[1]:
                global user_id, score, completed
                cursor.execute(f"SELECT id from users where username = '{username}'")
                u_id = cursor.fetchone()[0]
                user_id = u_id
                password_flag = 0
                cursor.execute(f"SELECT score from users where username = '{username}'")
                u_score = cursor.fetchone()[0]
                score = u_score
                cursor.execute(f"SELECT completed from levels where user_id = '{u_id}'")
                completed_l = cursor.fetchall()
                for l in completed_l:
                    completed.append(l[0])
                if completed == ['0']:
                    completed = []
                return True
        if password_flag == 1:
            return False


def authorization():
    font = pygame.font.Font(None, 104)
    color_inactive = pygame.Color((47, 25, 12))
    color_active = pygame.Color((104, 78, 63))

    input_username = pygame.Rect(500, 185, 693, 92)
    username_color = color_inactive
    active_username = False
    username = ''

    input_password = pygame.Rect(500, 335, 693, 92)
    password_color = color_inactive
    active_password = False
    password = ''
    display_password = ''

    clock = pygame.time.Clock()

    logged_in = False

    BackGround = Background('authorization.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    while not logged_in:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0], event.pos[1]
                if 1206 < x < 1280 and 0 < y < 72:
                    return False
                if input_username.collidepoint(event.pos):
                    active_username = True
                    active_password = False

                if input_password.collidepoint(event.pos):
                    active_password = True
                    active_username = False

                username_color = color_active if active_username else color_inactive
                password_color = color_active if active_password else color_inactive

                x, y = event.pos[0], event.pos[1]
                if 83 < x < 511 and 510 < y < 647:
                    logged_in = log_in(username, password)

                if 781 < x < 1207 and 510 < y < 647:
                    logged_in = log_up(username, password)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    continue
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                        display_password = display_password[:-1]
                    else:
                        password += event.unicode
                        display_password += '•'

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        username_surface = font.render(username, True, username_color)
        password_surface = font.render(display_password, True, password_color)
        width = 693
        input_username.w = width
        input_password.w = width
        screen.blit(username_surface, (505, 195))
        screen.blit(password_surface, (505, 345))
        pygame.draw.rect(screen, username_color, input_username, 3)
        pygame.draw.rect(screen, password_color, input_password, 3)
        pygame.display.flip()
        clock.tick(60)
    if logged_in:
        if select_level():
            return True
        else:
            return False


def select_level():
    clock = pygame.time.Clock()

    BackGround = Background('levels.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    global LEVEL, completed_levels
    completed_levels = pygame.sprite.Group()

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 1207 < x < 1280 and 0 < y < 70:
                    active = False
                elif 82 < x < 415 and 160 < y < 357:
                    LEVEL = 1
                elif 468 < x < 801 and 160 < y < 357:
                    LEVEL = 2
                elif 861 < x < 1194 and 160 < y < 357:
                    LEVEL = 3
                elif 82 < x < 415 and 435 < y < 635:
                    LEVEL = 4
                elif 468 < x < 801 and 435 < y < 635:
                    LEVEL = 5
                elif 861 < x < 1194 and 435 < y < 635:
                    LEVEL = 6

        cursor.execute(f"SELECT completed from levels where user_id = '{user_id}'")
        completed_l = cursor.fetchall()
        for l in completed_l:
            if l[0] == '1':
                lvl = Completed(82, 160)
                completed_levels.add(lvl)
            elif l[0] == '2':
                lvl = Completed(468, 160)
                completed_levels.add(lvl)
            elif l[0] == '3':
                lvl = Completed(861, 160)
                completed_levels.add(lvl)
            elif l[0] == '4':
                lvl = Completed(82, 435)
                completed_levels.add(lvl)
            elif l[0] == '5':
                lvl = Completed(468, 435)
                completed_levels.add(lvl)
            elif l[0] == '6':
                lvl = Completed(861, 435)
                completed_levels.add(lvl)
        completed_levels.update()
        completed_levels.draw(screen)
        if LEVEL != 0:
            active = False
        pygame.display.update()
        clock.tick(60)
    if LEVEL != 0:
        return True
    return False


def skins():
    clock = pygame.time.Clock()

    BackGround = Background('skins.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    global PLAYER, OPPONENT, B_SKINS, G_SKINS, BACKGROUND, BG

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 1204 < x < 1280 and 0 < y < 70:
                    active = False
                if 78 < x < 215 and 103 < y < 237:
                    PLAYER = G_SKINS[0]
                if 273 < x < 410 and 103 < y < 237:
                    PLAYER = G_SKINS[1]
                if 470 < x < 606 and 103 < y < 237:
                    PLAYER = G_SKINS[2]
                if 667 < x < 803 and 103 < y < 237:
                    PLAYER = G_SKINS[3]
                if 868 < x < 1001 and 103 < y < 237:
                    PLAYER = G_SKINS[4]
                if 1061 < x < 1198 and 103 < y < 237:
                    PLAYER = G_SKINS[5]

                if 78 < x < 215 and 307 < y < 440:
                    OPPONENT = B_SKINS[0]
                if 273 < x < 410 and 307 < y < 440:
                    OPPONENT = B_SKINS[1]
                if 470 < x < 606 and 307 < y < 440:
                    OPPONENT = B_SKINS[2]
                if 667 < x < 803 and 307 < y < 440:
                    OPPONENT = B_SKINS[3]
                if 868 < x < 1001 and 307 < y < 440:
                    OPPONENT = B_SKINS[4]
                if 1061 < x < 1198 and 307 < y < 440:
                    OPPONENT = B_SKINS[5]

                if 78 < x < 317 and 517 < y < 655:
                    BACKGROUND = BG[0]
                if 375 < x < 612 and 517 < y < 655:
                    BACKGROUND = BG[1]
                if 668 < x < 905 and 517 < y < 655:
                    BACKGROUND = BG[2]
                if 959 < x < 1197 and 517 < y < 655:
                    BACKGROUND = BG[3]

        pygame.display.update()
        clock.tick(60)


def leaderboard():
    clock = pygame.time.Clock()
    leaderb = []
    txt = ''

    BackGround = Background('leaderboard.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    cursor.execute("SELECT score from users")
    lb_score = cursor.fetchall()
    for s in lb_score:
        leaderb.append(s[0])
    leaderb = sorted(leaderb, reverse=True)
    if len(leaderb) < 5:
        for i in range(5 - len(leaderb)):
            leaderb.append(0)

    if leaderb[0] == 0:
        user = ''
        sc = ''
    else:
        cursor.execute(f"SELECT username from users WHERE score = {leaderb[0]}")
        user = cursor.fetchone()[0]
        sc = str(leaderb[0])
    u_1 = user
    s_1 = sc

    if leaderb[1] == 0:
        user = ''
        sc = ''
    else:
        cursor.execute(f"SELECT username from users WHERE score = {leaderb[1]}")
        user = cursor.fetchone()[0]
        sc = str(leaderb[1])
    u_2 = user
    s_2 = sc

    if leaderb[2] == 0:
        user = ''
        sc = ''
    else:
        cursor.execute(f"SELECT username from users WHERE score = {leaderb[2]}")
        user = cursor.fetchone()[0]
        sc = str(leaderb[2])
    u_3 = user
    s_3 = sc

    if leaderb[3] == 0:
        user = ''
        sc = ''
    else:
        cursor.execute(f"SELECT username from users WHERE score = {leaderb[3]}")
        user = cursor.fetchone()[0]
        sc = str(leaderb[3])
    u_4 = user
    s_4 = sc

    if leaderb[4] == 0:
        user = ''
        sc = ''
    else:
        cursor.execute(f"SELECT username from users WHERE score = {leaderb[4]}")
        user = cursor.fetchone()[0]
        sc = str(leaderb[4])
    u_5 = user
    s_5 = sc

    color = pygame.Color((46, 26, 14))
    font = pygame.font.Font(None, 80)

    lb = True
    while lb:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 1206 < x < 1280 and 0 < y < 71:
                    lb = False
                    main_menu()

        s1_surface = font.render(s_1, True, color)
        screen.blit(s1_surface, (880, 170))

        s2_surface = font.render(s_2, True, color)
        screen.blit(s2_surface, (880, 270))

        s3_surface = font.render(s_3, True, color)
        screen.blit(s3_surface, (880, 370))

        s4_surface = font.render(s_4, True, color)
        screen.blit(s4_surface, (880, 470))

        s5_surface = font.render(s_5, True, color)
        screen.blit(s5_surface, (880, 570))

        u1_surface = font.render(u_1, True, color)
        screen.blit(u1_surface, (300, 170))

        u2_surface = font.render(u_2, True, color)
        screen.blit(u2_surface, (300, 270))

        u3_surface = font.render(u_3, True, color)
        screen.blit(u3_surface, (300, 370))

        u4_surface = font.render(u_4, True, color)
        screen.blit(u4_surface, (300, 470))

        u5_surface = font.render(u_5, True, color)
        screen.blit(u5_surface, (300, 570))

        pygame.display.flip()
        clock.tick(60)

def controls():
    clock = pygame.time.Clock()

    BackGround = Background('controls.jpeg', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 1206 < x < 1280 and 0 < y < 71:
                    cont = False
                    main_menu()
        pygame.display.flip()
        clock.tick(60)


def main_menu():
    clock = pygame.time.Clock()

    BackGround = Background('intro.png', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 388 < x < 669 and 577 < y < 662:
                    menu = False
                    controls()
                if 511 < x < 1192 and 440 < y < 538:
                    menu = False
                    leaderboard()
                if 1012 < x < 1192 and 574 < y < 665:
                    menu = False
                    pygame.quit()
                    quit()
                if 338 < x < 670 and 578 < y < 665:
                    print('controls')
                if 1114 < x < 1192 and 39 < y < 119:
                    skins()
                    main_menu()
                if 712 < x < 1192 and 297 < y < 396:
                    menu = False
                    friendly_match()
                if 871 < x < 1192 and 158 < y < 259:
                    if user_id == 0:
                        if authorization():
                            menu = False
                            game()
                        else:
                            menu = False
                            main_menu()
                    else:
                        if select_level():
                            menu = False
                            game()
                        else:
                            menu = False
                            main_menu()
        pygame.display.flip()
        clock.tick(60)


def friendly_match():
    global friend_group, player_group, all_sprites, player, friend, friendly_m, OPPONENT, PLAYER, user_name, opponent_name

    color_names = pygame.Color((46, 26, 14))
    font = pygame.font.Font(None, 40)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    friend_group = pygame.sprite.Group()
    friend = Friend(800, height - 350)
    friend_group.add(friend)
    player = Player(150, height - 200)
    player_group.add(player)
    BackGround = Background(BACKGROUND, [0, 0])
    left = right = up = False
    f_left = f_right = f_up = False
    friendly_m = True

    pause = Pause(605, 5)
    all_sprites.add(pause)

    clock = pygame.time.Clock()

    if user_id != 0:
        cursor.execute(f"SELECT username from users where id = '{user_id}'")
        user_name = cursor.fetchone()[0]
    else:
        if PLAYER == G_SKINS[0]:
            user_name = 'Knight'
        if PLAYER == G_SKINS[1]:
            user_name = 'Smurf'
        if PLAYER == G_SKINS[2]:
            user_name = 'Fairy'
        if PLAYER == G_SKINS[3]:
            user_name = 'Cowboy'
        if PLAYER == G_SKINS[4]:
            user_name = 'Harry Potter'
        if PLAYER == G_SKINS[5]:
            user_name = 'Hero'

    if OPPONENT == B_SKINS[0]:
        opponent_name = 'Mr. Ghost'
    elif OPPONENT == B_SKINS[1]:
        opponent_name = 'Wicked Witch'
    elif OPPONENT == B_SKINS[2]:
        opponent_name = 'Spooky Skeleton'
    elif OPPONENT == B_SKINS[3]:
        opponent_name = 'Old Elf'
    elif OPPONENT == B_SKINS[4]:
        opponent_name = 'Plague Doctor'
    elif OPPONENT == B_SKINS[5]:
        opponent_name = 'Stone Man'

    running = True
    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                right = True

            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                left = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                up = False

            if event.type == pygame.KEYDOWN:
                if pygame.sprite.collide_mask(player, friend) and player.game:
                    if event.key == pygame.K_SPACE:
                        friend.hp -= 10
                    if event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        friend.hp -= 15

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                f_left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                f_right = True

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                f_right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                f_left = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                f_up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                f_up = False

            if event.type == pygame.KEYDOWN:
                if pygame.sprite.collide_mask(player, friend) and player.game:
                    if event.key == pygame.K_RETURN:
                        player.hp -= 10
                    if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_RCTRL:
                        player.hp -= 15

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 590 < x < 690 and 5 < y < 105:
                    friend.stop()
                    pause_func()

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        all_sprites.update()
        all_sprites.draw(screen)
        player_group.update(left, right, up)
        player_group.draw(screen)
        friend_group.update(f_left, f_right, f_up)
        friend_group.draw(screen)
        draw_shield_bar(screen, 5, 5, player.hp)
        draw_shield_bar(screen, 875, 5, friend.hp)

        user_name_surface = font.render(user_name, True, color_names)
        opponent_name_surface = font.render(opponent_name, True, color_names)
        screen.blit(user_name_surface, (10, 10))
        screen.blit(opponent_name_surface, (880, 10))

        pygame.display.flip()
        clock.tick(60)

    sys.exit()


def game():
    global opponent_group, player_group, all_sprites, player, opponent, friendly_m, OPPONENT

    color_names = pygame.Color((46, 26, 14))
    font = pygame.font.Font(None, 40)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    opponent_group = pygame.sprite.Group()
    opponent = Opponent(800, height - 350, LEVEL)
    opponent_group.add(opponent)
    player = Player(150, height - 200)
    player_group.add(player)
    BackGround = Background(BACKGROUND, [0, 0])
    left = right = up = False
    friendly_m = False

    pause = Pause(605, 5)
    all_sprites.add(pause)

    clock = pygame.time.Clock()

    cursor.execute(f"SELECT username from users where id = '{user_id}'")
    user_name = cursor.fetchone()[0]
    if OPPONENT == B_SKINS[0]:
        opponent_name = 'Mr. Ghost'
    elif OPPONENT == B_SKINS[1]:
        opponent_name = 'Wicked Witch'
    elif OPPONENT == B_SKINS[2]:
        opponent_name = 'Spooky Skeleton'
    elif OPPONENT == B_SKINS[3]:
        opponent_name = 'Old Elf'
    elif OPPONENT == B_SKINS[4]:
        opponent_name = 'Plague Doctor'
    elif OPPONENT == B_SKINS[5]:
        opponent_name = 'Stone Man'

    running = True
    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                right = True

            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                left = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                up = True

            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                up = False
            if event.type == pygame.KEYDOWN:
                if pygame.sprite.collide_mask(player, opponent) and player.game:
                    if event.key == pygame.K_SPACE:
                        opponent.hp -= 10
                    if event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        opponent.hp -= 15
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 590 < x < 690 and 5 < y < 105:
                    player.stop()
                    opponent.stop()
                    pause_func()

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        all_sprites.update()
        all_sprites.draw(screen)
        player_group.update(left, right, up)
        player_group.draw(screen)
        opponent_group.update()
        opponent_group.draw(screen)
        draw_shield_bar(screen, 5, 5, player.hp)
        draw_shield_bar(screen, 875, 5, opponent.hp)

        user_name_surface = font.render(user_name, True, color_names)
        opponent_name_surface = font.render(opponent_name, True, color_names)
        screen.blit(user_name_surface, (10, 10))
        screen.blit(opponent_name_surface, (880, 10))

        pygame.display.flip()
        clock.tick(60)

    sys.exit()


if __name__ == '__main__':
    data_base = sqlite3.connect('game_data/game_db.db')
    cursor = data_base.cursor()
    user_id = 0
    score = 0
    completed = []

    pygame.init()
    pygame.display.set_caption('game')
    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.mixer.music.load('game_data/music.mid')
    pygame.mixer.music.play(-1)
    main_menu()
