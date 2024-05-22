import math
import time


def parcer(obj, n):
    args = [iter(obj)] * n
    return zip(*args)


def convert_to_hex(num):
    if num == [0]:
        return '0'
    i = len(num) - 1
    while num[i] == 0:
        i -= 1
        if i == -1:
            return '0'
    num.reverse()
    hex_num = ''
    for i in range(len(num)):
        hex_el = hex(num[i])[2:]
        if len(hex_el) != 8:
            zeros = (8 - len(hex_el)) * '0'
            hex_str = zeros + hex_el
            hex_num += hex_str
        else:
            hex_num += hex_el
        hex_num = hex_num.lstrip('0')
    num.reverse()
    return hex_num.swapcase()


def convert_from_hex(hex_num):
    n = math.ceil(len(hex_num) / 8)
    hexs = []
    decs = []
    if len(hex_num) % 8 == 0:
        hexs = [''.join(i) for i in parcer(hex_num, 8)]
    else:
        zeros = 8 * n - len(hex_num)
        str_zeros = zeros * '0'
        final_hex = str_zeros + hex_num
        hexs = [''.join(i) for i in parcer(final_hex, 8)]
    for i in range(len(hexs)):
        decs.append(int(hexs[i], 16))
    decs.reverse()
    return decs


num_1_A = str(input('Enter the first number: '))
num_2_B = str(input('Enter the second number: '))
num_Module = str(input('Enter the module: '))
Module = convert_from_hex(num_Module)
A = convert_from_hex(num_1_A)
B = convert_from_hex(num_2_B)


def LongAddition(a, b):
    max_len = max(len(a), len(b))
    carry = 0
    sum = []
    for i in range(max_len):
        temp_A = int(a[i]) if i < len(a) else 0
        temp_B = int(b[i]) if i < len(b) else 0
        temp = temp_A + temp_B + carry
        sum.append(temp & (2 ** 32 - 1))
        carry = temp >> 32
    if carry > 0:
        sum.append(carry)
    return sum


def LongSubstraction(a, b):
    borrow = 0
    sub = []
    max_len = max(len(a), len(b))
    for i in range(max_len):
        temp_A = int(a[i]) if i < len(a) else 0
        temp_B = int(b[i]) if i < len(b) else 0
        temp = temp_A - temp_B - borrow
        if temp >= 0:
            sub.append(temp)
            borrow = 0
        else:
            sub.append((2 ** 32 + temp))
            borrow = 1
    if borrow != 0:
        return None
    else:
        return sub


def LongMultiply(a, b):
    if LongCompare(a, b) == -1:
        return LongMultiply(b, a)

    max_len = max(len(a), len(b))
    mul = [0] * (len(a) + len(b))

    for i in range(len(b)):
        carry = 0
        for j in range(len(a)):
            temp = mul[i + j] + a[j] * b[i] + carry
            mul[i + j] = temp & (2 ** 32 - 1)
            carry = temp >> 32

        if carry > 0:
            mul[i + len(a)] += carry

    while len(mul) > 1 and mul[-1] == 0:
        mul.pop()

    return mul


def LongDivideModule(a, b):
    k = BitLength(b)
    remainder = a
    div = []
    while LongCompare(remainder, b) != -1:
        t = BitLength(remainder)
        c = LongShiftBitsToHigh(b, t - k)
        if LongCompare(remainder, c) == -1:
            t -= 1
            while b[0] == 0:
                b = b[1:]
            c = LongShiftBitsToHigh(b, t - k)
        remainder = LongSubstraction(remainder, c)
        div = LongAddition(div, LongShiftBitsToHigh([1], t - k))
        while b[0] == 0:
            b = b[1:]
    return [div, remainder]


def LongSquare(a):
    return LongMultiply(a, a)


def LongPower(a, b):
    pow = [1]
    for i in range(BitLength(b)):
        if BitCheck(b, i) == 1:
            pow = LongMultiply(pow, a)
        a = LongMultiply(a, a)
        while len(a) < len(pow):
            a.append(0)
    return pow


