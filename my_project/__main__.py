import pygame
import sys
from pathlib import Path
from my_project.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from my_project.Model.menu_model import BackgroundModel
from my_project.Controller.menu_controller import main_menu_loop


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Garden Invasion")

    pkg_root = Path(__file__).resolve().parent
    bg_path = pkg_root / "Assets" / "images" / "Menu_background.png"
    background_model = BackgroundModel(bg_path)
    font_item = pygame.font.SysFont("Arial", 30)
    font_inst = pygame.font.SysFont("Arial", 16)
    font_title = pygame.font.SysFont("Arial", 72)
    fonts = (font_item, font_inst, font_title)

    try:
        main_menu_loop(screen, background_model.surface, background_model.rect, fonts)
    except Exception as e:
        print("Fatal error:", e)
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
