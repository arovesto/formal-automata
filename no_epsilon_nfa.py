from nfa import NFA


# class to store Not determined Final Automata (without possible epsilon transitions and in rather compact way)
class NoEpsilonNFA(NFA):
    def __init__(self, regular):
        # create regular NFA
        super(NoEpsilonNFA, self).__init__(regular)
        # convert type of automata storing to dict(node : (connection, symbol)) and we could have multiple ends now
        self.automata = {a : [(b, c) for i, b, c in self.automata if i == a] for a in self.nodes}
        # while node a have got an epsilon transition we add to A all connections it could get by epsilon transition
        for a in self.automata:
            # visited array is needed to store info about already visited nodes
            visited = set()
            while [b for b, c in self.automata[a] if c == "E" and b not in visited]:
                for b, c in self.automata[a]:
                    if c == "E" and b not in visited:
                        visited.add(b)
                        self.automata[a].extend(self.automata[b])
                        self.automata[a].remove((b, "E"))
                        if b in self.end:
                            self.end.add(a)
            # remove epsilon transitions to already visited vertices
            self.automata[a] = list({(b, c) for b, c in self.automata[a] if c != "E"})
        # if we got to ends, without no transitions, we count them as same
        for a in self.automata:
            if not self.automata[a]:
                for b in self.automata:
                    if not self.automata[b]:
                        self.replace(b, a)
        # in previous process unreachable vertices could be created, we don't nead them
        self.remove_unreachable()
        # now our vertices count not like 0...x but like arbitraly numbers, we should change that
        self.recount()
        # now we got no E transitions, so we can remove E from letters then
        self.letters -= {"E"}

    # printing method
    def __str__(self):
        return "End nodes: {ends}\n{transitions}".format(
            ends= self.end,
            transitions="\n".join("{}: {}".format(node, ", ".join(c + " -> " + str(a) for a, c in self.automata[node]))
                                  for node in self.automata))

    # method to replace b vertex with a vertex
    def replace(self, b, a):
        for i in self.automata:
            self.automata[i] = list(map(lambda x: ((a, x[1]) if x[0] == b else x), self.automata[i]))

    # method to get vertices order back
    def recount(self):
        for a,b in zip(range(len(self.automata)), list(self.automata.keys())):
            if a != b:
                self.automata[a] = self.automata[b]
                del self.automata[b]
                if b in self.end:
                    self.end.remove(b)
                    self.end.add(a)
                self.replace(b, a)
        self.nodes = range(len(self.automata))

    # BFS from zero function, to find unreachable nodes and remove them
    def remove_unreachable(self):
        reachable = set()
        stack = [0]
        while stack:
            a = stack.pop()
            reachable.add(a)
            stack.extend(b for b, c in self.automata[a] if b not in reachable)
        for a in self.nodes:
            if a not in reachable:
                del self.automata[a]
                self.end.discard(a)