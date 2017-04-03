#!/usr/bin/env python3
# coding:utf-8

from mashupsim.simlibs import *

from mashupsim.strategy.Baseline import *

from mashupsim.roles.Customer import *
from mashupsim.roles.Workload2 import *

from mashupsim.helpers import *

import simpy

import random

### 如果设计自己的实验

class MySimulator(SimulationLogic) :

    def observer(self) :

        """只需要记录那些希望添加到数据观察中的内容，建议由每个实验定制"""
        self.kwargs.update({'state' : self.state})
        self.kwargs.update({'loads' : self.val_service_load})
        #self.kwargs.update({'sf_overall' : self.val_sf_overall if self.val_sf_overall else 0})
        if self.val_running_units :
            self.kwargs.update({'质量满意度' : self.val_sf_quality})
            self.kwargs.update({'价格满意度' : self.val_sf_price})
            self.kwargs.update({'整体满意度' : self.val_sf_overall})
            self.kwargs.update({'协议满意度' : self.val_sf_assigned})
        else :
            pass

class MyStrategy(BaselineStrategy) :

    pass

class MyStrategySim(MySimulator, MyStrategy) :

    pass

class MyCustomer(Customer) :
    #def sf_quality(self, *args, **kwargs) :
    #    return 1.0
    pass
class MyWorkload(Workload2) :

    def do_composition(self) :
        pdim = len(self.env_s[0].p)
        qdim = len(self.env_s[0].q)
        fdim = len(self.env_s[0].f)
        developed = ServiceUnit(str(self.judging_units)).randomize_std(pdim=pdim,qdim=qdim,fdim=fdim)
        self.developed_service = developed
        self.developed_units = self.judging_units
        self.judging_units = []

        self.action_cost = self.cost_ref[1]
        self.action_time = self.time_ref[2]
        self._action_name = "compositing"
    pass

env = simpy.Environment()
env_s = [ServiceUnit(i).randomize_std() for i in range(0,30)]
env_u = MyCustomer().randomize() 
env_w = MyWorkload(env_s = env_s, env_u = env_u)
std = MyStrategySim(env, env_s=env_s,env_u=env_u, env_w=env_w)
std.run(until=300)

import sys
#print(pd.DataFrame(std.history))
pd.DataFrame(std.history).to_csv(sys.stdout)

vis = Visualizer(pandas=pd.DataFrame(std.history))

#vis.show_n_vars_on_right([['sf_quality','sf_price', 'sf_overall']])
vis.show_n_vars_on_right([['质量满意度','价格满意度', '整体满意度', '协议满意度']])
#vis.show_n_vars_on_right([['sf_quality'],['sf_price'], ['loads'], ['quality']])
#vis.show_n_vars_on_right([['sf_quality']])
