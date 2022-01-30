
# [START] Hacky fix for multi monitors 
# (https://github.com/python-pillow/Pillow/issues/1547)
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
# [END]
# [START] Hacky fix for PyInstaller + --onefile + multiprocessing 
# (https://github.com/pyinstaller/pyinstaller/issues/3957)
from multiprocessing import freeze_support
freeze_support()
# [END]


from engine import FuzzyBomberEngine
from gui import frontend

from os import system

def main():
    engine = FuzzyBomberEngine()
    frontend(engine)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        system('pause')