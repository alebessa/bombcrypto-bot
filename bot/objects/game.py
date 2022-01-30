from multiprocessing import Process
from multiprocessing import Queue

class Game():

    def __init__(self, id, position, zoom, player = None, command_queue: Queue = None):
        self.id = id
        self.position = position
        self.zoom = zoom
        self.player = player
        self.command_queue = command_queue