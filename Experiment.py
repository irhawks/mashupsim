#!/usr/bin/env python3
# coding:utf-8

from mashupsim.simlibs import *

from mashupsim.strategy.Baseline import *

from mashupsim.roles.Customer import *
from mashupsim.roles.Workload import *

from mashupsim.helpers import *


## -----------------------------------------------------------------
## -----------------------------------------------------------------

import simpy


import random

class Experiment :

    def run(self) :
        pass
    def show(self) :
        pass
    pass


class Experiment (Experiment):

    def __init__(self
        , env_s = [ServiceUnit(i).randomize_std() for i in range(0,30)]
        , env_u = Customer().randomize()) :
        """
        默认初始化
        """
        self.env_s = env_s
        self.env_u = env_u
        self.env_w = Workload(env_s = self.env_s, env_u = self.env_u)
        self.default_conf = {
                'env_s' : self.env_s
                , 'env_w' : self.env_w
                , 'env_u' : self.env_u
            }

    def run_with(self, time=200, **kwargs) :

        """
        单个实验的参数，执行单个实验的配置
        """

        self.default_conf.update(kwargs)
        
        ## 执行模拟器
        env = simpy.Environment()
        std = BaselineStrategy(env, **self.default_conf)
        std.run(until=time)
        self.result = std.history
        self.pandas = pd.DataFrame(self.result)
        return self.result

    def save_list(self, filename) :

        open(filename, 'w').write(json.dumps(self.std.history))

    def save_pandas(self, filename) :

        self.pandas.to_csv(open(filename, 'w'))

    def test() : 

        exp_inst = StandardExperiment()
        exp_inst.run()

class GroupExperiment (Experiment):

    def __init__(self
        , env_s = [ServiceUnit(i).randomize_std() for i in range(0,30)]
        , env_u = Customer().randomize()) : 
        """
        默认初始化
        """
        self.env_s = env_s
        self.env_u = env_u
        self.env_w = Workload(env_s = self.env_s, env_u = self.env_u)
        self.default_conf = {
                'env_s' : self.env_s
                , 'env_w' : self.env_w
                , 'env_u' : self.env_u
            }
        self.group_confs=[{}]

    def run_with(self, **group_confs)  :
        
        """
        这里的args指的是针对每个实验的配置项，一组对比实验
        """

        self.group_results = [Experiment.run_with(self, **i) for i in self.group_confs]
        return self.group_results

    def save(self, filename) :

        open(filename, 'w').write(json.dumps(self.group_results))

### 如果设计自己的实验


"""
class ExperimentFlow (GroupExperiment, Visualizer):
    pass

### 如何做自己的实验
env_s = [ServiceUnit(i).randomize_std() for i in range(0,30)]
env_u = Customer().randomize() 

myexp = ExperimentFlow()
myexp.run_with(time=400)
myexp.twins_show_consumer()
"""
