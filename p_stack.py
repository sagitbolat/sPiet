from collections import deque
import enum

class Stack:
    def __init__(self):
        self.current_val = 0
        self.current_col = 18
        self.stack = deque()
        self._pointer = Pointer()
    
    def push(self, value):
        self.stack.append(value)
        return value
    def pop(self):
        if self.stack:
            return self.stack.pop()
        else: return 0

    def resolve_operator(self, operator):
        a = self.pop()
        b = self.pop()
        return self.push(int(operator(b, a)))
    def _not(self):
        x = self.pop()
        if x == 0:
            return self.push(1)
        else: 
            return self.push(0)
    def greater(self):
        a = self.pop()
        b = self.pop()
        if b > a: return self.push(1)
        else: return self.push(0)
    
    def pointer(self):
        x = self.pop()
        if x > 0:
            for _ in range(x):
                self._pointer.rotate_cw()
        elif x < 0:
            for _ in range(-x):
                self._pointer.rotate_ccw()
    def switch(self):
        x = self.pop()
        if x % 2 == 1:
            self._pointer.chooser = not self._pointer.chooser

    def duplicate(self):
        self.push(self.stack[-1])
    def roll(self):
        num_rolls = self.pop() 
        depth = self.pop() - 1
        def bury_top(depth, stack):
            top = stack.pop()
            s = deque()
            for _ in range(depth):
                s.append(stack.pop())
            stack.push(top)
            for _ in range(depth):
                stack.push(s.pop())
        def raise_bottom(depth, stack):
            s = deque()
            for _ in range(depth):
                s.append(stack.pop())
            bottom = stack.pop()
            for _ in range(depth):
                stack.push(s.pop())
            stack.push(bottom)

        if num_rolls > 0:
            for _ in range(num_rolls):
                bury_top(depth, self)
        else:
            for _ in range(num_rolls):
                raise_bottom(depth, self)

    def input_num(self):
        x = int(input('IN:'))
        self.push(x)
    def input_char(self):
        x = ord(input('IN:'))
        self.push(x)
    def output_num(self):
        print('OUT:', self.pop())
    def output_char(self):
        print('OUT:', chr(self.pop()))        

class Pointer:
    def __init__(self):
        """direction values explained:
        0 - right
        1 - down
        2 - left
        3 - up
            chooser values explained:
            True - left
            False - right
        """
        self.direction = 0
        self.chooser = True
        self.total_times_stuck = 0

    def attemp_to_unstuck(self):
        self.total_times_stuck += 1
        if self.total_times_stuck % 2 == 0:
            self.rotate_cw()
        else:
            self.chooser = not self.chooser

    def rotate_cw(self):
        if self.direction == 3:
            self.direction = 0
        else:
            self.direction += 1
    def rotate_ccw(self):
        if self.direction == 0:
            self.direction = 3
        else:
            self.direction -= 1