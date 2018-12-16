

# function to make postfix-notation regular expression from expression
def parse_regular_expression(pre_regular):
    # function from [https://gist.github.com/DmitrySoshnikov/1239804] this source
    # at first we should ad concatenation where we should
    pre_regular = pre_regular.replace(" ", "")
    letters = set(pre_regular) - set("+*()")
    regular = "".join(a + "." if a in letters | set(")*") and b in letters or b in letters | set("(") and a in letters
                        or a in set("*)") and b in set("(") else a for a, b in zip(pre_regular[:-1], pre_regular[1:]))
    regular += pre_regular[-1]
    # we should add symbol to postfix notation based on it operation priority
    priority = {"(": 1, "+": 2, ".": 3}
    output = ""
    stack = []
    for c in regular:
        # open bracket - we will have some expression now, closed one means we should pop op an expression
        if c == "(":
            stack.append(c)
        elif c == ")":
            while stack[-1] != "(": output += stack.pop()
            stack.pop()
        else:
            # we should proceed forward symbols with higher priority and then add this new symbol
            while stack:
                if priority.get(stack[-1], 6) >= priority.get(c, 6):
                    output += stack.pop()
                else:
                    break
            stack.append(c)
    # we should add last in stack symbols and return
    while stack:
        output += stack.pop()
    return output
