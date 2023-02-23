import os
import paddle
import paddle.fluid as fluid
from paddle.fluid.optimizer import AdamOptimizer
import numpy as np
import argparse
from utils import AverageMeter
from 