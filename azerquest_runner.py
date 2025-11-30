import pygame 
import sys
import random
import math
import os

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

WIDTH, HEIGHT = 1000, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AMT Runner")
clock = pygame.time.Clock()

COL_BG = (10, 20, 40)
COL_TEXT = (240, 240, 240)
COL_PLAYER = (80, 200, 255)
COL_COLLECT = (255, 215, 0)
COL_OBS = (220, 80, 80)
COL_SEG_OLD = (70, 60, 90)
COL_SEG_MAIDEN = (90, 60, 60)
COL_SEG_MODERN = (40, 40, 90)
COL_SEG_BOULEVARD = (40, 80, 80)
COL_SEG_FLAME = (20, 10, 40)

COL_SEG_K_SHUSHA = (60, 50, 80)
COL_SEG_K_CIDIR = (40, 70, 50)
COL_SEG_K_FOREST = (20, 50, 30)

BTN_COLOR = (40, 80, 140)
BTN_HOVER = (70, 120, 200)

MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.7
LANGUAGE = "AZ"
GRAPHICS_MODE = "HD"
SHOW_KEY_BINDINGS = True


def safe_load_image(path, size=None):
    try:
        if not os.path.exists(path):
            return None
        img = pygame.image.load(path).convert_alpha()
        if size is not None:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception:
        return None


def safe_load_sound(path):
    try:
        if not os.path.exists(path):
            return None
        return pygame.mixer.Sound(path)
    except Exception:
        return None


PLAYER_RUN_IMAGES = [
    safe_load_image("assets/run_1.png", (60, 80)),
    safe_load_image("assets/run_2.png", (60, 80)),
    safe_load_image("assets/run_1.png", (60, 80)),
    safe_load_image("assets/run_2.png", (60, 80)),
]
PLAYER_JUMP_IMAGE = safe_load_image("assets/jump.png", (60, 80))
PLAYER_SLIDE_IMAGE = safe_load_image("assets/slide.png", (60, 50))
PLAYER_IDLE_IMAGE = safe_load_image("assets/idle.png", (60, 80))

BG_MENU = safe_load_image("assets/menu_bg.png", (WIDTH, HEIGHT))
BG_OLD = safe_load_image("assets/baku_oldcity.png", (WIDTH, HEIGHT))
BG_MAIDEN = safe_load_image("assets/baku_maiden.png", (WIDTH, HEIGHT))
BG_MODERN = safe_load_image("assets/baku_modern.png", (WIDTH, HEIGHT))
BG_BOULEVARD = safe_load_image("assets/baku_boulevard.png", (WIDTH, HEIGHT))
BG_FLAME = safe_load_image("assets/baku_flame_trial.png", (WIDTH, HEIGHT))
BG_INTRO = safe_load_image("baku_intro_map.png", (WIDTH, HEIGHT))
BG_CUTSCENE = safe_load_image("baku_panorama.png", (WIDTH, HEIGHT))

BG_SHEKI_TOWN = safe_load_image("assets/sheki_town.png", (WIDTH, HEIGHT))
BG_SHEKI_PALACE = safe_load_image("assets/sheki_palace.png", (WIDTH, HEIGHT))
BG_SHEKI_FOREST = safe_load_image("assets/sheki_forest.png", (WIDTH, HEIGHT))

BG_KARABAKH_INTRO = safe_load_image("karabakh_intro.png", (WIDTH, HEIGHT))
BG_KARABAKH_CUTSCENE = safe_load_image("karabakh_cutscene.png", (WIDTH, HEIGHT))
BG_KARABAKH_SHUSHA = safe_load_image("assets/karabakh_shusha.png", (WIDTH, HEIGHT))
BG_KARABAKH_CIDIR = safe_load_image("assets/karabakh_cidir.png", (WIDTH, HEIGHT))
BG_KARABAKH_FOREST = safe_load_image("assets/karabakh_forest.png", (WIDTH, HEIGHT))

COIN_IMAGE = safe_load_image("assets/coin.png", (30, 30))

OBST_WOOD_CART = safe_load_image("assets/wood_cart.png", (90, 60))
OBST_STONE = safe_load_image("assets/stone_block.png", (90, 60))
OBST_CAT = safe_load_image("assets/street_cat.png", (90, 60))
OBST_CAR = safe_load_image("assets/car.png", (90, 60))
OBST_SCOOTER = safe_load_image("assets/scooter.png", (90, 60))
OBST_BARRIER = safe_load_image("assets/barrier.png", (90, 60))
OBST_PUDDLE = safe_load_image("assets/puddle.png", (90, 60))
OBST_CYCLIST = safe_load_image("assets/cyclist.png", (90, 60))
OBST_BENCH = safe_load_image("assets/bench.png", (90, 60))
OBST_FLAME_PATCH = safe_load_image("assets/flame_patch.png", (90, 60))

ICON_SWEET = safe_load_image("assets/sheki_sweet.png", (30, 30))
ICON_SHEBEKE = safe_load_image("assets/sheki_shebeke.png", (30, 30))
ICON_FLOWER = safe_load_image("assets/sheki_flower.png", (30, 30))

OBST_SHEKI_CART = safe_load_image("sheki_cart.png", (90, 60))
OBST_STREET_HOLE = safe_load_image("sheki_hole.png", (90, 60))
OBST_GARDEN_DECOR = safe_load_image("sheki_garden.png", (90, 60))
OBST_TREE_ROOT = safe_load_image("sheki_root.png", (90, 60))
OBST_BRANCH = safe_load_image("sheki_branch.png", (90, 60))

ICON_TAR = safe_load_image("assets/collect_tar.png", (30, 30))
ICON_KAMANCHA = safe_load_image("collect_kamancha.png", (30, 30))
ICON_XARIBULBUL = safe_load_image("assets/collect_xaribulbul.png", (30, 30))
ICON_KARABAKH_CARPET = safe_load_image("assets/collect_carpet.png", (30, 30))
ICON_HORSE = safe_load_image("assets/collect_horse.png", (30, 30))
ICON_MUSIC_NOTE = safe_load_image("assets/collect_musicnote.png", (30, 30))
ICON_PHOTO_SPOT = safe_load_image("collect_photospot.png", (30, 30))
ICON_FOREST_FLOWER_K = safe_load_image("collect_forestflower.png", (30, 30))
ICON_WATER_DROP = safe_load_image("collect_water.png", (30, 30))
ICON_BIRD = safe_load_image("collect_bird.png", (30, 30))

OBST_SHUSHA_STONES = safe_load_image("obs_shusha_stones.png", (90, 60))
OBST_SHUSHA_ARCH = safe_load_image("obs_shusha_arch.png", (90, 60))
OBST_SHUSHA_FRAME = safe_load_image("obs_shusha_frame.png", (90, 60))
OBST_CIDIR_ROCKS = safe_load_image("obs_cidir_rocks.png", (90, 60))
OBST_CIDIR_STONES = safe_load_image("obs_cidir_stones.png", (90, 60))
OBST_FOREST_ROOT = safe_load_image("obs_forest_root.png", (90, 60))
OBST_FOREST_LOG = safe_load_image("obs_forest_log.png", (90, 60))
OBST_FOREST_BRANCH = safe_load_image("obs_forest_branch.png", (90, 60))

SND_JUMP = safe_load_sound("sound/jump1.wav")
SND_COLLECT = safe_load_sound("sound/collect.wav")
SND_HIT = safe_load_sound("sound/hit.mp3")
SND_CORRECT = safe_load_sound("sound/correct1.mp3")
SND_WRONG = safe_load_sound("sound/wrong1.mp3")
SND_GAME_OVER = safe_load_sound("sound/game_over1.mp3")

ALL_SFX = [
    s for s in
    [SND_JUMP, SND_COLLECT, SND_HIT, SND_CORRECT, SND_WRONG, SND_GAME_OVER]
    if s is not None
]

MUSIC_TRACKS = {
    "MENU": "sound/music_menu.mp3",
    "LEVEL_BAKU": "sound/music_baku.mp3",
    "LEVEL_SHEKI": "sound/music_sheki.mp3",
    "LEVEL_KARABAKH": "sound/music_karabakh.mp3",
}

CURRENT_MUSIC_MODE = None


def switch_music(mode):
    global CURRENT_MUSIC_MODE
    if not pygame.mixer.get_init():
        return
    if mode == CURRENT_MUSIC_MODE:
        return

    CURRENT_MUSIC_MODE = mode
    path = MUSIC_TRACKS.get(mode)

    if not path or not os.path.exists(path):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        return

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def apply_volume_settings():
    if pygame.mixer.get_init():
        try:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
        except Exception:
            pass
        for s in ALL_SFX:
            s.set_volume(SFX_VOLUME)


apply_volume_settings()


def draw_text(surface, text, size, color, x, y, center=True):
    font = pygame.font.SysFont("Arial", size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(surf, rect)


def draw_lives(surface, lives):
    for i in range(lives):
        pygame.draw.circle(
            surface,
            (255, 60, 90),
            (WIDTH - 30 - i * 30, 30),
            12
        )


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        color = BTN_HOVER if self.rect.collidepoint(mx, my) else BTN_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)
        draw_text(surface, self.text, 26, (255, 255, 255),
                  self.rect.centerx, self.rect.centery)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class Slider:
    def __init__(self, x, y, w, h, value=0.7):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = value
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = event.pos[0]
            t = (x - self.rect.x) / self.rect.w
            self.value = max(0.0, min(1.0, t))

    def draw(self, surface):
        cx = self.rect.x
        cy = self.rect.centery
        endx = self.rect.right
        pygame.draw.line(surface, (180, 180, 200), (cx, cy), (endx, cy), 4)
        knob_x = cx + int(self.value * self.rect.w)
        pygame.draw.circle(surface, (255, 255, 255), (knob_x, cy), self.rect.h // 2)


class Toggle:
    def __init__(self, x, y, w=60, h=30, state=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.state = state

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state

    def draw(self, surface):
        bg_color = (80, 180, 120) if self.state else (100, 100, 120)
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=15)
        knob_radius = self.rect.height // 2 - 3
        if self.state:
            cx = self.rect.right - knob_radius - 3
        else:
            cx = self.rect.x + knob_radius + 3
        cy = self.rect.centery
        pygame.draw.circle(surface, (240, 240, 240), (cx, cy), knob_radius)


class Checkbox:
    def __init__(self, x, y, size=22, checked=True):
        self.rect = pygame.Rect(x, y, size, size)
        self.checked = checked

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked

    def draw(self, surface):
        pygame.draw.rect(surface, (230, 230, 230), self.rect, 2)
        if self.checked:
            pygame.draw.line(surface, (230, 230, 230),
                             (self.rect.x + 3, self.rect.centery),
                             (self.rect.centerx, self.rect.bottom - 3), 3)
            pygame.draw.line(surface, (230, 230, 230),
                             (self.rect.centerx, self.rect.bottom - 3),
                             (self.rect.right - 3, self.rect.y + 3), 3)


class Player:
    def __init__(self, x, y):
        self.width = 50
        self.height = 80
        self.rect = pygame.Rect(x, y - self.height, self.width, self.height)

        self.vel_y = 0.0
        self.gravity = 2000.0
        self.jump_vel = -1100.0
        self.max_fall_speed = 1200.0
        self.on_ground = False

        self.base_speed_x = 300.0
        self.slide = False
        self.slide_height = 50
        self.normal_height = 80

        self.run_frames = [img for img in PLAYER_RUN_IMAGES if img is not None]
        self.jump_image = PLAYER_JUMP_IMAGE
        self.slide_image = PLAYER_SLIDE_IMAGE
        self.idle_image = PLAYER_IDLE_IMAGE
        self.anim_timer = 0.0
        self.anim_frame_index = 0
        self.image = None

    def handle_input(self, keys, dt):
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_vel
            self.on_ground = False
            if SND_JUMP:
                SND_JUMP.play()

        if keys[pygame.K_DOWN] and self.on_ground:
            if not self.slide:
                self.slide = True
                self.rect.height = self.slide_height
                self.rect.y += (self.normal_height - self.slide_height)
        else:
            if self.slide:
                self.rect.y -= (self.normal_height - self.slide_height)
                self.rect.height = self.normal_height
                self.slide = False

    @property
    def speed_x(self):
        return self.base_speed_x

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        self.vel_y += self.gravity * dt
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

        self.rect.y += self.vel_y * dt

        ground_y = HEIGHT - 80
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        self.update_animation(dt)

    def update_animation(self, dt):
        if not self.on_ground and self.jump_image is not None:
            self.image = self.jump_image
            return

        if self.slide and self.slide_image is not None:
            self.image = self.slide_image
            return

        if self.on_ground and self.speed_x > 0 and self.run_frames:
            self.anim_timer += dt
            if self.anim_timer >= 0.08:
                self.anim_timer = 0
                self.anim_frame_index = (self.anim_frame_index + 1) % len(self.run_frames)
            self.image = self.run_frames[self.anim_frame_index]
        else:
            self.image = self.idle_image if self.idle_image is not None else None

    def draw(self, surface):
        if self.image:
            img = self.image
            img_rect = img.get_rect()
            img_rect.midbottom = self.rect.midbottom
            surface.blit(img, img_rect)
        else:
            pygame.draw.rect(surface, COL_PLAYER, self.rect)


class Collectible:
    def __init__(self, x, y, image=None):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.collected = False
        self.image = image

    def update(self, dt_sec, speed_x):
        self.rect.x -= int(speed_x * dt_sec)

    def draw(self, surface):
        if self.collected:
            return
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, COL_COLLECT, self.rect)


