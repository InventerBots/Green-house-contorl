

import threading


def f(name):
    print(name)

def z():
    x = input()
    print(x)

if __name__ == '__main__':
    t2 = threading.Thread(f(__name__))
    t1 = threading.Thread(z())

    
    t1.start()
    t2.start()

    t1.join()
    t2.join()