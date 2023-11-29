'''
Battleship game

# Entities
- Ship
- board
- shots
- (abstract) actions
- (abstract) strategy

'''

from collections import defaultdict, namedtuple
from dataclasses import dataclass, field, replace
from textwrap import dedent
from functools import wraps
from itertools import count, product
from random import Random

# [Iteration 7]
class Position(namedtuple('Position', 'y x')):
    def __add__(self, other):
        return Position(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Position(self.y - other.y, self.x - other.x)

# [Iteration 1]
@dataclass(frozen=True)
class Ship:
    positions : frozenset[tuple[int, int]]

    # purpose of the game is not just to know where the ships are but also what state are they in --> frozen set of each location that has been hit so far (we need to capture every single state so that we can compare strategies) Therefore we make this immutable [Iteration 2]
    hits     : frozenset[tuple[int, int]] = field(default_factory=frozenset)

    _by_symbol = {}

    def __init_subclass__(cls, size, symbol):
        cls.size, cls.symbol = size, symbol
        cls._by_symbol[symbol] = cls

    @classmethod
    def from_positions(cls, symbol, positions):
        return cls._by_symbol[symbol](frozenset(positions))

    # If you hit some location that has not been previously hit, it will return a new object, else it will return itself
    def with_shot(self, shot):
        if shot in self.positions and shot not in self.hits:
            return replace(self, hits={*self.hits, shot})
        return self

@dataclass
class Board:
    ships_by_name : dict[str, Ship]
    size          : tuple[int, int]

    @classmethod
    def from_str(cls, raw_board):
        positions = defaultdict(set)
        for rownum, row in enumerate(raw_board.splitlines()):
            for colnum, cell in enumerate(row.split()):
                # positions[cell].add((rownum, colnum))
                positions[cell].add(Position(rownum, colnum)) # Iteration 7

        ships_by_name = {
            type(sh).__name__.lower(): sh
            for sh in (
                Ship.from_positions(sym, pos)
                for sym, pos in positions.items()
                if sym != '.'
            )
        }

        return cls(ships_by_name, (rownum, colnum))

    @property
    def status(self):
        return {
            nm: sh.positions != sh.hits
            for nm, sh in self.ships_by_name.items()
        }

class Carrier(Ship, size=5, symbol='C'): pass
class Battleship(Ship, size=4, symbol='B'): pass
class Submarine(Ship, size=3, symbol='S'): pass

# instead of modeling the state of the game as an object, we do it using a generator coroutine
## maybe we dont need the heavy object oriented approach for the game (a closure or a generator might be enough)
# [Iteration 3]
@lambda coro: wraps(coro)(lambda *a, **kw: [ci := coro(*a, **kw), next(ci)][0])
def game(board):
    # positions = defaultdict(set)
    # for rownum, row in enumerate(raw_board.splitlines()):
    #     for colnum, cell in enumerate(row.split()):
    #         positions[cell].add((rownum, colnum))

    # ships_by_name = {
    #     type(sh).__name__.lower(): sh
    #     for sh in (
    #         Ship.from_positions(sym, pos)
    #         for sym, pos in positions.items()
    #         if sym != '.'
    #     )
    # }

    # shot = yield
    # while not all(sh.positions == sh.hits for sh in ships_by_name.values()):
    #     for nm, sh in ships_by_name.items():
    #         if sh is not (new_sh := sh.with_shot(shot)):
    #             ships_by_name[nm] = new_sh
    #             res = nm
    #             break
    #     else:
    #         res = None
    #     shot = yield res

    # [Iteration 6] Simplify our main game loop
    shot = yield
    while any(board.status.values()):
        for nm, sh in board.ships_by_name.items():
            if sh is not (new_sh := sh.with_shot(shot)):
                board.ships_by_name[nm] = new_sh
                res = nm
                break
        else:
            res = None
        shot = yield res


# [Iteration 4] -> it is easy to change the strategy : All we have to do is replace this generator coroutine with another one (as a concequence of the choices that we made while modelling)
# I dont need to write an object with some subclassing iomplementation with an interface that people have to implement methods from
# Here the interface is very simple -> you pass one thing and you get one thing out
# You tell what the concequence of the last action was and you get the next action
def random_strategy(size, *, random_state=None):
    rnd = random_state if random_state is not None else Random()
    while True:
        # shot = rnd.randint(0, 5), rnd.randint(0, 5)
        shot = Position(rnd.randint(0, size[0]), rnd.randint(0, size[1])) # Iteration 7
        result = yield shot

# [Iteration 5] --> we can also have a better random strategy
# generate all the positions we can fire on and shuffle them and yeild them one by one
def better_random_strategy(size, *, random_state):
    rnd = random_state if random_state is not None else Random()
    # locations = [*product(*(range(0, sz + 1) for sz in size))]
    locations = [Position(y, x) for y, x in product(range(0, 6), repeat=2)] # Iteration 7
    rnd.shuffle(locations)
    for loc in locations:
        yield loc

# [Iteration 7]
def better_strategy(size, *, random_state=None):
    rnd = random_state if random_state is not None else Random()
    
    locations = {Position(y, y) for y, x in product(range(0, 6), repeat=2)}
    while locations:
        loc = locations.pop()
        if (yield loc) is not None:
            directions = {
                Position(+1, 0),
                Position(0, +1),
                Position(0, -1),
                Position(-1, 0),
            }
            candidates = {loc + d: d for d in directions}
            for loc in candidates.keys() & locations:
                if (yield loc) is not None:
                    d = candidates[loc]
                    new_loc = loc
                    for _ in range(5):
                        if (new_loc := new_loc + d) in locations:
                            if not (yield new_loc):
                                break
                            locations.remove(new_loc)
                    # new_loc = loc
                    # for _ in range(5):
                    #     if (new_loc := new_loc - d) in locations:
                    #         if not (yield new_loc):
                    #             break
                    #         locations.remove(new_loc)
            locations -= candidates.keys()

if __name__ == '__main__':
    # raw_board = dedent('''
    #     . . . . . .
    #     C . . . . .
    #     C B B B B .
    #     C . . . . S
    #     C . . . . S
    #     C . . . . S
    # ''').strip()

    b = Board.from_str(dedent('''
        . . . . . .
        C . . . . .
        C B B B B . 
        C . . . . S
        C . . . . S
        C . . . . S
    ''').strip())
    

    # [Iteration 6]
    # we might actually want to model the board -> we may need some information provided to us in a sttructured format --> the board could ne of any size
    # W we may need to store the state of the board


    # [Iteration 1]
    # positions = defaultdict(set)
    # for rownum, row in enumerate(raw_board.splitlines()):
    #     for colnum, cell in enumerate(row.split()):
    #         positions[cell].add((rownum, colnum))

    # [Iteration 2]
    # ships = {
    #     Ship.from_positions(sym, pos)
    #     for sym, pos in positions.items()
    #     if sym != '.'
    # }
    # ships_by_name = {type(sh).__name__.lower(): sh for sh in ships}

    # print(*ships, sep='\n')

    # print(
    #     ships_by_name['submarine'].with_shot((1, 1)),
    #     ships_by_name['submarine'].with_shot((5, 5)),
    #     sep='\n',
    # )

    # rnd = Random(10)
    # while not all(sh.positions == sh.hits for sh in ships):
    #     y, x = rnd.randint(0, 5), rnd.randint(0, 5)
    #     print(f'{y, x = }')
    #     for sh in ships:
    #         print(f'{sh.with_shot(sh) = }')
    #     break

    # strategy 1: randomly fire shots and pray [Iteration 3]
    # rnd = Random(0)
    # g = game(raw_board)
    # for x in range(10):
    #     shot = rnd.randint(0, 5), rnd.randint(0, 5)
    #     if (name := g.send(shot)):
    #         print(f'You hit a {name} at {shot}!')
    #     print(f'You missed at {shot}!')

    # let us try to access this strategy
    # [Iteration 4] --> we extract the random strategy and access it
    rnd = Random(0)
    g = game(b)
    # s = random_strategy(b.size, random_state=rnd) # 123 shots to win
    # s = better_random_strategy((5, 5), random_state=rnd) # 36 shots to win
    # s = better_random_strategy(b.size, random_state=rnd) # 36 shots to win
    s = better_strategy(b.size, random_state=rnd) # 6 shots to win 
    res = None
    for step in count():
        try:
            if (res := g.send(shot := s.send(res))):
                print(f'You hit a {res} at {shot}!')
            else:
                print(f'You missed at {shot}!')
        except StopIteration:
            print(f'Game over!')
            break
    print(f'You took {step} shots to win!')

    # this is terrible strategy --> fires at the same locations over and over again : takes 123 shots to win

    # despite the amount of object oriented approach that we take and our attempt in capturing all the important details of a game (or anything in the real world), there is no way we can capture every single nuances