def LongCompare(a, b):
    if a != [0]:
        while a[len(a) - 1] == 0:
            del a[len(a) - 1]
    if b != [0]:
        while b[len(b) - 1] == 0:
            del b[len(b) - 1]
    if len(a) == len(b):
        i = max(len(a), len(b)) - 1
        while a[i] == b[i]:
            i -= 1
            if i == -1:
                return 0
        else:
            if a[i] > b[i]:
                return 1
            else:
                return -1
    elif len(a) > len(b):
        return 1
    else:
        return -1


def LongShiftDigitsToHigh(n, l):
    for i in range(l):
        n.insert(0, 0)
    return n


def LongShiftBitsToLow(n, amount):
    if amount // 32 >= len(n):
        return convert_from_hex('0')
    if amount % 32 == 0:
        return LongShiftDigitsToLow(n, amount // 32)
    b = 32 - amount % 32
    k = 0 if n[len(n) - 1] >> 32 - b != 0 else 1
    result = [0] * (len(n) - k - amount // 32)
    if k == 0:
        result[len(n) - 1] = n[len(n) - 1] >> 32 - b
        i = len(result) - 2
    else:
        i = len(result) - 1
    for j in reversed(range(amount // 32 + 1, len(n))):
        result[i] = (n[j] << b) & (2 ** 32 - 1) | n[j - 1] >> 32 - b
        i -= 1
    return result


def LongShiftDigitsToLow(n, amount):
    if len(n) - amount <= 0:
        return [0]
    i = amount - 1
    while i > -1:
        del n[i]
        i -= 1
    return n


def LongShiftBitsToHigh(n, amount):
    if amount % 32 == 0:
        return LongShiftDigitsToHigh(n, amount // 32)
    b = 32 - amount % 32
    k = 1 if n[len(n) - 1] >> b != 0 else 0
    result = [0] * (len(n) + k + amount // 32)
    if k == 1:
        result[len(n) - 1] = n[len(n) - 1] >> b
        i = len(result) - 2
    else:
        i = len(result) - 1
    for j in reversed(range(1, len(n))):
        result[i] = (n[j] << 32 - b) & (2 ** 32 - 1) | n[j - 1] >> b
        i -= 1
    result[i] = (n[0] << 32 - b) & (2 ** 32 - 1)
    return result


def BitCheck(a, i):
    c = i % 32
    j = i // 32
    return (a[j] >> c) & 1


def BitLength(a):
    return (len(a) - 1) * 32 + a[len(a) - 1].bit_length()


def measure_time(func, *args, index=None):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    if index is not None:
        result = result[index]
    return result, execution_time

#LAB 2!!!!!!

def GCD(a, b):
    divisor = [1]
    compare = 0
    col_vo_sub = 0
    while a[0] % 2 == 0 and b[0] % 2 == 0:
        a = LongShiftBitsToLow(a, 1)
        b = LongShiftBitsToLow(b, 1)
        divisor = LongShiftBitsToHigh(divisor, 1)
    while a[0] % 2 == 0:
        a = LongShiftBitsToLow(a, 1)
    while LongCompare(b, convert_from_hex('0')) != 0:
        compare += 1
        while b[0] % 2 == 0:
            b = LongShiftBitsToLow(b, 1)
        compare_of_number = LongCompare(a, b)
        compare += 1
        if compare_of_number == 1:
            min_ab = b
            sub = LongSubstraction(a, b)
            col_vo_sub += 1
        elif compare_of_number == -1:
            min_ab = a
            sub = LongSubstraction(b, a)
            col_vo_sub += 1
        else:
            min_ab = b
            sub = [0]
        a = min_ab
        b = sub
    divisor = LongMultiply(divisor, a)
    return divisor, compare, col_vo_sub

# print('НСД(A, B) = ' + convert_to_hex(GCD(A, B)[0]) + '; кількість порівнянь = ' + str(GCD(A, B)[1]) + '; кількість віднімань = ' + str(GCD(A, B)[2]))


def EvklidGCD(a, b):
    compare = 0
    div = 0
    while LongCompare(a, [0]) != 0 and LongCompare(b, [0]) != 0:
        compare_of_number = LongCompare(a, b)
        compare += 3
        if compare_of_number == 1:
            a = LongDivideModule(a, b)[1]
            div += 1
        elif compare_of_number == -1:
            b = LongDivideModule(b, a)[1]
            div += 1
        else:
            b = [0]
    res = LongAddition(a, b)
    return res, compare, div


# EvklidGCD(A, B)
# print('НСД(A, B) за алгоритмом Евкліда = ' + convert_to_hex(EvklidGCD(A, B)[0]) + '; кількість порівнянь = ' + str(EvklidGCD(A, B)[1]) + '; кількість ділень = ' + str(EvklidGCD(A, B)[2]))



def LCM(a, b):
    gcd = GCD(a, b)[0]
    multiply = LongMultiply(a, b)
    result = LongDivideModule(multiply, gcd)[0]
    return result


def evaluateMu(module):
    k = len(module)
    ß = LongShiftDigitsToHigh([1], 2 * k)
    µ = LongDivideModule(ß, module)[0]
    return µ


def BarrettReduction(value, module, mu):
    k = len(module)
    q = LongShiftBitsToLow(value.copy(), (k - 1) * 32)
    q = LongMultiply(q, mu)
    q = LongShiftBitsToLow(q, (k + 1) * 32)
    reduction = LongSubstraction(value.copy(), LongMultiply(q, module))
    while LongCompare(reduction, module) >= 0:
        reduction = LongSubstraction(reduction, module)
    return reduction


def LongAdititonModule(a, b, mod):
    sum = LongAddition(a, b)
    result = LongDivideModule(sum, mod)[1]
    return result


def LongSubstractionModule(a, b, mod):
    if LongCompare(a, b) == -1:
        while LongCompare(a, b) == -1:
            a = LongAddition(a, mod)
        result = LongSubstraction(a, b)
    else:
        sub = LongSubstraction(a, b)
        result = LongDivideModule(sub, mod)[1]
    return result

def LongMultiplyModule(a, b, mod):
    µ = evaluateMu(mod)
    mul = LongMultiply(a, b)
    mul_mod = BarrettReduction(mul, mod, µ)
    return mul_mod


def LongSquareMod(a, mod):
    sq = LongMultiplyModule(a, a, mod)
    return sq


def LongModulePower(a, b, mod):
    a_mod = LongDivideModule(a, mod)[1]
    b_mod = LongDivideModule(b, mod)[1]
    pow = [1]
    µ = evaluateMu(mod)
    for i in range(BitLength(b_mod)):
        if BitCheck(b_mod, i) == 1:
            pow = BarrettReduction(LongMultiply(pow, a_mod), mod, µ)
        a_mod = BarrettReduction(LongSquare(a_mod), mod, µ)
    return pow


gcd_result, gcd_time = measure_time(GCD, A, B, index=0)
print(f'GCD = {convert_to_hex(gcd_result)}')
print(f'Time taken for GCD: {gcd_time} seconds')

lcm_result, lcm_time = measure_time(LCM, A, B)
print(f'LCM = {convert_to_hex(lcm_result)}')
print(f'Time taken for LCM: {lcm_time} seconds')

mod_sum_result, mod_sum_time = measure_time(LongAdititonModule, A, B, Module)
print(f'(A+B)modModule = {convert_to_hex(mod_sum_result)}')
print(f'Time taken for (A+B)modModule: {mod_sum_time} seconds')

mod_sub_result, mod_sub_time = measure_time(LongSubstractionModule, A, B, Module)
print(f'(A-B)modModule = {convert_to_hex(mod_sub_result)}')
print(f'Time taken for (A-B)modModule: {mod_sub_time} seconds')

mod_mul_result, mod_mul_time = measure_time(LongMultiplyModule, A, B, Module)
print(f'(A*B)modModule = {convert_to_hex(mod_mul_result)}')
print(f'Time taken for (A*B)modModule: {mod_mul_time} seconds')

mod_sq_result, mod_sq_time = measure_time(LongSquareMod, A, Module)
print(f'(A**2)modModule = {convert_to_hex(mod_sq_result)}')
print(f'Time taken for (A**2)modModule: {mod_sq_time} seconds')

mod_pow_result, mod_pow_time = measure_time(LongModulePower, A, B, Module)
print(f'(A**B)modModule = {convert_to_hex(mod_pow_result)}')
print(f'Time taken for (A**B)modModule: {mod_pow_time} seconds')


