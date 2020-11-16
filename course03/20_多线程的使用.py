import threading

tickets = 0
glock = threading.Lock()

def get_ticket():
    global tickets
    # glock.acquire()
    for x in range(1000000):
        tickets += 1
    # glock.release()
    print('tickets:%d' % tickets)


def main():
    for x in range(5):
        t = threading.Thread(target=get_ticket)
        t.start()


if __name__ == '__main__':
    main()