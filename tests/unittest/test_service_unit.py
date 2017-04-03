from mashupsim.service.ServiceUnit import *

class TestServiceUnit() :

    def test_attributes(self) : 

        assert ServiceUnit(1, quality=[0.1,0.9]).name == 1
        assert ServiceUnit(1, quality=[0.1,0.9]).q == [0.1,0.9]

    def test_random(self) :

        assert len(ServiceUnit(1, quality=np.random.random(5)).q) == 5
        assert len(ServiceUnit(1).randomize(qdim=5).q) == 5

        assert len(ServiceUnit(1).randomize(pdim=6).p) == 6
        assert len(ServiceUnit(1).randomize(pdim=5,qdim=6).p) == 5

        assert ServiceUnit(1, quality=[0.1,0.9], protocol=[0.2,0.8]).p == [0.2, 0.8]
        assert len(ServiceUnit(1).randomize(qdim=3,pdim=5, fdim=4).f) == 4
        assert len(ServiceUnit(1).randomize(qdim=3,pdim=5, fdim=4).p) == 5
        assert len(ServiceUnit(1).randomize(qdim=3,pdim=5, fdim=4).q) == 3

    def test_randomize_std(self) :

        ## 初始化的维度正确
        assert len(ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).f) == 4
        assert len(ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).q) == 3
        assert len(ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).p) == 5

        ## 初始化的分
        for i in range(0,10) : 
            ## 功能属性应该属于[0,4]这几个类别
            assert ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).f[0] in range(0,5)
            ## 质量属性应在0.5到1.0之间
            for i in ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).q :  
                assert i >= 0.5 
                assert i <= 1.0

        assert 2 in [ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).category for i in range(0,100)]
        assert 3 in [ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).category for i in range(0,100)]
        assert 4 in [ServiceUnit(1).randomize_std(qdim=3,pdim=5, fdim=4).category for i in range(0,100)]
