import numpy as np
import pandas as pd
import os, re
from functools import partial

INDICIES=['file', 'heartbeat']
IMU_DATA_COLS = ['ax','ay','az','gx','gy','gz']
IMU_TS = 'ts'
IMU_COLS = IMU_DATA_COLS + [IMU_TS]
BP_COLS = ['pp','sbp','dbp']
