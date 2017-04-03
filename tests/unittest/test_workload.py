from mashupsim.roles.Workload import *

class TestWorkload : 

    def test_init(self) : 

        developer = Workload(1,2)
        def abc(hello) :
            return "Hello, World"
        developer.do_with(a=3,b=3)(abc, "hello") == "Hello, World"
