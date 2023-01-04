import cv2
import os
import yaml
import CONFIG
import datetime
from my_logger import logger


class VideoUtils:
    def __init__(self, output_path='videos', frame_rate=14):
        self.output_path = output_path
        self.frame_rate = frame_rate
        self.video_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
        
        self.save_width = CONFIG.save_width
        self.save_height = CONFIG.save_height
        is_record = CONFIG.record
            
        self.video_writer = cv2.VideoWriter(os.path.join(output_path, self.video_name), 
                                            cv2.VideoWriter_fourcc(*'mp4v'), 
                                            frame_rate, 
                                            (self.save_width, self.save_height))
        if is_record:
            logger.info(f"VideoWriter initialized with output path: {self.output_path},\n video name: {self.video_name},\n frame rate: {frame_rate},\n frame size: { (self.save_width, self.save_height) }")
        self.start_time = datetime.datetime.now()
        

        
    def record_frame(self, frame=None, finish_record=False, plate_text=''):
        if finish_record:
            self.video_writer.release()
            return
        # if more than 30 minutes passed, finish recording and start a new one
        if (datetime.datetime.now() - self.start_time).seconds > 1800:
            self.video_writer.release()
            logger.info(f"Video recording finished. Video saved to {self.output_path}")
            self.video_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
            self.video_writer = cv2.VideoWriter(os.path.join(self.output_path, self.video_name),
                                                cv2.VideoWriter_fourcc(*'mp4v'),
                                                14,
                                                (self.save_width, self.save_height))
            logger.info(f"VideoWriter re-initialized with video name: {self.video_name}, { (self.save_width, self.save_height) }")
            self.start_time = datetime.datetime.now()
        if frame is not None: 
            frame = cv2.resize(frame, (self.save_width, self.save_height))            
        self.video_writer.write(frame)
        