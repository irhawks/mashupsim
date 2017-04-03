# 服务的版本库，里面包括了各种各样的服务的描述

class Function :

    def __init__ (self, kwargs) :

        self.args = kwargs

# 其实一个ServiceRepo就是一系列的List的集合，每个List是每个Service
# 每个服务由相应的属性所规定，每个属性可以是常值或约束

class Service :

    def __init__ (self, attrs) :
        self.attrs = attrs

class ServiceRepo :

    def __init__ (self, service_list) :
        self.services = service_list
