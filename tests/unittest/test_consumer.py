from mashupsim.roles.Customer import Customer
import numpy as np

class TestCustomer :

    def __init(self) :

        ref_q = Customer().ref_quality
        min_q = Customer().min_quality
        half_q= (ref_q + min_q) / 2

    def test_init (self) : 

        assert Customer().sf_price_decay == 10
    
    def test_randomize(self) :

        assert Customer().randomize().max_demands >= 100
        assert Customer().randomize().max_demands <= 200

    def test_sf_quality(self) :

        assert Customer().sf_quality(quality=Customer().ref_quality) == 1 ## 对最大质量的满意程度是1
        assert Customer().sf_quality(quality=Customer().min_quality) == 0 ## 对最低质量的满意程度是0
        assert Customer().sf_quality(
                quality=(np.array(Customer().ref_quality) + np.array(Customer().min_quality))/2) == 0.5 ## 对中间质量的满意程度是0.5

    def test_sf_price(self) :

        assert Customer().sf_price(price=0) == 1 ## 价格为零的时候满意度是1
        assert Customer().sf_price(price=Customer().sf_price_decay) == 0 ## 价格为接受上限的时候，没有满意度
        assert Customer().sf_price(price=Customer().sf_price_decay/2) == 0.5 ## 价格为上限的一半的时候，有0.5的满意度

    def test_sf_assigned(self) :
        assert Customer().sf_assigned() == 1
    
    def test_sf_overall(self) :

        assert Customer().sf_overall(price=0, quality=Customer().ref_quality) == 1
        assert Customer().sf_overall(price=0, quality=Customer().min_quality) == 0

    def test_service_demand(self) :

        assert Customer().get_service_demand(price=0, quality=Customer().ref_quality) == 100
        assert Customer().get_service_demand(price=1, quality=Customer().ref_quality) == 90

    def test_service_load(self) :

        assert Customer().get_service_load() == 0
