class Automata:
    # defaults values
    end = {}
    automata = []
    nodes = range(0)

    # we should get a star, sum or concatenation by automata
    def star(self):
        raise NotImplementedError("Star is * sign, should be implemented for automata")

    def __add__(self, other):
        raise NotImplementedError("+ should be defined for automata")

    def __or__(self, other):
        raise NotImplementedError("concatination should be defined for automata")
