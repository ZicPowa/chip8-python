from pathlib import Path

import pygame
from display import DEFAULT_HEIGHT, DEFAULT_WIDTH

roms_folder = "test_roms"

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        font = pygame.font.Font(None, 28)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class GUI:
    def __init__(self):
        self.x = DEFAULT_WIDTH
        self.y = DEFAULT_HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption("Chip8 Emulator Menu")
        self.clock = pygame.time.Clock() 
        self.running = True
        self.dt = 0
        self.buttons = []
        self.rom_files = self._load_rom_files()
        self.selected_rom = self.rom_files[0] if self.rom_files else None
        self._create_buttons()

    def _load_rom_files(self):
        folder_path = Path(roms_folder)
        if not folder_path.exists():
            return []

        return sorted(path.name for path in folder_path.iterdir() if path.is_file())

    def _create_buttons(self):
        btn_w, btn_h = 120, 40
        margin = 10
        y = self.y - btn_h - margin
        self.buttons.append(Button(
            margin, y, btn_w, btn_h,
            "Load ROM", (50, 120, 200), (70, 150, 230),
            self.on_load_rom
        ))
        self.buttons.append(Button(
            margin * 2 + btn_w, y, btn_w, btn_h,
            "Load Save", (200, 80, 80), (230, 110, 110),
            self.on_load_save
        ))

    def _list_item_rect(self, index):
        left = 260
        top = 20 + index * 34
        width = self.x - left - 20
        height = 28
        return pygame.Rect(left, top, width, height)

    def on_load_rom(self):
        print(self.selected_rom if self.selected_rom else "No ROM selected")
        self.running = False

    def on_load_save(self):
        print("Load Save clicked")

    def _draw_rom_list(self):
        title_font = pygame.font.Font(None, 30)
        item_font = pygame.font.Font(None, 26)

        title = title_font.render("ROM files", True, (240, 240, 240))
        self.screen.blit(title, (260, 0))

        if not self.rom_files:
            empty = item_font.render("No files found in test_roms", True, (220, 180, 180))
            self.screen.blit(empty, (260, 40))
            return

        mouse_pos = pygame.mouse.get_pos()
        for index, rom_file in enumerate(self.rom_files):
            item_rect = self._list_item_rect(index)
            is_selected = rom_file == self.selected_rom
            is_hovered = item_rect.collidepoint(mouse_pos)
            color = (70, 130, 210) if is_selected else (70, 70, 70)
            if is_hovered and not is_selected:
                color = (90, 90, 90)

            pygame.draw.rect(self.screen, color, item_rect, border_radius=4)
            label = item_font.render(rom_file, True, (255, 255, 255))
            self.screen.blit(label, (item_rect.x + 8, item_rect.y + 3))

    def _handle_rom_list_click(self, pos):
        for index, rom_file in enumerate(self.rom_files):
            if self._list_item_rect(index).collidepoint(pos):
                self.selected_rom = rom_file
                return True
        return False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self._handle_rom_list_click(event.pos):
                        continue
                for btn in self.buttons:
                    btn.handle_event(event)

            self.screen.fill((30, 30, 30))

            self._draw_rom_list()

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000.0

        pygame.quit()
        return self.selected_rom
        
