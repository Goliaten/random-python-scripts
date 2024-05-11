class hello:
    def __init__(self, inp):
        self.inp = inp

b = hello(2)
a = type(b)
print(a)

if isinstance(b, hello):
    print('yes')
    
print(hello.__name__[:2])
