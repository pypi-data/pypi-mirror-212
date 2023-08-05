# from tensorflow.python.summary.summary_iterator import summary_iterator
import torch
from tensorboard.backend.event_processing import event_accumulator
import os


event_file = "../../tb_logger/3DGAN_A01-k2d10-k2d100-with-ReLU/events.out.tfevents.1633723099.cbce57b16285.559.0"
# another_event = "events.out.tfevents.1633722986.cbce57b16285.403.0"

ea = event_accumulator.EventAccumulator(event_file, size_guidance={event_accumulator.SCALARS: 0})
ea.Reload()
print(ea.Tags())
for index, scaler in enumerate(ea.Scalars('D_fake')):
    print(scaler.value)
    if index == 20:
        break
