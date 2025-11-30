import pygame, sys, os
import random
import play_menu_music
from azerquest_runner import run_azerquest_runner
# Pygame-i başlatmaq üçün ilkin çağırış
pygame.init()
# Ekranın ölçüləri
WIDTH, HEIGHT = 1000, 700
# Əsas oyun pəncərəsini yaratmaq
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Oyun pəncərəsinin başlığını təyin etmək
pygame.display.set_caption("AMT")
# Səs sistemini təhlükəsiz şəkildə init etmək (problem olsa, oyunu dayandırmır)
try:
    pygame.mixer.init()
except Exception:
    pass

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None
# Oyun boyunca istifadə edilən səs effektləri
sfx_step        = load_sound("sound/sfx_step.wav")          # Xəritədə addım səsi
sfx_correct     = load_sound("sound/sfx_correct.wav")       # Düzgün cavab səsi
sfx_wrong       = load_sound("sound/sfx_wrong.wav")         # Səhv cavab səsi
sfx_open_shop   = load_sound("sound/sfx_open_shop.wav")     # Mağazanın açılması səsi
sfx_open_lesson = load_sound("sound/sfx_open_lesson.wav")   # Dərs / abidə info açılması səsi
sfx_open_page   = load_sound("sound/sfx_open_page.wav")     # Səhifə / overlay açılması səsi
sfx_menu_move   = load_sound("sfx_menu_move.wav")     # Menyuda yuxarı-aşağı hərəkət səsi
sfx_menu_select = load_sound("sfx_menu_select.wav")   # Menyuda seçim səsi
# Addım səslərinin tez-tez təkrar olmaması üçün son addım vaxtı
last_step_time = 0

# ---------------------------
# Background music (menu)
# ---------------------------

# Hal-hazırda hansı musiqinin çaldığını izləmək üçün dəyişən
# "menu" və ya None ola bilər
current_music = None  # track what is playing now ("menu" or None)


def stop_music():
    """Stop any playing background music."""
    global current_music
    if not pygame.mixer.get_init():
        return
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    current_music = None
# Rəng konstantları (RGB formatında)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 120, 215)
GREEN = (34, 177, 76)
RED   = (200, 0, 0)
GRAY  = (220, 220, 220)
BG    = (10, 40, 80)
GOLD  = (255, 200, 80)
# Oyun daxilində istifadə edilən fontlar
font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 48, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

#Metni (text) maksimum simvol sayina (max_chars) uygun setirlere bolur.
#Ornek: uzun metni avtomatik olaraq bir nece setire bolmek ucun istifade olunur.
def wrap_text(text, max_chars=70):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
#Verilen setirlerin (lines) ekranda tutdugu umumilikde hundurluyu hesablayir.
#line_spacing – setirler arasindaki boslugu (piksel) gosterir.
def get_text_height(lines, line_spacing=6):
    total = 0
    for line in lines:
        label = font.render(line, True, BLACK)
        total += label.get_height() + line_spacing
    return total
#Verilen metn setir-setir (lines) verilmis sahenin (rect) icinde qutunun daxilinde cekir.
#rect = (x, y, w, h) — qutunun koordinatlari ve olculeri.
def draw_text_box(lines, rect, line_spacing=6):
    x, y, w, h = rect
    pygame.draw.rect(screen, WHITE, (x, y, w, h), border_radius=14)
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2, border_radius=14)
    ty = y + 10
    for line in lines:
        label = font.render(line, True, BLACK)
        screen.blit(label, (x + 12, ty))
        ty += label.get_height() + line_spacing

def draw_scrollable_box(lines, rect, scroll_offset, line_spacing=6):
    x, y, w, h = rect
    pygame.draw.rect(screen, WHITE, (x, y, w, h), border_radius=14)
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2, border_radius=14)
    clip = screen.get_clip()
    screen.set_clip(pygame.Rect(x+4, y+4, w-8, h-8))
    ty = y + 10 - scroll_offset
    for line in lines:
        label = font.render(line, True, BLACK)
        screen.blit(label, (x + 12, ty))
        ty += label.get_height() + line_spacing
    screen.set_clip(clip)

