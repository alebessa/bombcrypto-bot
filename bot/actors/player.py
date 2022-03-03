from shared import center
from shared import im_path
from shared import log

import imagesize
from multiprocessing import Process
from multiprocessing import Queue
from pyautogui import click
from pyautogui import hold
from pyautogui import moveTo
from pyautogui import press
from pyautogui import locateCenterOnScreen
from queue import Empty
from random import uniform
from time import sleep
from time import time
import sys


class Player(Process):
    confidence_ratio = .95
    state_img_map = {
        'error': ['error', 'error2'],
        'new_map': ['new_map', 'new_map2', 'new_map3'],
        'login': ['connect-login', 'connect'],
        'main': ['treasure_mode'],
        'heroes': ['heroes_title', 'heroes_title2'],
        'playing': ['play_header', 'play_header2', 'play_header3']
    }

    def reset_player_stats(self):

        self.state = None 
        self.new_state = None

        self.last_login = None 
        self.login_delay = 60

        self.last_shift = None
        self.shift_every = 40 * 60 # 40 mins

        self.last_unknown_time = None
        self.unknown_timeout = 60

        self.last_prevent_stuck = None
        self.prevent_stuck_every = 2 * 60 # 2 mins

    def __init__(self, game, mouse_lock, logger = None, command_queue = None):
        super(Player, self).__init__()
        self.game = game
        self.mouse_lock = mouse_lock
        self.logger = logger
        self.command_queue = command_queue
        self.reset_player_stats()
        self.paused = False
        self.logger.put(log('success', f'Starting player {self.game.id}!'))

    def pull_command(self):
        try:
            return self.command_queue.get(block=False)
        except Empty:
            return False

    def check_game_state(self):

        for state, images in self.state_img_map.items():
            region = self.game.position
            try:
                self._find_any(images, region=region, timeout=1)
                return state
            except TimeoutError:
                continue
        
        return 'unknown'
    
    def update_state(self):
        self.state = self.new_state

    def _find_any(self, names, confidence = 0.999,
        region = None, timeout = 10, jitter=False):
        
        start = time()

        coords = None
        while True:
            sleep(uniform(.1, .3))
            for name in names:
                path = im_path(name, self.game.zoom)
                w, h = imagesize.get(path)
                coords = locateCenterOnScreen(
                    path,
                    **({'region': region} if region else {}),
                    **({'confidence': confidence * self.confidence_ratio} if confidence else {})
                )                    
                if coords:
                    print(f'[GAME{self.game.id}] Found image {name}: {coords}')
                    break
            if coords:
                break
            if time() - start > timeout:
                raise TimeoutError(
                    f"""[GAME{self.game.id}] Could not find any of the following images:
                    {", ".join(names)}
                    during the {timeout} seconds timeout.""")

        if jitter:
            dx = w * jitter
            dy = h * jitter
            x, y = coords
            return (int(uniform(x - dx, x + dx)), int(uniform(y - dy, y + dy)))
        
        return coords

    def _click_any(self, *args, **kwargs):
        x, y = self._find_any(*args, **kwargs)
        moveTo(x, y, duration=.01)
        sleep(uniform(.05, .1))
        click()

    def login(self):
        self._click_any(
            ['connect'],
            region=self.game.position,
            timeout=10)

        self._click_any(
            ['sign'],
            timeout=25)

    def refresh(self):
        x, y, w, h = self.game.position
        click(x + int(w/4), y + int(h/2))

        with hold('ctrl'):
            press('f5')
        
        sleep(5)

    def new_shift(self):

        self._click_any(
            ['heroes'],
            region=self.game.position,
            timeout=10)

        sleep(.666)

        try:
            tries = 0
            while coords:= self._find_any(
                ['work_all'],
                region=self.game.position,
                confidence=.9 * self.confidence_ratio,
                timeout=4):
                
                tries += 1
                if tries > 5:
                    break

                x, y = coords
                click(x, y)
                sleep(.5)

        except TimeoutError as e:
            pass

        self._click_any(
            ['x', 'x2', 'x3'],
            region=self.game.position,
            timeout=5)

        self._click_any(
            ['treasure_mode'],
            region=self.game.position,
            timeout=5)

        self.last_prevent_stuck = time()

    def prevent_stuck(self):
        self._click_any(
            ['return'],
            region=self.game.position,
            confidence=.9 * self.confidence_ratio,
            timeout=2)
        
        self._click_any(
            ['treasure_mode'],
            region=self.game.position,
            timeout=2)

    def exit_game(self):
        self._click_any(
            ['return'],
            region=self.game.position,
            confidence=.9 * self.confidence_ratio,
            timeout=5)

    def new_map(self):
        self._click_any(
            self.state_img_map['new_map'],
            region=self.game.position,
            timeout=5)

    def error(self):
        self._click_any(
            ['ok', 'x', 'x1', 'x2'],
            region=self.game.position,
            timeout=5)

    def check_command(self):

        if command := self.pull_command():

            print(f'[GAME{self.game.id}] command: {command}')
            if command == 'pause':
                self.paused = True
            elif command == 'resume':
                self.paused = False
            elif command == 'die':
                # goodbye TT_TT
                sys.exit()

    def play_loop(self):

        self.new_state = self.check_game_state()
        print(f'[GAME{self.game.id}] Found state: {self.new_state}')                

        # Unknown timer running
        if isinstance(self.last_unknown_time, float):

            # Unknown timeout reached
            if time() - self.last_unknown_time > self.unknown_timeout:
                self.last_unknown_time = None
                with self.mouse_lock:
                    self.refresh()
                    self.login()
                
            # Known state found
            if self.state == 'unknown' and self.new_state != 'unknown':
                self.last_unknown_time = None

        # Begin unknown timer
        if self.state != 'unknown' and self.new_state == 'unknown':
            self.last_unknown_time = time()

        # Login
        if self.new_state == 'login':
            
            # First login or next login attempt
            if self.state is None or time() - self.last_login > self.login_delay:
                self.last_login = time()
                with self.mouse_lock:
                    self.login()

        # Reached main menu
        if self.state != 'main' and self.new_state == 'main':
            
            # New shift needed
            if self.last_shift is None or time() - self.last_shift > self.shift_every:
                self.last_shift = time()
                with self.mouse_lock:
                    self.new_shift()

        # In-game
        if self.new_state == 'playing':
            
            print(f'[GAME{self.game.id}] New shift in: {self.shift_every - (time() - self.last_shift)}')
            print(f'[GAME{self.game.id}] Unstuck in: {self.prevent_stuck_every - (time() - self.last_prevent_stuck)}')
            
            # New shift needed
            if time() - self.last_shift > self.shift_every:
                with self.mouse_lock:
                    self.exit_game()
            
            # Prevent stuck
            elif time() - self.last_prevent_stuck > self.prevent_stuck_every:
                self.last_prevent_stuck = time()
                with self.mouse_lock:
                    self.prevent_stuck()

        # Found new map
        if self.state != 'new_map' and self.new_state == 'new_map':
            with self.mouse_lock:
                self.new_map()

        # Found error
        if self.state != 'error' and self.new_state == 'error':
            with self.mouse_lock:
                self.error()

        self.update_state()
        sleep(uniform(2.5, 3.5))

    def run(self):
        while True:
            try:
                self.check_command()

                while self.paused:
                    sleep(1)
                    self.check_command()
                    
                self.play_loop()
            except Exception as e:
                
                self.logger.put(log('error', f'[GAME{self.game.id}] Player crashed with error: "{e}". \nRespawning in 3...'))
                sleep(3)
                self.refresh()
                self.reset_player_stats()
