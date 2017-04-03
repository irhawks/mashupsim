#!/usr/bin/env python3
# coding:utf-8

from mashupsim.simlibs import *

from mashupsim.strategy.Baseline import *

from mashupsim.roles.Customer import *
from mashupsim.roles.Workload import *

from mashupsim.helpers import *

import simpy

import random

### 如果设计自己的实验

class MySimulator(SimulationLogic) :

    def observer(self) :

        """只需要记录那些希望添加到数据观察中的内容，建议由每个实验定制"""
        self.kwargs.update({'state' : self.state})
        self.kwargs.update({'loads' : self.val_service_load})
        self.kwargs.update({'action' : self.val_action_name})
        self.kwargs.update({'开发支出' : self.val_action_cost}) ## 单位运转的时候的支出（内部人员的开发活动）
        self.kwargs.update({'全部成本' : self.val_total_cost}) ## 额外的运行支出
        self.kwargs.update({'投资回报率' : self.val_ROI})
        self.kwargs.update({'A累积收益' : self.val_cumsum_total_income})
        self.kwargs.update({'A累积投入' : self.val_cumsum_total_cost})
        #self.kwargs.update({'sf_overall' : self.val_sf_overall if self.val_sf_overall else 0})
        if self.val_running_units :
            self.kwargs.update({'服务负载' : self.val_service_load})
            self.kwargs.update({'组件支出' : self.val_component_cost})
            self.kwargs.update({'运行支出' : self.val_running_cost}) ## 额外的运行支出
            self.kwargs.update({'服务收益' : self.val_consumer_payment}) ## 额外的运行支出
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
class MyWorkload(Workload) :

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
std.run(until=200)

import sys
#print(pd.DataFrame(std.history))
pd.DataFrame(std.history).to_csv(sys.stdout)

vis = Visualizer(pandas=pd.DataFrame(std.history))

#vis.show_n_vars_on_right([['sf_quality','sf_price', 'sf_overall']])
vis.show_n_vars_on_right([['全部成本', '组件支出', '开发支出', '运行支出', '服务收益'], ['投资回报率']])

data = pd.DataFrame(std.history)
for i in ['全部成本', '组件支出', '开发支出', '运行支出', '服务收益', '服务负载'] :
    data[i] = data[i].cumsum()
vis2 = Visualizer(pandas=data)


#vis.show_n_vars_on_right([['sf_quality','sf_price', 'sf_overall']])
vis2.show_n_vars_on_right([['全部成本', '组件支出', '开发支出', '运行支出', '服务收益'], ['投资回报率']])

#vis.show_n_vars_on_right([['服务收益'], ['服务负载'], ["价格"]])
#vis.show_n_vars_on_right([['sf_quality'],['sf_price'], ['loads'], ['quality']])
#vis.show_n_vars_on_right([['sf_quality']])