class Obstacle:
    def __init__(self, x, ground_y, w=90, h=60, image=None):
        self.rect = pygame.Rect(x, ground_y - h, w, h)
        self.image = image

    def update(self, dt_sec, speed_x):
        self.rect.x -= int(speed_x * dt_sec)

    def draw(self, surface):
        if self.image:
            img_rect = self.image.get_rect()
            img_rect.midbottom = self.rect.midbottom
            surface.blit(self.image, img_rect)
        else:
            pygame.draw.rect(surface, COL_OBS, self.rect)


class Segment:
    def __init__(self, name, length, bg_color, bg_image=None):
        self.name = name
        self.length = length
        self.bg_color = bg_color
        self.bg_image = bg_image
        self.distance_travelled = 0
        self.obstacles = []
        self.collectibles = []

    def spawn_obstacle(self, x, ground_y, w=90, h=60, image=None):
        self.obstacles.append(Obstacle(x, ground_y, w, h, image))

    def spawn_collectible(self, x, y, image=None):
        self.collectibles.append(Collectible(x, y, image))

    def update(self, dt_ms, player):
        dt = dt_ms / 1000.0
        speed_x = player.speed_x
        self.distance_travelled += speed_x * dt

        for obs in self.obstacles:
            obs.update(dt, speed_x)
        for col in self.collectibles:
            col.update(dt, speed_x)

        self.obstacles = [o for o in self.obstacles if o.rect.right > 0]
        self.collectibles = [c for c in self.collectibles if c.rect.right > 0]

    def draw_background(self, surface):
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            surface.fill(self.bg_color)

    def draw_objects(self, surface):
        for col in self.collectibles:
            col.draw(surface)
        for obs in self.obstacles:
            obs.draw(surface)

    def is_finished(self):
        return self.distance_travelled >= self.length

    def maybe_trigger_info(self, level_controller):
        pass


# LEVEL 1 – SAHDAG

class OldCitySegment(Segment):
    def __init__(self):
        super().__init__("Asagi Sahdag cığirlari", length=3000, bg_color=COL_SEG_OLD, bg_image=BG_OLD)
        ground_y = HEIGHT - 80

        for x in [600, 1000, 1400, 2000, 2600]:
            self.spawn_obstacle(x, ground_y, image=OBST_WOOD_CART)
        self.spawn_obstacle(1800, ground_y, image=OBST_STONE)
        self.spawn_obstacle(2300, ground_y, image=OBST_CAT)

        for x in [400, 900, 1500, 2200]:
            self.spawn_collectible(x, ground_y - 120, COIN_IMAGE)

        self.info_1_distance = 800
        self.info_1_done = False
        self.info_2_distance = 1500
        self.info_2_done = False

    def maybe_trigger_info(self, level_controller):
        if not self.info_1_done and self.distance_travelled >= self.info_1_distance:
            level_controller.show_info(
                "Sahdag seyahetin zirvenin etegindeki kiçik dag kendlerinin yaninda baslayir."
            )
            self.info_1_done = True

        if not self.info_2_done and self.distance_travelled >= self.info_2_distance:
            level_controller.dialog_manager.start([
                "Bu daha asan cıgırlar ayaqlarini isinmaga komek edir,",
                "yol daha dik ve çetin olmamishdan evvel."
            ])
            self.info_2_done = True


class MaidenTowerSegment(Segment):
    def __init__(self):
        super().__init__("Orta yamac yolu", length=2200, bg_color=COL_SEG_MAIDEN, bg_image=BG_MAIDEN)
        ground_y = HEIGHT - 80

        self.spawn_obstacle(400, ground_y, image=OBST_STONE)
        self.spawn_obstacle(900, ground_y, image=OBST_CAT)
        self.spawn_obstacle(1400, ground_y)

        for x in [700, 1300, 1900]:
            self.spawn_collectible(x, ground_y - 130, COIN_IMAGE)

        self.info_distance = 500
        self.info_done = False

    def maybe_trigger_info(self, level_controller):
        if not self.info_done and self.distance_travelled >= self.info_distance:
            level_controller.show_info(
                "Sahdaga qalxdıqca hava daha sərin, daha temiz ve çox ferah olur."
            )
            level_controller.dialog_manager.start([
                "Buradan artiq Boyuk Qafqaz silsilesine genish menzereler gorursen,",
                "hem de muxtelif fesillerde gelen xizekcilere ve piyada seyahetçilere ayrilan yamaclari."
            ])
            self.info_done = True


class ModernBakuSegment(Segment):
    def __init__(self):
        super().__init__("Kurort zonasi", length=2800, bg_color=COL_SEG_MODERN, bg_image=BG_MODERN)
        ground_y = HEIGHT - 80

        self.spawn_obstacle(500, ground_y, image=OBST_CAR)
        self.spawn_obstacle(1100, ground_y, image=OBST_BARRIER)
        self.spawn_obstacle(1700, ground_y, image=OBST_SCOOTER)
        self.spawn_obstacle(2300, ground_y, image=OBST_BARRIER)

        for x in [400, 900, 1500, 2100]:
            self.spawn_collectible(x, ground_y - 120, COIN_IMAGE)

        self.info_flame_distance = 600
        self.info_flame_done = False
        self.info_heydar_distance = 1600
        self.info_heydar_done = False

    def maybe_trigger_info(self, level_controller):
        if not self.info_flame_done and self.distance_travelled >= self.info_flame_distance:
            level_controller.show_info(
                "Sahdag kurort zonasinda muasir oteller, xizek traslari ve kanat yolllari birbasha daglarda yerlesib."
            )
            level_controller.dialog_manager.start([
                "Qishda xizekçiler bu yamaclardan suretle ashagi dusur,",
                "yaz ve yayda ise qonaqlar piyada yuruyus, zip-line ve velosiped marşrutlarindan zovq alir."
            ])
            self.info_flame_done = True

        if not self.info_heydar_done and self.distance_travelled >= self.info_heydar_distance:
            level_controller.show_info(
                "Muasir infrastukturuna gore Sahdag Azerbaycanin en inkisaf etmis dag turizm merkezlerinden biridir."
            )
            self.info_heydar_done = True


class BoulevardSegment(Segment):
    def __init__(self):
        super().__init__("Meşe kənari istirahet zonasi", length=2600, bg_color=COL_SEG_BOULEVARD, bg_image=BG_BOULEVARD)
        ground_y = HEIGHT - 80

        self.spawn_obstacle(500, ground_y, image=OBST_PUDDLE)
        self.spawn_obstacle(1100, ground_y, image=OBST_CYCLIST)
        self.spawn_obstacle(1700, ground_y, image=OBST_BENCH)
        self.spawn_obstacle(2200, ground_y, image=OBST_PUDDLE)

        for x in [300, 900, 1500, 2100]:
            self.spawn_collectible(x, ground_y - 120, COIN_IMAGE)

        self.info_1_done = False
        self.info_1_distance = 400
        self.info_2_done = False
        self.info_2_distance = 900

    def maybe_trigger_info(self, level_controller):
        if not self.info_1_done and self.distance_travelled >= self.info_1_distance:
            level_controller.show_info(
                "Sahdag etrafinda uzun yuruyusden ve xizek gununden sonra ailelerin istirahet etdiyi yashil yamaclar, çaylar ve piknik saheleri var."
            )
            self.info_1_done = True

        if not self.info_2_done and self.distance_travelled >= self.info_2_distance:
            level_controller.show_info(
                "Taxta skamyalar ve kiçik baxish meydançalari sakit dag menzeresinden zovq almaq ucun dayanmagina imkan verir."
            )
            level_controller.dialog_manager.start([
                "Burasi qonaqlarin foto çektirdiyi,",
                "isti çay ichib agaclar arasinda esen kuli dinlediyi sevimli mekandir."
            ])
            self.info_2_done = True


class FlameTrialSegment(Segment):
    def __init__(self):
        super().__init__("En dik son qalxish", length=2000, bg_color=COL_SEG_FLAME, bg_image=BG_FLAME)
        ground_y = HEIGHT - 80

        for x in [400, 700, 1000, 1300, 1600]:
            self.spawn_obstacle(x, ground_y, image=OBST_FLAME_PATCH)

        for x in [500, 900, 1400, 1800]:
            self.spawn_collectible(x, ground_y - 130, COIN_IMAGE)

        self.intro_done = False
        self.intro_distance = 100

    def maybe_trigger_info(self, level_controller):
        if not self.intro_done and self.distance_travelled >= self.intro_distance:
            level_controller.dialog_manager.start([
                "Indi Sahdag marşrutunun en dik hisselerinden birine gelmisen.",
                "Tarazini qoru, suretine nezaret et ve Sahdag dag nişanini qazan!"
            ])
            self.intro_done = True


