import numpy as np
import pandas as pd
import os, re
from functools import partial

TS = 'ts'
INDICIES=['file', 'heartbeat']
IMU_DATA_COLS = ['ax','ay','az','gx','gy','gz']
IMU_COLS = IMU_DATA_COLS + [TS]
BP_COLS = ['pp','sbp','dbp']
INFO_COLS = ['patient','test_type','test_num']
