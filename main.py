import math
import time


def measure_time(func, *args, index=None):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    if index is not None:
        result = result[index]
    return result, execution_time


def parcer(obj, n):
    args = [iter(obj)] * n
    return zip(*args)


def convert_to_hex(num):
    if num is None:
        return '0'
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


num_1_A = str(input('Перше значення: '))
num_2_B = str(input('Друге значення: '))
num_Module = str(input('Модуль: '))

A = convert_from_hex(num_1_A)
B = convert_from_hex(num_2_B)
Module = convert_from_hex(num_Module)

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


def LongSubstration(a, b):
    '''if LongCompare(a, b) == -1:
        result = LongSubstration(b, a)
        result.insert(0, 1)
        return result
'''
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
        while len(sub) > 1 and sub[-1] == 0:
            sub.pop()
        return sub



def LongMultiply(a, b):
    if LongCompare(a, b) == -1:
        return LongMultiply(b, a)

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
    if a == b:
        return ([1], [0])
    k = BitLength(b)
    remainder = a.copy()
    quotient = [0]
    while LongCompare(remainder, b) != -1:
        t = BitLength(remainder)
        c = LongShiftBitsToHigh(b, t - k)
        if LongCompare(remainder, c) < 0:
            t -= 1
            length = t - k
            c = LongShiftBitsToHigh(b, length)
        remainder = LongSubstration(remainder, c)
        temp = LongShiftBitsToHigh([1], t - k)
        quotient = LongAddition(quotient, temp)
    return (quotient, remainder)


def LongSquare(a):
    result = LongMultiply(a, a)
    return result


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
        while len(a) > 0 and a[-1] == 0:
            del a[-1]
    if b != [0]:
        while len(b) > 0 and b[-1] == 0:
            del b[-1]
    if len(a) == len(b):
        i = max(len(a), len(b)) - 1
        while i >= 0 and a[i] == b[i]:
            i -= 1
        if i == -1:
            return 0
        elif a[i] > b[i]:
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


def LongShiftDigitsToLow(n, amount):
    if len(n) - amount <= 0:
        return [0]
    i = amount - 1
    while i > -1:
        del n[i]
        i -= 1
    return n


def LongShiftBitsToHigh(number, width_shift):
    if width_shift <= 0 or number == [0]:
        return number.copy()
    remainder = width_shift % 32
    width_shift //= 32
    result = LongShiftDigitsToHigh(number.copy(), width_shift)
    if remainder > 0:
        for i in range(remainder):
            last_bit = (result[-1] >> 31) & 1
            for j in range(len(result) - 1, 0, -1):
                result[j] = ((result[j] << 1) ^ ((result[j - 1] >> 31) & 1)) & 0xFFFFFFFF
            result[0] = (result[0] << 1) & 0xFFFFFFFF
            if last_bit != 0:
                result.append(last_bit)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def LongShiftBitsToLow(number, width_shift):
    if width_shift <= 0 or number == [0]:
        return number
    remainder = width_shift % 32
    width_shift //= 32
    result = number.copy()
    for i in range(width_shift):
        result.pop(0)
    if remainder > 0:
        for i in range(remainder):
            last_bit = (result[0] & 1) << 31
            for j in range(len(result) - 1):
                result[j] = ((result[j] >> 1) ^ (result[j + 1] & 1) << 31) & 0xFFFFFFFF
            result[-1] = ((result[-1] >> 1) | last_bit) & 0xFFFFFFFF
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def BitCheck(a, i):
    c = i % 32
    j = i // 32
    return (a[j] >> c) & 1


def BitLength(a):
    result = (len(a) - 1) * 32 + a[len(a) - 1].bit_length()
    return result


#LAB2!!!


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
            sub = LongSubstration(a, b)
            col_vo_sub += 1
        elif compare_of_number == -1:
            min_ab = a
            sub = LongSubstration(b, a)
            col_vo_sub += 1
        else:
            min_ab = b
            sub = [0]
        a = min_ab
        b = sub
    divisor = LongMultiply(divisor, a)
    return divisor, compare, col_vo_sub

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
    reduction = LongSubstration(value.copy(), LongMultiply(q, module))
    while LongCompare(reduction, module) >= 0:
        reduction = LongSubstration(reduction, module)
    return reduction


def LongAdititonModule(a, b, mod):
    sum = LongAddition(a, b)
    result = LongDivideModule(sum, mod)[1]
    return result


def LongSubstractionModule(a, b, mod):
    if LongCompare(a, b) == -1:
        while LongCompare(a, b) == -1:
            a = LongAddition(a, mod)
        result = LongSubstration(a, b)
    else:
        sub = LongSubstration(a, b)
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