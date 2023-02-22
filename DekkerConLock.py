from multiprocessing import Process, Value, Array, Lock

N = 3

def task(common, tid, critical, lock):
    for i in range(10):
        print(f'{tid}-{i}: Non-critical Section')
        lock.acquire()
        critical[tid] = 1
        while any(critical) and not critical[tid]:
            lock.release()
            print(f'{tid}-{i}: Giving up')
            lock.acquire()
            critical[tid] = 1
        lock.release()
        print(f'{tid}-{i}: End of non-critical Section')
        
        lock.acquire()
        v = common.value + 1
        common.value = v
        lock.release()
        
        print(f'{tid}-{i}: Critical section')
        print(f'{tid}-{i}: Inside critical section')
        
        lock.acquire()
        critical[tid] = 0
        lock.release()

    print(f'{tid}-{i}: End of task')

def main():
    lp = [] 
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    lock = Lock()

    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, critical, lock)))

    print(f"Initial value of counter: {common.value}")
    for p in lp:
        p.start()

    for p in lp:
        p.join()

    print(f"Final value of counter: {common.value}")
    print("Finished")

if __name__ == "__main__":
    main()
