from automata import Automata


# class to store Not determined Final Automata (with possible epsilon transitions)
# There are one input point and possible many end points
class NFA(Automata):
    # Method to create NFA from string
    def __init__(self, regular):
        # we should erase spaces
        regular = regular.replace(" ", "")
        # we should know our letters
        self.letters = set(regular) - set("+.*")
        # stack of automata
        stack = []
        # if we got one symbol, then we could add it, if it is ok as 0 -symbol> 1 automata
        if len(regular) <= 1:
            if regular in set("+.*"): raise ValueError("Bad input string " + regular)
            self.nodes = range(2)
            self.end = {1}
            self.automata = {(0, 1, regular)}
            return
        # now we use stack to go by string and properly manage automata
        for l in regular:
            if l in self.letters: stack.append(NFA(l));
            elif l == "+": stack.append(stack.pop() + stack.pop())
            elif l == ".": stack.append(stack.pop(-2) | stack.pop())
            elif l == "*": stack.append(stack.pop().star())
            else: raise ValueError("{} is not in {}".format(l, self.letters | set("+.*E")))
        # it is supposed, we will have one automata in stack, so it is our target automata
        if len(stack) > 1: raise ValueError("Bad input string, stack is not empty in the end")
        self.automata = stack[0].automata
        self.end = stack[0].end
        self.nodes = stack[0].nodes

    # method to show our automata
    def __str__(self):
        return "End node: {}\n{}".format(self.end, "\n".join("{}: {}"
            .format(i, ", ".join(c + " -> " + str(b) for a, b, c in self.automata if a ==i)) for i in self.nodes))

    # automata + automata is just one new node, with epsilon transition to one and other automata
    def __add__(self, other):
        self.automata = set(map(lambda x: (x[0] + 1, x[1] + 1, x[2]), self.automata))
        self.automata.add((0, 1, "E"))
        self.automata.add((0, len(self.nodes) + 1, "E"))
        self.automata.update((a + len(self.nodes) + 1, b + len(self.nodes) + 1, c) for a, b, c in other.automata)
        self.end = {a + 1 for a in self.end}
        self.end.update({a + len(self.nodes) + 1 for a in other.end})
        self.nodes = range(len(self.nodes) + len(other.nodes) + 1)
        return self

    # concatenation is just going to second automata is connected to the end of the first one by epsilon transition
    def __or__(self, other):
        self.automata.update((a, len(self.nodes), "E") for a in self.end)
        self.automata.update((a + len(self.nodes), b + len(self.nodes), c) for a, b, c in other.automata)
        self.end = {a + len(self.nodes) for a in other.end}
        self.nodes = range(len(self.nodes) + len(other.nodes))
        return self

    # in star we could get back from every of our ends, and also we use one additional node for concatenation safety
    def star(self):
        self.automata = set(map(lambda x: (x[0] + 1, x[1] + 1, x[2]), self.automata))
        self.automata.add((0, 1, "E"))
        self.end = {a + 1 for a in self.end}
        self.automata.update((a, 1, "E") for a in self.end)
        self.end = {1}
        self.nodes = range(len(self.nodes) + 1)
        return self
