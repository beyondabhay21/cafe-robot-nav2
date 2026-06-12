class OrderQueue:

    def __init__(self):

        self.queue = []

    def add(self, table):

        self.queue.append(table)

    def next_order(self):

        if len(self.queue) == 0:
            return None

        return self.queue.pop(0)

    def empty(self):

        return len(self.queue) == 0

    def clear(self):

        self.queue.clear()