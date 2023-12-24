import datetime
import colorama
import random
import time
import asyncio

def main():
    loop = asyncio.get_event_loop()

    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "Starting at {}".format(t0), flush=True)

    data = asyncio.Queue()
    
    task = asyncio.gather(
        generate_data(10, data),
        generate_data(10, data),
        process_data(20, data) # if we split processing in batches of 5, by adding more process_data() calls, we can see that the processing is done more efficiently by furthur reducing the latency.
    )

    loop.run_until_complete(task)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "Total time: {:,.2f} sec".format(dt.total_seconds()), flush=True)

async def generate_data(n, data: asyncio.Queue):
    for idx in range(1, n + 1):
        item = idx * idx

        work = (item, datetime.datetime.now())
        await data.put(work) # put is an async method --> needs to be awaited so that other stuff can happen while we wait

        print(colorama.Fore.YELLOW + " -- generated item {}".format(item), flush=True)
        await asyncio.sleep(random.random() + 0.5) # whenever we call an async method, we need to await it

async def process_data(n, data: list):
    processed = 0
    while processed < n:
        item = await data.get() # without the await we get a coroutine object, with the await we get a tuple

        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN + " +++ Processed value {} after {:,.2f} sec".format(value, dt.total_seconds()), flush=True)
        await asyncio.sleep(0.5)

if __name__ == '__main__':
    main() # Total time: 10.74 sec