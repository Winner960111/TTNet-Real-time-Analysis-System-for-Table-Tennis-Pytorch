#!/bin/bash

python demo.py \
  --saved_fn 'demo' \
  --arch 'ttnet' \
  --gpu_idx 0 \
  --pretrained_path ../../checkpoints/ttnet_3rd_phase/ttnet_3rd_phase_epoch_9.pth \
  --seg_thresh 0.5 \
  --event_thresh 0.5 \
  --thresh_ball_pos_mask 0.05 \
  --video_path ../../dataset/test/videos/test_6.mp4 \
  --show_image \
  --save_demo_output