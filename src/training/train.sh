#!/bin/bash

python main.py \
  --saved_fn 'ttnet_no_local_no_event' \
  --arch 'ttnet' \
  --no-val \
  --batch_size 32 \
  --sigma 1. \
  --thresh_ball_pos_mask 0.01 \
  --start_epoch 1 \
  --num_epochs 100 \
  --lr 0.001 \
  --lr_type 'step_lr' \
  --lr_step_size 10 \
  --lr_factor 0.2 \
  --world-size 1 \
  --rank 0 \
  --dist-backend 'nccl' \
  --multiprocessing-distributed \
  --weight_decay 0. \
  --no_local \
  --no_event \
  --global_weight 5.0 \
  --seg_weight 1.0