from subprocess import TimeoutExpired
from shared import center
from shared import im_path
from shared import max_diff_centroid
from shared import relative_box
from shared import RelativeDimensions

import imagesize
from PIL.Image import FLIP_LEFT_RIGHT
from pyautogui import click
from pyautogui import hold
from pyautogui import mouseDown
from pyautogui import mouseUp
from pyautogui import moveTo
from pyautogui import press
from pyautogui import locateOnScreen
from pyautogui import locateCenterOnScreen
from pyautogui import scroll
from pyscreeze import screenshot
from random import random
from random import randint
from random import uniform
from time import sleep
from time import time

class Player:
    confidence_ratio = .95
    
    def __init__(self, game, mouse_lock):

        self.game = game
        self.mouse_lock = mouse_lock

        self.state_img_map = {
            'error': ['error'],
            'new_map': ['new_map', 'new_map2'],
            'captcha': ['captcha'],
            'login': ['connect'],
            'main': ['treasure_mode'],
            'heroes': ['heroes_title'],
            'playing': ['play_header', 'play_header2']
        }
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

        self.captcha_dims = RelativeDimensions(
            x_offset = 280,
            y_offset = 177,
            width = 400,
            height = 265
        )

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
        region = None, timeout = 10, jitter=.25):
        
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
        x, y= self._find_any(*args, **kwargs)
        moveTo(x, y, duration=uniform(.2, .333))
        sleep(uniform(.05, .2))
        click()

    def solve_captcha(self):
        """DEPRECATED"""
        # find captcha_box
        x = self.game.position.left
        y = self.game.position.top
        prop = self.game.zoom / 100

        captcha_box = relative_box(x, y, self.captcha_dims, prop)

        # get piece_mask from rightmost side
        piece_im_w = 70
        piece_im_h = 160
        piece_im_y_offset = -8


        piece_mask_box = relative_box(
            captcha_box.left,
            captcha_box.top,
            RelativeDimensions(
                x_offset = self.captcha_dims.width - 5 - piece_im_w,
                y_offset = piece_im_y_offset,
                width = piece_im_w,
                height = piece_im_h),
            prop)
        
        piece_mask_im = screenshot(region = piece_mask_box)
        flipped_piece_mask_im = piece_mask_im.transpose(FLIP_LEFT_RIGHT)


        # get piece_centroid using horizontally flipped mask
        piece_box = relative_box(
            captcha_box.left,
            captcha_box.top,
            RelativeDimensions(
                x_offset = 5,
                y_offset = piece_im_y_offset,
                width = piece_im_w,
                height = piece_im_h),
            prop)
        piece_im = screenshot(region = piece_box)

        piece_relative_x, piece_relative_y = max_diff_centroid(
            piece_im,
            flipped_piece_mask_im
        )

        piece_centroid = (
            piece_box.left + piece_relative_x,
            piece_box.top + piece_relative_y)
        
        # find captcha_start
        captcha_start_centroid = self._find_any(
            [
                'captcha/drag_start',
                'captcha/drag_start2',
                'captcha/drag_start3'
            ],
            region=captcha_box,
            timeout=2,
            jitter=False)

        
        # mouseDown(captcha_start_centroid)
        moveTo(captcha_start_centroid, duration=.2)
        mouseDown()


        # overdrag to right
        moveTo(
            x = captcha_box.left + captcha_box.width - 10,
            y = captcha_start_centroid.y,
            duration=.4)
        

        # find captcha_end
        captcha_end_centroid = self._find_any(
            [
                'captcha/drag_end',
                'captcha/drag_end2',
                'captcha/drag_end3'
            ],
            region=captcha_box,
            timeout=2,
            jitter=False)


        # find dragged_piece_centroid
        dragged_piece_im = screenshot(region = piece_mask_box)
        
        (dragged_piece_relative_x,
        dragged_piece_relative_y) = max_diff_centroid(
            dragged_piece_im,
            piece_mask_im)

        dragged_piece_centroid = (
            piece_mask_box.left + dragged_piece_relative_x,
            piece_mask_box.top + dragged_piece_relative_y)

        # find prop
        prop = (
            (captcha_end_centroid.x - captcha_start_centroid.x)
            /
            (dragged_piece_centroid[0] - piece_centroid[0])
        )


        # find piece_slot_centroid
        captcha_img = screenshot(region = captcha_box)
        sleep(.4)
        captcha_img2 = screenshot(region = captcha_box)

        (piece_slot_relative_x,
        piece_slot_relative_y) = max_diff_centroid(
            captcha_img,
            captcha_img2)
        
        piece_slot_centroid = (
            captcha_box.left + piece_slot_relative_x,
            captcha_box.top + piece_slot_relative_y)
        
        # find drag dist
        drag_dist = prop * (piece_slot_centroid[0] - piece_centroid[0])
        drag_to_x = captcha_start_centroid.x + drag_dist
        drag_to_y = captcha_start_centroid.y

        
        # drag and release click
        moveTo(x=drag_to_x, y=drag_to_y, duration=.3)
        mouseUp()

    def login(self):
        self._click_any(
            ['connect'],
            region=self.game.position,
            timeout=10)

        try:
            sleep(1)
            while self._find_any(
            ['captcha'],
            region=self.game.position,
            confidence=.95 * self.confidence_ratio,
            timeout=2):
                self.solve_captcha()
        except TimeoutError as e:
            print('Captcha solved!')

        self._click_any(
            ['sign'],
            timeout=10)

    def refresh(self):
        x, y = center(self.game.position)
        click(x, y)

        with hold('ctrl'):
            press('f5')
        
        sleep(5)

        self.login()

    def new_shift(self):

        self._click_any(
            ['heroes'],
            region=self.game.position,
            timeout=10)

        try:
            if self._find_any(
            ['captcha'],
            region=self.game.position,
            timeout=5):
                self.solve_captcha()
        except TimeoutError:
            pass

        self._click_any(
            ['disabled_work', 'enabled_work'],
            region=self.game.position,
            confidence=.9 * self.confidence_ratio,
            timeout=10,

        )

        for _ in range(60):
            sleep(random() / 10)
            scroll(-randint(0,4))

        while True:
            try:
                x, y = self._find_any(
                    ['disabled_work'],
                    region=self.game.position,
                    timeout=3)
                moveTo(x, y, duration = .2)
                click()
            except TimeoutError:
                break
        
        self._click_any(
            ['x', 'x2'],
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
            ['new_map'],
            region=self.game.position,
            timeout=5)

        try:
            if self._find_any(
            ['captcha'],
            region=self.game.position,
            timeout=5):
                self.solve_captcha()
        except TimeoutError:
            pass

    def error(self):
        self._click_any(
            ['ok', 'x'],
            region=self.game.position,
            timeout=5)

    def play(self):

        while True:

            self.new_state = self.check_game_state()
            print(f'[GAME{self.game.id}] Found state: {self.new_state}')                

            # Unknown timer running
            if isinstance(self.last_unknown_time, float):

                # Unknown timeout reached
                if time() - self.last_unknown_time > self.unknown_timeout:
                    self.last_unknown_time = None
                    with self.mouse_lock:
                        self.refresh()
                    
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


def spawn_player(game, mouse_lock):
    Player(game, mouse_lock).play()