class InfoPopupManager:
    def __init__(self):
        self.active = False
        self.text = ""
        self.timer = 0
        self.duration = 3500

    def show(self, text):
        self.text = text
        self.timer = 0
        self.active = True

    def update(self, dt):
        if self.active:
            self.timer += dt
            if self.timer >= self.duration:
                self.active = False

    def draw(self, surface):
        if not self.active:
            return
        overlay = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))
        draw_text(surface, self.text, 24, COL_TEXT, WIDTH // 2, 40)


class DialogManager:
    def __init__(self):
        self.lines = []
        self.current_index = 0
        self.active = False

    def start(self, lines):
        self.lines = lines
        self.current_index = 0
        self.active = True

    def next_line(self):
        self.current_index += 1
        if self.current_index >= len(self.lines):
            self.active = False

    def get_current(self):
        if not self.active or not self.lines:
            return ""
        return self.lines[self.current_index]

    def draw(self, surface):
        if not self.active:
            return

        box_h = 60
        y_pos = HEIGHT - box_h - 20

        box = pygame.Surface((WIDTH, box_h), pygame.SRCALPHA)
        box.fill((0, 0, 0, 200))
        surface.blit(box, (0, y_pos))

        draw_text(
            surface,
            self.get_current(),
            22,
            COL_TEXT,
            WIDTH // 2,
            y_pos + box_h // 2
        )


class QuizScreen:
    def __init__(self, screen, questions, title="Quiz", intro_subtitle="Sual cavaba hazir ol..."):
        self.screen = screen
        self.all_questions = questions
        self.questions = random.sample(questions, min(5, len(questions)))
        self.current_index = 0
        self.score = 0

        self.state = "INTRO"
        self.state_timer = 0

        self.selected_option = None
        self.is_correct = False

        self.font_q = pygame.font.SysFont("Arial", 32)
        self.font_opt = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 20)

        self.shake_offset = 0
        self.confetti_particles = []

        w, h = self.screen.get_size()
        self.option_rects = [
            pygame.Rect(w * 0.1, h * 0.55, w * 0.8, 50),
            pygame.Rect(w * 0.1, h * 0.65, w * 0.8, 50),
            pygame.Rect(w * 0.1, h * 0.75, w * 0.8, 50),
        ]

        self.title = title
        self.intro_subtitle = intro_subtitle

    def start(self):
        self.state = "INTRO"
        self.state_timer = 0
        self.shake_offset = 0
        self.confetti_particles.clear()

    def update(self, dt):
        self.state_timer += dt

        if self.state == "INTRO":
            self.update_intro(dt)
        elif self.state == "SHOW_QUESTION":
            self.update_show_question(dt)
        elif self.state == "FEEDBACK":
            self.update_feedback(dt)
        elif self.state == "SHOW_FACT":
            self.update_show_fact(dt)

    def handle_event(self, event):
        if self.state == "WAIT_ANSWER":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mx, my):
                        self.on_option_chosen(i)
        elif self.state == "RESULT":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return "QUIZ_DONE"
        return None

    def update_intro(self, dt):
        if self.state_timer > 500:
            self.state = "SHOW_QUESTION"
            self.state_timer = 0

    def update_show_question(self, dt):
        if self.state_timer > 300:
            self.state = "WAIT_ANSWER"
            self.state_timer = 0

    def on_option_chosen(self, option_index):
        self.selected_option = option_index
        correct_index = self.questions[self.current_index]["correct_index"]
        self.is_correct = (option_index == correct_index)

        if self.is_correct:
            self.score += 1
            if SND_CORRECT:
                SND_CORRECT.play()
            self.spawn_confetti()
        else:
            if SND_WRONG:
                SND_WRONG.play()
            self.start_shake()

        self.state = "FEEDBACK"
        self.state_timer = 0

    def update_feedback(self, dt):
        if self.is_shaking():
            self.update_shake(dt)
        self.update_confetti(dt)

        if self.state_timer > 800:
            self.state = "SHOW_FACT"
            self.state_timer = 0

    def update_show_fact(self, dt):
        if self.state_timer > 1500:
            self.next_question_or_result()

    def next_question_or_result(self):
        self.current_index += 1
        self.selected_option = None
        self.is_correct = False
        self.shake_offset = 0
        self.confetti_particles.clear()

        if self.current_index >= len(self.questions):
            self.state = "RESULT"
            self.state_timer = 0
        else:
            self.state = "SHOW_QUESTION"
            self.state_timer = 0

    def start_shake(self):
        self.shake_offset = 0

    def is_shaking(self):
        return (not self.is_correct) and self.selected_option is not None

    def update_shake(self, dt):
        t = self.state_timer / 50.0
        self.shake_offset = int(5 * math.sin(t * 10))

    def spawn_confetti(self):
        w, h = self.screen.get_size()
        for _ in range(30):
            self.confetti_particles.append([
                w // 2, h // 2,
                random.uniform(-2, 2),
                random.uniform(-4, -1),
                random.randint(500, 1000)
            ])

    def update_confetti(self, dt):
        for p in self.confetti_particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= dt
        self.confetti_particles = [p for p in self.confetti_particles if p[4] > 0]

    def draw(self):
        self.screen.fill((10, 20, 40))
        w, h = self.screen.get_size()
        panel_offset_x = self.shake_offset

        if self.state in ("SHOW_QUESTION", "WAIT_ANSWER", "FEEDBACK", "SHOW_FACT"):
            q = self.questions[self.current_index]
            question_text = q["question"]

            q_surf = self.font_q.render(question_text, True, (255, 255, 255))
            q_rect = q_surf.get_rect(center=(w // 2 + panel_offset_x, int(h * 0.25)))
            self.screen.blit(q_surf, q_rect)

            for i, rect in enumerate(self.option_rects):
                color = (40, 40, 80)
                outline = (200, 200, 200)

                mx, my = pygame.mouse.get_pos()
                if self.state == "WAIT_ANSWER" and rect.collidepoint(mx, my):
                    color = (60, 60, 110)

                if self.state in ("FEEDBACK", "SHOW_FACT") and self.selected_option is not None:
                    correct_index = q["correct_index"]
                    if i == correct_index:
                        outline = (50, 220, 120)
                    elif i == self.selected_option:
                        outline = (220, 60, 60)

                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                pygame.draw.rect(self.screen, outline, rect, 2, border_radius=8)

                opt_text = q["options"][i]
                opt_surf = self.font_opt.render(opt_text, True, (255, 255, 255))
                opt_rect = opt_surf.get_rect(center=rect.center)
                self.screen.blit(opt_surf, opt_rect)

            if self.state == "SHOW_FACT":
                fact = q["fact"]
                fact_surf = self.font_small.render("Bilirdin ki? " + fact, True, (200, 220, 255))
                fact_rect = fact_surf.get_rect(center=(w // 2, int(h * 0.45)))
                self.screen.blit(fact_surf, fact_rect)

            total = len(self.questions)
            current = self.current_index + 1
            bar_w = int((w * 0.6) * current / total)
            bar_bg = pygame.Rect(w * 0.2, h * 0.1, w * 0.6, 10)
            bar_fg = pygame.Rect(w * 0.2, h * 0.1, bar_w, 10)
            pygame.draw.rect(self.screen, (60, 60, 90), bar_bg, border_radius=5)
            pygame.draw.rect(self.screen, (120, 220, 250), bar_fg, border_radius=5)

        for x, y, vx, vy, life in self.confetti_particles:
            pygame.draw.circle(self.screen, (255, 255, 0), (int(x), int(y)), 3)

        if self.state == "INTRO":
            if BG_BOULEVARD:
                self.screen.blit(BG_BOULEVARD, (0, 0))
            draw_text(self.screen, self.title, 40, (255, 215, 0),
                      w // 2, h // 2 - 40)
            draw_text(self.screen, self.intro_subtitle,
                      24, (220, 220, 220), w // 2, h // 2 + 10)

        if self.state == "RESULT":
            result_text = f"Quiz bitdi! Neticen: {self.score}/{len(self.questions)}"
            res_surf = self.font_q.render(result_text, True, (255, 215, 0))
            res_rect = res_surf.get_rect(center=(w // 2, h // 2))
            self.screen.blit(res_surf, res_rect)

            cont_surf = self.font_small.render("Davm etmek ucun istenilen duymeni six.", True, (220, 220, 220))
            cont_rect = cont_surf.get_rect(center=(w // 2, h // 2 + 60))
            self.screen.blit(cont_surf, cont_rect)


class BakuLevel:
    def __init__(self, screen):
        self.screen = screen
        self.state = "LEVEL_INTRO"
        self.state_timer = 0

        self.player = Player(200, HEIGHT - 80)
        self.segments = [
            OldCitySegment(),
            MaidenTowerSegment(),
            ModernBakuSegment(),
            BoulevardSegment(),
            FlameTrialSegment(),
        ]
        self.current_segment_index = 0

        self.info_manager = InfoPopupManager()
        self.dialog_manager = DialogManager()

        self.score = 0
        self.collected_count = 0
        self.damage_taken = 0

        self.level_finished = False
        self.game_over = False

    def current_segment(self):
        if 0 <= self.current_segment_index < len(self.segments):
            return self.segments[self.current_segment_index]
        return None

    def show_info(self, text):
        self.info_manager.show(text)

    def update(self, dt, events):
        self.state_timer += dt

        if self.state == "LEVEL_INTRO":
            self.update_intro(dt, events)
        elif self.state == "CUTSCENE_ARRIVAL":
            self.update_cutscene_arrival(dt, events)
        elif self.state.startswith("SEGMENT_"):
            self.update_segment_state(dt, events)
        elif self.state == "LEVEL_END_CUTSCENE":
            self.update_end_cutscene(dt, events)
        elif self.state == "LEVEL_SUMMARY":
            self.update_summary(dt, events)

        self.info_manager.update(dt)

    def update_intro(self, dt, events):
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.state = "CUTSCENE_ARRIVAL"
                self.state_timer = 0

    def update_cutscene_arrival(self, dt, events):
        if self.state_timer == 0:
            lines = [
                "Sahdag dagina xos gelmisen – Azerbaycanin en meshur yaylaqlarindan biri.",
                "Bu seviyede kendlerden, meşe cığirlarindan ve muasir Sahdag kurort zonasindan kecersen.",
                "Sahdag Boyuk Qafqaz silsilesinin bir hissesi olaraq butun fesillerde seyahetçileri ceklir.",
                "Indi onun marşrutlarini kesf et ve dag turizminin nece ishlediyini oyren."
            ]
            self.dialog_manager.start(lines)

        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.dialog_manager.active:
                    self.dialog_manager.next_line()
                else:
                    self.state = "SEGMENT_OLD_CITY"
                    self.state_timer = 0

    def update_segment_state(self, dt, events):
        segment = self.current_segment()
        if not segment:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, dt / 1000.0)
        self.player.update(dt)

        segment.update(dt, self.player)
        segment.maybe_trigger_info(self)

        for col in segment.collectibles:
            if not col.collected and self.player.rect.colliderect(col.rect):
                col.collected = True
                self.score += 10
                self.collected_count += 1
                if SND_COLLECT:
                    SND_COLLECT.play()

        for obs in segment.obstacles:
            if self.player.rect.colliderect(obs.rect):
                self.damage_taken += 1
                self.player.rect.x -= 40
                if SND_HIT:
                    SND_HIT.play()

        if self.player.rect.right < 0 or self.player.rect.top > HEIGHT + 100:
            self.game_over = True
            return

        if segment.is_finished():
            self.current_segment_index += 1
            if self.current_segment_index >= len(self.segments):
                self.state = "LEVEL_END_CUTSCENE"
                self.state_timer = 0
            else:
                idx = self.current_segment_index
                if idx == 1:
                    self.state = "SEGMENT_MAIDEN_TOWER"
                elif idx == 2:
                    self.state = "SEGMENT_MODERN_BAKU"
                elif idx == 3:
                    self.state = "SEGMENT_BOULEVARD"
                elif idx == 4:
                    self.state = "SEGMENT_FLAME_TRIAL"
                self.state_timer = 0

    def update_end_cutscene(self, dt, events):
        if self.state_timer == 0:
            lines = [
                "Sahdag marşrutunu ugurla tamamladin.",
                "Asagi kendlerden, orta yamac yollarindan, kurort zonasindan ve meşe kenarindan kecdin.",
                "Butun bu melumat senin dag seyaheti pasportunun bir hissesi olur.",
                "Indi ise Sahdag barede ne qeder yadinda qaldigini yoxlayaq."
            ]
            self.dialog_manager.start(lines)

        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.dialog_manager.active:
                    self.dialog_manager.next_line()
                else:
                    self.state = "LEVEL_SUMMARY"
                    self.state_timer = 0

    def update_summary(self, dt, events):
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.level_finished = True

    def draw(self):
        if self.state == "LEVEL_INTRO":
            self.draw_intro()
        elif self.state == "CUTSCENE_ARRIVAL":
            self.draw_cutscene_arrival()
        elif self.state.startswith("SEGMENT_"):
            self.draw_segment()
        elif self.state == "LEVEL_END_CUTSCENE":
            self.draw_end_cutscene()
        elif self.state == "LEVEL_SUMMARY":
            self.draw_summary()

        self.info_manager.draw(self.screen)
        self.dialog_manager.draw(self.screen)

        if self.state.startswith("SEGMENT_"):
            draw_text(self.screen, f"Xal: {self.score}", 24, COL_TEXT, 90, 30, center=False)
            draw_text(self.screen, f"Toplanilan: {self.collected_count}", 24, COL_TEXT, 90, 60, center=False)
            draw_text(self.screen, f"Zede: {self.damage_taken}", 24, COL_TEXT, 90, 90, center=False)

    def draw_intro(self):
        if BG_INTRO:
            self.screen.blit(BG_INTRO, (0, 0))
        else:
            self.screen.fill(COL_BG)
        draw_text(self.screen, "Sahdag dagi – Macera baslayir", 36,
                  COL_TEXT, WIDTH // 2, HEIGHT // 2 - 40)
        draw_text(self.screen, "Seviye 1", 26, (200, 220, 255),
                  WIDTH // 2, HEIGHT // 2)
        draw_text(self.screen, "Baslamaq ucun istenilen duymeni six", 24,
                  (180, 220, 255), WIDTH // 2, HEIGHT // 2 + 40)

    def draw_cutscene_arrival(self):
        if BG_CUTSCENE:
            self.screen.blit(BG_CUTSCENE, (0, 0))
        else:
            self.screen.fill((20, 20, 60))
            pygame.draw.rect(self.screen, (255, 120, 40),
                             (0, HEIGHT - 200, WIDTH, 200))
        draw_text(self.screen, "Sahdag – daglara giris qapisi", 32, COL_TEXT, WIDTH // 2, 80)

    def draw_segment(self):
        seg = self.current_segment()
        if not seg:
            self.screen.fill(COL_BG)
            return
        seg.draw_background(self.screen)
        seg.draw_objects(self.screen)
        self.player.draw(self.screen)

    def draw_end_cutscene(self):
        self.screen.fill((20, 20, 40))
        draw_text(self.screen, "Sahdag seyahetini tamamladin!", 36,
                  COL_TEXT, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(self.screen,
                  "Davm etmek ucun istenilen duymeni veya mausu six.",
                  22, (200, 220, 255), WIDTH // 2, HEIGHT // 2 + 20)

    def draw_summary(self):
        self.screen.fill((15, 15, 35))
        draw_text(self.screen, "SEVIYE 1 YEKUNU – SAHDAG", 40, COL_TEXT, WIDTH // 2, 100)
        draw_text(self.screen, f"Xal: {self.score}", 28, COL_TEXT, WIDTH // 2, 200)
        draw_text(self.screen, f"Toplanilan: {self.collected_count}", 28, COL_TEXT, WIDTH // 2, 250)
        draw_text(self.screen, f"Alinan zede: {self.damage_taken}", 28, COL_TEXT, WIDTH // 2, 300)
        draw_text(self.screen, "Sahdag Quizine baslamaq ucun istenilen duymeni six.",
                  24, (200, 220, 255), WIDTH // 2, 380)


# LEVEL 2 – BAZARDUZU

class ShekiTownSegment(Segment):
    def __init__(self):
        super().__init__("Bazarduzu bazalist kend zonasi", length=2800,
                         bg_color=(70, 70, 90), bg_image=BG_SHEKI_TOWN)
        ground_y = HEIGHT - 80

        for x in [500, 900, 1300, 1900, 2300]:
            self.spawn_obstacle(x, ground_y,
                                image=OBST_SHEKI_CART or OBST_WOOD_CART)
        self.spawn_obstacle(1600, ground_y,
                            image=OBST_STREET_HOLE or OBST_STONE)

        for x in [400, 800, 1500, 2100]:
            self.spawn_collectible(x, ground_y - 120,
                                   image=ICON_SWEET or COIN_IMAGE)

        self.info_silk_distance = 500
        self.info_silk_done = False
        self.info_sweets_distance = 1500
        self.info_sweets_done = False

    def maybe_trigger_info(self, level_controller):
        if (not self.info_silk_done and
                self.distance_travelled >= self.info_silk_distance):
            level_controller.show_info(
                "Bazarduzu Azerbaycanin en yuksek zirvesidir, alpinistler adeten yaxin dag kendlerinden start goturur."
            )
            level_controller.dialog_manager.start([
                "Bu bazalist erazilerde qidalanma, hava proqnozu ve marşrut planlashdirilmasinda yerli bələdchilar komek edir."
            ])
            self.info_silk_done = True

        if (not self.info_sweets_done and
                self.distance_travelled >= self.info_sweets_distance):
            level_controller.show_info(
                "Qalxishdan once bir çox seyahetçi kiçik dukanlardan yemek, isti geyim ve tehlukesizlik avadanligi alir."
            )
            level_controller.dialog_manager.start([
                "Yaxshi hazirliq vacibdir, cunki Bazarduzunun yuksekliyi ve soyuq havasi çetinlik yarada biler.",
                "Yuxari hisselere yalniz yaxshi hazirlashmish seyahetçiler qalxmalidir."
            ])
            self.info_sweets_done = True


class ShekiPalaceSegment(Segment):
    def __init__(self):
        super().__init__("Yuksek camp zonasi", length=2200,
                         bg_color=(60, 60, 90), bg_image=BG_SHEKI_PALACE)
        ground_y = HEIGHT - 80

        self.spawn_obstacle(500, ground_y,
                            image=OBST_GARDEN_DECOR or OBST_BENCH)
        self.spawn_obstacle(1100, ground_y,
                            image=OBST_GARDEN_DECOR or OBST_BARRIER)
        self.spawn_obstacle(1700, ground_y,
                            image=OBST_GARDEN_DECOR or OBST_STONE)

        for x in [400, 1000, 1500, 2000]:
            self.spawn_collectible(x, ground_y - 130,
                                   image=ICON_SHEBEKE or COIN_IMAGE)

        self.info_palace_distance = 400
        self.info_palace_done = False
        self.info_shebeke_distance = 1300
        self.info_shebeke_done = False

    def maybe_trigger_info(self, level_controller):
        if (not self.info_palace_done and
                self.distance_travelled >= self.info_palace_distance):
            level_controller.show_info(
                "Yuksek camplarda alpinistler dincelir, saglamliqlarini yoxlayir ve zirveye son qalxishi planlashdirir."
            )
            level_controller.dialog_manager.start([
                "Buradan Boyuk Qafqaz silsilesine menzereler cok tesirli gorunur,",
                "geceler ise shahar ishiqlarindan uzaqda parlaq ulduzlarla doludur."
            ])
            self.info_palace_done = True

        if (not self.info_shebeke_done and
                self.distance_travelled >= self.info_shebeke_distance):
            level_controller.show_info(
                "Bazarduzu ciddi alp zirvesi oldugu ucun komandalar qaydalara riayet etmeli ve bələdchilere qulaq asmalidir."
            )
            level_controller.dialog_manager.start([
                "Yaxshi komanda isi, munasib geyim ve diqqetle secilmis marşrut",
                "tehlukesiz qalxish ile tehlukeli veziyyet arasindaki ferqi yaradir."
            ])
            self.info_shebeke_done = True


class ShekiForestSegment(Segment):
    def __init__(self):
        super().__init__("Bazarduzu dereleri ve çaylari", length=2400,
                         bg_color=(30, 60, 40), bg_image=BG_SHEKI_FOREST)
        ground_y = HEIGHT - 80

        self.spawn_obstacle(600, ground_y,
                            image=OBST_TREE_ROOT or OBST_STONE)
        self.spawn_obstacle(1200, ground_y,
                            image=OBST_BRANCH or OBST_PUDDLE)
        self.spawn_obstacle(1800, ground_y,
                            image=OBST_TREE_ROOT or OBST_STONE)

        for x in [500, 1100, 1700, 2100]:
            self.spawn_collectible(x, ground_y - 130,
                                   image=ICON_FLOWER or COIN_IMAGE)

        self.info_nature_distance = 700
        self.info_nature_done = False

    def maybe_trigger_info(self, level_controller):
        if (not self.info_nature_done and
                self.distance_travelled >= self.info_nature_distance):
            level_controller.show_info(
                "Bazarduzu etrafinda yashil dereler, çaylar ve alp otlaqlari terefsizleri ve tebie severleri buraya celb edir."
            )
            level_controller.dialog_manager.start([
                "Zirveye qalxmasan da, bu asagi hisselerde uzun piyada yuruyusler,",
                "taze dag havası ve sakit piknik sahelerinden zovq almaq olar."
            ])
            self.info_nature_done = True


class ShekiLevel:
    def __init__(self, screen):
        self.screen = screen
        self.state = "L2_INTRO"
        self.state_timer = 0

        self.player = Player(200, HEIGHT - 80)
        self.segments = [
            ShekiTownSegment(),
            ShekiPalaceSegment(),
            ShekiForestSegment(),
        ]
        self.current_segment_index = 0

        self.info_manager = InfoPopupManager()
        self.dialog_manager = DialogManager()

        self.score = 0
        self.collected_count = 0
        self.damage_taken = 0

        self.level_finished = False
        self.game_over = False

    def current_segment(self):
        if 0 <= self.current_segment_index < len(self.segments):
            return self.segments[self.current_segment_index]
        return None

    def show_info(self, text):
        self.info_manager.show(text)

    def update(self, dt, events):
        self.state_timer += dt

        if self.state == "L2_INTRO":
            self.update_intro(dt, events)
        elif self.state == "L2_CUTSCENE_ARRIVAL":
            self.update_cutscene_arrival(dt, events)
        elif self.state.startswith("L2_SEGMENT_"):
            self.update_segment_state(dt, events)
        elif self.state == "L2_END_CUTSCENE":
            self.update_end_cutscene(dt, events)
        elif self.state == "L2_SUMMARY":
            self.update_summary(dt, events)

        self.info_manager.update(dt)

    def update_intro(self, dt, events):
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.state = "L2_CUTSCENE_ARRIVAL"
                self.state_timer = 0

    def update_cutscene_arrival(self, dt, events):
        if self.state_timer == 0:
            lines = [
                "Bazarduzuye xos gelmisen – Azerbaycanin en yuksek zirvesi.",
                "Bu seviyede bazalist kendlerden yuksek camplara ve dag etrafindaki yashil derelere dogru hereket edeceksen.",
                "Bazarduzu Azerbaycan ile Rusiya serhedinde, Boyuk Qafqaz silsilesinde yerlesir.",
                "Cox az insan zirveye qeder qalxir, amma minlerle seyahetçi onun asagi hisselerinin menzeresinden zovq alir.",
                "Yol boyu topladigin melumatlar – Bazarduzu quizi ucun sana komek edecek!"
            ]
            self.dialog_manager.start(lines)

        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.dialog_manager.active:
                    self.dialog_manager.next_line()
                else:
                    self.state = "L2_SEGMENT_TOWN"
                    self.state_timer = 0

    def update_segment_state(self, dt, events):
        segment = self.current_segment()
        if not segment:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, dt / 1000.0)
        self.player.update(dt)

        segment.update(dt, self.player)
        segment.maybe_trigger_info(self)

        for col in segment.collectibles:
            if (not col.collected) and self.player.rect.colliderect(col.rect):
                col.collected = True
                self.score += 10
                self.collected_count += 1
                if SND_COLLECT:
                    SND_COLLECT.play()

        for obs in segment.obstacles:
            if self.player.rect.colliderect(obs.rect):
                self.damage_taken += 1
                self.player.rect.x -= 40
                if SND_HIT:
                    SND_HIT.play()

        if self.player.rect.right < 0 or self.player.rect.top > HEIGHT + 100:
            self.game_over = True
            return

        if segment.is_finished():
            self.current_segment_index += 1
            if self.current_segment_index >= len(self.segments):
                self.state = "L2_END_CUTSCENE"
                self.state_timer = 0
            else:
                idx = self.current_segment_index
                if idx == 1:
                    self.state = "L2_SEGMENT_PALACE"
                elif idx == 2:
                    self.state = "L2_SEGMENT_FOREST"
                self.state_timer = 0

    def update_end_cutscene(self, dt, events):
        if self.state_timer == 0:
            lines = [
                "Aferin! Bazarduzu etrafindaki seyahetini tamamladin.",
                "Bazalist kendleri, yuksek camp zonalarini ve sakit dere ve çay erazilerini kesf etdin.",
                "Indi gel, Azerbaycanin bu en yuksek zirvesi barede ne qeder melumat topladigini yoxlayaq."
            ]
            self.dialog_manager.start(lines)

        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.dialog_manager.active:
                    self.dialog_manager.next_line()
                else:
                    self.state = "L2_SUMMARY"
                    self.state_timer = 0

    def update_summary(self, dt, events):
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.level_finished = True

    def draw(self):
        if self.state == "L2_INTRO":
            self.draw_intro()
        elif self.state == "L2_CUTSCENE_ARRIVAL":
            self.draw_cutscene_arrival()
        elif self.state.startswith("L2_SEGMENT_"):
            self.draw_segment()
        elif self.state == "L2_END_CUTSCENE":
            self.draw_end_cutscene()
        elif self.state == "L2_SUMMARY":
            self.draw_summary()

        self.info_manager.draw(self.screen)
        self.dialog_manager.draw(self.screen)

        if self.state.startswith("L2_SEGMENT_"):
            draw_text(self.screen, f"Xal: {self.score}", 24, COL_TEXT, 90, 30, center=False)
            draw_text(self.screen, f"Toplanilan: {self.collected_count}", 24, COL_TEXT, 90, 60, center=False)
            draw_text(self.screen, f"Zede: {self.damage_taken}", 24, COL_TEXT, 90, 90, center=False)

    def draw_intro(self):
        if BG_SHEKI_TOWN:
            self.screen.blit(BG_SHEKI_TOWN, (0, 0))
        else:
            self.screen.fill(COL_BG)
        draw_text(self.screen, "SEVIYE 2: Bazarduzu – Azerbaycanin dami", 32,
                  COL_TEXT, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(self.screen, "Baslamaq ucun istenilen duymeni six", 24,
                  (200, 220, 255), WIDTH // 2, HEIGHT // 2 + 20)

    def draw_cutscene_arrival(self):
        if BG_SHEKI_TOWN:
            self.screen.blit(BG_SHEKI_TOWN, (0, 0))
        else:
            self.screen.fill((20, 40, 60))
        draw_text(self.screen, "Bazarduzu etrafinada gelyirik", 32, COL_TEXT, WIDTH // 2, 80)

    def draw_segment(self):
        seg = self.current_segment()
        if not seg:
            self.screen.fill(COL_BG)
            return
        seg.draw_background(self.screen)
        seg.draw_objects(self.screen)
        self.player.draw(self.screen)

    def draw_end_cutscene(self):
        self.screen.fill((20, 20, 40))
        draw_text(self.screen, "Bazarduzu erazisindeki seyahet bitdi!", 32,
                  COL_TEXT, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(self.screen,
                  "Davm etmek ucun istenilen duymeni veya mausu six.",
                  22, (200, 220, 255), WIDTH // 2, HEIGHT // 2 + 20)

    def draw_summary(self):
        self.screen.fill((15, 15, 35))
        draw_text(self.screen, "SEVIYE 2 YEKUNU – BAZARDUZU", 40, COL_TEXT, WIDTH // 2, 100)
        draw_text(self.screen, f"Xal: {self.score}", 28, COL_TEXT, WIDTH // 2, 200)
        draw_text(self.screen, f"Toplanilan: {self.collected_count}", 28, COL_TEXT, WIDTH // 2, 250)
        draw_text(self.screen, f"Alinan zede: {self.damage_taken}", 28, COL_TEXT, WIDTH // 2, 300)
        draw_text(self.screen, "Bazarduzu quizi ucun davm etmek ucun istenilen duymeni six.",
                  24, (200, 220, 255), WIDTH // 2, 380)


# LEVEL 3 – TUFANDAG

class KarabakhShushaSegment(Segment):
    def __init__(self):
        super().__init__(
            "Tufandag bazalist stansiyasi",
            length=2800,
            bg_color=COL_SEG_K_SHUSHA,
            bg_image=BG_KARABAKH_SHUSHA
        )
        ground_y = HEIGHT - 80

        self.spawn_obstacle(500, ground_y, image=OBST_SHUSHA_STONES or OBST_STONE)
        self.spawn_obstacle(900, ground_y, image=OBST_SHUSHA_ARCH or OBST_BARRIER)
        self.spawn_obstacle(1300, ground_y, image=OBST_SHUSHA_FRAME or OBST_WOOD_CART)
        self.spawn_obstacle(1800, ground_y, image=OBST_SHUSHA_STONES or OBST_STONE)
        self.spawn_obstacle(2200, ground_y, image=OBST_SHUSHA_ARCH or OBST_BARRIER)

        self.spawn_collectible(400, ground_y - 130, image=ICON_TAR or COIN_IMAGE)
        self.spawn_collectible(800, ground_y - 130, image=ICON_KAMANCHA or COIN_IMAGE)
        self.spawn_collectible(1400, ground_y - 130, image=ICON_XARIBULBUL or COIN_IMAGE)
        self.spawn_collectible(2000, ground_y - 130, image=ICON_KARABAKH_CARPET or COIN_IMAGE)

        self.info_1_distance = 600
        self.info_1_done = False
        self.info_2_distance = 1500
        self.info_2_done = False
        self.warn_1_distance = 1000
        self.warn_1_done = False

    def maybe_trigger_info(self, level_controller):
        if (not self.info_1_done and
                self.distance_travelled >= self.info_1_distance):
            level_controller.show_info(
                "Tufandag Qebele yaxinliginda yerleshen meshur dag kurortudur, muasir kanat yolllari ve xizek yamaclari ile taninir."
            )
            self.info_1_done = True

        if (not self.info_2_done and
                self.distance_travelled >= self.info_2_distance):
            level_controller.show_info(
                "Bazalist stansiyadan qonaqlar kanat kabineleri ile meşeler ve derelerin uzerinden yuksek baxish meydançalarina qalxir."
            )
            self.info_2_done = True

        if (not self.warn_1_done and
                self.distance_travelled >= self.warn_1_distance):
            level_controller.dialog_manager.start([
                "Diqqetli ol! Stansiya etrafindaki yollar bazi yerde dashli ve qeyri-duz ola biler.",
                "Ashagi kemerlerin altindan surush ve marşrutu diqqetle izzle!"
            ])
            self.warn_1_done = True


class KarabakhCidirSegment(Segment):
    def __init__(self):
        super().__init__(
            "Tufandag silsileleri ve baxish noqteeleri",
            length=2600,
            bg_color=COL_SEG_K_CIDIR,
            bg_image=BG_KARABAKH_CIDIR
        )
        ground_y = HEIGHT - 80

        self.spawn_obstacle(600, ground_y, image=OBST_CIDIR_ROCKS or OBST_STONE)
        self.spawn_obstacle(1200, ground_y, image=OBST_CIDIR_STONES or OBST_STONE)
        self.spawn_obstacle(1800, ground_y, image=OBST_CIDIR_ROCKS or OBST_STONE)
        self.spawn_obstacle(2200, ground_y, image=OBST_CIDIR_STONES or OBST_STONE)

        self.spawn_collectible(400, ground_y - 130, image=ICON_HORSE or COIN_IMAGE)
        self.spawn_collectible(1000, ground_y - 140, image=ICON_MUSIC_NOTE or COIN_IMAGE)
        self.spawn_collectible(1700, ground_y - 150, image=ICON_PHOTO_SPOT or COIN_IMAGE)

        self.info_1_distance = 400
        self.info_1_done = False
        self.info_2_distance = 1400
        self.info_2_done = False
        self.warn_1_distance = 900
        self.warn_1_done = False

    def maybe_trigger_info(self, level_controller):
        if (not self.info_1_done and
                self.distance_travelled >= self.info_1_distance):
            level_controller.show_info(
                "Tufandagin yuksek stansiyalarindan Qebele sheherine ve etraf daglara genish menzereler acilir."
            )
            self.info_1_done = True

        if (not self.info_2_done and
                self.distance_travelled >= self.info_2_distance):
            level_controller.show_info(
                "Qish feslinde bu yamaclar xizek traslarina cevrilir, daha isti aylarda ise piyada yuruyus ve foto seyahet ucun elverishlidir."
            )
            self.info_2_done = True

        if (not self.warn_1_done and
                self.distance_travelled >= self.warn_1_distance):
            level_controller.dialog_manager.start([
                "Dashli saheliere atlayaraq kec ve isaretlenmish marşrutlardan kenara cixma,",
                "cunki bu yukseklikde dag havasi tez deyishe biler."
            ])
            self.warn_1_done = True


class KarabakhForestSegment(Segment):
    def __init__(self):
        super().__init__(
            "Tufandag meşe cığirlari",
            length=2500,
            bg_color=COL_SEG_K_FOREST,
            bg_image=BG_KARABAKH_FOREST
        )
        ground_y = HEIGHT - 80

        self.spawn_obstacle(600, ground_y, image=OBST_FOREST_ROOT or OBST_TREE_ROOT)
        self.spawn_obstacle(1200, ground_y, image=OBST_FOREST_BRANCH or OBST_BRANCH)
        self.spawn_obstacle(1800, ground_y, image=OBST_FOREST_LOG or OBST_STONE)

        self.spawn_collectible(500, ground_y - 140, image=ICON_FOREST_FLOWER_K or ICON_FLOWER or COIN_IMAGE)
        self.spawn_collectible(1100, ground_y - 150, image=ICON_WATER_DROP or COIN_IMAGE)
        self.spawn_collectible(1700, ground_y - 160, image=ICON_BIRD or COIN_IMAGE)

        self.info_1_distance = 700
        self.info_1_done = False
        self.warn_1_distance = 1000
        self.warn_1_done = False

    def maybe_trigger_info(self, level_controller):
        if (not self.info_1_done and
                self.distance_travelled >= self.info_1_distance):
            level_controller.show_info(
                "Tufandagin yamaclari yaz ve yayda insanların piknik etdiyi, seyahet etdiyi sıx meşeler ile örtuludur."
            )
            self.info_1_done = True

        if (not self.warn_1_done and
                self.distance_travelled >= self.warn_1_distance):
            level_controller.dialog_manager.start([
                "Ashagi sallanan budaqlarin altindan eyilerek kec ve yoldaki kokleri izle,",
                "belelikle meşe cığirlarini kesf ederken yixilmazsan."
            ])
            self.warn_1_done = True


class KarabakhLevel:
    def __init__(self, screen):
        self.screen = screen
        self.state = "L3_INTRO"
        self.state_timer = 0

        self.player = Player(200, HEIGHT - 80)
        self.segments = [
            KarabakhShushaSegment(),
            KarabakhCidirSegment(),
            KarabakhForestSegment(),
        ]
        self.current_segment_index = 0

        self.info_manager = InfoPopupManager()
        self.dialog_manager = DialogManager()

        self.score = 0
        self.collected_count = 0
        self.damage_taken = 0

        self.level_finished = False
        self.game_over = False

    def current_segment(self):
        if 0 <= self.current_segment_index < len(self.segments):
            return self.segments[self.current_segment_index]
        return None

    def show_info(self, text):
        self.info_manager.show(text)

    def update(self, dt, events):
        self.state_timer += dt

        if self.state == "L3_INTRO":
            self.update_intro(dt, events)
        elif self.state == "L3_CUTSCENE_ARRIVAL":
            self.update_cutscene_arrival(dt, events)
        elif self.state.startswith("L3_SEGMENT_"):
            self.update_segment_state(dt, events)
        elif self.state == "L3_END_CUTSCENE":
            self.update_end_cutscene(dt, events)
        elif self.state == "L3_SUMMARY":
            self.update_summary(dt, events)

        self.info_manager.update(dt)

    def update_intro(self, dt, events):
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.state = "L3_CUTSCENE_ARRIVAL"
                self.state_timer = 0

    def update_cutscene_arrival(self, dt, events):
        if self.state_timer == 0:
            lines = [
                "Tufandaga xos gelmisen – kanat yolllari, xizek yamaclari ve meşe menzereleri ile taninan dag kurortu.",
                "Seyahetimiz bazalist stansiyadan yuksek silsilelere ve derin meşe cığirlarina qeder davam edecek.",
                "Qebele sheherinden buraya coxlu turist gelir, istirahet edir, foto çekir ve dag fealiyyetlerinden zovq alir.",
                "Yol boyu simvollar ve melumatlar topla – bunlar Tufandag quizi ucun lazim olacaq.",
                "Hazirsan? Gəlin dag yollarina dogru yola cixaq!"
            ]
            self.dialog_manager.start(lines)

        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.dialog_manager.active:
                    self.dialog_manager.next_line()
                else:
                    self.state = "L3_SEGMENT_SHUSHA"
                    self.state_timer = 0

    def update_segment_state(self, dt, events):
        segment = self.current_segment()
        if not segment:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, dt / 1000.0)
        self.player.update(dt)

        segment.update(dt, self.player)
        segment.maybe_trigger_info(self)

        for col in segment.collectibles:
            if (not col.collected) and self.player.rect.colliderect(col.rect):
                col.collected = True
                self.score += 10
                self.collected_count += 1
                if SND_COLLECT:
                    SND_COLLECT.play()

        for obs in segment.obstacles:
            if self.player.rect.colliderect(obs.rect):
                self.damage_taken += 1
                self.player.rect.x -= 40
                if SND_HIT:
                    SND_HIT.play()

        if self.player.rect.right < 0 or self.player.rect.top > HEIGHT + 100:
            self.game_over = True
            return

        if segment.is_finished():
            self.current_segment_index += 1
            if self.current_segment_index >= len(self.segments):
                self.state = "L3_END_CUTSCENE"
                self.state_timer = 0
            else:
                idx = self.current_segment_index
                if idx == 1:
                    self.state = "L3_SEGMENT_CIDIR"
                elif idx == 2:
                    self.state = "L3_SEGMENT_FOREST"
                self.state_timer = 0

    def update_end_cutscene(self, dt, events):
        if self.state_timer == 0:
            lines = [
                "Ela ish gordun! Tufandag marşrutunu tam seyahet etdin.",
                "Bazalist stansiyani, yuksek baxish noqteelerini ve sakit meşe cığirlarini gordun.",
                "Indi ise bu dag kurortu barede ne qeder melumat saxladigini yoxlayaq."
            ]
            self.dialog_manager.start(lines)

        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.dialog_manager.active:
                    self.dialog_manager.next_line()
                else:
                    self.state = "L3_SUMMARY"
                    self.state_timer = 0

    def update_summary(self, dt, events):
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.level_finished = True

    def draw(self):
        if self.state == "L3_INTRO":
            self.draw_intro()
        elif self.state == "L3_CUTSCENE_ARRIVAL":
            self.draw_cutscene_arrival()
        elif self.state.startswith("L3_SEGMENT_"):
            self.draw_segment()
        elif self.state == "L3_END_CUTSCENE":
            self.draw_end_cutscene()
        elif self.state == "L3_SUMMARY":
            self.draw_summary()

        self.info_manager.draw(self.screen)
        self.dialog_manager.draw(self.screen)

        if self.state.startswith("L3_SEGMENT_"):
            draw_text(self.screen, f"Xal: {self.score}", 24, COL_TEXT, 90, 30, center=False)
            draw_text(self.screen, f"Toplanilan: {self.collected_count}", 24, COL_TEXT, 90, 60, center=False)
            draw_text(self.screen, f"Zede: {self.damage_taken}", 24, COL_TEXT, 90, 90, center=False)

    def draw_intro(self):
        if BG_KARABAKH_INTRO:
            self.screen.blit(BG_KARABAKH_INTRO, (0, 0))
        else:
            self.screen.fill(COL_BG)
        draw_text(self.screen, "SEVIYE 3: Tufandag – Kanat yolllari ve menzereler", 30,
                  COL_TEXT, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(self.screen, "Baslamaq ucun istenilen duymeni six", 24,
                  (200, 220, 255), WIDTH // 2, HEIGHT // 2 + 20)

    def draw_cutscene_arrival(self):
        if BG_KARABAKH_CUTSCENE:
            self.screen.blit(BG_KARABAKH_CUTSCENE, (0, 0))
        else:
            self.screen.fill((30, 30, 60))
        draw_text(self.screen, "Tufandaga catiriq", 32, COL_TEXT, WIDTH // 2, 80)

    def draw_segment(self):
        seg = self.current_segment()
        if not seg:
            self.screen.fill(COL_BG)
            return
        seg.draw_background(self.screen)
        seg.draw_objects(self.screen)
        self.player.draw(self.screen)

    def draw_end_cutscene(self):
        self.screen.fill((20, 20, 40))
        draw_text(self.screen, "Tufandag seyaheti tamamlandi!", 32,
                  COL_TEXT, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(self.screen,
                  "Davm etmek ucun istenilen duymeni veya mausu six.",
                  22, (200, 220, 255), WIDTH // 2, HEIGHT // 2 + 20)

    def draw_summary(self):
        self.screen.fill((15, 15, 35))
        draw_text(self.screen, "SEVIYE 3 YEKUNU – TUFANDAG", 40, COL_TEXT, WIDTH // 2, 100)
        draw_text(self.screen, f"Xal: {self.score}", 28, COL_TEXT, WIDTH // 2, 200)
        draw_text(self.screen, f"Toplanilan: {self.collected_count}", 28, COL_TEXT, WIDTH // 2, 250)
        draw_text(self.screen, f"Alinan zede: {self.damage_taken}", 28, COL_TEXT, WIDTH // 2, 300)
        draw_text(self.screen, "Tufandag quizi ucun davm etmek ucun istenilen duymeni six.",
                  24, (200, 220, 255), WIDTH // 2, 380)


# QUIZ QUESTION BANKS – AZ dili (ə→e)

quiz_questions_baku = [
    {
        "question": "Sahdag dagi harada yerlesir?",
        "options": [
            "Xezr denezinde bir ada uzerinde",
            "Azerbaycanin şimalindaki Boyuk Qafqaz silsilesinde",
            "Cenubda duz sehra erazisinde"
        ],
        "correct_index": 1,
        "fact": "Sahdag Azerbaycanin şimalindaki Boyuk Qafqaz daglarinin bir hissesidir ve Rusiya serhedine yaxindir."
    },
    {
        "question": "Niyə qish feslinde bir cox insan Sahdaga gelir?",
        "options": [
            "Isti denizde uzmek ucun",
            "Hazirlanmish yamaclarda xizek ve snoubord surmek ucun",
            "Qayalar uzerindeki qaya rəsmlerine baxmaq ucun"
        ],
        "correct_index": 1,
        "fact": "Sahdagda muasir xizek yamaclari ve kanat yolllari var, bu da onu qish turizmi ucun basliqa merkez edir."
    },
    {
        "question": "Yay feslinde Sahdagda turistler ne ede biler?",
        "options": [
            "Yalniz otelde qalib televiziya izlemek",
            "Piyada yuruyus etmek, velosiped surmek, zip-line sinamaq ve taze dag havasindan zovq almaq",
            "Yarish masini trasinda suret sinagi etmek"
        ],
        "correct_index": 1,
        "fact": "Yayda Sahdag sərin hava, yuruyus marşrutlari ve açiq havada fealiyyetler ucun ideal mekana cevrilir."
    },
    {
        "question": "Sahdagin havasini qonaqlar ucun ozel eden nedir?",
        "options": [
            "Boyuk zavodlar sebebinden cox tozlu ve çirkli olmasi",
            "Yuksekliyin hesabina daha sərin, temiz ve ferah olmasi",
            "Havada cox guclu benzin iyi olmasi"
        ],
        "correct_index": 1,
        "fact": "Sahdag boyuk sheherlerden mesafede ve yukseklikde oldugu ucun havasi cox daha temiz ve sərin hiss olunur."
    },
    {
        "question": "Ashağidaki cumlelerden hansi Sahdag haqqinda DUZDUR?",
        "options": [
            "O, muasir otelleri ve kanat yolllari olan dag kurortudur.",
            "O, Azerbaycanin paytaxt sheheridir.",
            "O, golun ortasinda kiçik bir adadir."
        ],
        "correct_index": 0,
        "fact": "Sahdag dag kurortu kimi taninir, paytaxt sheher veya ada deyil."
    },
]

quiz_questions_sheki = [
    {
        "question": "Bazarduzu nəyə gore en cox taninir?",
        "options": [
            "Azerbaycanin en yuksek dagi olmasina gore",
            "Olkenin en boyuk çimərligi olmasina gore",
            "Azerbaycanin paytaxti olmasina gore"
        ],
        "correct_index": 0,
        "fact": "Bazarduzu zirvesi 4400 metreden yuksekliyi ile Azerbaycanin en yuksek dagidir."
    },
    {
        "question": "Bazarduzu harada yerlesir?",
        "options": [
            "Xezr denezinin ortasinda",
            "Azerbaycan ile Rusiya serhedinde, Boyuk Qafqaz dag silsilesinde",
            "Azerbaycanin merkezinde sehra erazisinde"
        ],
        "correct_index": 1,
        "fact": "Bazarduzu zirvesi Azerbaycan ile Rusiya serhedinde, Boyuk Qafqaz sirasinin bir hissesidir."
    },
    {
        "question": "Niyə Bazarduzuda alpinistler yaxşi hazirliqli olmalidir?",
        "options": [
            "Cunki zirve cox alçaq ve asan qalxishlidir",
            "Cunki yuksekliyi, soyuq havasi ve buzlu saheleri tehlukeli ola biler",
            "Cunki zirvede coxlu ticarət merkezleri var"
        ],
        "correct_index": 1,
        "fact": "Bazarduzuda yuksek alpin zona şertleri olduqundan yaxşi avadanliq, fiziki forma ve planlashdirma teleb olunur."
    },
    {
        "question": "Bazarduzu ucun en tipik fealiyyet hansi hesab olunur?",
        "options": [
            "Ciddi dag alpinismi ve bir nece gunluk trekinq",
            "Denizde uzmek ve qum qalalari tikmek",
            "Trasda mashin yarishlari kecirmek"
        ],
        "correct_index": 0,
        "fact": "Bazarduzu daha cox alpinistler ve trekinq sevənler ucun maragli istiqametdir."
    },
    {
        "question": "Zirveye qalxmasalar bele, insanlar Bazarduzu etrafinda nədən zovq ala biler?",
        "options": [
            "Yalniz qapali ticaret merkezlerinde olmaqdan",
            "Dag menzereleri, taze hava ve derelerde, otlaqlarda yuruyushlerden",
            "Tropik çimərliklerde güneshlenmeden"
        ],
        "correct_index": 0,
        "fact": "Bir cox seyahetçi yalniz Bazarduzu etrafindaki menzere ve tabiat ucun gelir, zirveye qalxmir."
    },
    {
        "question": "Niyə yerli dag kendleri Bazarduzu turizmi ucun onemlidir?",
        "options": [
            "Cunki orada bazalist eraziler, yemek, qonaqlama ve bələdçi xidmetleri var",
            "Cunki orada yalniz zavodlar fealiyyet gosterir",
            "Cunki dagin yaxinliginda hec kim yashamır"
        ],
        "correct_index": 0,
        "fact": "Dag kendleri seyahetçilerin istirahet etdiyi, qidalandigi ve marşrut hazirladigi baslama noqteeleridir."
    },
    {
        "question": "Bazarduzunun yuksek hisselerinin iqlimini hansi sozler daha yaxshi izah edir?",
        "options": [
            "Isti ve rutil, tropik meşeye oxshar",
            "Soyuq, kuləkli ve bazi vaxtlar qarli",
            "Hemishe isti çimərlik kimi"
        ],
        "correct_index": 1,
        "fact": "Yuksek alpin zonalarda hava cox zaman soyuq ve qarli ola biler, ona gore munasib geyim teleb olunur."
    },
    {
        "question": "Bazarduzu Azerbaycanin imici ucun ne ucun onemlidir?",
        "options": [
            "Olkenin yuksek daglara ve ciddi açiq hava maceralarina malik oldugunu gosterdiyi ucun",
            "Kosmik raketlerin buradan uchruldugu ucun",
            "En boyuk ticaret merkezinin orada olduguna gore"
        ],
        "correct_index": 0,
        "fact": "En yuksek zirve kimi Bazarduzu Azerbaycanin dag turizmi potensialini simvolashdirir."
    },
    {
        "question": "Bazarduzu etrafindaki turizmi daha dogru hansi variant izah edir?",
        "options": [
            "Yalniz sheher gece heyati ve klublar",
            "Tabiat temelli turizm: trekinq, kampinq, dag fotoqrafiyasi",
            "Yalniz qapali eğlence parkları"
        ],
        "correct_index": 1,
        "fact": "Bazarduzu etrafinda esas meqsed tabiatla elaqe, yuruyusler ve kamp hayatidir."
    },
    {
        "question": "Niyə Bazarduzuda bələdçiler ve tehlukesizlik qaydalari bu qeder vacibdir?",
        "options": [
            "Cunki dag exlaqi deyil",
            "Cunki şertler tez deyishe biler ve sehf addimlar tehlukeli ola biler",
            "Cunki seyahetçilere piyada gezmek gadagandir"
        ],
        "correct_index": 1,
        "fact": "Peşekar bələdçiler hava deyişikliyi, buzlanma kimi riskleri nezarete almaqda komek edir."
    },
]

quiz_questions_karabakh = [
    {
        "question": "Tufandag dag kurortu harada yerlesir?",
        "options": [
            "Azerbaycanda Qebele sheheri yaxinliginda",
            "Uzaq okeanin ortasindaki adada",
            "Bosh sehra erazisinde"
        ],
        "correct_index": 0,
        "fact": "Tufandag Qebele rayonunda yerleshen, hem yerli, hem de xarici turistlerin sevdiyi dag istiqametidir."
    },
    {
        "question": "Tufandagda esas celbedici nelerden biridir?",
        "options": [
            "Kosmik raket uchurulmasi",
            "Qonaxlari meşe ve derelerin uzerinden yukseklere aparan kanat yolllari",
            "Su altinda muzeyler"
        ],
        "correct_index": 1,
        "fact": "Tufandagdaki muasir kanat sistemleri insanlari baxish meydançalarina ve xizek zonalarina catdirir."
    },
    {
        "question": "Qish feslinde Tufandagda turistler hansi fealiyyetden zovq ala biler?",
        "options": [
            "Denezde uzmekden",
            "Hazirlanmish xizek yamaclarinda xizek ve snoubord surmekden",
            "Tropik meyveler ekmekden"
        ],
        "correct_index": 1,
        "fact": "Qishda Tufandag muxtelif seviyeli xizekçilere uygun yamaclar teqdim edir."
    },
    {
        "question": "Daha isti fesillerde insanlar Tufandagi adeten nece kesf edir?",
        "options": [
            "Yalniz otaqda qalaraq",
            "Meşelerde piyada yuruyerek, kanat yolllarina minerek ve sərin dag havasindan zovq alaraq",
            "Yeraltı tunellərdə mashin surerek"
        ],
        "correct_index": 1,
        "fact": "Qish olmasa bele, Tufandagda menzereli yuruyusler ve kanat seferleri cox meşhurdur."
    },
    {
        "question": "Niyə Tufandag aileler ucun rahatlidir?",
        "options": [
            "Cunki hec bir tehlukesiz yol yoxdur",
            "Cunki butun yas qruplari ucun yüngul cığirlar, baxish noqteeleri ve kafeler var",
            "Cunki oraya yalniz peşekar alpinistler baja bilir"
        ],
        "correct_index": 1,
        "fact": "Tufandagda hem uşaqlar, hem boyukler ucun munasib yuruyus yolları ve istirahet saheleri movcuddur."
    },
    {
        "question": "Tufandagi nece menzere ehatə edir?",
        "options": [
            "Qalin meşeler ve dag yamaclari",
            "Bitib-tukenmeyen qumluq sehra",
            "Donmush denez buzlari"
        ],
        "correct_index": 0,
        "fact": "Tufandag etrafindaki meşeler illerin muxtelif fesillerinde reng deyishir ve menzereni daha da gozel edir."
    },
    {
        "question": "Niyə Tufandagda isaretlenmish marşrutlar ve nişanlara əməl etmek lazimdir?",
        "options": [
            "Cunki bu nişanlar yalniz bezek ucundur",
            "Cunki onlar insanlara tehlukesiz yolları gostermeye ve tehlukeli sahelerden uzaq tutmaga komek edir",
            "Cunki piyada gezmek tamamile gadagandir"
        ],
        "correct_index": 1,
        "fact": "Nişanlarin gosterishine riayet etmek dag erazisinde itme ve qezalardan qorunmaga komek edir."
    },
    {
        "question": "Tufandagin yuksek stansiyalarindan gorunen menzere niyə ozel hesab olunur?",
        "options": [
            "Cunki yalniz divarlar gorunur",
            "Cunki Qebele ve etraf daglara dogru genish panoramalar acilir",
            "Cunki yalniz yeraltı magaralar gorunur"
        ],
        "correct_index": 1,
        "fact": "Bir cox seyahetçi Tufandagin yuksek noqteelerinden dag panoramalarinin fotosunu çeker."
    },
    {
        "question": "Tufandag Qebele regionunun turizmini nece destekleyir?",
        "options": [
            "Dag idmani, tabiatla elaqe ve muasir kurort xidmetleri teqdim ederek",
            "Butun yolları baglayaraq",
            "Bura gelen turistleri geri qaytararaq"
        ],
        "correct_index": 0,
        "fact": "Tufandaga gelen turistler eyni zamanda Qebeledaki diger eğlence ve istirahet obyektlerine de bas ceker."
    },
    {
        "question": "Ashağidaki cumlelerden hansi Tufandag haqqinda DUZDUR?",
        "options": [
            "O, duz ve alçaq duzluq sahesidir.",
            "O, kanat yolllari, xizek yamaclari ve meşe cığirlari olan dag kurortudur.",
            "O, iri gemilerin esas limanidir."
        ],
        "correct_index": 1,
        "fact": "Tufandag liman veya düz sahil deyil, dag turizmi ucun muasir kurortdur."
    },
]


def draw_main_menu(play_btn, settings_btn, quit_btn):
    if BG_MENU:
        screen.blit(BG_MENU, (0, 0))
    else:
        screen.fill((8, 18, 40))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 80))
    screen.blit(overlay, (0, 0))

    draw_text(screen, "AMT: Runner", 52, (255, 215, 0), WIDTH // 2, 150)
    draw_text(screen, "Azerbaycanda dag turizmi", 24,
              (200, 220, 255), WIDTH // 2, 200)

    play_btn.draw(screen)
    settings_btn.draw(screen)
    quit_btn.draw(screen)


def draw_level_select(level_buttons, back_btn):
    if BG_MENU:
        screen.blit(BG_MENU, (0, 0))
    else:
        screen.fill((15, 25, 50))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 80))
    screen.blit(overlay, (0, 0))

    draw_text(screen, "Dag seviyyesini sec", 40, (255, 215, 0), WIDTH // 2, 100)

    for btn in level_buttons:
        btn.draw(screen)
    back_btn.draw(screen)


def draw_settings_screen(
    music_slider, sfx_slider,
    lang_toggle, gfx_toggle,
    checkbox_show_keys,
    back_btn
):
    screen.fill((10, 20, 35))
    draw_text(screen, "Parametrlər", 40, (255, 215, 0), WIDTH // 2, 60)

    draw_text(screen, "Ses", 30, (200, 220, 255), 120, 120, center=False)
    draw_text(screen, "Musigi ses seviyyesi", 22, COL_TEXT, 120, 160, center=False)
    music_slider.draw(screen)
    draw_text(screen, "SFX ses seviyyesi", 22, COL_TEXT, 120, 210, center=False)
    sfx_slider.draw(screen)

    draw_text(screen, "Dil", 30, (200, 220, 255), 120, 260, center=False)
    draw_text(screen, "AZ", 22, COL_TEXT, 120, 300, center=False)
    lang_toggle.draw(screen)
    draw_text(screen, "EN", 22, COL_TEXT, 120 + 160, 300, center=False)

    draw_text(screen, "Qrafika", 30, (200, 220, 255), 550, 120, center=False)
    draw_text(screen, "Pixel rejim / HD rejim", 22, COL_TEXT, 550, 160, center=False)
    gfx_toggle.draw(screen)

    draw_text(screen, "UI idarəetme", 30, (200, 220, 255), 550, 220, center=False)
    checkbox_show_keys.draw(screen)
    draw_text(screen, "Ekranda duymeler ucun yo’l goster", 22, COL_TEXT,
              checkbox_show_keys.rect.right + 10, checkbox_show_keys.rect.y, center=False)

    draw_text(screen, "Idareetme duymeleri", 30, (200, 220, 255), 120, 360, center=False)
    lines = [
        "Tullanma: SPACE veya YUXARI OX",
        "Surushme: ASAGI OX",
        "Qaçish: avtomatik olaraq irəli scroll",
        "Menu: ESC (Game Over / Son ekranindan)"
    ]
    y = 400
    for line in lines:
        draw_text(screen, line, 22, (220, 220, 230), 120, y, center=False)
        y += 30

    back_btn.draw(screen)


def run_azerquest_runner():
    global MUSIC_VOLUME, SFX_VOLUME, LANGUAGE, GRAPHICS_MODE, SHOW_KEY_BINDINGS

    app_state = "MAIN_MENU"
    game_mode = None

    level = None
    quiz = None
    current_quiz_questions = None

    game_over_sound_played = False
    lives = 3

    switch_music("MENU")

    play_btn = Button((WIDTH // 2 - 120, 280, 240, 60), "Basla")
    settings_btn = Button((WIDTH // 2 - 120, 360, 240, 60), "Parametrler")
    quit_btn = Button((WIDTH // 2 - 120, 440, 240, 60), "Çixis")

    level_btns = [
        Button((WIDTH // 2 - 300, 200, 240, 80), "Seviye 1 – Sahdag"),
        Button((WIDTH // 2 + 60, 200, 240, 80), "Seviye 2 – Bazarduzu"),
        Button((WIDTH // 2 - 300, 320, 240, 80), "Seviye 3 – Tufandag"),
        Button((WIDTH // 2 + 60, 320, 240, 80), "Seviye 4 – Tezlikle")
    ]
    back_from_levels = Button((40, HEIGHT - 80, 180, 50), "Geri")

    music_slider = Slider(280, 160, 200, 16, value=MUSIC_VOLUME)
    sfx_slider = Slider(280, 210, 200, 16, value=SFX_VOLUME)
    lang_toggle = Toggle(200, 290, 60, 30, state=(LANGUAGE == "EN"))
    gfx_toggle = Toggle(700, 160, 60, 30, state=(GRAPHICS_MODE == "HD"))
    checkbox_show_keys = Checkbox(550, 260, 22, checked=SHOW_KEY_BINDINGS)
    back_from_settings = Button((40, HEIGHT - 80, 180, 50), "Geri")

    running = True
    while running:
        dt = clock.tick(FPS)
        events = [event for event in pygame.event.get()]
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        desired_music_mode = "MENU"
        if app_state == "GAME" and level is not None:
            if isinstance(level, ShekiLevel):
                desired_music_mode = "LEVEL_SHEKI"
            elif isinstance(level, KarabakhLevel):
                desired_music_mode = "LEVEL_KARABAKH"
            else:
                desired_music_mode = "LEVEL_BAKU"
        switch_music(desired_music_mode)

        if app_state == "MAIN_MENU":
            for e in events:
                if play_btn.is_clicked(e):
                    app_state = "LEVEL_SELECT"
                elif settings_btn.is_clicked(e):
                    app_state = "SETTINGS"
                elif quit_btn.is_clicked(e):
                    running = False

            draw_main_menu(play_btn, settings_btn, quit_btn)

        elif app_state == "LEVEL_SELECT":
            for e in events:
                if back_from_levels.is_clicked(e):
                    app_state = "MAIN_MENU"
                elif level_btns[0].is_clicked(e):
                    level = BakuLevel(screen)
                    quiz = None
                    current_quiz_questions = quiz_questions_baku
                    app_state = "GAME"
                    game_mode = "LEVEL"
                    game_over_sound_played = False
                    lives = 3
                elif level_btns[1].is_clicked(e):
                    level = ShekiLevel(screen)
                    quiz = None
                    current_quiz_questions = quiz_questions_sheki
                    app_state = "GAME"
                    game_mode = "LEVEL"
                    game_over_sound_played = False
                    lives = 3
                elif level_btns[2].is_clicked(e):
                    level = KarabakhLevel(screen)
                    quiz = None
                    current_quiz_questions = quiz_questions_karabakh
                    app_state = "GAME"
                    game_mode = "LEVEL"
                    game_over_sound_played = False
                    lives = 3

            draw_level_select(level_btns, back_from_levels)

        elif app_state == "SETTINGS":
            for e in events:
                music_slider.handle_event(e)
                sfx_slider.handle_event(e)
                lang_toggle.handle_event(e)
                gfx_toggle.handle_event(e)
                checkbox_show_keys.handle_event(e)

                if back_from_settings.is_clicked(e):
                    app_state = "MAIN_MENU"

            MUSIC_VOLUME = music_slider.value
            SFX_VOLUME = sfx_slider.value
            apply_volume_settings()

            LANGUAGE = "EN" if lang_toggle.state else "AZ"
            GRAPHICS_MODE = "HD" if gfx_toggle.state else "PIXEL"
            SHOW_KEY_BINDINGS = checkbox_show_keys.checked

            draw_settings_screen(
                music_slider, sfx_slider,
                lang_toggle, gfx_toggle,
                checkbox_show_keys,
                back_from_settings
            )

        elif app_state == "GAME":
            if game_mode == "LEVEL":
                level.update(dt, events)
                level.draw()
                draw_lives(screen, lives)

                if level.game_over and not game_over_sound_played:
                    game_over_sound_played = True
                    lives -= 1
                    if SND_GAME_OVER:
                        SND_GAME_OVER.play()
                    game_mode = "GAME_OVER"

                if level.level_finished:
                    questions = current_quiz_questions or quiz_questions_baku
                    if isinstance(level, ShekiLevel):
                        title = "Bazarduzu Quizi"
                        subtitle = "Bazarduzu barede suallara hazir ol..."
                    elif isinstance(level, KarabakhLevel):
                        title = "Tufandag Quizi"
                        subtitle = "Tufandag barede suallara hazir ol..."
                    else:
                        title = "Sahdag Quizi"
                        subtitle = "Sahdag barede suallara hazir ol..."
                    quiz = QuizScreen(screen, questions, title=title, intro_subtitle=subtitle)
                    quiz.start()
                    game_mode = "QUIZ"

            elif game_mode == "QUIZ":
                for e in events:
                    result = quiz.handle_event(e)
                    if result == "QUIZ_DONE":
                        game_mode = "END"
                quiz.update(dt)
                quiz.draw()

            elif game_mode == "END":
                screen.fill((0, 0, 0))
                draw_text(screen, "Bu seviyeni oynadigin ucun teshekkurler!", 36,
                          (255, 215, 0), WIDTH // 2, HEIGHT // 2 - 20)
                draw_text(screen, "Esas menyuya qayitmaq ucun ESC duymesini six.", 24,
                          (220, 220, 220), WIDTH // 2, HEIGHT // 2 + 20)
                for e in events:
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        app_state = "MAIN_MENU"
                        game_mode = None
                        level = None
                        quiz = None
                        game_over_sound_played = False
                        lives = 3

            elif game_mode == "GAME_OVER":
                screen.fill((10, 0, 20))
                draw_text(screen, "GAME OVER", 60, (255, 80, 80),
                          WIDTH // 2, HEIGHT // 2 - 80)

                if lives > 0:
                    draw_text(screen, f"Qalan heyat: {lives}", 30, (240, 240, 240),
                              WIDTH // 2, HEIGHT // 2 - 30)
                    draw_text(screen, "Xeritenin kenarina dushdun.", 26, (240, 240, 240),
                              WIDTH // 2, HEIGHT // 2 + 10)
                    draw_text(screen, "Seviyeni yeniden baslamaq ucun R, Esas menyuya qayitmaq ucun ESC six.",
                              22, (220, 220, 220), WIDTH // 2, HEIGHT // 2 + 50)
                else:
                    draw_text(screen, "Heyat qalmadi!", 30, (240, 240, 240),
                              WIDTH // 2, HEIGHT // 2 - 20)
                    draw_text(screen, "Esas menyuya qayitmaq ucun istənilen duymeni six.",
                              22, (220, 220, 220), WIDTH // 2, HEIGHT // 2 + 20)

                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if lives > 0:
                            if e.key == pygame.K_r:
                                if isinstance(level, ShekiLevel):
                                    level = ShekiLevel(screen)
                                    current_quiz_questions = quiz_questions_sheki
                                elif isinstance(level, KarabakhLevel):
                                    level = KarabakhLevel(screen)
                                    current_quiz_questions = quiz_questions_karabakh
                                else:
                                    level = BakuLevel(screen)
                                    current_quiz_questions = quiz_questions_baku
                                quiz = None
                                game_mode = "LEVEL"
                                game_over_sound_played = False
                            elif e.key == pygame.K_ESCAPE:
                                app_state = "MAIN_MENU"
                                game_mode = None
                                level = None
                                quiz = None
                                game_over_sound_played = False
                                lives = 3
                        else:
                            app_state = "MAIN_MENU"
                            game_mode = None
                            level = None
                            quiz = None
                            game_over_sound_played = False
                            lives = 3

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_azerquest_runner()
