#!/usr/bin/env python3

import numpy as np

from mashupsim.constant import *

import math

class Customer :

    """
    客户模型
    """

    def __init__ (self) :

        self.sf_price_decay = 10 ## 价格满意系数
        self.max_demands = 100   ## 市场最大需求量
        self.quality_dim = NUM_QUALITIES
        self.ref_quality = [0.90 for i in range(0, self.quality_dim)]
        self.min_quality = [0.60 for i in range(0, self.quality_dim)]

    def randomize (self) :

        """
        随机产生一个用户需求，初始化所有因子
        """

        self.sf_price_decay = 10 + 10 * np.random.random() ## 随机化价格满意系数
        self.max_demands = 100 + 100 * np.random.random()  ## 随机化市场最大需求
        return self

    ## -----------------------------------------------------------------
    ## 满意程度函数, qsf质量满意程度

    def sf_quality(self, quality=np.random.random(NUM_QUALITIES), service=None) :

        """质量满意程度的计算"""

        if service == None : 
            q_value = np.min(quality)
            qmin_value = np.min(self.min_quality)
            qmax_value = np.max(self.ref_quality)
            if q_value > qmax_value : return 1.0
            if q_value < qmin_value : return 0
            return (q_value-qmin_value) / (qmax_value - qmin_value)
        else :
            return self.sf_quality(quality=service.q)

    def sf_price(self, price=np.random.random(), service=None) :
        
        """
        对单价的满意程度
        """

        if service == None : 
            if (price >0 and price < self.sf_price_decay) :  # 表示按照价格
                return 1-price/self.sf_price_decay
            else : 
                if (price > 0) : return 0
                else : return math.exp(0.01*price) # 表示一次性收费的满意度
        else :
            return self.sf_price(price=service.quota[0]) ## 对正在运行当中的服务的价格满意的程度

    def sf_assigned(self, assigned=np.random.random(NUM_PROTOCOLS), service=None) : 

        """ 外在属性的满意度度量，原则上也采取归一化的形式 """
        if service == None :
            return 1
        else : 
            return self.sf_assigned(assigned=service.p) ## 返回正在运行的服务的宣告属性

    def sf_overall(self, price=1.0
        , quality=np.random.random(NUM_QUALITIES)
        , assigned=np.random.random(NUM_PROTOCOLS)
        , service =None) :

        """
        用户的满意度是这些满意度的相乘
        """
        if service == None : 
            q = self.sf_quality(quality=quality)
            p = self.sf_price(price=price)
            a = self.sf_assigned(assigned=assigned)
            return p * q * a
        else :
            # 对正在运行的服务的满意程度
            return self.sf_overall(price=service.unit_price,quality=service.q,assigned=service.p)

    ## -----------------------------------------------------------------
    ## 调用客户模型
    
    def get_service_demand(self
        , time=0
        , price=1
        , quality=np.random.random(NUM_QUALITIES)
        , assigned=np.random.random(NUM_PROTOCOLS)
        , service =None, **kwargs) :

        """
        用户对于开发者开发出来的服务的需求量
        """

        # return 100 ## 先返回一个简单的函数，对服务的需求量固定是100。

        if service == None : 
            return self.max_demands * self.sf_overall(price=price,quality=quality,assigned=assigned)
        else : 
            return self.max_demands * self.sf_overall(price=service.unit_price, quality=service.q, assigned=service.p)

    def get_service_load(self,time=0, service=None) :

        """
        得到用户对特定服务的(开发者开发出来的服务的）实际的购买量，是
            * 服务容量
            * 假如开发者提供充足的服务容量的时候购买的转化率
        """

        if service :
            capacity = service.capacity
            result = min(capacity, 0.5*(1+np.random.random()) * self.get_service_demand(service=service))
            return result
        return 0


    ## -----------------------------------------------------------------
    ## -----------------------------------------------------------------

    def feedback (self, service=[]) :

        """
        开发者对用户的认知，与用户的实际是不同的，feedback用于构建对服务的反馈
        """
        return None
