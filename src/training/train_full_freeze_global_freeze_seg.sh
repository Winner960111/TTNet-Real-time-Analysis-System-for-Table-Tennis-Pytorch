#!/bin/bash

python main.py \
  --saved_fn 'ttnet_full_freeze_global_freeze_seg' \
  --arch 'ttnet' \
  --no-val \
  --batch_size 32 \
  --num_workers 8 \
  --sigma 1. \
  --thresh_ball_pos_mask 0.01 \
  --start_epoch 1 \
  --num_epochs 21 \
  --lr 0.001 \
  --lr_type 'step_lr' \
  --lr_step_size 5 \
  --lr_factor 0.2 \
  --world-size 1 \
  --rank 0 \
  --dist-backend 'nccl' \
  --multiprocessing-distributed \
  --weight_decay 0. \
  --global_weight 0. \
  --seg_weight 0. \
  --event_weight 2. \
  --local_weight 1. \
  --pretrained_path ../../checkpoints/ttnet_no_local_no_event/ttnet_no_local_no_event_epoch_21.pth \
  --overwrite_global_2_local \
  --freeze_seg \
  --freeze_global