
# from collections import deque
from pathlib import Path
import sys
# from string import ascii_lowercase

import pygame

import setup_syspath  # noqa
from auraboros import engine
from auraboros.utils import AssetFilePath, draw_grid
from auraboros.gametext import GameText, Font2
from auraboros.gamescene import Scene, SceneManager
from auraboros.gameinput import Keyboard
from auraboros.oldold_ui import GameMenuSystem, GameMenuUI, MsgWindow
from auraboros.particle import Emitter
from auraboros import global_

engine.init(caption="Test Particle System")

AssetFilePath.set_asset_root(Path(sys.argv[0]).parent / "assets")

GameText.setup_font(
    Font2(AssetFilePath.font("misaki_gothic.ttf"), 16), "misakigothic")


class DebugScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyboard["menu"] = Keyboard()
        self.keyboard.set_current_setup("menu")
        self.menusystem = GameMenuSystem()
        self.keyboard["menu"].register_keyaction(
            pygame.K_UP, 0, 122, 122, self.menusystem.menu_cursor_up)
        self.keyboard["menu"].register_keyaction(
            pygame.K_DOWN, 0, 122, 122, self.menusystem.menu_cursor_down)
        self.keyboard["menu"].register_keyaction(
            pygame.K_z, 0, 0, 0, self.menusystem.do_selected_action)
        self.menusystem.add_menu_item(
            "play", self.run_emitter, text="Play")
        self.menusystem.add_menu_item(
            "stop", self.pause_emitter, text="STOP")
        self.menusystem.add_menu_item(
            "reset", self.reset_emitter, text="RESET")
        self.menuui = GameMenuUI(self.menusystem, GameText.font, "filled_box")
        self.menuui.padding = 4
        self.msgbox = MsgWindow(GameText.font)
        self.msgbox.padding = 4
        self.msgbox.text = "Press 'Z'"
        self.msgbox2 = MsgWindow(GameText.font)
        self.msgbox2.padding = 4
        self.msgbox3 = MsgWindow(GameText.font)
        self.msgbox3.padding = 4
        self.msgbox4 = MsgWindow(GameText.font)
        self.msgbox4.padding = 4
        self.msgbox5 = MsgWindow(GameText.font)
        self.msgbox5.padding = 4
        self.msgbox6 = MsgWindow(GameText.font)
        self.msgbox6.padding = 4
        self.testemitter = Emitter()
        self.testemitter.x = global_.w_size[0] // 2
        self.testemitter.y = global_.w_size[1] // 2

    def run_emitter(self):
        self.testemitter.reset_lifetime_count()
        self.testemitter.let_emit()

    def pause_emitter(self):
        self.testemitter.let_freeze()

    def reset_emitter(self):
        self.testemitter.reset()

    def update(self, dt):
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_UP)
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_DOWN)
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_z)
        self.menuui.set_pos_to_center()
        self.menusystem.update()
        self.msgbox2.text = \
            f"lifetime:{self.testemitter.lifetime}"
        self.msgbox2.pos[1] = \
            self.msgbox.real_size[1]
        self.msgbox3.pos[1] = \
            self.msgbox.real_size[1] +\
            self.msgbox2.real_size[1]
        self.msgbox4.pos[1] = \
            self.msgbox.real_size[1] +\
            self.msgbox2.real_size[1] +\
            self.msgbox3.real_size[1]
        self.msgbox5.pos[1] = \
            self.msgbox.real_size[1] +\
            self.msgbox2.real_size[1] +\
            self.msgbox3.real_size[1] +\
            self.msgbox5.real_size[1]
        self.msgbox6.pos[1] = \
            self.msgbox.real_size[1] +\
            self.msgbox2.real_size[1] +\
            self.msgbox3.real_size[1] +\
            self.msgbox5.real_size[1] +\
            self.msgbox5.real_size[1]
        self.testemitter.update()
        self.testemitter.erase_finished_particles()

    def draw(self, screen):
        draw_grid(screen, 16, (78, 78, 78))
        self.menuui.draw(screen)
        self.msgbox.draw(screen)
        self.msgbox2.draw(screen)
        self.testemitter.draw(screen)


scene_manager = SceneManager()
scene_manager.push(DebugScene(scene_manager))

if __name__ == "__main__":
    engine.run(scene_manager=scene_manager, fps=60)
