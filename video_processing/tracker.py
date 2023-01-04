import cv2
import numpy as np
import time
# unique id
import uuid
import random


class Tracker():
    def __init__(
            self, 
            model=None,
            model_size=608,
            height=720, 
            width=720, 
            dist_threshold=70,
            max_disappear=1.5,
            exit_polygon=None, 
            entry_polygon=None,
            polygon_patience=2,
    ):
        assert model is not None, "Model is not provided into tracker."
        self.model = model
        self.model_size = model_size
        
        self.height = height
        self.width = width

        # self.tracked_objects:
        # dict{id, point, last, exit_flag, entry_flag, color, exit_done, entry_done}
        self.tracked_objects = []

        self.UPDATE_DISTANCE_THRESHOLD = dist_threshold
        self.MAX_AGE = max_disappear
        self.POLYGON_PATIENCE = polygon_patience
        
        entry_polygon, exit_polygon = self.init_polygons(
            entry_polygon, exit_polygon)
        self.entry_polygon = entry_polygon
        self.exit_polygon = exit_polygon

    def update(self, img, convert_to_rgb=True):
        """
        Update the tracked objects
        Input:
            img: the image with the objects points
            object_locations: list[x,y, width, height]
        """
#         fps_start = time.time() 
        img = cv2.resize(img, (self.width, self.height))
        if convert_to_rgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get the head points
        object_locations = self.detect_objects(img)

        if len(self.tracked_objects) == 0:
            self.tracked_objects = [
                {
                    'id': uuid.uuid4(),
                    'point':point, 
                    'last':time.time(), 
                    'exit_flag':False, 
                    'entry_flag':False,
                    'color': self.random_color(),
                    'exit_done':False,
                    'entry_done':False,} for point in object_locations]
        else:
            self.add_or_update_points(object_locations)
            img = self.clean_old_points(img)

        return self.tracked_objects, img

    def add_or_update_points(self, object_locations):
        """
        Compare the new objects with the tracked objects, 
        if the distance is less than the threshold,
        then update the tracked objects with the new objects.
        Otherwise, add a new object to the tracked object list.
        """
        for new_point in object_locations:
            distances = [self.calc_distance(
                new_point, tracked_point['point']) for tracked_point in self.tracked_objects]
            # find minimum distance along with its index in "distances"
            min_dist = min(distances)
            min_dist_index = distances.index(min_dist)
            if min_dist < self.UPDATE_DISTANCE_THRESHOLD:
                self.tracked_objects[min_dist_index]['point'] = new_point
                self.tracked_objects[min_dist_index]['last'] = time.time()
            else:
                # append and get the index of the new point
                self.tracked_objects.append(
                    {
                        'id': uuid.uuid4(),
                        'point':new_point,
                        'last':time.time(),
                        'exit_flag':False,
                        'entry_flag':False,
                        'color': self.random_color(),
                        'exit_done':False,
                        'entry_done':False,
                     })

    def clean_old_points(self, img):
        """
        Clean the old points

        Return:
            img
        """
        # clean the old points that did not used for long time
        for index, track in enumerate(self.tracked_objects):
            if time.time() - track['last'] > self.MAX_AGE:
                # iterate through the tracked_head_point and remove point where 1st index is greater than MAX_AGE
                self.tracked_objects.remove(track)

            # If the object is in the exit polygon,
            if cv2.pointPolygonTest(self.exit_polygon, (track['point'][0], track['point'][1]), False) == 1:
                if track['entry_flag'] == True:
                    track['exit_done'] = True
                track['exit_flag'] = True

            # if the point is in the entry polygon, then set the entry flag to True
            if cv2.pointPolygonTest(self.entry_polygon, (track['point'][0], track['point'][1]), False) == 1:
                if track['exit_flag'] == True:
                    track['entry_done'] = True
                track['entry_flag'] = True
        return img

    def calc_distance(self, obj1, obj2):
        distance = np.sqrt((obj1[0] - obj2[0])**2 + (obj1[1] - obj2[1])**2)
        return distance

    def detect_objects(self, img):
        """
        Detect object locations by using the model
        """
        object_locations = []
        
        results = self.model(img)
        
        # iterate through detected objects
        for i in range(len(results.pandas().xyxy[0])):
            x1, y1, x2, y2, conf, cls, name = results.pandas().xyxy[0].iloc[i]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # find the middle point of the object
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2
            x_mid, y_mid = int(x_mid), int(y_mid)

            # find width and height of the objects
            width = x2 - x1
            height = y2 - y1

            # append the middle point to the list
            object_locations.append([x_mid, y_mid, width, height])

        return object_locations

    def init_polygons(self, entry_polygon, exit_polygon, scale=1.0):
        width = self.width
        height = self.height
        # convert polygons to contour
        exit_polygon = np.array(exit_polygon)
        entry_polygon = np.array(entry_polygon)

        # multiply all values in polygon by width and height
        exit_polygon = exit_polygon * np.array([width, height])
        entry_polygon = entry_polygon * np.array([width, height])

        # scale the polygon
        exit_polygon = exit_polygon * scale
        entry_polygon = entry_polygon * scale
        
        # change dtype to int32
        exit_polygon = exit_polygon.astype(np.int32)
        entry_polygon = entry_polygon.astype(np.int32)
        
        return entry_polygon, exit_polygon

    def random_color(self):
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))