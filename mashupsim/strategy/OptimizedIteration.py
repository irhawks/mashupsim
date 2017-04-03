from mashupsim.simlibs.SimulationLogic import *
from mashupsim.strategy.StateMachine import *

class OptimizedIteration (StrategyStateMachine) :

    def discover(self):

        self.state = 0 # 自我宣告

        """如果不为空，从中选择一个服务方案，放在judging里
        更新当前服务发现的状态。如果可供选择的组合不为空，那么就去掉第一组合，
        然后将judging的方案移到最前面来
        """

        ## 时间为零尝试找到匹配的服务
        if self.val_current_time == 0 :
            yield self.call(self.env_w.do_service_match)

        ## 从所有方案中进行服务选择

        #for case in self.val_service_solutions :
        if self.val_service_solutions :

            yield self.call(self.env_w.do_service_select)
            yield self.call(self.env_w.do_eval_case_quality)
            ## 这个时候是服务发现程序当前计算出来的单元，比如两个单元的优劣

            ## 这个时候也进行迭代，根据正在运行的服务的质量，以及可能的组合的质量判断，是质量改进
            ## 如果有运行的方案，就拿运行的方案与之比较
            if self.val_running_units : ## 空列表，空集，以及None返回的都是False

                ## 更好的方案，替代原有sf_judging_quality，这是在
                if (self.val_sf_quality < self.env_w.do_eval_case_quality(self.env_w.selected_case)) : 
                        self.env_w.assign_best_case(self.env_w.selected_case)
                        yield self.goto(self.composite)
                else : ## 候选方案还不如当前选择的最优方案，因此丢弃，重新发现
                    yield self.env.process(self.discover())
            ## 没有运行的方案，就直接使用原来的
            else : ## 没有方案的时候最优的方案就是当前选择的
                self.env_w.assign_best_case(self.env_w.selected_case)
                yield self.goto(self.composite)
        ## 没有多末的方案了
        else : 
            if self.val_running_units :
                yield self.env.process(self.use())
            else :
                yield self.env.process(self.end()) ## 没有合适的方案

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
        # 只能继续使用了
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
