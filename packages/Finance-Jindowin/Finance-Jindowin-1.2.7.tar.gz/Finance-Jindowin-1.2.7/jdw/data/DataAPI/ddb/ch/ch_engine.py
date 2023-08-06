# -*- coding: utf-8 -*-
import os, six, itertools
import numpy as np
import pandas as pd

import pdb
from jdw.kdutils.singleton import Singleton
from jdw.data.DataAPI.ddb.fetch_engine import FetchEngine


@six.add_metaclass(Singleton)
class FetchCHEngine(FetchEngine):

    def __init__(self):
        super(FetchCHEngine, self).__init__('kd', os.environ['DDB_URL'])