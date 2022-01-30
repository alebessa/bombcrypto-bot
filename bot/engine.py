from actors import GameManager
from actors import Player

import atexit
from multiprocessing import Lock
from multiprocessing import Queue
from queue import Empty


class FuzzyBomberEngine():

    def __init__(self):
        self.log_queue = Queue()
        self.game_manager = GameManager(logger = self.log_queue)
        self.mouse_lock = Lock()
        self.players = []

    def find_games(self):
        self.game_manager.find_games()
        return len(self.game_manager.games)

    def assign_players(self):
        for game in self.game_manager.games:
            if not game.player:
                game.command_queue = Queue()
                player = Player(game, self.mouse_lock, self.log_queue, game.command_queue).start()
                self.players.append(player)
            
        atexit.register(self.kill_players)

    def kill_players(self):
        self.game_manager.kill_all()

    def start(self):
        self.assign_players()

    def pause(self):
        self.game_manager.pause_all()

    def resume(self):
        self.game_manager.resume_all()

    def pull_log(self):
        try:
            return self.log_queue.get(block=False)
        except Empty:
            return False