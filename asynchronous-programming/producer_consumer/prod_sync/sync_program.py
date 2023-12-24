import time
import datetime
import colorama
import random

def main():
    # create asyncio event loop

    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "Starting at {}".format(t0), flush=True)
    data = []

    # run these with asyncio.gather()
    generate_data(10, data)
    generate_data(10, data)
    process_data(20, data)

    # run_until_complete

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "Total time: {:,.2f} sec".format(dt.total_seconds()), flush=True)

# functions need to be marked as explicitly async: not required as the language figures it out when it sees the await keyword
def generate_data(n, data: list):
    for idx in range(1, n + 1):
        item = idx * idx
        # use queue
        data.append((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + " -- generated item {}".format(item), flush=True)
        # sleep better
        time.sleep(random.random() + 0.5)

def process_data(n, data: list):
    processed = 0
    while processed < n:
        # use queue
        item = data.pop(0)
        if not item:
            time.sleep(0.01)
            continue

        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN + " +++ Processed value {} after {:,.2f} sec".format(value, dt.total_seconds()), flush=True)
        time.sleep(0.5)

if __name__ == '__main__':
    main() # Total time: 28.97 sec
    '''
    An item is generated only after the previous one is generated. We can see that we are not taking advantage of the time it takes to generate an item to process the previous one. In essence we are waiting for the item to be generated before we can process it. This is a synchronous program. 

    Next, we will see how to make this program asynchronous. Do more work while waiting for the item to be generated.
    '''