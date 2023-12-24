from typing import List

def fib(n: int) -> List[int]:
    numbers = []
    cur, nxt = 0, 1
    while len(numbers) < n:
        cur, nxt = nxt, cur + nxt
        numbers.append(cur)
    return numbers

def fib_gen():
    cur, nxt = 0, 1
    while True:
        yield cur
        cur, nxt = nxt, cur + nxt

# result = fib(50)
result = fib_gen()

for n in result:
    print(n, end=', ')
    if n > 1000: break