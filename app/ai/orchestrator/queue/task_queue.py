from collections import deque


class TaskQueue:

    def __init__(self):

        self._queue = deque()

    def push(self, task):

        self._queue.append(task)

    def pop(self):

        if self.is_empty():

            return None

        return self._queue.popleft()

    def peek(self):

        if self.is_empty():

            return None

        return self._queue[0]

    def clear(self):

        self._queue.clear()

    def size(self):

        return len(self._queue)

    def is_empty(self):

        return len(self._queue) == 0

    def to_list(self):

        return list(self._queue)

    def __len__(self):

        return len(self._queue)

    def __iter__(self):

        return iter(self._queue)
