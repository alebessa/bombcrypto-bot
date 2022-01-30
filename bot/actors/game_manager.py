from pyautogui import locateAllOnScreen
from typing import List

from objects import Game
from shared import command
from shared import im_path
from shared import log
from shared import relative_box
from shared import RelativeDimensions


class GameManager:
    # zooms = [33, 50, 67, 75, 80, 90, 100]
    #TODO: Add support for multiple chrome zoom/resolution pairs.

    zooms = [50]
    game_dims = RelativeDimensions(
        x_offset = -340,
        y_offset = -428,
        width = 960,
        height = 600)

    def __init__(self, logger, games: List[Game] = []):
        self.games = games
        self.logger = logger

    def kill_all(self):
        for game in self.games:
            game.command_queue.put(command('die'))

    def pause_all(self):
        for game in self.games:
            game.command_queue.put(command('pause'))

    def resume_all(self):
        for game in self.games:
            game.command_queue.put(command('resume'))

    def _find_game_position(self, button_box, zoom):
        x = button_box.left
        y = button_box.top
        prop = zoom / 100

        return relative_box(x, y, self.game_dims, prop)

    def find_games(self):

        for zoom in self.zooms:
            connect_buttons = [x for x in locateAllOnScreen(im_path('connect', zoom),confidence=.9)]

            for button in connect_buttons:
                position = self._find_game_position(button, zoom)
                
                new_game_id = len(self.games) + 1
                
                game = Game(new_game_id, position, zoom)
                
                self.games.append(game)
        
        if len(self.games) == 0:
            self.logger.put(log('error', 'GameManager could not find Bombcrypto games.'))
        
        else:
            self.logger.put(log('success', f'GameManager found {len(self.games)} games!'))
