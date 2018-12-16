from dfa import DFA


# class to store minimum possible Determined Formal Automata (it should be full by algorithm)
class MinDFA(DFA):

    # creates from regular expression and uses Full DFA to proceed
    def __init__(self, regular):
        super(MinDFA, self).__init__(regular, True)
        # change our letters and automata to more handy storing
        self.letters = list(sorted(self.letters))
        self.automata = {a : {c : b for b, c in self.automata[a]} for a in self.automata}
        # our automata always starts at 0, but during this algorithm it could be changed, we restore it in the end
        start = 0
        # using table as (class, transition-to-class-by-this-letter * number-of-letters) for every vertex
        classes = list(map(lambda x: [1] + [0] * len(self.letters) if x in self.end else [0] + [0] * len(self.letters),
                           self.nodes))
        # need to store previous classes table, when there are no more changes we stop the algorithm
        previous_classes = None
        while previous_classes != classes:
            previous_classes = classes
            # calculate new classes based on possible transitions from current classes
            classes = [tuple([classes[n][0]] + [(classes[self.automata[n][c]])[0] for c in self.letters])
                       for n in self.nodes]
            # we should enumerate our classes from 0 to n - 1, we use this thing (why not)
            new_numbers = {s : i for i, s in enumerate(sorted(set(classes)))}
            classes = [[new_numbers[s]] + list(s[1:]) for s in classes]
            # we should store our start point
            start = classes[0][0]
        # ends are classes, that contain end vertices
        self.end = {classes[a][0] for a in self.nodes if a in self.end}
        # we use classes (set to get only different classes) as new vertices, with transitions from classes table
        self.automata = {n[0]: [(a, self.letters[i]) for i, a in enumerate(n[1:])]
                         for n in sorted(set(tuple(a) for a in classes))}
        # regular nodes-as-range calculation
        self.nodes = range(len(self.automata))
        # code to restore 0-is-start-vertex invariant
        if start in self.end:
            self.end.remove(start)
            self.end.add(0)
        self.automata[0], self.automata[start] = self.automata[start], self.automata[0]
        self.replace(start, len(self.nodes))
        self.replace(0, start)
        self.replace(len(self.nodes), 0)

