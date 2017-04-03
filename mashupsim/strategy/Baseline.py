from mashupsim.simlibs.SimulationLogic import *
from mashupsim.strategy.StateMachine import *

class BaselineStrategy (StrategyStateMachine) :

    def discover(self):

        self.state = 0 # 自我宣告

        """如果不为空，从中选择一个服务方案，放在judging里
        更新当前服务发现的状态。如果可供选择的组合不为空，那么就去掉第一组合，
        然后将judging的方案移到最前面来
        """

        ## 时间为零尝试找到匹配的服务
        if self.val_current_time == 0 :
            yield self.call(self.env_w.do_service_match)
            #self.env_w.do_service_match()
            #yield self.env.process(self.new_record())

        ## 从方案中进行服务选择

        if self.env_w.possible_solutions :
            yield self.call(self.env_w.do_service_select)

        #yield self.env.process(self.composite())

        # 跳转与决策
        if self.env_w.selected_case : ## 空列表，空集，以及None返回的都是False
            
            yield self.call(self.env_w.do_eval_case_quality)

            if (self.val_sf_judging_quality > 0.6)  :
                self.env_w.assign_best_case(self.env_w.selected_case)
                yield self.goto(self.composite)
            else :
                yield self.env.process(self.discover())

        else : 
            if self.val_running_units :
                yield self.env.process(self.use())
            else :
                #yield self.env.process(self.end())
                self.end()

    def composite(self) :

        self.state = 1 # 自我宣告

        yield self.call(self.env_w.do_composition)

        yield self.call(self.env_w.do_unit_consult_for_developed)

        # 跳转
        yield self.env.process(self.use())


    def use(self):

        self.state = 2 # 自我宣告


        if self.val_developed_units : ## 准备部署新服务

            if self.val_running_service :
                ## 原来的服务先下线，服务保持为空，但是服务组件还没有失效
                yield self.call(self.env_w.undo_service_consult) 
            ## 进行新组件的运行，然后及时去掉那些没有协商的服务
            yield self.call(self.env_w.do_running_units)
            yield self.call(self.env_w.undo_unit_consult_if_useless)

            # 开发者为用户提供了服务
            yield self.call(self.env_w.do_service_consult)
        else :
            yield self.call(self.env_w.do_continue_running_service)

        # 跳转
        if self.val_service_solutions :
            yield self.env.process(self.discover())
        else :
            yield self.env.process(self.use())

    def end(self) :

        self.state = 3 # 自我宣告

        # 处理
        #self.kwargs['deployed'] = False
        """服务终止的设计
        在服务终止的时候，首先要停止各类协商的服务的
        """

        # 记录
        #yield self.env.process(self.do_record())
