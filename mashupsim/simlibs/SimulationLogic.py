# -*- coding:utf-8 -*-

import numpy as np
import json, jsonpickle

from mashupsim.helpers import *

class SimulationLogic :

    """
    尽量把所有的变量与策略都写在抽象类当中
    各个过程尽量不使用自己的私有成员
    """

    def __init__ (self, env, env_s, env_w, env_u) :

        self.env = env
        self.env_s = env_s
        self.env_u = env_u
        self.env_w = env_w

        self.kwargs = {}  # 仅供当前事件
        self.history = [] # 提供所有记录
        self._internal_kwargs = {'total_cost' : 0, 'total_income' : 0}
        self._internal_history = [] # 内部观察的一些量，比如OB。

        self.action = self.env.process(self.discover())

    def run(self, **kwargs) :

        """
        运行模型，得到模型的结果
        """
        self.env.run(**kwargs)

    def call(self,f, *args, **kwargs) :
        """
        调用Workload模型中的相应活动
        """
        f()
        return self.env.process(self.do_record())

    def goto(self, f, *args, **kwargs) :
        """
        调用goto函数实现状态的转移
        """
        return self.env.process(f(*args, **kwargs))

    def do_record (self) : # new_record不再接受参数，而只被动地记录

        """
        如果阶段持续的时间为零，就不记载，也就是yield empty
        没有持续时间的活动我们都可以认为是假的活动，
        """

        for i in range(0, self.env_w.action_time) :
            self._internal_record()
            self._external_record()

            # 记录完成之后延迟到下一个时间片，表示这个时间片的任务完成
            yield self.env.timeout(1)

    def _external_record(self) :
            self.kwargs = {} ## 每次都清空kwargs，然后重新生成
            self.kwargs.update({'time' : self.val_current_time})
            self.observer()
            # 序列化与记录历史
            text = json.dumps(self.kwargs)
            #text = json.dumps(json.loads(jsonpickle.encode(self.kwargs)))
            #text = jsonpickle.encode(self.kwargs, keys=True)
            self.history.append(json.loads(text))

    def _internal_record(self) :

            """同时内部记录一些信息"""
            #self._internal_kwargs = {} ## 内部kwargs存放历史信息
            self._internal_kwargs.update({'time' : self.val_current_time})
            self._internal_observer()
            # 序列化与记录历史
            text = json.dumps(self._internal_kwargs)
            #text = json.dumps(json.loads(jsonpickle.encode(self.kwargs)))
            #text = jsonpickle.encode(self.kwargs, keys=True)
            self._internal_history.append(json.loads(text))

    def observer(self) :

        """只需要记录那些希望添加到数据观察中的内容，建议由每个实验定制"""
        self.kwargs.update({'state' : self.state})
        self.kwargs.update({'price' : self.val_service_price})
        self.kwargs.update({'loads' : self.val_service_load})

    def _internal_observer(self) :
        self._internal_kwargs.update({'state' : self.state})
        if 'cumsum_total_cost' in self._internal_kwargs.keys() :
            self._internal_kwargs['cumsum_total_cost'] += self.val_total_cost 
        else : 
            self._internal_kwargs.update({'cumsum_total_cost' : 0})

        if 'cumsum_total_income' in self._internal_kwargs.keys() :
            if self.val_running_units : income = self.val_consumer_payment
            else : income = 0
            self._internal_kwargs['cumsum_total_income'] += income
        else : 
            self._internal_kwargs.update({'cumsum_total_income' : 0})

    ## 开发过程
    @property
    def val_current_time(self) :
        return self.env.now
    @property
    def val_action_name (self) :
        return self.env_w.action_name
    @property 
    def val_action_cost (self) :
        return self.env_w.action_cost

    ## 开发过程属性

    """服务库中的剩余方案"""
    @property
    def val_service_solutions(self) :
        return self.env_w.possible_solutions
    """正在判断的服务"""
    @property
    def val_judging_units(self) :
        return self.env_w.judging_units
    @property
    def val_sf_judging_quality(self) :
        return self.env_w.do_eval_case_quality(self.val_judging_units)
    @property
    def val_sf_case_quality(self) :
        return self.env_w.do_eval_case_quality(self.selected_case)
    """正在运行的服务"""
    @property
    def val_developed_units(self) :
        return self.env_w.developed_units
    @property
    def val_developed_service(self) :
        return self.env_w.developed_service
    @property
    def val_developed_quality(self) :
        return list(self.env_w.developed_service.q)
    @property
    def val_running_units(self) :
        return self.env_w.running_units
    @property
    def val_running_service(self) :
        return self.env_w.running_service
    @property
    def val_running_quality(self) :
        return list(self.env_w.running_service.q)
    @property
    def val_running_cost(self) :
        return self.env_w.running_service.unit_cost


    ## 正在运行的服务属性

    @property
    def val_service_price(self) :
        if self.env_w.running_units : 
            return self.env_w.running_service.unit_price
        else : return 0
    @property
    def val_service_capacity(self) : 
        if self.env_w.running_service : 
            return self.env_w.running_service.capacity
        else : return 0
    @property
    def val_service_load(self) :
        if self.env_w.running_units : 
            return self.env_u.get_service_load(time=self.env.now, service=self.env_w.running_service)
        else : return 0
    @property
    def val_consumer_payment(self) :
        if self.env_w.running_units : 
            return self.val_service_price * self.val_service_load
        else : return 0


    ## 用户方面的信息（用户肯定是对已部署的服务的满意度

    @property
    def val_sf_overall(self) :
        return self.env_u.sf_overall(service=self.env_w.running_service)
    @property
    def val_max_demands(self) : 
        return self.env_u.max_demands
    @property
    def val_service_demands(self) :
        return self.env_u.get_service_demand(service=self.env_w.running_service)
    @property
    def val_sf_price(self) :
        return self.env_u.sf_price(service=self.env_w.running_service)
    @property 
    def val_sf_quality(self) :
        return self.env_u.sf_quality(service=self.env_w.running_service)
    @property
    def val_sf_assigned(self) :
        return self.env_u.sf_assigned(service=self.env_w.running_service)

    ## 开发者与供应商方面的信息
    @property 
    def val_component_cost(self) : ## 组件的支付费用的情况(单价乘以容量)
        cost_list = []
        for i in self.val_running_units :
            cost_list.append(self.env_s[i].literal_unit_cost*self.env_s[i].literal_capacity) ## 注意使用的是literal_unit_cost
        cost = sum(cost_list)
        return cost
    @property
    def val_total_cost(self) :
        cost = 0
        if self.val_running_units :
            cost += self.val_component_cost
            cost += self.val_running_cost
        cost += self.val_action_cost
        return cost

    ## 与历史有关的信息，需要查history才能知道这些信息
    @property
    def val_cumsum_total_cost(self) :
        return self._internal_kwargs['cumsum_total_cost']
    @property
    def val_cumsum_total_income(self) :
        return self._internal_kwargs['cumsum_total_income']
    @property
    def val_ROI(self) :
        if self._internal_kwargs['cumsum_total_cost'] == 0 : return 0
        else : return self.val_cumsum_total_income / self.val_cumsum_total_cost
