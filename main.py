from regular_parser import parse_regular_expression
from min_dfa import MinDFA
from dfa import DFA
from no_epsilon_nfa import NoEpsilonNFA
from nfa import NFA


def main():
    regular = parse_regular_expression("(a)")
    print(regular)
    print(NFA(regular))
    print(NoEpsilonNFA(regular))
    print(DFA(regular))
    print(MinDFA(regular))


if __name__ == "__main__":
    main()