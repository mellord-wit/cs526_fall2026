import sys

def isValidParenMatch(inputstring):
    openParens = []

    stringValid = True
    for i in range(len(inputstring)):
        curChar = inputstring[i]
        if curChar == "(":
            openParens.append(curChar)
        if curChar == ")":
            if len(openParens) == 0:
                stringValid = False
                break
            else:
                openParens.pop()

    if stringValid:
        if len(openParens) > 0:
            print("The string ", inputstring, " is invalid")
        else:
            print("The string ", inputstring, " is valid")
    else:
        print("The string ", inputstring, " is invalid")


def main():
    print("start solution")
    inputstring = "(){}[()]"
    isValidParenMatch(inputstring)

    inputstring = "({)}, ([{[]}], )("
    isValidParenMatch(inputstring)

    inputstring = "((((({}}}}}{))[[[])[][])())[{{}}(}}}(]]]{){()]]{){]"
    isValidParenMatch(inputstring)

main()