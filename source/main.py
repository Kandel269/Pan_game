import sys
import time

import source.sql as sql
from source.the_game import *


class MainMenu():
    def __init__(self):
        self.current_level, self.allow_sounds = sql.get_data()

        self.display_title = pygame.display.set_caption("Pan - menu główne")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)

        self.FONT = pygame.font.Font(None, 36)
        self.load_textures()
        self.load_sounds()

        self.total_height = (MM_HEIGHT * 3) + (MM_SPACING * 2)

        self.start_button = pygame.Rect((WIDTH - MM_WIDTH) // 2, (HEIGHT - self.total_height) // 2, MM_WIDTH, MM_HEIGHT)
        self.settings_button = pygame.Rect((WIDTH - MM_WIDTH) // 2, (HEIGHT - self.total_height) // 2 + MM_HEIGHT + MM_SPACING, MM_WIDTH, MM_HEIGHT)
        self.exit_button = pygame.Rect((WIDTH - MM_WIDTH) // 2, (HEIGHT - self.total_height) // 2 + (MM_HEIGHT + MM_SPACING) * 2, MM_WIDTH, MM_HEIGHT)

    def load_sounds(self) -> None:
        current_file = os.path.dirname(__file__)
        sounds_folder = os.path.join(current_file, "../sounds")
        self.sounds = {}
        for sound in os.listdir(sounds_folder):
            sounds_path = os.path.join(sounds_folder, sound)
            file = pygame.mixer.Sound(sounds_path)
            self.sounds[sound.replace(".wav", "")] = file

    def load_textures(self) -> None:
        current_file = os.path.dirname(__file__)
        texture_folder = os.path.join(current_file, "../img", "img_wg")
        self.textures = {}
        for img in os.listdir(texture_folder):
            texture_path = os.path.join(texture_folder, img)
            texture = pygame.image.load(texture_path)
            texture.set_colorkey((255,255,255))
            self.textures[img.replace(".png","")] = texture

    def check_events(self, events) -> (str or None):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button.collidepoint(mouse_pos):
                    return "game"
                elif self.settings_button.collidepoint(mouse_pos):
                    return "settings"
                elif self.exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    def center_txt(self, text, color, button) -> None:
        text_edited = self.FONT.render(text, True, color)
        text_rect = text_edited.get_rect()
        text_rect.center = button.center
        self.screen.blit(text_edited, text_rect)

    def draw(self) -> None:
        self.screen.fill(WHITE)
        self.screen.blit(self.textures['MM_background'],(0,0))
        pygame.draw.rect(self.screen, BLACK, self.start_button)
        pygame.draw.rect(self.screen, BLACK, self.settings_button)
        pygame.draw.rect(self.screen, BLACK, self.exit_button)

        self.center_txt("Rozpocznij grę",RED,self.start_button)
        self.center_txt("Ustawienia",RED,self.settings_button)
        self.center_txt("Wyjście",RED,self.exit_button)

    def add_image(self, image_name, button) -> None:
        image = self.textures[image_name]
        image_rect = image.get_rect()
        image_rect.topleft = button.topleft
        self.screen.blit(image, image_rect)

class Settings(MainMenu):
    def __init__(self):
        super().__init__()
        self.question_window = False

        self.display_title = pygame.display.set_caption("Pan - ustawienia")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)

        self.FONT = pygame.font.Font(None, 36)

        self.text_level = self.FONT.render("Poziom analizy drzewa", True, BLACK)
        text_rect = self.text_level.get_rect()
        self.text_level_width = text_rect.width
        self.text_level_height = text_rect.height

        self.button_level_height = 100 +self.text_level_height +MM_SPACING
        self.level_2 = pygame.Rect((WIDTH - (S_WIDTH * 3) - (S_SPACING *2) ) //2, self.button_level_height, S_WIDTH, S_HEIGHT)
        self.level_3 = pygame.Rect(((WIDTH - (S_WIDTH * 3) - (S_SPACING *2) ) //2)+S_SPACING+S_WIDTH, self.button_level_height, S_WIDTH, S_HEIGHT)
        self.level_4 = pygame.Rect(((WIDTH - (S_WIDTH * 3) - (S_SPACING *2) ) //2)+(S_SPACING*2)+(S_WIDTH*2), self.button_level_height, S_WIDTH, S_HEIGHT)
        self.question_mark = pygame.Rect((WIDTH + self.text_level_width + MM_SPACING) / 2, 100, QUESTION_MARK_WIDTH,QUESTION_MARK_HEIGHT)
        self.sounds_button = pygame.Rect((WIDTH-80)//2,self.button_level_height + S_SPACING + S_HEIGHT, WG_SOUNDS_WIDTH, WG_SOUNDS_HEIGHT)
        self.main_menu_button = pygame.Rect((WIDTH-MM_WIDTH)/2, self.button_level_height + (S_SPACING * 2) + (S_HEIGHT * 2), MM_WIDTH, MM_HEIGHT)

    def check_events(self, events) -> (str or None):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            self.question_window = False
            if self.question_mark.collidepoint(mouse_pos):
                self.question_window = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.level_2.collidepoint(mouse_pos):
                    self.current_level = 2
                elif self.level_3.collidepoint(mouse_pos):
                    self.current_level = 3
                elif self.level_4.collidepoint(mouse_pos):
                    self.current_level = 4
                elif self.sounds_button.collidepoint(mouse_pos):
                    if self.allow_sounds:
                        self.allow_sounds = False
                    else:
                        self.allow_sounds = True
                elif self.main_menu_button.collidepoint(mouse_pos):
                    sql.edit_data(self.current_level, self.allow_sounds)
                    return "menu"

    def draw(self) -> None:
        self.screen.fill(WHITE)
        self.screen.blit(self.textures['MM_background'], (0, 0))
        self.screen.blit(self.text_level,((WIDTH - self.text_level_width)/2,100))

        self.add_image('question',self.question_mark)

        if self.question_window:
            self.screen.blit(self.textures['question_cloud'],((WIDTH + self.text_level_width + MM_SPACING-150) / 2,20))
        color_2 = color_3 = color_4 = BLACK
        if self.current_level == 2:
            color_2 = GREEN
        elif self.current_level == 3:
            color_3 = GREEN
        elif self.current_level == 4:
            color_4 = GREEN

        pygame.draw.rect(self.screen, color_2, self.level_2)
        self.center_txt("2",RED,self.level_2)
        pygame.draw.rect(self.screen, color_3, self.level_3)
        self.center_txt("3",RED,self.level_3)
        pygame.draw.rect(self.screen, color_4, self.level_4)
        self.center_txt("4",RED,self.level_4)

        if self.allow_sounds:
            image = 'sounds'
        else:
            image = 'no_sounds'
        self.add_image(image, self.sounds_button)

        pygame.draw.rect(self.screen, BLACK,self.main_menu_button)
        self.center_txt("Menu główne", RED,self.main_menu_button)

class WindowGame(MainMenu):
    def __init__(self):
        super().__init__()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.display_title = pygame.display.set_caption("Pan")
        self.screen = pygame.display.set_mode(GAME_SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_GAME_SCREEN_SIZE)

        self.load_sounds()

        self.FONT = pygame.font.Font(None, 36)
        self.end_font = pygame.font.Font(None, 120)

        self.play_card_button = pygame.Rect(GAME_WIDTH - ((BORDER + WG_WIDTH) / 2), 100, WG_WIDTH, WG_HEIGHT)
        self.pull_button = pygame.Rect(GAME_WIDTH - ((BORDER + WG_WIDTH) / 2), 220, WG_WIDTH, WG_HEIGHT)
        self.sounds_button = pygame.Rect(GAME_WIDTH - ((BORDER + WG_SOUNDS_WIDTH) / 2), 340, WG_SOUNDS_WIDTH, WG_SOUNDS_HEIGHT)
        self.main_menu_button = pygame.Rect(GAME_WIDTH - ((BORDER + WG_WIDTH) / 2), GAME_HEIGHT - 100 - WG_HEIGHT, WG_WIDTH, WG_HEIGHT)

        self.game = TheGame(self.current_level)

    def check_events(self, events) -> (None or str):
        if self.game.turn == "bot":
            self.game.bot_tree()
            self.game.best_bot_move()
            best = self.game.best_bot_move()
            self.game.bot_play_best(best)
            if self.allow_sounds:
                if best == "pull_cards":
                    self.sounds['draw_card'].play()
                else:
                    self.sounds['play_card'].play()
            self.game.turn = "player"
            self.game.new_turn()

        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        clicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                if self.play_card_button.collidepoint(mouse_pos):
                    if self.game.turn == "player":
                        if self.game.check_rules_play(self.game.player_hand):
                            if self.allow_sounds:
                                self.sounds['play_card'].play()
                            self.game.turn = "bot"
                            self.game.new_turn()
                elif self.pull_button.collidepoint(mouse_pos):
                    if self.game.turn == "player":
                        if self.game.check_rules_pull():
                            if self.allow_sounds:
                                self.sounds['draw_card'].play()
                            self.game.turn = "bot"
                            self.game.new_turn()
                elif self.sounds_button.collidepoint(mouse_pos):
                    if self.allow_sounds:
                        self.allow_sounds = False
                    else:
                        self.allow_sounds = True
                elif self.main_menu_button.collidepoint(mouse_pos):
                    return "menu"

        for card_position in range(len(self.game.player_hand)):
            card = self.game.player_hand[card_position]
            if card.up and not card.lock:
                card.up = False
                card.y += 50
            if card.collidepoint(mouse_pos):
                if not card_position + 1 == len(self.game.player_hand):
                    if card.x + 50 <= mouse_x:
                        continue
                if not card.up:
                    card.up = True
                    card.y -= 50
                if clicked:
                    if not card.lock:
                        card.lock = True
                    else:
                        card.lock = False

    def draw(self) -> None:
        self.screen.fill(BLUE)

        start = (GAME_WIDTH -BORDER, 0)
        end = (GAME_WIDTH -BORDER, GAME_HEIGHT)
        pygame.draw.line(self.screen, BLACK, start, end, width= 4)

        self.draw_cards(self.game.player_hand)
        self.draw_cards(self.game.bot_hand)
        self.draw_cards(self.game.board_hand)

        self.draw_buttons()

    def draw_buttons(self) -> None:
        pygame.draw.rect(self.screen, RED, self.play_card_button)
        self.center_txt("Zagraj",BLACK,self.play_card_button)

        pygame.draw.rect(self.screen, RED, self.pull_button)
        self.center_txt("Dobierz karty",BLACK,self.pull_button)

        if self.allow_sounds:
            image = 'sounds'
        else:
            image = 'no_sounds'
        self.add_image(image,self.sounds_button)

        pygame.draw.rect(self.screen, GREEN, self.main_menu_button)
        self.center_txt("Menu główne", BLACK, self.main_menu_button)

    def draw_cards(self,hand) -> None:
        for card in hand:
            self.screen.blit(card.image, card)

    def end_game(self, winner) -> None:
        end_text = self.end_font.render(f"Koniec gry, Wygrał: {winner}", True, BLACK)
        text_width, text_height = end_text.get_size()
        blit_end = (GAME_WIDTH - 300 - text_width) // 2,(GAME_HEIGHT - 300 - text_height) // 2
        self.screen.blit(end_text,blit_end)
        if self.allow_sounds:
            if winner == "komputer":
                self.sounds['lose'].play()
            else:
                self.sounds['victory'].play()

    def close(self) -> None:
        time.sleep(5)
        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    pygame.init()
    current_state = MainMenu()
    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        new_state = current_state.check_events(events)
        if new_state:
            if new_state == "menu":
                current_state = MainMenu()
            elif new_state == "settings":
                current_state = Settings()
            elif new_state == "game":
                current_state = WindowGame()

        if isinstance(current_state,WindowGame):
            if len(current_state.game.player_hand) == 0:
                current_state.draw()
                current_state.end_game("gracz")
                pygame.display.update()
                current_state.close()

            elif len(current_state.game.bot_hand) == 0:
                current_state.draw()
                current_state.end_game("komputer")
                pygame.display.update()
                current_state.close()

        current_state.draw()

        pygame.display.update()