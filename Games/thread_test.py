import time
import sys
import threading

def func(value, delay):
    print("val: " +str(value) + " - " +str(threading.current_thread().ident))
    time.sleep(delay)
    print("end thread - ", threading.current_thread().ident)

for x in range(1,5):
    t1 = threading.Thread(target=func, args=(x*10, 5-x))
    t1.start()