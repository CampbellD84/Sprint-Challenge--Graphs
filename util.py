class Graph():
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vert_id):
        self.vertices[vert_id] = {}

    def add_edge(self, v1, v2, nav_direction):
        if v2 in self.vertices and v2 in self.vertices:
            self.vertices[v1][nav_direction] = v2

    def get_neighbors(self, vert_id):
        if vert_id in self.vertices:
            return self.vertices[vert_id]


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)
