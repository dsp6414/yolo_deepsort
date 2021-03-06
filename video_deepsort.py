import logging

from action.action_Identify import ActionIdentify
from action.actions import *
from deep_sort import DeepSort
from yolo3.detect.video_detect import VideoDetector
from yolo3.models import Darknet

if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    model = Darknet("config/yolov4.cfg", img_size=608)
    model.load_darknet_weights("weights/yolov4.weights")
    model.to("cuda:0")

    # 跟踪器
    tracker = DeepSort("weights/ckpt.t7",
                       min_confidence=0.5,
                       use_cuda=True,
                       nn_budget=30,
                       n_init=10,
                       max_iou_distance=0.7,
                       max_dist=0.2,
                       max_age=70)

    # 动作识别器
    # action_id = ActionIdentify(actions=[TakeOff(4, delta=(0, 1)),
    #                                     Landing(4, delta=(2, 2)),
    #                                     Glide(4, delta=(1, 2)),
    #                                     FastCrossing(4, speed=0.2),
    #                                     BreakInto(0, timeout=2)],
    #                            max_age=30,
    #                            max_size=8)

    video_detector = VideoDetector(model, "config/coco.names",
                                   # font_path="font/sarasa-bold.ttc",
                                   font_size=5,
                                   thickness=4,
                                   skip_frames=2,
                                   conf_thres=0.5,
                                   class_mask=[0, 2, 4],
                                   nms_thres=0.2,
                                   tracker=tracker,
                                   half=True)

    for image, detections, _ in video_detector.detect(0,
                                                      # output_path="../data/output.ts",
                                                      real_show=True,
                                                      skip_secs=0):
        pass
