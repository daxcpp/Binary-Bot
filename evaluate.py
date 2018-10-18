import re

#Binary comparison operators
def is_greater(a, b):
    maxlen = max(len(str(a)), len(str(b)))
    #Normalize lengths
    a = a.zfill(maxlen)
    b = b.zfill(maxlen)
    if a[0] == '0' and b[0] == '1':
        return True
    elif a[0] == '1' and b[0] == '0':
        return False
    else:
        for i in range(0, maxlen, 1):
            if a[i] > b[i]:
                return True
    return False

#Reverse binary number function
def binary_reverse(a):
    reverse = ""

    for i in range(len(str(a)) - 1, -1, -1):
        if a[i] == '0':
            reverse = '1' + reverse
        else:
            reverse = '0' + reverse
    return binary_sum(reverse, "01")

#Binary sum
def binary_sum(a,b):
    maxlen = max(len(str(a)), len(str(b)))
    signequal = -1
    if a[0] == b[0]:
        signequal = a[0]
    #Normalize lengths
    a = a.zfill(maxlen)
    b = b.zfill(maxlen)

    result = ''
    carry = 0

    for i in range(maxlen-1, -1, -1):
        r = carry
        r += 1 if a[i] == '1' else 0
        r += 1 if b[i] == '1' else 0

        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if (signequal == '0') & (result[0] != signequal):   #Signbit check1
        result = '0' + result[1:]
    elif (signequal == '1') & (result[0] != signequal): #Signbit check2
        result = '1' + result[1:]

    return result.zfill(maxlen)

#Binary subtraction
def binary_sub(a,b):
    maxlen = max(len(str(a)), len(str(b)))
    #Normalize lengths
    a = a.zfill(maxlen)
    b = b.zfill(maxlen)
    return binary_sum(a, binary_reverse(b))

#Binary multiply
def binary_multiply(a, b):
    sum = "0"

    maxlen = max(len(str(a)), len(str(b)))

    #Normalize lengths
    a = a.zfill(maxlen)
    b = b.zfill(maxlen)

    for i in range(len(str(b)) - 1,-1, -1):
        partial = ""
        for j in range(0 , len(str(a)), 1):
            if a[j] == '1' and b[i] == '1':
                partial += '1'
            elif a[j] == '1' and b[i] == '0':
                partial += '0'
            elif a[j] == '0' and b[i] == '1':
                partial += '0'
            elif a[j] == '0' and b[j] == '0':
                partial += '0'
        partial += '0'*(len(b) - i - 1)
        sum = binary_sum(sum, partial)
    return sum.zfill(maxlen)

#Binary division
def binary_div(a, b):
    result = ""
    maxlen = max(len(str(a)), len(str(b)))
    a = a.zfill(maxlen)
    b = b.zfill(maxlen)
    print("a: " + a + " b:" + b)
    while(is_greater(a,b) or a == b):
        #print("a: " + a + " b:" + b)
        if(is_greater(a,b)):
            result = result + "1"
        else:
            result = result + "0"
        a = binary_sub(a,b)
    return result.zfill(maxlen)
#Shunting-yard algorithm (Edger Dijkstra).

#Function that controls if str is a binary
def is_binary(str):
    if re.match("^[0-1]*$", str):
        return True
    return False

#Function that controls if str is an operation
def is_name(str):
    if re.match("\w+", str):
        return True
    return False

#Function that return stack[-1] if stack is not empy else return None
def peek(stack):
    return stack[-1] if stack else None

#Function that append operation result in values stack
def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    if operator == '+':
        values.append(binary_sum(left, right))
    elif operator == '-':
        values.append(binary_sub(left, right))
    elif operator == '*':
        values.append(binary_multiply(left, right))
    elif operator == '/':
        values.append(binary_div(left, right))

def greater_precedence(op1, op2):
    precedences = {'+' : 0, '-' : 0, '*' : 1, '/' : 1}
    return precedences[op1] > precedences[op2]

def evaluate(expression):
    tokens = re.findall("[+/*()-]|[0-1]+", expression)
    values = []
    operators = []
    for token in tokens:
        if is_binary(token):
            values.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            operators.pop() # Discard the '('
        else:
            # Operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values)

    return values[0]
