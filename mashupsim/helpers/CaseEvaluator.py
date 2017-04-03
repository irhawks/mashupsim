#!/usr/bin/env python3

import numpy as np
import networkx as nx

import random

from mashupsim.service.ServiceUnit import *

class CaseEvaluator :

    """
    服务组合方案的评估器
    """

    def __init__(self, service_list, case, spec=[]) :

        self.s_list = service_list
        self.case = case
        self.spec = spec
        self.network = []

    @property
    def fitness_randomized(self) :

        return np.random.random() ## 随机返回一个0到1之间的满意度

    @property
    def fitness_all_passs(self) :

        return 1 ## 每个方案都以最大的程度进行推荐

    @property
    def fitness_deny_all(self) : ## 拒绝一切的评估方案
        return 0

    @property
    def fitness_case_min_quality(self) :
        return min(avg_case_quality)
    @property 
    def fitness_case_avg_quality(self) : ## 根据组合方案的质量的判断方案
        return sum(self.avg_case_quality)/len(self.avg_case_quality)

    @property
    def avg_case_quality(self) : 

        """ 
        评估方案的质量，返回的是质量的列表
        """
        q_matrix = [self.s_list[i].q for i in self.case]
        q = sum(q_matrix)/len(q_matrix)
        return q

    ## -----------------------------------------------------------------
    ## -----------------------------------------------------------------
    ## 根据外部条件才能判断出来的满意程度

    def fitness_sf_quality(self, customer) :

        return customer.sf_quality(quality=self.avg_case_quality)

    def fitness_sf_price(self, customer) :

        return customer.sf_price(quality=self.avg_case_quality)

