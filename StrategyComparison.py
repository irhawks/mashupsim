#!/usr/bin/env python3
# coding:utf-8

from mashupsim.simlibs import *

from mashupsim.strategy.NonIterative import *
from mashupsim.strategy.OptimizedIteration import *
from mashupsim.strategy.OptimizedROI import *

from mashupsim.roles.Customer import *
from mashupsim.roles.Workload2 import *


from mashupsim.helpers import *

import simpy

import random

### 如果设计自己的实验

class MySimulator(SimulationLogic) :

    def observer(self) :

        """只需要记录那些希望添加到数据观察中的内容，建议由每个实验定制"""
        self.kwargs.update({'开发阶段' : self.state})
        self.kwargs.update({'loads' : self.val_service_load})
        self.kwargs.update({'action' : self.val_action_name})
        self.kwargs.update({'全部成本' : self.val_total_cost}) ## 额外的运行支出
        self.kwargs.update({'投资回报率' : self.val_ROI})

        #self.kwargs.update({'sf_overall' : self.val_sf_overall if self.val_sf_overall else 0})
        if self.val_running_units : 
            self.kwargs.update({'质量属性' : self.val_running_quality[0]})

class Strategy1(NonIterativeStrategy) :

    pass

class Strategy2(OptimizedIteration) :

    pass

class Strategy3(OptimizedROI) :

    pass

class MyStrategySim1(MySimulator, Strategy1) :

    pass
class MyStrategySim2(MySimulator, Strategy2) :

    pass
class MyStrategySim3(MySimulator, Strategy3) :

    pass

class MyCustomer(Customer) :
    #def sf_quality(self, *args, **kwargs) :
    #    return 1.0
    pass
class MyWorkload(Workload2) :

    #def do_composition(self) :
    #    pdim = len(self.env_s[0].p)
    #    qdim = len(self.env_s[0].q)
    #    fdim = len(self.env_s[0].f)
    #    developed = ServiceUnit(str(self.judging_units)).randomize_std(pdim=pdim,qdim=qdim,fdim=fdim)
    #    self.developed_service = developed
    #    self.developed_units = self.judging_units
    #    self.judging_units = []

    #    self.action_cost = self.cost_ref[1]
    #    self.action_time = self.time_ref[2]
    #    self._action_name = "compositing"
    pass

env_s = [ServiceUnit(i).randomize_std() for i in range(0,20)]
print("服务方案数", len(env_s))
env_u = MyCustomer().randomize() 
env_w = MyWorkload(env_s = env_s, env_u = env_u)

import copy

### 固定的因素
env = simpy.Environment()
exp1 = MyStrategySim1(env, env_s=copy.deepcopy(env_s),env_u=copy.deepcopy(env_u), env_w=copy.deepcopy(env_w))
env = simpy.Environment()
exp2 = MyStrategySim2(env, env_s=copy.deepcopy(env_s),env_u=copy.deepcopy(env_u), env_w=copy.deepcopy(env_w))
env = simpy.Environment()
exp3 = MyStrategySim3(env, env_s=copy.deepcopy(env_s),env_u=copy.deepcopy(env_u), env_w=copy.deepcopy(env_w))

exp1.run(until=2000)
exp2.run(until=100)
exp3.run(until=100)

import sys
#print(pd.DataFrame(std.history))

for exp in [exp1, exp2, exp3] : 

    pd.DataFrame(exp.history).to_csv(sys.stdout)
    vis = Visualizer(pandas=pd.DataFrame(exp.history))

    #vis.show_n_vars_on_right([['sf_quality','sf_price', 'sf_overall']])
    from itertools import cycle
    vis.show_n_vars_on_right([['投资回报率'],['全部成本'], ['质量属性'], ['开发阶段']]
            , line_styles = cycle(['-','-.','None', 'None', '-.'])
            , markers = cycle(['None', 'None', '.', 'v', '^', '<'])
            )

#vis.show_n_vars_on_right([['sf_quality','sf_price', 'sf_overall']])
#vis2.show_n_vars_on_right([['全部成本', '组件支出', '开发支出', '运行支出', '服务收益'], ['投资回报率']])

#vis.show_n_vars_on_right([['服务收益'], ['服务负载'], ["价格"]])
#vis.show_n_vars_on_right([['sf_quality'],['sf_price'], ['loads'], ['quality']])
#vis.show_n_vars_on_right([['sf_quality']])