def load_and_scale(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    except Exception:
        return None

def draw_centered_text(text, y, font_obj, color=WHITE):
    label = font_obj.render(text, True, color)
    x = (WIDTH - label.get_width()) // 2
    screen.blit(label, (x, y))

# ---------------------------
# Transition overlay
# ---------------------------
transition_message = None
transition_start_time = 0
transition_duration = 400  

def start_transition(message):
    global transition_message, transition_start_time
    transition_message = message
    transition_start_time = pygame.time.get_ticks()
    if sfx_open_page:
        sfx_open_page.play()

def draw_transition_overlay():
    global transition_message
    if not transition_message:
        return
    now = pygame.time.get_ticks()
    elapsed = now - transition_start_time
    if elapsed >= transition_duration:
        transition_message = None
        return
    alpha = max(0, 255 - int(255 * (elapsed / transition_duration)))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha // 2))
    screen.blit(overlay, (0, 0))
    box_w, box_h = 420, 80
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(screen, (0, 0, 0, 200), (box_x, box_y, box_w, box_h), border_radius=16)
    label = font.render(transition_message, True, GOLD)
    screen.blit(label, (box_x + (box_w - label.get_width()) // 2,
                        box_y + (box_h - label.get_height()) // 2))

map_bg = load_and_scale("assets/azerbaijan_map.png", (WIDTH, HEIGHT))
if map_bg is None:
    map_bg = pygame.Surface((WIDTH, HEIGHT))
    map_bg.fill((20, 80, 140))

shop_icon = load_and_scale("assets/shop_icon.png", (48, 48))

skin_assets = [
    {"name": "Male Default Explorer", "path": "assets/character.png"},
    {"name": "Male Blue Outfit",      "path": "assets/character_blue.png"},
    {"name": "Male Green Outfit",     "path": "assets/character_green.png"},
    {"name": "Male Red Outfit",       "path": "assets/character_red.png"},
    {"name": "Female Green Traveler",  "path": "assets/character_green_traveler.png"},
]
for s in skin_assets:
    s["image"] = load_and_scale(s["path"], (50, 70))
    s["owned"] = False
skin_assets[0]["owned"] = True  

flame_img     = load_and_scale("assets/flame_towers.png",       (80, 80))
gobustan_img  = load_and_scale("assets/gobustan.png",           (80, 80))
maiden_img    = load_and_scale("maiden_tower.png",       (80, 80))
boulevard_img = load_and_scale("assets/caspian_boulevard.png",  (80, 80))
menu_bg = load_and_scale("assets/menu_bg1.jpg", (WIDTH, HEIGHT))
shahdag_img    = load_and_scale("assets/shahdag.png",    (80, 80))
bazarduzu_img  = load_and_scale("assets/bazarduzu.png",  (80, 80))
tufandag_img   = load_and_scale("assets/tufandag.png",   (80, 80))

player_pos = [120, 120]
speed = 6
score = 0

# NEW: points from Shahdag / Bazarduzu / Tufandag lessons
mountain_points = 0

state = "menu"
current_landmark = None
question_index = 0
answers_record = []  
player_skin_index = 0
player_img = skin_assets[player_skin_index]["image"]
player_color_fallback = [BLUE, GREEN, RED, (255, 165, 0)]
skin_cost = 30

adventure_intro_start_time = None

results_scroll = 0
shop_scroll_x = 0
passport_scroll = 0
timeline_scroll = 0
modern_scroll = 0
ency_scroll = 0
lesson_results_scroll = 0

current_lessons = None
current_lesson = None
current_category = ""
selected_lesson = 0
lesson_question_index = 0
lesson_answers_record = []
origin_state = "menu"

# ---------------------------
# Discount wheel data
# ---------------------------
discount_cards = []  # cards won from the wheel

wheel_options = [
    {
        "name": "10% Dağ Turu",
        "description": "10% discount: promo1. azerbaijanmountainturism.lovable.app",
        "weight": 40
    },
    {
        "name": "15% Dağ Turu",
        "description": "15% discount: promo1.5. azerbaijanmountainturism.lovable.app",
        "weight": 30
    },
    {
        "name": "20% Dağ Turu",
        "description": "20% discount: promo2. azerbaijanmountainturism.lovable.app",
        "weight": 15
    },
    {
        "name": "30% Dağ Turu",
        "description": "30% discount: promo3. azerbaijanmountainturism.lovable.app",
        "weight": 10
    },
    {
        "name": "50% Dağ Turu",
        "description": "50% discount: promo5. azerbaijanmountainturism.lovable.app",
        "weight": 5
    }
]

# wheel runtime state
wheel_selected_index = 0
wheel_spinning = False
wheel_spin_start_time = 0
wheel_spin_duration = 2500  # ms
wheel_final_index = 0
wheel_done = True  # ensure reward is only given once per spin

def choose_wheel_index():
    total = sum(opt["weight"] for opt in wheel_options)
    r = random.uniform(0, total)
    upto = 0
    for i, opt in enumerate(wheel_options):
        w = opt["weight"]
        if upto + w >= r:
            return i
        upto += w
    return len(wheel_options) - 1

def draw_wheel():
    screen.fill(BG)
    draw_centered_text("Mountain Discount Wheel", 40, title_font, GOLD)
    info_lines = [
        f"Mountain Points: {mountain_points}",
        "Her spin üçün 100 dağ balı lazımdır.",
        "Fırlandırmaq üçün SPACE ve ya ENTER düymesini basın."
    ]
    draw_text_box(info_lines, (180, 90, 640, 110))

    # determine which option is highlighted
    now = pygame.time.get_ticks()
    if wheel_spinning:
        elapsed = now - wheel_spin_start_time
        steps = len(wheel_options) * 8  # how many highlight hops
        step_time = max(40, wheel_spin_duration // steps)
        idx = int(elapsed // step_time)
        highlight_index = idx % len(wheel_options)
    else:
        highlight_index = wheel_selected_index

    start_y = 230
    box_w, box_h = 700, 60
    for i, opt in enumerate(wheel_options):
        x = (WIDTH - box_w) // 2
        y = start_y + i * (box_h + 10)
        rect = pygame.Rect(x, y, box_w, box_h)
        if i == highlight_index:
            pygame.draw.rect(screen, GOLD, rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)
            text_color = BLACK
        else:
            pygame.draw.rect(screen, (0, 0, 0, 150), rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, rect, 1, border_radius=12)
            text_color = WHITE
        label = small_font.render(
            f"{opt['name']}  (lower chance, bigger discount!)", True, text_color
        )
        screen.blit(label, (x + 12, y + (box_h - label.get_height()) // 2))

    footer = small_font.render(
        "Discount sizes are inverse to the chance of winning them.", True, (230, 230, 230)
    )
    screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 40))

menu_selected = 0
menu_items = [
    {"label": "Macera Başlayın (Xerite ve Viktorinalar)", "state": "map"},
    {"label": "AMT Runner (Adventure)",   "state": "president"},
    {"label": "Şahdağ",                        "state": "timeline"},
    {"label": "Bazardüzü",                      "state": "modern"},
    {"label": "Tufandağ",                       "state": "regions"},
    # NEW: discount wheel
    {"label": "Spin Mountain Endirim Çarxı",   "state": "wheel"},
    # Renamed from "Passport & Travel Cards"
    {"label": "Endirim kartları",                 "state": "passport"},
    {"label": "Oyundan çıxın",                      "state": "exit"},
]
menu_button_rects = []

travel_cards_unlocked = set()

# ---------------------------
# Lessons (Shahdag / Bazarduzu / Tufandag)
# ---------------------------
history_lessons = [
    (
        "Şahdağ dağı nedir?",
        "Şahdağ dağı Azerbaycanın en meşhur tebii abidelerinden biridir ve Böyük Qafqaz silsilesinin Qusar rayonu "
        "erazisinde yerleşir. Texminen 4 243 metr hündürlüyü ile ölkenin en uca zirvelerinden biridir ve möhteşem "
        "alp gözelliyinin simvolu sayılır. Şahdağ tekce dağ deyil, eyni zamanda geniş, qorunan tebii erazidir ve "
        "tenha landşaftları, derin dereleri, temiz dağ havası ve toxunulmamış tebieti ile tanınır. Onu ehate eden "
        "Şahdağ Milli Parkı Azerbaycanın en böyük milli parkıdır ve nadir bitkiler, dağ keçileri ve çoxsaylı quş "
        "növleri daxil olmaqla zengin bioloji müxtelifliye malikdir. Dağ, Qafqazın gücünü tehlükesiz ve elçatan "
        "şekilde yaşamaq isteyen tebiet severleri, piyada gezinti heveskarları, fotoqraflar ve seyahetçileri celb edir. "
        "Bu gün Şahdağ hem de müasir infrastrukturla techiz olunmuş kurortu ile meşhurdur; burada xizek yamacları, "
        "yürüş marşrutları, oteller, macera parkları ve aileler, elce de turistler üçün ilboyu müxtelif fealiyyetler "
        "mövcuddur.",
        [
            {
                "q": "Şahdağ dağı harada yerleşir?",
                "options": ["Qusar rayonu", "Bakı merkezi", "Naxçıvan", "Qarabağ düzenliyi"],
                "answer": 0
            },
            {
                "q": "Şahdağın texmini hündürlüyü ne qederdir?",
                "options": ["4 243 metr", "800 metr", "12 000 metr", "150 metr"],
                "answer": 0
            },
            {
                "q": "Şahdağ hansı dağ silsilesinin terkibine daxildir?",
                "options": ["Böyük Qafqaz", "Himalaylar", "And dağları", "Alplar"],
                "answer": 0
            },
            {
                "q": "Dağı hansı milli park ehate edir?",
                "options": ["Şahdağ Milli Parkı", "Qobustan Qoruğu", "Yelloustoun", "Everest Baza Parkı"],
                "answer": 0
            },
            {
                "q": "Şahdağ ne ile tanınır?",
                "options": [
                    "Gözäl tebieti ve müasir kurort fealiyyetleri ile",
                    "Sehraya çevrilmesi ile",
                    "Göydelenleri ile",
                    "Suyun altında olması ile"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Şahdağın tarixi",
        "Şahdağ dağı esrler boyu hem medeni, hem de coğrafi baxımdan böyük ehemiyyet daşıyıb. Tarixen bu erazi "
        "qedim dağ tayfaları, çoban icmaları ve Qafqaz silsilesi boyu heräket eden seyyahlar üçün tebii keçid "
        "rolunu oynayıb. “Şahdağ” adı “Kral dağ” menasını verir ve onun landşaftdakı üstünlüyünü, möhteşem "
        "görünüşünü eks etdirir. Yerli icmalar üçün Şahdağ tekce tebii maneä deyil, hem de iqlimi, kend tesärrüfatını "
        "ve etraf kendlerin hayatını formalaşdıran qoruyucu bir dağ sayılıb. Arxeoloji tapıntılar gösterir ki, "
        "Şahdağ etrafındakı yüksek yaylaqlar qedim dövrlerden beri mal-qaranın mövsümi köçürülmesi üçün istifade "
        "olunmuş ve bu, Azerbaycanın enenevi köçeri maldarlıq medeniyyetinin bir hissesini teşkil etmişdir. Sovet "
        "dövründe bu bölgä unikal qaya süxurları ve geoloji yaşı sebebinden alpinistler ve geoloqlar terefinden "
        "araşdırılıb. Müasir dövrde ise 2006-cı ilda Şahdağ Milli Parkının yaradılması ile dağın ehemiyyeti daha da "
        "artıb; bu park dağın ekosistemlerini qorumaqla yanaşı, erazini populyar turizm ve tedqiqat mekanına "
        "çevir­mişdir.",
        [
            {
                "q": "'Şahdağ' adı ne demekdir?",
                "options": ["Kral dağ", "Qızıl çay", "Qar sehrası", "Küläk vadisi"],
                "answer": 0
            },
            {
                "q": "Qedim dövrlerde Şahdağın yüksek yaylaqlarından kimler istifade edirdi?",
                "options": ["Çoban icmaları", "Kosmonavtlar", "Quldurlar", "Afrikadan qedim fermerler"],
                "answer": 0
            },
            {
                "q": "Şahdağ Milli Parkı ne vaxt yaradılıb?",
                "options": ["2006", "1950", "1800", "2020"],
                "answer": 0
            },
            {
                "q": "Sovet dövründe Şahdağı kimler daha çox öyrenirdi?",
                "options": ["Alpinistler ve geoloqlar", "Deb dizaynerleri", "Balıqçılar", "Yalnız astronomlar"],
                "answer": 0
            },
            {
                "q": "Şahdağ tarixen ne kimi rol oynayıb?",
                "options": [
                    "Yerlı hayat üçün tebii keçid ve qoruyucu kimi",
                    "Tropik meşe kimi",
                    "Sehralı ada kimi",
                    "Qızıl medeni kimi"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Niye Şahdağa getmelisiniz?",
        "Şahdağ macera, istirahet ve ailevi seyahet üçün Azerbaycanın en celbedici istiqametlerinden biridir. "
        "Ziyaretçiler onun dörd mövsüm davam eden gözelliyine göre buraya gelirler: qışda qarlı yamaclar, "
        "yazda yaşıl meşeler ve çemenlikler, yayda serin hava, payızda ise möhteşem reng çalarları. Siz xizek "
        "sürmäyi, snoubord etmeyi, dağ yürüşlerini, kanat yolunu, at turlarını, paraleytingi ve ya sadəcə tebietde "
        "gezmäyi sevirsinizse, Şahdağ her yaş üçün uygun tecrübeler teklif edir. Kurort müasir, temiz ve tehlükesizdir; "
        "burada oteller, kafeler, avadanlıq icaresi ve telim keçmiş meşqçiler fealiyyet gösterir. Aileler üçün "
        "Şahdağda uşaqlar üçün parklar, qarda oyun saheleri, macera zonaları ve başlayanı üçün yüngül yamaclar var. "
        "Tebiet fotoqrafları ve piyada seyahet heveskarları üçün bu landşaftlar sonsuz foto ve keşf imkanı yaradır. "
        "Mekan hem de çox elçatandır – Bakıdan maşınla bir neçe saatlıq mesafede yerleşir. En esası ise, Şahdağ "
        "ziyaretçilere başqa heç yerdä asan tapa bilmeyecekleri bir sakitlik ve teravet hissi bexş edir ve şehir "
        "heyatından qaçmaq üçün ideal mekandır.",
        [
            {
                "q": "Şahdağ esasen neye göre meşhurdur?",
                "options": [
                    "İlboyu davam eden fealiyyetlere göre",
                    "Derin deniz dalışı üçün",
                    "Şeher gece heyatı üçün",
                    "Sehra düşergeleri üçün"
                ],
                "answer": 0
            },
            {
                "q": "Ziyaretçiler Şahdağda hansı fealiyyetlerden zövq ala bilerler?",
                "options": ["Xizek sürme ve yürüşler", "Yalnız sörfinq", "Cenge­llik dırmanışı", "Skuba dayvinq"],
                "answer": 0
            },
            {
                "q": "Aileler Şahdağı niye sevirler?",
                "options": [
                    "Uşaq üçün uygun parklar ve tehlükesiz eraziler olduğu üçün",
                    "Çünki heç bir şerait yoxdur",
                    "Çünki tamami­le pulsuzdur",
                    "Çünki her zaman çox istidir"
                ],
                "answer": 0
            },
            {
                "q": "Şahdağ harada yerleşir?",
                "options": [
                    "Bakıdan bir neçe saatlıq mesafede",
                    "Bir­başa Bakı şeherinin içinde",
                    "Bir adada",
                    "Başqa ölkede"
                ],
                "answer": 0
            },
            {
                "q": "Şahdağ ziyaretçilere hansı hissi bexş edir?",
                "options": ["Sakitlik ve teravet", "Ses-küylü şeher heyatı", "Stress", "Heddinden artıq isti hava"],
                "answer": 0
            }
        ]
    ),
    (
        "Şahdağ ne derecede müsbät ve faydalıdır?",
        "Şahdağ Azerbaycanın en müsbät istirahet mekanlarından biri hesab olunur, çünki tebii gözellik, temiz hava, "
        "aktiv heyat terzi imkanları ve müasir turizm xidmetlerini bir yerdä birleşdirir. Etraf mühit yaxşı "
        "qorunur ve milli park sayesinde vehşi tebiet, meşeler ve dağ ekosistemleri mühafize altında saxlanılır. "
        "Ziyaretçiler tez-tez deyirler ki, Şahdağ onlara hem psixoloji, hem de fiziki baxımdan yenilenmeye kömek edir: "
        "temiz dağ havası sağlamlığı yaxşılaşdırır, xizek sürme ve piyada yürüş kimi fiziki fealiyyetler ise sağlam "
        "heyat terzini destekleyir. Erazi semimi yerli insanlar, yüksek seviyeli xidmət ve tebiete hörmet eden "
        "düşünülmüş infrastruktur ile tanınır. Oteller landşaftla uyğunlaşdırılaraq inşa olunub ve ekoloji cehetden "
        "dost yanaşmalar teşviq edilir. Şahdağ hemçinin aileler üçün tehlükesiz mekandır, çünki burada peşekar "
        "xilasedme komandaları ve telim keçmiş heyet fealiyyet gösterir. Ümümilikde, Şahdağ Azerbaycanın dağ "
        "turizminin en yaxşı cehetlerini eks etdiren, parlaq, müsbät ve ruhlandırıcı bir istiqamet kimi seçilir.",
        [
            {
                "q": "Şahdağ niye müsbät istirahet mekany hesab olunur?",
                "options": [
                    "Temiz tebiet ve müasir xidmətlere göre",
                    "Güclü çirklänmä olduğu üçün",
                    "Fealiyyet imkanları olmadığı üçün",
                    "Zavodlarla dolu olduğu üçün"
                ],
                "answer": 0
            },
            {
                "q": "Ziyaretçiler Şahdağ barede hansı faydanı tez-tez qeyd edirler?",
                "options": [
                    "Psixi ve fiziki yenilenme",
                    "Artan stress",
                    "Daha çox ses-küy",
                    "Daimi darıxma"
                ],
                "answer": 0
            },
            {
                "q": "Şahdağın etraf mühiti kim terefinden qorunur?",
                "options": ["Şahdağ Milli Parkı", "Ticaret merkezi", "Zavod", "Heç bir qurum"],
                "answer": 0
            },
            {
                "q": "Şahdağda hansı cür yanaşmalar teşviq edilir?",
                "options": ["Ekoloji cehetden temiz yanaşmalar", "Çirklendirici üsullar", "Zibil yandırma", "Ses-küylü fealiyyetler"],
                "answer": 0
            },
            {
                "q": "Şahdağın tehlükesiz sayılmasının eses sebebi nedir?",
                "options": [
                    "Peşekar xilasedme komandaları ve telim keçmiş heyet",
                    "Ümümiyyetle heç bir heyetin olmaması",
                    "Cenge­llikde yerleşmesi",
                    "Heç bir xidmətin olmaması"
                ],
                "answer": 0
            }
        ]
    )
]

modern_lessons = [
    (
        "Bazardüzü dağı nedir?",
        "Bazardüzü dağı Azerbaycanın en yüksek zirvesidir ve deniz seviyyesinden texminen 4 466 metr yüksäklikde "
        "yerleşir. O, Böyük Qafqaz silsilesinin Azerbaycanla Rusiya Federasiyasının Dağıstan bölgäsi arasındakı serhed "
        "hissesinde yerleşir. “Bazardüzü” adı çox vaxt “bazar meydanı” ve ya “bazar düzenliyi” kimi tercüme olunur ve "
        "bunun, etraf vadilerde yerleşen qedim ticaret yolları ve yığıncaq yerleri ile bağlı olduğu düşünülür. "
        "Dağın yamaclarından ve zirvesinden sert qayalı silsileler, derin dereler ve her iki ölkäye geniş menzäre "
        "açılır. İqlim alp tipli olduğuna göre dağın yuxarı hisses­i ilin böyük hissesinde qarla örtülü olur. "
        "Hündürlüyü ve yerleşdiyi mövqe sebebile Bazardüzü yerli hava şeraitine ve su ehtiyatlarına mühüm tesir "
        "gösterir. O, Şahdağ kimi xizek kurortu deyil, daha çox tecrübeli yürüşçüler, alpinistler, tebiet fotoqrafları "
        "ve Azerbaycanın “damında” dayanmaq isteyen insanlar üçün celbedici olan vehşi, tebii yüksek dağ mühitidir.",
        [
            {
                "q": "Bazardüzü dağı Azerbaycan üçün ne ile xüsusidir?",
                "options": [
                    "Ölkenin en yüksek zirvesi olması ile",
                    "En alçaq nöqte olması ile",
                    "Vulkan olması ile",
                    "Deniz altında yerleşmesi ile"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzü hansı serheddä yerleşir?",
                "options": ["Azerbaycan–Dağıstan (Rusiya) serhedi", "Azerbaycan–Gürcüstan serhedi", "Azerbaycan–Türkiyä serhedi", "Azerbaycan–İran serhedi"],
                "answer": 0
            },
            {
                "q": "Bazardüzünün texmini hündürlüyü ne qederdir?",
                "options": ["4 466 metr", "400 metr", "14 metr", "10 000 metr"],
                "answer": 0
            },
            {
                "q": "Bazardüzü etrafındakı landşaftı ne xarakterize edir?",
                "options": [
                    "Qayalı silsileler ve derin dereler",
                    "Yalnız qumlu çimerlikler",
                    "Tropik cenge­llik",
                    "Tamami­le düz sehralar"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzünü nece tesvir etmek daha düzgündür?",
                "options": [
                    "Vehşi yüksek dağ erazisi kimi",
                    "Meşgul şeher merkezi kimi",
                    "Sualtı mağara kimi",
                    "Sehradakı vahe kimi"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Bazardüzü dağının tarixi",
        "Bazardüzü dağı etrafındakı bölgä esrler boyu Qafqazın medeni ve coğrafi tarixinin bir hisses­i olmuşdur. "
        "Yerli dağ xalqları, çobanlar ve tacirler yaxınlıqdakı vadilerden ve aşırımlardan kendler ve bazarlar arasında "
        "marşrut kimi istifade ediblär. Digär zirvelerden xeyli uca olan bu dağ, istiqamet te­yini ve serhedlerin "
        "müäyyenleşdirilmesi üçün tebii bir işare nöqtesi rolunu oynayıb. XIX ve XX esrlerde Qafqaz daha deqiq "
        "xeriteleşdirildikce, Bazardüzü coğrafiyaçılar ve geodeziya mütexessisleri üçün mühüm istinad nöqtesine "
        "çevirildi. Onun Azerbaycanın en yüksek nöqtesi olduğu müäyyen edildi ve bu dağ ölke üçün simvolik mena "
        "kesb etdi. Zaman keçdikce müxtelif regionlardan alpinistler ve dağçı qrupları zirveye yürüşler teşkil "
        "etmeye başladılar ve Bazardüzü Qafqaz alpinizmi üçün hörmet edilen hedefe çevrildi. Bu gün onun tarixi hem "
        "enenevi köçeri maldarlıq heyatı, hem de müasir araşdırma ve dağ turizmi ile sıx bağlıdır ve qedim yaşayış "
        "terzi ile yeni macera medeniyyeti arasında körpü rolunu oynayır.",
        [
            {
                "q": "Bazardüzü etrafındakı vadilerden enenevi olaraq kimler istifade edirdi?",
                "options": [
                    "Yerli dağ xalqları ve çobanlar",
                    "Derin deniz balıqçıları",
                    "Sehra köçerileri",
                    "Qütb tedqiqatçıları"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzü qedim seyyahlar üçün hansı rol oynayırdı?",
                "options": [
                    "Tebii istiqamet ve oriyentir nöqtesi kimi",
                    "Ticaret merkezi kimi",
                    "Zavod kimi",
                    "Hava limanı kimi"
                ],
                "answer": 0
            },
            {
                "q": "Qafqaz, o cümleden Bazardüzü, hansı esrlerde daha deqiq xeriteleşdirilmişdir?",
                "options": ["XIX ve XX esrlerde", "V ve VI esrlerde", "I ve II esrlerde", "XXX ve XXXI esrlerde"],
                "answer": 0
            },
            {
                "q": "Bazardüzü Azerbaycan üçün niye simvolik mena daşıyır?",
                "options": [
                    "Çünki ölkenin en yüksek nöqtesidir",
                    "En isti çimerliyi olduğuna göre",
                    "En böyük şeher olduğuna göre",
                    "Meşhur vulkan olduğuna göre"
                ],
                "answer": 0
            },
            {
                "q": "Müasir dövrde Bazardüzü ile hansı fealiyyet sıx bağlıdır?",
                "options": [
                    "Alpinist yürüşleri ve ekspedisiyalar",
                    "Kosmik turizm",
                    "Sualtı dalğıc turları",
                    "Formula 1 yarışı"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Niye Bazardüzü dağını ziyaret etmälisiniz?",
        "Bazardüzü dağını ziyaret etmek ciddi tebiet, yüksek hündürlüklär ve heqiqi macera seven insanlar üçün "
        "unikal tecrübädir. Meşgul kurortlardan ferqli olaraq, Bazardüzü sakit, vehşi landşaftlar, tam temiz hava ve "
        "möhteşem menzäreler teklif edir. Yürüşçüler ve alpinistler Azerbaycanın en yüksek nöqtesine çatmaq üçün "
        "buraya gelir ve bu, yaxşı fiziki hazırlıq, planlaşdırma ve adeten tecrübeli beledçi teleb edir. Yol boyu "
        "mövsümden asılı olaraq ziyaretçiler alp çemenliklerinden, qayalı cığırlarla ve bezen de qar saheleri ile "
        "keçirler. Erazi tebiet fotoqrafiyası, quş müşahidesi ve yüksek dağ ekosistemleri ile tanış olmaq üçün "
        "ideal mekandır. Hemçinin yaxın kendlerde yaşayan yerli icmalarla tanış olmaq, onların qonaqperverliyini "
        "ve enenevi heyat terzini görmäk mümkündür. Region kommersiya baxımından daha az inkişaf etdiyine göre "
        "daha orijinal ve toxunulmamış görünür. Ölkenin en yüksek zirvesinde dayanmaq ve kenara çıxmış, menalı bir "
        "seyahet yaşamaq isteyenler üçün Bazardüzü mükemmel istiqametdir.",
        [
            {
                "q": "Bazardüzü daha çox hansı tip seyahetçiler üçün uygundur?",
                "options": [
                    "Macera ve tebiet sevenler üçün",
                    "Şoppinq merkezi axtaranlar üçün",
                    "Çimerlik eylencesi isteyenler üçün",
                    "Attraksion parkı sevenler üçün"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzünü ziyaret etmäyin eses sebeblerinden biri nedir?",
                "options": [
                    "Azerbaycanın en yüksek nöqtesine çatmaq",
                    "İsti denizde üzmäk",
                    "Zooparka getmäk",
                    "Metro ile gezmäk"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzüye qalxmaq üçün adeten ne tövsiyä olunur?",
                "options": [
                    "Yaxşı fiziki hazırlıq ve beledçi",
                    "Ümümiyyetle heç bir avadanlıq",
                    "Yalnız şap-şap (deniz çekmesi)",
                    "Sörf lövhesi"
                ],
                "answer": 0
            },
            {
                "q": "Ziyaretçiler Bazardüzü etrafında nelerden zövq ala bilerler?",
                "options": [
                    "Alp çemenlikleri ve qayalı cığırlar",
                    "Koral rifler",
                    "Nehenq göydelenler",
                    "Yalnız qum tepeleri"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzü etrafı nece tesvir edilir?",
                "options": [
                    "Daha orijinal ve az kommersiya tesirli",
                    "Alver merkezleri ile dolu, izdihamlı",
                    "Tamamile süni",
                    "Nehenq eylence parkı kimi"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Bazardüzü dağı ne derecede müsbät ve faydalıdır?",
        "Bazardüzü dağı çox vaxt hem fiziki sınag, hem tebietin saflığı, hem de emosional memnuniyyeti birleşdirdiyi "
        "üçün çox müsbät ve ilhamverici mekan kimi tesvir olunur. Dağa yaxınlaşmaq ve ya zirveye qalxmaq insanlara "
        "stressden, texnologiyadan ve gur şeher heyatından uzaqlaşmağa kömek edir. Temiz, serin hava ve geniş açıq "
        "menzäreler zehni aydınlıq ve rahatlanma hissini güclendirir. Bir çox ziyaretçi üçün yürüş ve qalxma prosesi "
        "özüne inamı, intizamı ve xüsusen de qrup halinde seyahet ederkän komanda işini inkişaf etdirir. Erazi ekoloji "
        "baxımdan da önemlidir; o, temiz su ehtiyatlarının formalaşmasına, bioloji müxtelifliye ve regionun iqlim "
        "tarazlığına töhfe verir. Mesuliyyetli turizm burada cığırları qorumaq, zibil atmamaq ve hessas dağ florasını "
        "mühafize etmek demekdir. Ziyaretçiler qaydalara emel etdikde, Bazardüzü hem tebiet, hem de insanlar üçün "
        "temiz ve ruhlandırıcı mühit olaraq qalır. Bu menada dağ sağlam heyat terzinin, etraf mühitä hörmetin ve "
        "Azerbaycanın tebii irsi üzärinde qürurun remzine çevrilir.",
        [
            {
                "q": "İnsanlar Bazardüzünü niye ilhamverici hesab edirler?",
                "options": [
                    "Fiziki sınag ve tebietin saflığını birleşdirdiyine göre",
                    "Çoxlu ticaret merkezleri olduğuna göre",
                    "Ses-küylü klublarla dolu olduğuna göre",
                    "Plastik tullantılarla örtülü olduğuna göre"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzü ziyaretçilerin düşüncesine nece tesir ede biler?",
                "options": [
                    "Daha çox aydınlıq ve rahatlanma hissi vere biler",
                    "Daha çox ses-küy ve stress yaradar",
                    "Daimi çaşqınlıq yaradar",
                    "Daimi darıxma hissi yaradar"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzüye yürüş etmek hansı şəxsi keyfiyyetleri güclendire biler?",
                "options": [
                    "Özüne inam ve komanda işi",
                    "Yalnız video oyun bacarıqları",
                    "Yol heräketinde maşın sürmek",
                    "Televizora baxmaq"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzüde mesuliyyetli turizm ne demekdir?",
                "options": [
                    "Zibil atmamaq ve tebietä hörmetle yanaşmaq",
                    "Qayaların üzärine yazı yazmaq",
                    "Suyu israf etmek",
                    "Heyvanlara qışqırmaq"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzü neyin remzi kimi qebul edile biler?",
                "options": [
                    "Sağlam heyat terzi ve tebii irs",
                    "Ağır senaye ve çirklänmä",
                    "Fast-food medeniyyeti",
                    "Tam urbanizasiya"
                ],
                "answer": 0
            }
        ]
    )
]

region_lessons = [
    (
        "Tufandağ dağı nedir?",
        "Tufandağ dağı Azerbaycanın en populyar dağ istiqametlerinden biridir ve Böyük Qafqaz silsilesinde, Qebele "
        "şeherinin yaxınlığında yerleşir. Bu dağ hem tebii gözelliyi, hem de onun yamaclarında fealiyyet gösteren "
        "müasir Tufandağ Qış–Yay Turizm Kompleksi ile tanınır. Erazi xüsusile qış aylarında meşelik tepeleri, derin "
        "vadileri ve qarlı zirveleri ile tesir bağışlayır. Tufandağ silsilesinde bəzi zirveler texminen dörd min metre "
        "qeder yükselse de, kurort daha elçatan yüksäkliklerde yerleşdiyinden aileler ve ilk defä dağa gedänler üçün "
        "uyğundur. Tufandağ, xüsusile, vadilerin üzärinden geçen kanat yolları (kanatka) ile meşhurdur ve bu kanat "
        "yolları her mövsümde panoramik menzäreler teklif edir. Qışda insanlar buraya xizek ve snoubord üçün, yayda ise "
        "piyada gezintiler, piknikler ve temiz dağ havası üçün gelirler. Kurort hem inkişaf etmiş infrastruktur, hem de "
        "vehşi tebiet görüntüsü ile Tufandağı Azerbaycanın yüksek dağ landşaftlarına rahat giriş qapısına çevirir.",
        [
            {
                "q": "Tufandağ dağı Azerbaycanın hansı şeherinin yaxınlığında yerleşir?",
                "options": ["Qebele", "Bakı", "Gence", "Lenkeran"],
                "answer": 0
            },
            {
                "q": "Tufandağ hansı dağ silsilesinin terkibine daxildir?",
                "options": ["Böyük Qafqaz", "Himalaylar", "And dağları", "Alplar"],
                "answer": 0
            },
            {
                "q": "Tufandağ esasen ne ile tanınır?",
                "options": [
                    "Müasir qış–yay turizm kompleksi ile",
                    "Nehenq sehrası ile",
                    "Senaye limanı ile",
                    "Yeraltı mağara şeheri ile"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağda ziyaretçilere geniş panoramik menzäreni ne temin edir?",
                "options": ["Kanat yolları", "Sualtı qayıklar", "Metro qatarları", "Yalnız hava şarları"],
                "answer": 0
            },
            {
                "q": "Qışda insanlar Tufandağı esasen neye göre ziyaret edirler?",
                "options": ["Xizek ve snoubord üçün", "Denizde üzmek üçün", "Zooparka getmek üçün", "Tropik meşeni araşdırmaq üçün"],
                "answer": 0
            }
        ]
    ),
    (
        "Tufandağ dağının tarixi",
        "Tufandağ bölgäsi uzun müddet Qebele ve etraf kendlerde yaşayan insanlar üçün gündelik hayatın bir hissesi "
        "olub. Esrler boyu yerli kendliler ve çobanlar etraf yamacları ve yüksek yaylaqları heyvan otarmaq, vadilerde "
        "mehsul yetişdirmek ve meşeden müxtelif nemetler toplamaq üçün istifade ediblär. Dağ yamacları qedim ticaret "
        "yolları üzärinde yerleşen ve bir zamanlar mühüm şeher olan Qedim Qebelenin tebii fonunu teşkil edib. Azerbaycanda "
        "turizm XX esrin sonları ve XXI esrin evvellerinde inkişaf etmeye başlayanda, Tufandağın qış idmanı ve dağ "
        "istiraheti üçün potensialı daha aydın nezere çarpdı. Bu meqsedle kanat yollarına, xizek traslarına ve otellere "
        "investisiyalar qoyuldu ve neticede erazi ilboyu ziyaret olunan turizm merkezine çevrildi, eyni zamanda yerli "
        "enenelerle elaqesini de qoruyub saxladı. Bu gün Tufandağ hem enenevi dağ hayatını, hem de rahatlıq, idman ve "
        "dayanıqlı turizm üçün nezerdä tutulmuş müasir infrastrukturu özünde birleşdiren bir mekan kimi qebul edilir.",
        [
            {
                "q": "Tufandağ erazisinden yerli sakinler enenevi olaraq nece istifade edirdiler?",
                "options": [
                    "Heyvan otarmaq ve kend hayatı üçün",
                    "Böyük hava limanı kimi",
                    "Neft yatagı kimi",
                    "Sehrada düşerge kimi"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağ ile tarixi elaqesi olan yaxın şeher hansıdır?",
                "options": ["Qebele", "Sumqayıt", "Naxçıvan", "Şirvan"],
                "answer": 0
            },
            {
                "q": "Tufandağ ne vaxt turizm ve xizek menteqesi kimi inkişaf etmeye başlamışdır?",
                "options": ["XX esrin sonu ve XXI esrin evvellerinde", "Qedim Roma dövründe", "Daş dövründe", "1500-cü ilde"],
                "answer": 0
            },
            {
                "q": "Tufandağın kurorta çevrilmesinde hansı infrastruktur eses rol oynayıb?",
                "options": [
                    "Kanat yolları ve xizek trasları",
                    "Sualtı qayıklar",
                    "Kosmik limanlar",
                    "Yalnız yeraltı tuneller"
                ],
                "answer": 0
            },
            {
                "q": "Bu gün Tufandağ neyi birleşdirir?",
                "options": [
                    "Enenevi dağ hayatını ve müasir turizmi",
                    "Yalnız ağır senayeni",
                    "Yalnız kend tesärrüfatını, heç bir turist olmadan",
                    "Yalnız sehrada safari turlarını"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Niye Tufandağ dağını ziyaret etmälisiniz?",
        "Tufandağ dağı hem rahatlıq, hem de macera isteyen ziyaretçiler üçün ela seçimdir. Qış mövsümünde "
        "kurort müxtelif çetinlik derecesine malik xizek yamacları, peşekar meşqçiler ve avadanlıq icaresi ile "
        "techiz olunur ve bu da onu yeni başlayanlar, uşaqlar ve tecrübeli xizekçiler üçün elverişli edir. Yay ve "
        "payızda ise hemin yamaclar temiz hava, meşeler ve Qebele üzerine açılan geniş menzärelerle yürüş ve gezinti "
        "marşrutlarına çevrilir. Kanat yolları bütün mövsümlerde eses celbedici xüsusiyyetlerden biridir, çünki "
        "qonaqlara menzäreni yuxarıdan, müxtelif reng çalarları ile izlemeye imkan verir. Oteller, kafeler ve "
        "eylence zonaları dağın eteyinde yerleşdiyinden idman, tebiet ve istiraheti asanlıqla birleşdirmek mümkündür. "
        "Aileler uşaqlar üçün nezerdä tutulmuş fealiyyetlerden zövq ala, cütlükler ve dost qrupları ise daha çetin "
        "marşrutları keşf ede bilerler. Eses şeherlerden yolla rahat çatmaq mümkün olduğu üçün Tufandağ heftäsonu "
        "ve bayram tetilleri üçün praktiki ve celbedici istiqametdir.",
        [
            {
                "q": "Tufandağda qış mövsümünde hansı fealiyyetlerden zövq almaq olar?",
                "options": [
                    "Xizek sürme ve snoubord",
                    "Okeanda üzmek",
                    "Sehrada sörfinq",
                    "Köpäkbalığı ile dalğıc"
                ],
                "answer": 0
            },
            {
                "q": "Yay ve payızda xizek yamaclarına ne baş verir?",
                "options": [
                    "Onlar yürüş ve gezinti marşrutlarına çevrilir",
                    "Tamamilä yoxa çıxır",
                    "Zavodlara çevrilir",
                    "Deniz suyu ile dolur"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağda kanat yolları niye meşhurdur?",
                "options": [
                    "Gözäl hava menzäreleri teklif etdiyi üçün",
                    "Suyun altına endiyi üçün",
                    "İnsanları başqa ölkeye apardığı üçün",
                    "Alış-veriş üçün istifade edildiyi üçün"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağ xüsusile kimler üçün uygundur?",
                "options": [
                    "Aileler, yeni başlayanlar ve tecrübeli xizekçiler üçün",
                    "Yalnız kosmonavtlar üçün",
                    "Yalnız denizçiler üçün",
                    "Yalnız fermerler üçün"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağa çatmaq ne derecede asandır?",
                "options": [
                    "Eses şeherlerden avtomobil yolu ile elçatandır",
                    "Yalnız kosmik gemi ile",
                    "Yalnız sualtı qayıkla",
                    "Ümümiyyetle çatmaq mümkün deyil"
                ],
                "answer": 0
            }
        ]
    ),
    (
        "Tufandağ dağı ne derecede müsbät ve faydalıdır?",
        "Tufandağ dağı tez-tez son derecede müsbät mekan kimi tesvir olunur, çünki burada temiz hava, aktiv heyat terzi "
        "imkanları ve müxtelif yaş qrupları üçün tehlükesiz mühit mövcuddur. Burada vaxt keçirmek insanlara gündelik "
        "stressden ve texnologiyadan uzaqlaşmağa kömek edir, hereket, temiz hava ve gözäl dağ menzäreleri ile eväzlenir. "
        "Xizek sürme, snoubord, dağ yürüşü ve sade gezinti kimi fiziki fealiyyetler hem bedeni, hem de zehni daha "
        "sağlam edir. Kurort tehlükesizlik nezere alınaraq layihelendiril­ib: traslar işarelenib, meşqçiler telimlidir "
        "ve xilasedme xidmətleri mövcuddur. Eyni zamanda, etraf tebiet tikililer ve marşrutların diq­qetle planlaşdırılması "
        "sayesinde qorunur. Turistler eses ekoloji qaydalara – zibil atmamaq ve işarelenmiş cığırlar üzrä hereket etmek "
        "kimi – emel etdikde, Tufandağ temiz ve qonaqperver olaraq qalır. Bu baxımdan dağ, sağlam istirahetin, tebietä "
        "hörmetin ve Azerbaycanda müasir, aile yönümlü dağ turizminin remzi kimi çıxış edir.",
        [
            {
                "q": "Tufandağ niye müsbät istirahet yeri hesab olunur?",
                "options": [
                    "Temiz hava ve aktiv heyat terzi imkanlarına göre",
                    "Ağır neqliyyat ve çirklänmä olduğuna göre",
                    "Heç bir fealiyyet olmadığı üçün",
                    "Daimi ses-küy ve tüstü olduğuna göre"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağda hansı fealiyyetler sağlam heyat terzini destekleyir?",
                "options": [
                    "Xizek sürme, dağ yürüşü ve gezinti",
                    "Yalnız iceride oturmaq",
                    "Gün boyu televizora baxmaq",
                    "Tıxacda maşın sürmek"
                ],
                "answer": 0
            },
            {
                "q": "Kurort ziyaretçilərin tehlükesizliyini nece temin edir?",
                "options": [
                    "İşarelenmiş traslar ve telim keçmiş heyet vasitəsilə",
                    "Heç bir qayda tetbiq etmeyerek",
                    "Ümümiyyetle heç bir heyet saxlamayaraq",
                    "Yalnız tehlükeli, işaresiz eraziler yaradaraq"
                ],
                "answer": 0
            },
            {
                "q": "Turistler Tufandağın temiz qalması üçün ne etmelidirlər?",
                "options": [
                    "Zibil atmamaq ve tebietä hörmetle yanaşmaq",
                    "Zibili her yere atmaq",
                    "Ağacları eylence üçün sındırmaq",
                    "Vehşi heyvanlara zererli qida vermek"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağı neyin remzi kimi görmäk olar?",
                "options": [
                    "Sağlam, aile yönümlü dağ turizmi kimi",
                    "Terk edilmiş senaye zonas­ı kimi",
                    "Sehrada sağ qalma yeri kimi",
                    "İzdihamlı şeher bazarları kimi"
                ],
                "answer": 0
            }
        ]
    )
]

# (encyclopedia_lessons, language_phrases, landmarks etc. unchanged – keeping as in your code)
# For brevity, I’m not re-commenting them; only functional changes below.

encyclopedia_lessons = { ... }  # KEEP YOUR EXISTING CONTENT HERE UNCHANGED
ency_selected_category = None

landmarks = {
    "Shahdag Mountain": {
        "pos": (760, 220),
        "image": shahdag_img,
        "info": [
            "Şahdag dağı Azerbaycanın en meşhur istiqametlerinden biridir ve gösterir ki, tebiet ile turizm "
            "harmoniyada birge mövcud ola biler. Böyük Qafqaz silsilesinde, Qusar regionunda yerleşen bu dağ "
            "meşelerin, derin vadilerin ve qayalı qayalıqlarin üzerine qalxır ve her mövsüm temiz hava, "
            "geniş menzereler teklif edir. Qışda ziyaretçiler buraya xizek sürmek, snoubord etmek ve ya sadce "
            "qarda oynamaq üçün gelirlər, yaz ve yay aylarında ise yamaclar yaşıl yürüş cığırlarına ve piknik "
            "mekanlarına çevrilir. Aileler Şahdağı ona göre sevirler ki, bura tehlükesiz, temiz ve kanat yolu, "
            "tubinq xetleri, macera parkları kimi çoxlu eylenceli fealiyyetlerle zengindir."
        ],
        "questions": [
            {
                "q": "Şahdag dağı Azerbaycanın hansı regionunda yerleşir?",
                "options": ["Qusar", "Qebele", "Lenkeran", "Naxçıvan"],
                "answer": 0
            },
            {
                "q": "Şahdagın xizek yamaclarına yaz ve yayda ne olur?",
                "options": [
                    "Onlar yaşıl yürüş cığırlarına ve piknik mekana çevrilir",
                    "Onlar deniz suyu ile dolur",
                    "Onlar avtoparklara çevrilir",
                    "Onlar başqa ölkeye köçürülür"
                ],
                "answer": 0
            },
            {
                "q": "Niye bir çox aileler Şahdağa getmeği sevir?",
                "options": [
                    "Çünki bura tehlükesiz, temizdir ve çoxlu fealiyyet var",
                    "Çünki bura səs-küylü senaye zonasidir",
                    "Çünki ümumiyyetle heç bir xidmət yoxdur",
                    "Çünki burasi her zaman sehra kimi çox istidir"
                ],
                "answer": 0
            }
        ]
    },

    "Bazarduzu Mountain": {
        "pos": (600, 150),
        "image": bazarduzu_img,
        "info": [
            "Bazardüzü dağı Azerbaycanın en yüksek zirvesidir ve məşğul xizek kurortlari ve şeher parklarindan "
            "tam ferqli bir ab-hava yaradır. Dagestan serhedinde, deniz seviyyesinden texminen 4 466 metr "
            "yükseklikde yerleşen bu zirve çox vaxt 'Azerbaycanın damı' adlanır. Bazardüzünün yamaclari "
            "vehşi ve sakitdir; qayalı cığirlar, alp çemenlikleri ve ilin böyük hissesinde qarlı sahələr "
            "burada yer alır. Adeten yalnız hazirliqli piyada yürüşçüler ve alpinistler, çox vaxt tecrübeli "
            "beledçilerin kömeyi ile daha yüksek hisselere qalxmağa cehd edirler. Yol boyu nadir dağ "
            "güllerini, quşlari ve Qafqaz silsilesi üzre unudulmaz menzereleri görmək olur."
        ],
        "questions": [
            {
                "q": "Bazardüzü niye bezen 'Azerbaycanın damı' adlanır?",
                "options": [
                    "Çünki o, ölkenin en yüksek zirvesidir",
                    "Çünki orada çoxlu binanin dami var",
                    "Çünki zirve tamamile evlerle örtülüb",
                    "Çünki ora meşhur alış-veriş merkezidir"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzünün yamaclarindaki mühit nece daha yaxşı tesvir olunur?",
                "options": [
                    "Vehşi, sakit ve alp çemenlikleri ile qayalı cığirlarla dolu",
                    "Çadırlarla dolu izdihamlı çimerlik",
                    "Qum tepeleri olan düz sehra",
                    "Göydelenlerle dolu böyük şeher"
                ],
                "answer": 0
            },
            {
                "q": "Bazardüzünün daha yüksek hisselerine adeten kim çatmağa cehd edir?",
                "options": [
                    "Hazirliqli piyada yürüşçüler ve alpinistler, çox vaxt beledçi ile birlikde",
                    "Tasirüfi keçen ve şap-şap geyinen adamlar",
                    "Yalnız maşin sürücüleri",
                    "Mektebe geden uşaqlar"
                ],
                "answer": 0
            }
        ]
    },

    "Tufandag Mountain": {
        "pos": (600, 280),
        "image": tufandag_img,
        "info": [
            "Qebele şeherine yaxın yerleşen Tufandağ dağı hem rahatlıq, hem de heqiqi dağ menzereleri isteyen "
            "ziyaretçiler üçün sevimli məkandır. Tufandağ Qış–Yay Turizm Kompleksi xizek yamaclari, kanat "
            "yolları, oteller ve kafeler teklif edir, etrafdakı tepe ve meşeler ise tebii gözelliyini qoruyub "
            "saxlayır. Qışda aileler yumşaq başlanğıc traslarda xizek öyrenmek üçün buraya gelir, daha "
            "tecrübeli sürücüler ise dağın yuxarı hissesindeki daha dik yamacları seçirler. İsti mövsümlerde "
            "eyni kanat yolları qonaqları piknik erazileri, yürüş cığirları ve sərin, temiz hava olan yaşıl "
            "yaylalara aparır. Her şey bir-birine yaxın olduğuna göre idmanı, istirahati ve gözel menzerelere "
            "seyri bir gün içinde birleşdirmek çox asandır."
        ],
        "questions": [
            {
                "q": "Tufandağ dağına en yaxın şeher hansıdır?",
                "options": ["Qebele", "Bakı", "Gence", "Sumqayıt"],
                "answer": 0
            },
            {
                "q": "Qışda Tufandağda ziyaretçiler ne ede biler?",
                "options": [
                    "Yumşaq yamaclarda xizek öyrenmek ve daha dik traslarda sürmek",
                    "Okeanda üzmek",
                    "Sehrada sörfinq etmek",
                    "Buzla dolu yeraltı mağaralara getmek"
                ],
                "answer": 0
            },
            {
                "q": "Tufandağ nece hem rahatlığı, hem de tebieti birleşdirir?",
                "options": [
                    "Orada lifter, oteller ve kafeler meşe ve tepelere yaxın yerleşib",
                    "Ora yalnız düz avtopark sahesidir",
                    "Orada ne xidmət, ne de tebiet var",
                    "O, alış-veriş merkezinin içinde yerleşir"
                ],
                "answer": 0
            }
        ]
    }
}


def draw_menu():
    global menu_button_rects
    menu_button_rects = []
    screen.blit(menu_bg, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 40, 100))
    screen.blit(overlay, (0, 0))
    draw_centered_text("AMT: Azerbaijan Mountain Tourism", 80, title_font, GOLD)
    draw_centered_text("Azerbaycan dağlarinin gözelliyini keşf edin", 140, font, (220, 230, 255))
    start_y = 200
    btn_w, btn_h = 600, 50
    gap = 12
    for i, item in enumerate(menu_items):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + gap)
        rect = pygame.Rect(x, y, btn_w, btn_h)
        if i == menu_selected:
            pygame.draw.rect(screen, GOLD, rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)
            label_color = BLACK
        else:
            pygame.draw.rect(screen, (0, 0, 0, 200), rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, rect, 1, border_radius=12)
            label_color = WHITE
        txt = font.render(item["label"], True, label_color)
        screen.blit(txt, (x + 20, y + (btn_h - txt.get_height()) // 2))
        menu_button_rects.append(rect)
    footer = small_font.render("", True, (230, 230, 230))
    screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 50))

def draw_timeline():
    pygame.draw.rect(screen, (15, 45, 90), (0, 0, WIDTH, HEIGHT))
    draw_centered_text("Shahdag", 40, title_font, GOLD)
    lines = []
    for (title, text, _) in history_lessons:
        lines.append(title + ":")
        lines.extend(wrap_text(text[:160] + "...", max_chars=80))
        lines.append("")
    lines.append("Use ↑/↓ to scroll. Press ESC to return to main menu.")
    draw_scrollable_box(lines, (80, 100, 840, 520), timeline_scroll)

def draw_modern():
    pygame.draw.rect(screen, (15, 45, 90), (0, 0, WIDTH, HEIGHT))
    draw_centered_text("Bazarduzu", 40, title_font, GOLD)
    lines = [
        "Use the lesson map to explore detailed stories and quizzes about Bazarduzu Mountain.",
        "Press ESC to return to main menu."
    ]
    draw_text_box(lines, (200, 150, 600, 120))

def draw_regions():
    pygame.draw.rect(screen, (15, 45, 90), (0, 0, WIDTH, HEIGHT))
    draw_centered_text("Tufandag", 40, title_font, GOLD)
    lines = [
        "Use the lesson map to explore Tufandag and related lessons.",
        "Press ESC to return to main menu."
    ]
    draw_text_box(lines, (200, 150, 600, 120))

def draw_encyclopedia():
    pygame.draw.rect(screen, (15, 45, 90), (0, 0, WIDTH, HEIGHT))
    draw_centered_text("Kaputjung", 40, title_font, GOLD)
    lines = []
    for (title, text, _) in history_lessons:
        lines.append(title + ":")
        lines.extend(wrap_text(text[:160] + "...", max_chars=80))
        lines.append("")
    lines.append("Use ↑/↓ to scroll. Press ESC to return to main menu.")
    draw_scrollable_box(lines, (80, 100, 840, 520), timeline_scroll)



def draw_passport():
    # NOW ACTS AS DISCOUNT CARDS SCREEN
    pygame.draw.rect(screen, (15, 45, 90), (0, 0, WIDTH, HEIGHT))
    draw_centered_text("Discount Cards", 40, title_font, GOLD)
    lines = []
    if not travel_cards_unlocked and not discount_cards:
        lines.append("Heç bir endiriminiz yoxdur.")
        lines.append("Abidəleri araşdıraraq və Dağ endirim çarxını fırlatmaqla kartlar qazanın.")
    else:
        if travel_cards_unlocked:
            lines.append("Unlocked Travel Cards (Monuments):")
            lines.append("")
            for name in travel_cards_unlocked:
                lm = landmarks[name]
                card = lm["card"]
                lines.append(f"• {name}")
                lines.append("  Why visit: " + card["why"])
                lines.append("  Best time: " + card["time"])
                lines.append("  Visit duration: " + card["duration"])
                lines.append("  Tip: " + card["tip"])
                lines.append("")
        if discount_cards:
            lines.append("Endirim kartlarınız:")
            lines.append("")
            for dc in discount_cards:
                lines.append(f"• {dc['name']}")
                lines.append("  " + dc["description"])
                lines.append("")
    lines.append("Sürüşdürmek üçün ↑/↓ istifade edin. Geri qayıtmaq üçün ESC düymesini basın.")
    draw_scrollable_box(lines, (80, 100, 840, 520), passport_scroll)

def draw_adventure_intro_overlay():
    info = [
        "Macera rejimi:",
        "Xarakterinizi xeritede hereket etdirmek üçün W/A/S/D istifadə edin.",
        "Approach a monument and press E to learn about it."
    ]
    draw_text_box(info, (80, 480, 840, 140))

clock = pygame.time.Clock()
running = True
prev_state = None

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state in ["map", "info", "trivia", "results", "shop"]:
                    state = "menu"
                elif state == "lesson_map":
                    if origin_state == "encyclopedia":
                        state = "encyclopedia"
                    else:
                        state = "menu"
                elif state in ["lesson_info", "lesson_quiz", "lesson_results"]:
                    state = "lesson_map"
                elif state in ["president", "timeline", "modern", "regions",
                               "encyclopedia", "language", "passport", "wheel"]:
                    state = "menu"
                elif state == "menu":
                    running = False
                continue

            if event.key == pygame.K_p and state in ["map", "info", "trivia", "results"]:
                state = "passport"
                passport_scroll = 0
                start_transition("Opening Discount Cards")
                continue

            if state == "menu":
                if event.key == pygame.K_UP:
                    menu_selected = (menu_selected - 1) % len(menu_items)
                    if sfx_menu_move:
                        sfx_menu_move.play()
                elif event.key == pygame.K_DOWN:
                    menu_selected = (menu_selected + 1) % len(menu_items)
                    if sfx_menu_move:
                        sfx_menu_move.play()
                elif event.key == pygame.K_RETURN:
                    chosen = menu_items[menu_selected]["state"]
                    if sfx_menu_select:
                        sfx_menu_select.play()
                    if chosen == "exit":
                        running = False
                    else:
                        state = chosen
                        if state == "president":
                            president_state = "intro"
                            president_scenario_index = 0
                            success_count = 0
                            start_transition("Entering AMT Runner")
                        elif state == "timeline":
                            current_lessons = history_lessons
                            current_category = "Shahdag"
                            state = "lesson_map"
                            selected_lesson = 0
                            origin_state = "menu"
                            start_transition("History of Azerbaijan (Shahdag)")
                        elif state == "modern":
                            current_lessons = modern_lessons
                            current_category = "Bazarduzu"
                            state = "lesson_map"
                            selected_lesson = 0
                            origin_state = "menu"
                            start_transition("Modern Azerbaijan (Bazarduzu)")
                        elif state == "regions":
                            current_lessons = region_lessons
                            current_category = "Tufandag"
                            state = "lesson_map"
                            selected_lesson = 0
                            origin_state = "menu"
                            start_transition("Regions (Tufandag)")
                        elif state == "encyclopedia":
                            ency_scroll = 0
                            ency_selected_category = None
                            start_transition("Cultural Encyclopedia")
                        elif state == "passport":
                            passport_scroll = 0
                            start_transition("Opening Discount Cards")
                        elif state == "map":
                            adventure_intro_start_time = pygame.time.get_ticks()
                            start_transition("Adventure Mode")
                        elif state == "wheel":
                            # reset wheel state
                            wheel_selected_index = 0
                            wheel_spinning = False
                            wheel_done = True
                            start_transition("Mountain Discount Wheel")

            elif state == "map":
                if event.key == pygame.K_r:
                    state = "shop"
                    start_transition("Opening Skin Shop")
                    if sfx_open_shop:
                        sfx_open_shop.play()
                elif event.key == pygame.K_e:
                    near_name = None
                    px, py = player_pos
                    for name, lm in landmarks.items():
                        lx, ly = lm["pos"]
                        if abs(px - lx) < 60 and abs(py - ly) < 60:
                            near_name = name
                            break
                    if near_name:
                        current_landmark = near_name
                        state = "info"
                        question_index = 0
                        answers_record = []
                        start_transition(f"Exploring {current_landmark}")
                        if sfx_open_lesson:
                            sfx_open_lesson.play()

            elif state == "info":
                if event.key == pygame.K_RETURN:
                    state = "trivia"
                    question_index = 0
                    answers_record = []
                    start_transition("Starting Monument Quiz")
                elif event.key == pygame.K_r:
                    state = "shop"
                    start_transition("Opening Skin Shop")
                    if sfx_open_shop:
                        sfx_open_shop.play()

            elif state == "trivia":
                if event.key == pygame.K_r:
                    state = "shop"
                    start_transition("Opening Skin Shop")
                    if sfx_open_shop:
                        sfx_open_shop.play()
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    choice_idx = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4].index(event.key)
                    lm = landmarks[current_landmark]
                    q = lm["questions"][question_index]
                    correct_idx = q["answer"]
                    is_correct = (choice_idx == correct_idx)
                    answers_record.append((q["q"], choice_idx, correct_idx, is_correct))
                    if is_correct:
                        score += 5
                        if sfx_correct:
                            sfx_correct.play()
                    else:
                        if sfx_wrong:
                            sfx_wrong.play()
                    question_index += 1
                    if question_index >= len(lm["questions"]):
                        correct_count = sum(1 for _, _, _, ok in answers_record if ok)
                        if correct_count >= max(1, len(lm["questions"]) // 2):
                            travel_cards_unlocked.add(current_landmark)
                        results_scroll = 0
                        state = "results"
                        start_transition("Quiz Results")
            elif state == "trivia":
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    choice_idx = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4].index(event.key)

                    lm = landmarks[current_landmark]
                    q = lm["questions"][question_index]
                    correct_idx = q["answer"]
                    is_correct = (choice_idx == correct_idx)

        # save result for results screen
                    answers_record.append((q["q"], choice_idx, correct_idx, is_correct))

        # ★ Give 5 points for each correct answer ★
                    if is_correct:
                        score += 5
                        if sfx_correct:
                            sfx_correct.play()
                    else:
                        if sfx_wrong:
                            sfx_wrong.play()

                    question_index += 1
                    if question_index >= len(lm["questions"]):
            # move to your quiz results state
                        state = "results"
                        results_scroll = 0            
            elif state == "results":
                if event.key == pygame.K_RETURN:
                    state = "map"
                elif event.key == pygame.K_UP:
                    results_scroll = max(0, results_scroll - 20)
                elif event.key == pygame.K_DOWN:
                    results_scroll += 20
                elif event.key == pygame.K_r:
                    state = "shop"
                    start_transition("Opening Skin Shop")
                    if sfx_open_shop:
                        sfx_open_shop.play()

            elif state == "shop":
                if event.key == pygame.K_LEFT:
                    shop_scroll_x = max(0, shop_scroll_x - 40)
                elif event.key == pygame.K_RIGHT:
                    shop_scroll_x += 40
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    idx = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5].index(event.key)
                    if idx < len(skin_assets):
                        skin = skin_assets[idx]
                        if not skin["owned"]:
                            if score >= skin_cost:
                                score -= skin_cost
                                skin["owned"] = True
                                player_skin_index = idx
                                player_img = skin["image"]
                                start_transition("Skin Purchased & Equipped")
                            else:
                                start_transition("Not Enough Points")
                        else:
                            player_skin_index = idx
                            player_img = skin["image"]
                            start_transition("Skin Equipped")
                elif event.key == pygame.K_r:
                    state = "map"
                    start_transition("Back to Adventure")

            elif state == "president":   
                run_azerquest_runner()
                state = "menu"
                menu_selected = 0

            elif state == "lesson_map":
                if event.key == pygame.K_UP:
                    selected_lesson = max(0, selected_lesson - 1)
                elif event.key == pygame.K_DOWN:
                    selected_lesson = min(len(current_lessons) - 1, selected_lesson + 1)
                elif event.key in [pygame.K_RETURN, pygame.K_e]:
                    current_lesson = current_lessons[selected_lesson]
                    state = "lesson_info"
                    lesson_question_index = 0
                    lesson_answers_record = []
                    start_transition("Entering Lesson")

            elif state == "lesson_info":
                if event.key == pygame.K_RETURN:
                    if current_lesson and current_lesson[2]:
                        state = "lesson_quiz"
                        lesson_question_index = 0
                        lesson_answers_record = []
                        start_transition("Starting Lesson Quiz")
                    else:
                        state = "lesson_map"

            elif state == "lesson_quiz":
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    choice_idx = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4].index(event.key)
                    qobj = current_lesson[2][lesson_question_index]
                    correct_idx = qobj["answer"]
                    is_correct = (choice_idx == correct_idx)
                    lesson_answers_record.append((qobj["q"], choice_idx, correct_idx, is_correct))
                    if is_correct:
                        score += 5
                        # NEW: only count mountain points for Shahdag/Bazarduzu/Tufandag lesson sets
                        if current_lessons in (history_lessons, modern_lessons, region_lessons):
                            mountain_points += 5
                        if sfx_correct:
                            sfx_correct.play()
                    else:
                        if sfx_wrong:
                            sfx_wrong.play()
                    lesson_question_index += 1
                    if lesson_question_index >= len(current_lesson[2]):
                        state = "lesson_results"
                        lesson_results_scroll = 0
                        start_transition("Lesson Results")

            elif state == "lesson_results":
                if event.key == pygame.K_RETURN:
                    state = "lesson_map"
                elif event.key == pygame.K_UP:
                    lesson_results_scroll = max(0, lesson_results_scroll - 20)
                elif event.key == pygame.K_DOWN:
                    lesson_results_scroll += 20

            elif state == "wheel":
                # Spin with SPACE or ENTER if enough points
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    if not wheel_spinning:
                        if mountain_points >= 100:
                            mountain_points -= 100
                            wheel_spinning = True
                            wheel_spin_start_time = pygame.time.get_ticks()
                            wheel_final_index = choose_wheel_index()
                            wheel_done = False
                            if sfx_menu_select:
                                sfx_menu_select.play()
                        else:
                            start_transition("Fırlanma üçün 100 dağ balı lazımdır!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                for i, rect in enumerate(menu_button_rects):
                    if rect.collidepoint(mouse_pos):
                        chosen = menu_items[i]["state"]
                        if chosen == "exit":
                            running = False
                        else:
                            state = chosen
                            if sfx_menu_select:
                                sfx_menu_select.play()
                            if state == "president":
                                president_state = "intro"
                                president_scenario_index = 0
                                success_count = 0
                                start_transition("Entering AMT Runner")
                            elif state == "timeline":
                                current_lessons = history_lessons
                                current_category = "Shahdag"
                                state = "lesson_map"
                                selected_lesson = 0
                                origin_state = "menu"
                                start_transition("Shahdag Lessons")
                            elif state == "modern":
                                current_lessons = modern_lessons
                                current_category = "Bazarduzu"
                                state = "lesson_map"
                                selected_lesson = 0
                                origin_state = "menu"
                                start_transition("Bazarduzu Lessons")
                            elif state == "regions":
                                current_lessons = region_lessons
                                current_category = "Tufandag"
                                state = "lesson_map"
                                selected_lesson = 0
                                origin_state = "menu"
                                start_transition("Tufandag Lessons")
                            elif state == "encyclopedia":
                                ency_selected_category = None
                                start_transition("Kaputjugh")
                            elif state == "passport":
                                passport_scroll = 0
                                start_transition("Opening Discount Cards")
                            elif state == "map":
                                adventure_intro_start_time = pygame.time.get_ticks()
                                start_transition("Adventure Mode")
                            elif state == "wheel":
                                wheel_selected_index = 0
                                wheel_spinning = False
                                wheel_done = True
                                start_transition("Mountain Discount Wheel")
            if state in ["map", "info", "trivia", "results"] and shop_icon:
                icon_rect = pygame.Rect(20, HEIGHT - 68, 48, 48)
                if icon_rect.collidepoint(mouse_pos):
                    if state != "shop":
                        state = "shop"
                        start_transition("Opening Skin Shop")
                        if sfx_open_shop:
                            sfx_open_shop.play()
                    else:
                        state = "map"
                        start_transition("Back to Adventure")

    # ---------------------------
    # Movement on map
    # ---------------------------
    if state == "map":
        moving = False
        if keys[pygame.K_w]:
            player_pos[1] -= speed
            moving = True
        if keys[pygame.K_s]:
            player_pos[1] += speed
            moving = True
        if keys[pygame.K_a]:
            player_pos[0] -= speed
            moving = True
        if keys[pygame.K_d]:
            player_pos[0] += speed
            moving = True
        if moving and sfx_step:
            now = pygame.time.get_ticks()
            if now - last_step_time > 300:
                sfx_step.play()
                last_step_time = now
    else:
        moving = False

    player_pos[0] = max(0, min(WIDTH - 50, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT - 70, player_pos[1]))

    # ---- Music control based on state ----
    if state != prev_state:
        if state == "menu":
            play_menu_music.play_menu_music()
        if prev_state == "menu" and state != "menu":
            stop_music()
        prev_state = state

    # ---- Wheel timing & reward ----
    if state == "wheel" and wheel_spinning:
        now_t = pygame.time.get_ticks()
        if now_t - wheel_spin_start_time >= wheel_spin_duration and not wheel_done:
            wheel_spinning = False
            wheel_selected_index = wheel_final_index
            reward = wheel_options[wheel_final_index]
            # add discount card if not already present
            if all(dc["name"] != reward["name"] for dc in discount_cards):
                discount_cards.append(reward)
            start_transition(f"You won: {reward['name']}")
            wheel_done = True
    # ---------------------------
    # Drawing
    # ---------------------------
    if state == "menu":
        draw_menu()
        draw_transition_overlay()
        pygame.display.flip()
        continue

    if state in ["map", "info", "trivia", "results", "shop"]:
        screen.blit(map_bg, (0, 0))
    elif state in ["president", "timeline", "modern", "regions",
                   "encyclopedia", "language", "passport",
                   "lesson_map", "lesson_info", "lesson_quiz",
                   "lesson_results", "wheel"]:
        screen.fill(BG)

    if state == "map":
        current_landmark = None
        for name, lm in landmarks.items():
            lx, ly = lm["pos"]
            if lm["image"]:
                img = lm["image"]
                screen.blit(img, (lx - img.get_width()//2, ly - img.get_height()//2))
            else:
                pygame.draw.circle(screen, RED, (lx, ly), 24)
                screen.blit(small_font.render(name, True, BLACK), (lx - 40, ly - 70))
            px, py = player_pos
            if abs(px - lx) < 60 and abs(py - ly) < 60:
                current_landmark = name
                draw_text_box([f"Press E to explore: {name}"], (320, 600, 360, 60))
        if player_img:
            offset_y = -4 if moving and (pygame.time.get_ticks() // 120) % 2 == 0 else 0
            screen.blit(player_img, (player_pos[0], player_pos[1] + offset_y))
        else:
            color = player_color_fallback[player_skin_index % len(player_color_fallback)]
            pygame.draw.rect(screen, color, (*player_pos, 50, 70), border_radius=6)
        if shop_icon:
            screen.blit(shop_icon, (20, HEIGHT - 68))
            screen.blit(small_font.render("R düyməsini basın və ya Shop üçün işarəni basın", True, BLACK), (76, HEIGHT - 52))
        else:
            pygame.draw.rect(screen, GRAY, (20, HEIGHT - 68, 48, 48), border_radius=6)
            screen.blit(small_font.render("Shop (R)", True, BLACK), (76, HEIGHT - 52))
        if adventure_intro_start_time is not None:
            if pygame.time.get_ticks() - adventure_intro_start_time < 2000:
                draw_adventure_intro_overlay()

    elif state == "info":
        lm = landmarks[current_landmark]
        title_label = title_font.render(current_landmark, True, BLACK)
        screen.blit(title_label, (40, 30))
        if lm["image"]:
            screen.blit(lm["image"], (40, 110))
        info_lines = []
        for line in lm["info"]:
            info_lines.extend(wrap_text(line, max_chars=70))
        num_q = len(lm["questions"])
        info_lines.append("")
        info_lines.append(f"Başlamaq üçün ENTER düymesini basın {num_q}- sual viktorina {current_landmark}.")
        draw_text_box(info_lines, (300, 120, 640, 360))

    elif state == "trivia":
        lm = landmarks[current_landmark]
        q = lm["questions"][question_index]
        lines = wrap_text(q["q"], max_chars=70)
        lines.append("")
        for i, opt in enumerate(q["options"]):
            lines.extend(wrap_text(f"{i+1}. {opt}", max_chars=70))
        draw_text_box(lines, (80, 120, 840, 320))
        screen.blit(small_font.render("Answer with keys 1–4", True, BLACK), (80, 460))

    elif state == "results":
        result_lines = [f"Quiz Results for {current_landmark}:", ""]
        for (q_text, choice_idx, correct_idx, is_correct) in answers_record:
            status = "Correct" if is_correct else "Wrong"
            q_obj = None
            for qq in landmarks[current_landmark]["questions"]:
                if qq["q"] == q_text:
                    q_obj = qq
                    break
            if q_obj:
                player_answer = q_obj["options"][choice_idx]
                correct_answer = q_obj["options"][correct_idx]
            else:
                player_answer = f"Option {choice_idx+1}"
                correct_answer = f"Option {correct_idx+1}"
            result_lines.extend(wrap_text(f"- {q_text}", max_chars=70))
            result_lines.append(f"  Your answer: {player_answer} | {status}")
            result_lines.append(f"  Correct answer: {correct_answer}")
            result_lines.append("")
        result_lines.append("Use ↑/↓ to scroll if needed.")
        result_lines.append("Press ENTER to return to the map.")
        box_rect = (80, 80, 840, 460)
        inner_h = box_rect[3] - 20
        total_h = get_text_height(result_lines, line_spacing=6)
        max_scroll = max(0, total_h - inner_h)
        results_scroll = max(0, min(results_scroll, max_scroll))
        draw_scrollable_box(result_lines, box_rect, results_scroll, line_spacing=6)

    elif state == "shop":
        draw_text_box(["Skin Shop"], (260, 40, 480, 60))
        draw_text_box([
            f"Score: {score} points",
            f"Mountain Points (lessons): {mountain_points}",
            f"Each skin costs: {skin_cost} points",
            "Use ←/→ to scroll skins, 1–5 to buy/equip, R or ESC to exit."
        ], (260, 110, 480, 110))
        bx = 140
        by = 230
        gap = 220
        content_width = bx + len(skin_assets) * gap
        max_shop_scroll = max(0, content_width - WIDTH + 80)
        shop_scroll_x = max(0, min(shop_scroll_x, max_shop_scroll))
        for i, s in enumerate(skin_assets):
            frame_x = bx + i * gap - shop_scroll_x
            frame = pygame.Rect(frame_x, by, 180, 220)
            if frame.right < 0 or frame.left > WIDTH:
                continue
            pygame.draw.rect(screen, GRAY, frame, border_radius=10)
            pygame.draw.rect(screen, BLACK, frame, 2, border_radius=10)
            if s["image"]:
                screen.blit(s["image"], (frame_x + 65, by + 40))
            else:
                color = player_color_fallback[i % len(player_color_fallback)]
                pygame.draw.rect(screen, color, (frame_x + 60, by + 35, 60, 90), border_radius=6)
            owned_txt = "Owned" if s["owned"] else "Locked"
            screen.blit(small_font.render(f"{i+1}. {s['name']}", True, BLACK), (frame_x + 15, by + 140))
            screen.blit(small_font.render(f"Cost: {skin_cost} pts", True, BLACK), (frame_x + 30, by + 165))
            screen.blit(small_font.render(owned_txt, True, BLACK), (frame_x + 60, by + 190))

    elif state == "timeline":
        draw_timeline()

    elif state == "modern":
        draw_modern()

    elif state == "regions":
        draw_regions()

    elif state == "encyclopedia":
        draw_encyclopedia()

    elif state == "passport":
        draw_passport()

    elif state == "lesson_map":
        pygame.draw.rect(screen, (15, 45, 90), (0, 0, WIDTH, HEIGHT))
        draw_centered_text(f"Lessons: {current_category.title()}", 20, title_font, GOLD)
        start_y = 80
        gap_y = 80
        left_x = WIDTH//2 - 200
        right_x = WIDTH//2 + 100
        for i, lesson in enumerate(current_lessons):
            x = left_x if i % 2 == 0 else right_x
            y = start_y + i * gap_y
            if i < len(current_lessons) - 1:
                next_x = right_x if i % 2 == 0 else left_x
                next_y = start_y + (i+1) * gap_y
                pygame.draw.line(screen, WHITE, (x+20, y+20), (next_x+20, next_y+20), 3)
            color = GREEN if i == selected_lesson else WHITE
            pygame.draw.circle(screen, color, (x+20, y+20), 20)
            num_label = font.render(str(i+1), True, BLACK)
            screen.blit(num_label, (x + 20 - num_label.get_width()//2,
                                    y + 20 - num_label.get_height()//2))
            title_text = lesson[0]
            title_label = small_font.render(title_text, True, WHITE)
            tx = x + 60 if i % 2 == 0 else x - 60 - title_label.get_width()
            screen.blit(title_label, (tx, y + 10))
        instr = small_font.render("Use ↑/↓ to select a lesson, ENTER/E to open it. ESC to go back.", True, WHITE)
        screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT - 40))

    elif state == "lesson_info":
        pygame.draw.rect(screen, BG, (0, 0, WIDTH, HEIGHT))
        lesson_title, lesson_text, questions = current_lesson
        draw_centered_text(lesson_title, 30, title_font, GOLD)
        text_lines = wrap_text(lesson_text, max_chars=80)
        text_lines.append("")
        text_lines.append(f"Press ENTER to start a {len(questions)}-question quiz.")
        draw_scrollable_box(text_lines, (60, 100, 880, 500), 0)

    elif state == "lesson_quiz":
        qobj = current_lesson[2][lesson_question_index]
        lines = wrap_text(qobj["q"], max_chars=70)
        lines.append("")
        for idx, opt in enumerate(qobj["options"]):
            lines.extend(wrap_text(f"{idx+1}. {opt}", max_chars=70))
        draw_text_box(lines, (80, 120, 840, 320))
        screen.blit(small_font.render("Answer with keys 1–4", True, BLACK), (80, 460))

    elif state == "lesson_results":
        lines = ["Lesson Quiz Results:", ""]
        for (q_text, choice_idx, correct_idx, is_correct) in lesson_answers_record:
            status = "Correct " if is_correct else "Wrong "
            q_obj = None
            for q in current_lesson[2]:
                if q["q"] == q_text:
                    q_obj = q
                    break
            if q_obj:
                player_txt = q_obj["options"][choice_idx]
                correct_txt = q_obj["options"][correct_idx]
            else:
                player_txt = f"Option {choice_idx+1}"
                correct_txt = f"Option {correct_idx+1}"
            lines.extend(wrap_text(f"- {q_text}", max_chars=70))
            lines.append(f"  Your answer: {player_txt} | {status}")
            lines.append(f"  Correct answer: {correct_txt}")
            lines.append("")
        lines.append("Use ↑/↓ to scroll. Press ENTER to return to lessons.")
        box_rect = (80, 80, 840, 460)
        inner_h = box_rect[3] - 20
        total_h = get_text_height(lines, line_spacing=6)
        max_scroll = max(0, total_h - inner_h)
        lesson_results_scroll = max(0, min(lesson_results_scroll, max_scroll))
        draw_scrollable_box(lines, box_rect, lesson_results_scroll, line_spacing=6)

    elif state == "wheel":
        draw_wheel()

    # HUD – now shows score and mountain points
    if state in ["map", "info", "trivia", "results", "shop"]:
        hud_bg = pygame.Surface((320, 40), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 150))
        screen.blit(hud_bg, (10, 10))
        hud_text = small_font.render(
            f"Score: {score}   Mountain Points: {mountain_points}",
            True, WHITE
        )
        screen.blit(hud_text, (20, 20))

    draw_transition_overlay()
    pygame.display.flip()

pygame.quit()
sys.exit()
