"""
# -*- coding: utf-8 -*-
-----------------------------------------------------------------------------------
# Author: Nguyen Mau Dung
# DoC: 2020.06.10
# email: nguyenmaudung93.kstn@gmail.com
# project repo: https://github.com/maudzung/TTNet-Realtime-for-Table-Tennis-Pytorch
-----------------------------------------------------------------------------------
# Description: This script for demonstration
"""

import os
import sys
import torch
from collections import deque

import cv2
import numpy as np

sys.path.append('../')

from data_process.ttnet_video_loader import TTNet_Video_Loader
from training.train_utils import get_model, load_pretrained_model
from config.config import parse_configs
from inference.post_processing import post_processing


def demo(configs):
    video_loader = TTNet_Video_Loader(configs.video_path, configs.input_size, configs.num_frames_sequence)
    result_filename = os.path.join(configs.save_demo_dir, 'results.txt')
    frame_rate = video_loader.video_fps

    configs.frame_dir = None if configs.output_format == 'text' else os.path.join(configs.save_demo_dir, 'frame')
    if not os.path.isdir(configs.frame_dir):
        os.makedirs(configs.frame_dir)

    configs.device = torch.device('cuda:{}'.format(configs.gpu_idx))

    # model
    model = get_model(configs)
    model.cuda()

    assert configs.pretrained_path is not None, "Need to load the pre-trained model"
    model = load_pretrained_model(model, configs.pretrained_path, configs.gpu_idx, configs.overwrite_global_2_local)

    model.eval()
    middle_idx = int(configs.num_frames_sequence / 2)
    queue_frames = deque(maxlen=middle_idx + 1)
    frame_idx = 0
    w_ratio = 1920. / 320.
    h_ratio = 1080. / 128.
    with torch.no_grad():
        for count, origin_imgs, resized_imgs in video_loader:
            # take the middle one
            img = np.copy(origin_imgs[3 * middle_idx: 3 * (middle_idx + 1), :, :]).transpose(1, 2, 0)
            # Expand the first dim
            resized_imgs = torch.from_numpy(resized_imgs).to(configs.device, non_blocking=True).float().unsqueeze(0)
            origin_imgs = torch.from_numpy(origin_imgs).to(configs.device, non_blocking=True).float().unsqueeze(0)
            pred_ball_global, pred_ball_local, pred_events, pred_seg = model.run_demo(origin_imgs, resized_imgs)
            prediction_global, prediction_local, prediction_seg, prediction_events = post_processing(
                pred_ball_global, pred_ball_local, pred_events, pred_seg, configs.input_size[0],
                configs.thresh_ball_pos_mask, configs.seg_thresh, configs.event_thresh)
            prediction_ball_final = [
                int(prediction_global[0] * w_ratio + prediction_local[0] - 320 / 2),
                int(prediction_global[1] * h_ratio + prediction_local[1] - 128 / 2)
            ]

            # Get infor of the (middle_idx + 1)th frame
            if len(queue_frames) == middle_idx + 1:
                frame_pred_infor = queue_frames.popleft()
                seg_img = frame_pred_infor['seg'].astype(np.uint8)
                ball_pos = frame_pred_infor['ball']
                seg_img = cv2.resize(seg_img, (1920, 1080))
                ploted_img = plot_detection(img, ball_pos, seg_img, prediction_events)

                ploted_img = cv2.cvtColor(ploted_img, cv2.COLOR_RGB2BGR)
                if configs.show_image:
                    cv2.imshow('ploted_img', ploted_img)
                    cv2.waitKey(10)
                if configs.save_demo_output:
                    cv2.imwrite(os.path.join(configs.frame_dir, '{:06d}.jpg'.format(frame_idx)), ploted_img)

            frame_pred_infor = {
                'seg': prediction_seg,
                'ball': prediction_ball_final
            }
            queue_frames.append(frame_pred_infor)

            frame_idx += 1

    if configs.output_format == 'video':
        output_video_path = os.path.join(configs.save_demo_dir, 'result.mp4')
        cmd_str = 'ffmpeg -f image2 -i {}/%05d.jpg -b 5000k -c:v mpeg4 {}'.format(
            os.path.join(configs.frame_dir), output_video_path)
        os.system(cmd_str)


def plot_detection(img, ball_pos, seg_img, events):
    """Show the predicted information in the image"""
    img = cv2.addWeighted(img, 1., seg_img * 255, 0.3, 0)
    img = cv2.circle(img, tuple(ball_pos), 5, (255, 0, 255), -1)
    event_name = 'is bounce: {}, is net: {}'.format(events[0], events[1])
    img = cv2.putText(img, event_name, (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    return img


if __name__ == '__main__':
    configs = parse_configs()
    demo(configs=configs)
