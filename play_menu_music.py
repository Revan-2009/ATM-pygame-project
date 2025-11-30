import pygame
current_music = None  
def play_menu_music():
    """Start looping background music for the main menu."""
    global current_music
    if not pygame.mixer.get_init():
        return
    if current_music == "menu":
        return  # already playing

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/menu_music1.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)  # loop forever
        current_music = "menu"
    except Exception:
        current_music = None
