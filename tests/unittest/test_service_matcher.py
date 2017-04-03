from mashupsim.helpers.ServiceMatcher import *
from mashupsim.service.ServiceUnit import *

class TestServiceMatcher :

    def test_init(self) :
        assert ServiceMatcher(source=0).source == 0

    def test_mock_network_edges1(self) : 
        assert len(ServiceMatcher(source=range(0,5)).mock_network_edges1()) != 0
        assert len(ServiceMatcher(source=range(0,4)).mock_network_edges1()) == 0

    def test_mock_network_edges2(self) :

        for i in range(0,10) :
            assert len(ServiceMatcher(source=range(0,10)).mock_network_edges2()) != 0 ## 极少的失败率

    def test_mock_network_edges3(self) :

        for i in range(0,10) :
            assert len(ServiceMatcher(source=range(0,5)).mock_network_edges3()) != 0 ## 极少的失败率

    def test_path_match(self) : 
        assert ServiceMatcher(source=range(0,6)).path_match() != []
        assert ServiceMatcher(source=range(0,5)).path_match() != []

    def test_randomized_func_match(self) :
        
        assert ServiceMatcher(source=range(0,5)).multiset([[0]]) == [[0]]
        assert ServiceMatcher(source=range(0,5)).multiset([[0],[1]]) == [[0,1]]
        assert ServiceMatcher(source=range(0,5)).multiset([[0,1],[1,2]]) == [[0,1],[0,2],[1,1],[1,2]]
        assert ServiceMatcher(source=range(0,5)).multiset([[0,1],[1,2],[3]]) == [[0,1,3],[0,2,3],[1,1,3],[1,2,3]]
        assert ServiceMatcher([ServiceUnit(1).randomize_std() for i in range(0,20)]).randomized_func_match != []
