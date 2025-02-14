dogcat = int(input('You like cats or dogs:'))
def function1(dog, cat):
    """显示信息"""
    if (dogcat == 1):
        print((('hello,this is my' + ' ') + dog.title()))
    else:
        print((('hello,this is my' + ' ') + cat.title()))

function1('hot', 'foot')