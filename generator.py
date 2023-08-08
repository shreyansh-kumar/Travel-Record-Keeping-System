import time
import threading


def generate_random():
    t_end = time.time() + (60 * 60 * 6)
    while time.time() < t_end:
        NotImplementedError


if __name__ =="__main__":

    t1 = threading.Thread(target=generate_random)
    t2 = threading.Thread(target=generate_random)
    t3 = threading.Thread(target=generate_random)
    t4 = threading.Thread(target=generate_random)
    t5 = threading.Thread(target=generate_random)
    t6 = threading.Thread(target=generate_random)
 

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
 

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()