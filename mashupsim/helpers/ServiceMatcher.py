#!/usr/bin/env python3

import numpy as np
import networkx as nx

import random

from mashupsim.service.ServiceUnit import *

class ServiceMatcher :

    """
    服务匹配器，用来从世界当中得到服务匹配的各类信息
    主要匹配服务的功能
    """

    def __init__(self, source, spec=[]) :

        self.source = source
        self.target = []
        self.spec = spec
        self.network = []

    def mock_network_edges1(self) :

        if len(self.source) >= 5 :
            self.network_edges = [(1,2), (1,3), (2,3), (2,4), (2,5), (4,5), (3,5), (1,4)]
        else : 
            self.network_edges = []
        return self.network_edges

    def mock_network_edges2(self) :
        l = len(self.source) 
        self.network_edges = []
        for i in range(0,l) :
            for j in range(0,l) :
                if np.random.random() > 0.5 : ## 随机有序连接
                    self.network_edges.append([j,i])
        return self.network_edges

    def mock_network_edges3(self, prob=0.3) :

        GRG = nx.gnp_random_graph(len(self.source), prob, directed=True)
        return GRG.edges()

    def path_match(self, node_from=1, node_to=5
            , edges_generator=[]) : 
 
        if not edges_generator :
            edges_generator = self.mock_network_edges1
        edges_generator()

        self.network = nx.DiGraph()
        self.network.add_edges_from(self.network_edges)

        self.target = nx.all_simple_paths(self.network, source=node_from, target=node_to)

        return list(self.target) ## 转化为list才行

    def cats_match(self) :
        pass

    @property
    def randomized_func_match(self) :

        """
        随机选择，先归好每类，然后每类选择一个，使用random库中的select函数即可
        这个时候假设都是满足要求的项目（当然，也可以多给一些cat。将服务分成五类
        """
        self.target = []
        cat_list = [i for i in range(0,5)]
        for c in range(0,5) : ## 从零到五的服务种类中各自选择
            cat_list[c] = [i for i in range(0,len(self.source)) if self.source[i].f[0] == c]
        #self.target.append([random.sample(cat,1)[0] for cat in cat_list]) # 这只能返回一个结果
        for i in cat_list :
            if i == [] :
                print("catgory is", cat_list)
                raise Exception("Found None Valid Combinations")
        self.target = self.multiset(cat_list)

        ## 应该返回所有的可能的列表
        return self.target

    def multiset(self, categorized_list) :
        if len(categorized_list) == 2 :
            return [[i,j] for i in categorized_list[0] for j in categorized_list[1]]
        elif len(categorized_list) == 1 :
            return categorized_list
        else :
            return [j+[i] for i in categorized_list[-1] for j in self.multiset(categorized_list[0:-1])]
