from random import random
from threading import Thread
from time import sleep


def short_task():
    global q2
    while True:
        sleep(2)
        q2 = random()


def long_task():
    global q1
    while True:
        sleep(5)
        q1 = random()


def main():
    while True:
        print(q1)
        print(q2)
        sleep(1)


if __name__ == "__main__":
    try:
        q1 = 5
        q2 = 3
        t1 = Thread(target=long_task)
        t2 = Thread(target=short_task)
        t1.start()
        t2.start()
        main()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("exiting cuz of keyboard interrupt")
        exit(2)
    # st = threading.Thread(target=short_task, args=("Thread-1", queue1))
    # lt = threading.Thread(target=long_task, args=("Thread-2", queue2))
    # m = threading.Thread(target=main, args=(queue1, queue2))
    # st.start()
    # lt.start()
    # m.start()
    # st.join()
    # lt.join()
    # m.join()
