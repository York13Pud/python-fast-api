from app.calculations import add_test, sub_test

def test_add():
    print("Testing add function")
    total_sum = add_test(5, 3)
    # True is ok, False will error
    assert total_sum == 8
    
test_add()

def test_sub():
    print("Testing add function")
    total_sum = sub_test(5, 3)
    # True is ok, False will error
    assert total_sum == 2
    
