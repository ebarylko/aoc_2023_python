input = open("input.txt", "r").readlines()

def test_file_content():
    assert "hi" == input

def test_simple_assertion():
    assert 1 == 2
