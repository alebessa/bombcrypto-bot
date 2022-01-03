
# [START] Hacky fix for multi monitors 
# (https://github.com/python-pillow/Pillow/issues/1547)
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
# [END]

from actors import GameManager
from actors import spawn_player

# [START] Hacky fix for PyInstaller + --onefile + multiprocessing 
# (https://github.com/pyinstaller/pyinstaller/issues/3957)
from multiprocessing import freeze_support
freeze_support()
# [END]

from multiprocessing import Lock
from multiprocessing import Process
from os import system
from time import sleep

def main():
    
    
    print('Please move and/or resize this window in order to unblock any BombCrypto browser window.')
    print()
    system('pause')

    game_manager = GameManager()
    game_manager.find_games()
    mouse_lock = Lock()
    
    players = []
    for game in game_manager.games:
        a = Process(target=spawn_player, args=(game, mouse_lock))
        a.daemon = True
        a.start()
        players.append(a)

    while True:
        sleep(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        system('pause')