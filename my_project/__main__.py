import my_project
import sys
from pathlib import Path
import pygame

# this is the main module of your app
# it is only required if your project must be runnable
# this is the script to be executed whenever some users writes `python -m my_project` on the command line, eg.

def load_background_keep_ratio(image_path: Path, screen_size: tuple[int, int]) -> tuple[pygame.Surface, pygame.Rect]:
    background_img = pygame.image.load(str(image_path)) #loads an image into pygame which later will be used as background
    img_w, img_h = background_img.get_size() #assess the width and height of the image
    scr_w, scr_h = screen_size
    scale = min(scr_w / img_w, scr_h / img_h) 
    new_size = (max(1, round(img_w * scale)), max(1, round(img_h * scale))) # calculate new size of the picture
    scaled = pygame.transform.smoothscale(background_img, new_size) # new scaled image
    rect = scaled.get_rect(center=(scr_w // 2, scr_h // 2))
    return scaled, rect

def main():
    try:
        pygame.init() # initializes pygames modules
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Garden Invasion") # sets the title displayed in the window bar
        clock = pygame.time.Clock() # creates a clock object to manage the frame rate
        print("check print: First window created") # quick confirmation to that the window was created

        pkg_root = Path(__file__).resolve().parent
        bg_path = pkg_root/"Assets"/"images"/"Menu_background.png" # path to the background image
        background_surf = None
        background_rect = None # prepare placeholders for background surface and rectangle
        if bg_path.is_file():
            background_surf, background_rect = load_background_keep_ratio(bg_path, (600, 600))
        else:
            print(f"[Error] Background not found") # if the file exists load and scale it otherwise return the error message


        running = True # main loop active until a quit action is received, such as ESC or the x button
        while running:
            for event in pygame.event.get(): # event loop to handle user inputs and system events
                if event.type == pygame.QUIT:
                    running = False # if the user clicks the window's close button, exit the loop
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False # if the user presses the ESC key, exit the loop
                if background_surf is not None:
                    screen.fill((0, 0, 0))
                    screen.blit(background_surf, background_rect) # draw the background image if available
                else:
                    screen.fill((0, 0, 50)) # fill the screen with a solid color if no background image is available

            # title
            font = pygame.font.SysFont("Arial", 72) # create a font object with Arial font and size 72
            title_text = font.render("Garden Invasion", True, (98, 222, 109)) # render the title text with anti-aliasing and a RGB color
            title_rect = title_text.get_rect(center=(300, 150)) # get the rectangle of the text and center it on the screen
            screen.blit(title_text, title_rect) # draw the title text on the screen

            # Menu
            font_small = pygame.font.SysFont("Arial", 36)
            menutitle_text = font_small.render("Menu", True, (98, 222, 109))
            menutitle_rect = menutitle_text.get_rect(center=(300, 250))
            screen.blit(menutitle_text, menutitle_rect)

            # Instructions
            font_small = pygame.font.SysFont("Arial", 16)
            inst_text = font_small.render("Press ESC or close window to exit", True, (200, 200, 200))
            inst_rect = inst_text.get_rect(center=(300, 400))
            screen.blit(inst_text, inst_rect)

            # Update display
            pygame.display.flip() # update the full display surface to the screen
            clock.tick(60) # limit the frame rate to 60 frames per second

        print("check print: Windows created successfully") # quick confirmation that the window closed without
                                                           # errors after the loop finished, aka pressed ESC or the x button

    except Exception as e:
        print(f"Error in window creation: {e}")
        return 1 # return a non-zero value to indicate an error occurred
    finally:
        pygame.quit()
        sys.exit() # ensure pygame quits properly and the program exits

if __name__ == "__main__":
    main()