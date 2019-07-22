
from rounder import rounder

import pytest

@pytest.mark.parametrize('value,error,string,exp10',[
        ( 1.43e-10,5.4e-11,"1.4(5)",-10),  # standard case
        ( 1.43e-10,2.54e-11,"1.43(25)",-10),  # when error is less than 3
        ( 8.2435e2,9.11234e-2,"8.2435(9)",2), # small exponents
        ( 1.2080e2,3.546e3,"0(4)",3),        # will round to 0(?)
        ( -1.2080e2,3.546e3,"0(4)",3),        # will round to 0(?), but negative
        ( -1.2354e2,2.105e3,"-0.1(2.1)",3),   # will round to 0.?(?.?)
        (0.25357132763047585,0.0022637236874722437,"2.536(23)",-1),
        (4.243004776996428,0.5712967536987361,"4.2(6)",0),
        (0.24083631867794936,0.001806943442636247,"2.408(18)",-1),
        (3.973490630762723,0.5558804626794045,"4.0(6)",0)
        ])
def test_rounder(value,error,string,exp10):

    ret_string,ret_exp10 = rounder(value,error)
    print(value,error,string,exp10,ret_string,ret_exp10)

    assert ret_exp10 == exp10
    assert ret_string == string 


