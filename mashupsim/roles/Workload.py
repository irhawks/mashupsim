#!/usr/bin/env python3

import numpy as np

from mashupsim.helpers.CaseEvaluator import *
from mashupsim.helpers.ServiceMatcher import *


class Workload :

    """
    开发者的开发能力的建模。人员的capability，
    人员所做的事情等。规定了内在的属性与外在的属性
    封装所有不影响流程的行为
    """
    def __init__ (self, env_s, env_u) :

        self.env_s = env_s
        self.env_u = env_u

        ## SD, SC, SU, SE
        self.cost_ref = [1, 2, 0.5, 1]
        self.time_ref = [1, 20, 5, 10]

        self.running_units = []
        self.running_service = None
        self.developed_units = []
        self.developed_service = None
        self.judging_units = []
        self.sf_judging_quality = []

        self._action_cost = 0
        self._action_time = 0
        self._total_cost = 0
        self._total_time = 0

        # 记录下行为的名子
        self._action_name = "NONE"
    
    @property
    def action_name(self) :
        return self._action_name
    @property
    def total_cost(self):
        return self._total_cost
    def total_time(self):
        return self._total_time

    # 防止未预料到的对total_time等函数的修改
    # 并且在更新action_cost的时候自动更新total_cost
    @property
    def action_cost(self) :
        return self._action_cost
    @action_cost.setter
    def action_cost(self, v) :
        self._action_cost = v
        self._total_cost += v
    @property
    def action_time(self) :
        return self._action_time
    @action_time.setter
    def action_time(self, v) :
        self._action_time = v
        self._total_time += v

    def do_service_match(self, time=1) :

        #self.possible_solutions = ServiceMatcher(self.env_s).path_match()    
        self.possible_solutions = ServiceMatcher(self.env_s).randomized_func_match

        self.action_cost = self.cost_ref[0]
        self.action_time = self.time_ref[0]
        self._action_name = "service match"


    def do_service_select(self, time=1) :

        ## 必要的参数更析
        current = self.possible_solutions[0]
        self.possible_solutions = self.possible_solutions[1:]
        self.judging_units = current

        self.action_cost = self.cost_ref[0]
        self.action_time = self.time_ref[0]
        self._action_name = "service_select"

    def do_eval_case_quality(self, case=[]) :

        self.sf_judging_quality = CaseEvaluator(self.env_s, self.judging_units).fitness_sf_quality(self.env_u)

        self.action_cost = self.cost_ref[0]
        self.action_time = self.time_ref[0]
        self._action_name = "unit case quality"

    def do_composition(self, time=20) :

        """
        随机的组件是不准确的
        实现一个平均质量的组合方案
        """

        pdim = len(self.env_s[0].p)
        qdim = len(self.env_s[0].q)
        fdim = len(self.env_s[0].f)
        #developed = ServiceUnit(str(self.judging_units)).randomize_std(pdim=pdim,qdim=qdim,fdim=fdim)
        f = [np.average([self.env_s[i].f[j] for i in self.judging_units]) for j in range(0,fdim)]
        q = [np.average([self.env_s[i].q[j] for i in self.judging_units]) for j in range(0,qdim)]
        p = [np.average([self.env_s[i].p[j] for i in self.judging_units]) for j in range(0,pdim)]
        developed = ServiceUnit(str(self.judging_units), quality=q,function=f,protocol=p)
        self.developed_service = developed
        self.developed_units = self.judging_units
        self.judging_units = []

        self.action_cost = self.cost_ref[1]
        self.action_time = self.time_ref[2]
        self._action_name = "compositing"

    def do_running_units(self) :

        # self.do_service_consult()
        # 现在阶段，运行单元的时候可以什么也不错，成功
        self.action_cost = 1
        self.action_time = 1
        self._action_name = "running units"

    def do_unit_consult_for_developed(self, time=1) :

        # 自我宣告

        # 服务组件协商，只有那些新服务需要运行而未运行的才需要重新协商
        for unit in set(self.developed_units) - set(self.running_units) :
            self.env_s[unit].do_consult()
        self.recently_outdated_running_units = set(self.running_units) - set(self.developed_units)

        self.action_cost = 2
        self.action_time = 2
        self._action_name = "unit consult for developed"



    def undo_unit_consult_if_useless(self, time=1) :

        # 停止那些新复合应用不需要的组件与服务，减少成本
        # 停止这些组件之前应该先停止running的service
        # 只有那些老服务中不再需要的才需要协商
        if self.running_units :
            for unit in self.recently_outdated_running_units :
                self.env_s[unit].undo_consult()

        self.action_cost = 1
        self.action_time = 1
        self._action_name = "undo_unit_consult_if_useless"


    def do_service_consult(self, time=1) :

        # 开发者与消费者的服务动态参数协商
        self.developed_service.do_consult()
        self.running_service = self.developed_service
        self.running_units = self.developed_units
        self.developed_service = None
        self.developed_units = []

        self.action_cost = self.cost_ref[2]
        self.action_time = self.time_ref[2]
        self._action_name = "do service consult"

    def undo_service_consult(self) :

        self.running_service.undo_consult()
        self.running_service = None
        self.running_units = []
        self.action_cost = 1
        self.action_time = 1
        self._action_name = "undo service consult"

    def replace_with_new_service(self) :

        self.running_service = self.developed_service
        self.running_units = self.developed_units
        self._action_name = "replace_with new service"

    def do_continue_running_service(self) :

        self.action_cost = self.cost_ref[2]
        self.action_time = self.time_ref[2]
        self._action_name = "continuing_running_service"


    def do_with(self, **kargs) :

        def wrapped_f(f, *args, **kwargs):
            f(*args, **kwargs)
        return wrapped_f

        self.action_cost = self.cost_ref[0]
        self.action_time = self.cost_ref[0]
