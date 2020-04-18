from room import Room
from player import Player
from world import World
from util import Graph, Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

#### Explore rooms and fill Graph ####
# instantiate Graph
g = Graph()

start_rm = world.starting_room

## Implement Depth First Traversal ##
stk = Stack()
stk.push(start_rm)
visited = set()
while stk.size() > 0:
    rm = stk.pop()
    rm_id = rm.id
    if rm_id not in g.vertices:
        g.add_vertex(rm_id)

    rm_connected = rm.get_exits()
    for drt in rm_connected:
        rm_connected = rm.get_room_in_direction(drt)
        rm_connected_id = rm_connected.id
        if rm_connected_id not in g.vertices:
            g.add_vertex(rm_connected_id)
        g.add_edge(rm_id, rm_connected_id, drt)
        if rm_connected_id not in visited:
            stk.push(rm_connected)
    visited.add(rm_id)


## Method to implement Breadth First Search ##
def bfs_search_rooms(rm_id, visited, g=g):
    rms_moves = {}
    rms_moves[rm_id] = [[rm_id], []]
    q = Queue()
    q.enqueue([[rm_id], []])
    while q.size() > 0:
        rms, moves = q.dequeue()
        id_last_rm = rms[-1]
        adj = g.get_neighbors(id_last_rm)
        keys_adj = list(adj.keys())
        if len(keys_adj) == 1 and adj[keys_adj[0]] not in visited:
            not_explored_path_de = list(moves) + [keys_adj[0]]
            return not_explored_path_de
        else:
            for card_dir in adj:
                nxt_rm = adj[card_dir]
                new_rms = list(rms) + [nxt_rm]
                new_moves = list(moves) + [card_dir]
                if nxt_rm not in rms_moves:
                    q.enqueue([new_rms, new_moves])
                    rms_moves[nxt_rm] = [new_rms, new_moves]
                if nxt_rm not in visited:
                    return new_moves


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

## Logic to search room map and use BFS ##
visited = set()
visited.add(start_rm.id)
curr_rm_id = start_rm.id
num_rms = len(g.vertices)
while len(visited) < num_rms:
    mvmts = bfs_search_rooms(curr_rm_id, visited)
    for direct in mvmts:
        player.travel(direct)
        traversal_path.append(direct)
        visited.add(player.current_room.id)
    curr_rm_id = player.current_room.id

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
