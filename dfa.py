from no_epsilon_nfa import NoEpsilonNFA
from queue import Queue
from collections import defaultdict


# Class to store Determined Final Automata (could be Full or not Full)
class DFA(NoEpsilonNFA):

    # if full = True will build Full DFA and else will build regular DFA by Thompson algorithm
    def __init__(self, regular, full=False):
        super(DFA, self).__init__(regular)
        # stores new translation table, new array of nodes, new ends, puts there {0} if needed
        new_automata = defaultdict(list)
        new_nodes = [frozenset({0})]
        new_ends = set()
        if frozenset({0}) & self.end:
            new_ends.add(frozenset({0}))
        # queue is used by Thompson algorithm
        queue = Queue()
        queue.put(frozenset({0}))
        while not queue.empty():
            node = queue.get()
            # we need to add char transition to {every possible node by this char}
            for char in set([c for a in node for b, c in self.automata[a]]):
                new_node = frozenset(b for a in node for b, c in self.automata[a] if c == char)
                # traverse next node if we should
                if new_node not in new_nodes:
                    queue.put(new_node)
                    new_nodes.append(new_node)
                # if we got an intersection with end nodes, this is end node too
                if new_node & self.end:
                    new_ends.add(new_node)
                # we should add transition by this char
                new_automata[node].append((new_node, char))
        # make our nodes without this sets
        self.end = set()
        for a, k in enumerate(new_nodes):
            self.automata[a] = new_automata[k]
            if k in new_ends:
                self.end.add(a)
        for a, k in enumerate(new_nodes):
            self.replace(k, a)
        self.remove_unreachable()
        self.nodes = range(len(new_nodes))
        # add junk vertex if we should
        if full:
            self.make_full()

    # add junk vertex and connections there
    def make_full(self):
        if all({c for b, c in self.automata[node]} == self.letters for node in self.automata): return
        for node in self.automata:
            possible_letters = {c for b, c in self.automata[node]}
            for letter in self.letters - possible_letters:
                self.automata[node].append((len(self.nodes), letter))
        self.automata[len(self.nodes)] = [(len(self.nodes), c) for c in self.letters]
        self.nodes = range(len(self.nodes) + 1)

