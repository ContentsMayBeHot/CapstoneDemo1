import replayparser as rp
import os
import numpy as np
from operator import itemgetter
import skimage.io
import cv2
import time


class OrderedList:
    def __init__(self, replay, frames_path):
        temp_list = []
        for file_name in os.listdir(frames_path):
            if file_name != ".DS_Store":
                f = open("data/frames/sample/" + file_name, "rb")
                frame_num = float(file_name[:-3])
                data = np.load(f)
                temp_list.append((frame_num, data))
                f.close()

        player = replay.players[1]
        for action in player.actions:
            temp_list.append((float(action.frame_index), action.type))

        temp_list.sort(key=itemgetter(0))
        self.list = []
        self.frame_action_packager(temp_list)

    def frame_action_packager(self, sorted_list):
        actions = []
        for item in sorted_list:
            if not isinstance(item[1], rp.ActionType):
                self.list.append(Package(item, actions))
                actions = []
            else:
                actions.append(item[1])


class Package:
    def __init__(self, frame, action_list):
        self.frame = frame
        self.action_list = action_list


if __name__ == "__main__":
    replay = rp.Replay("data/replay.roa")
    events = OrderedList(replay, "data/frames/sample/")

    for e in events.list:
        actions_string = ""
        for action in e.action_list:
            actions_string += str(action) + "\n"
        skimage.io.imsave('output/tmp.png', e.frame[1])
        f = open("output/tmp.txt", "w+")
        f.write(actions_string)
        f.close()
        print("frame", e.frame[0])
        time.sleep(1)
    print("OWO: it doesn't error")
