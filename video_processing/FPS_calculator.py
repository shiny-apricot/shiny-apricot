import time
from my_logger import logger
class FPS:
    def __init__(self, sleep=0):
        self.time_start = 0
        self.time_end = 0
        self.fps = 0
        self.fps_list = []
        self.sleep = sleep

    def start(self):
        self.time_start = time.time()

    def end(self, text="", print_fps=20):
        self.time_end = time.time()
        self.fps = 1 / (self.time_end - self.time_start)
        self.fps_list.append(self.fps)
        if len(self.fps_list) > print_fps:
            logger.info(f"## {text} FPS: {sum(self.fps_list) / len(self.fps_list)}")
            self.fps_list = []
            # time.sleep(self.sleep)
    
    def fps_reset(self):
        self.fps_list = []