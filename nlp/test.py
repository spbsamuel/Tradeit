from interpreter import  interpret

def test_command():
    assert interpret("How to!!")[0]=="howto"
    print("test passed")

test_command()