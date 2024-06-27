class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def shift(self, dx: int, dy: int) -> 'Point':
        return Point(self.x + dx, self.y + dy)

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'


class Offset:
    @staticmethod
    def random(max_x: int, max_y: int) -> 'Offset':
        import random
        return Offset(random.randint(-max_x, max_x), random.randint(-max_y, max_y))

    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __iter__(self):
        return iter((self.dx, self.dy))
