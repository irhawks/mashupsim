#!/usr/bin/env python3

## 服务模型，服务单元

import networkx as nx

import copy
import json

from mashupsim.constant import *

class ServiceUnit :

    """
    服务单元，对服务、服务合同以及服务合同的生命周期进行建模
    """

    def __init__ (self, name, quality=np.random.random(NUM_QUALITIES)
                , protocol=np.random.random(NUM_PROTOCOLS) ## 随机化协议属性
                , function=np.random.random(NUM_FUNCTIONS)
                ) :

        """
        用特定的质量属性与功能属性初始化服务，还有服务合同属性信息
        """

        self.q=quality
        self.p=protocol
        self.f=function
        self.name = name

        self.quota = None
        self.extra = None

    def randomize(self, qdim=NUM_QUALITIES, pdim=NUM_PROTOCOLS, fdim=NUM_FUNCTIONS) :

        """
        默认情况下，应该使用rand函数生成。不使用rand函数表示手动的生成
        """
        if pdim==[] : pdim=qdim   
        if fdim==[] : fdim=qdim   
        self.q=np.random.random(qdim)
        self.p=np.random.random(pdim) ## 随机化协议属性
        self.f=np.random.random(fdim)
        return self

    @property
    def category(self) :
        return self.f[0]
    @category.setter
    def category(self, cat) :
        self.f[0] = cat

    @property
    def literal_unit_price(self) :
        return self.p[0]
    @literal_unit_price.setter
    def literal_unit_price(self, v) :
        self.p[0] = v
    @property
    def unit_price(self) :
        return self.quota[0]
    @unit_price.setter
    def unit_price(self,val) :
        self.quota[0] = val

    @property
    def literal_unit_cost(self) :
        return self.p[1]
    @literal_unit_cost.setter
    def literal_unit_cost(self, v) :
        self.p[1] = v
    @property
    def unit_cost(self) :
        return self.quota[1]
    @unit_cost.setter
    def unit_cost(self,val) :
        self.quota[1] = val

    @property
    def literal_capacity(self) :
        return self.p[2]
    @literal_capacity.setter
    def literal_capacity(self,val) :
        self.p[2] = val
    @property
    def capacity(self) : 
        return self.quota[2]
    @capacity.setter
    def capacity(self, value) :
        self.quota[2] = value

    @property
    def avg_q(self) :

        """
        一组质量属性的平均值函数，方便通过服务单元计算质量属性与功能属性值
        因为经常计算，也就有了这样的属性
        """
        if len(self.q) == 0 : return 0.0 
        else : return sum(self.q)/len(self.q)
    @property
    def std_q(self) :
        return np.std(self.q)


    def randomize_std(self, qdim=NUM_QUALITIES, pdim=NUM_PROTOCOLS, fdim=NUM_FUNCTIONS) :

        """
        标准服务分布，产生比较符合实际的
        服务的功能属性、质量属性与合同属性是只读的，只有Quota可以改变
        """

        self.randomize(qdim=qdim,pdim=pdim,fdim=fdim)

        ## 功能属性分类
        ref = [6, 3, 4, 2, 5]
        rate = [sum(ref[0:i+1])/20.0 for i in range(0,5)]
        
        if self.f[0] < rate[0] : 
            self.f[0] = 0
        elif self.f[0] < rate[1] : 
            self.f[0] = 1
        elif self.f[0] < rate[2] : 
            self.f[0] = 2 
        elif self.f[0] < rate[3] : 
            self.f[0] = 3 
        else : 
            self.f[0] = 4  ## rate=4=1

        ## 质量属性分布，[0.5,1.0]之间的均匀分布
        self.q = 1 - 0.5 * np.random.random(qdim)

        ## 质量价格
        self.literal_unit_price = 1.0 + np.random.random() ## 设置单位服务的价格为1。
        ### 服务的成本
        self.literal_unit_cost = 0.1 ## 固定付费的时候的服务使用计费
        ### 服务的容量
        self.literal_capacity = 100

        ## 可供协商的动态的属性在random之后为空
        self.quota = None

        return self

    ## -----------------------------------------------------------------
    ## -----------------------------------------------------------------
    ## 服务的生命周期中的一些活动

    ## 使用只读的状态变量保证服务周期的正确性
    @property
    def executing_status (self):
        return self._executing_status
    @property
    def consulting_status (self):
        return self._consulting_status

    def do_consult(self, **kwargs) :
        """
        模拟服务合同协商的过程，缺省情况下直接深拷贝合同信息
        """
        if not kwargs:
            self.quota = copy.deepcopy(self.p)
        self.info_do_consult = kwargs
        self._consulting_status = True

        return True

    def undo_consult(self, **kwargs) :

        """
        撤消合同协商，将合同恢复到刚发布的状态，将self.quota的值设为None
        """

        self.quota = None
        self.info_undo_consult = kwargs
        self._consulting_status = False
        return True

    def do_execution(self, **kwargs) :
        """
        通常执行的过程中也不需要修改参数
        """
        self.info_do_execution = kwargs
        self._executing_status = True
        pass

    def undo_execution(self, **kwargs) :
        self.info_undo_execution = kwargs
        self._executing_status = False
        pass

    def resume(self) : 
        self.info_do_consult = {}
        self.info_undo_consult = {}
        self.info_do_execution = {}
        self.info_undo_execution = {}
        self._executing_status = False
        self._consulting_status = False


    ## -----------------------------------------------------------------
    ## -----------------------------------------------------------------
    ## 序列化与字符表示

    def __str__ (self) :
        return "Service " + str(self.name)

    #def __expr__(self) :
    #    return self.__str__()

    #def __repr__(self) : 
    #    return json.dumps(self.__dict__)

    def __getstate__(self) : # pickle serilization
        return self.__dict__

    #@property
    #def __dict__(self) :
    #    #return {'function' : self.f, 'protocol' : self.p, 'quality' : self.q}
    #    return {'function' : list(self.f)}

    def __json__(self) :
        return self.__dict__

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)
