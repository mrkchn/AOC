import numpy as np

def combo_op(registers, op, formula):
    if op <= 3:
        return op, op
    elif op <= 6:
        try:
            return registers[op-4], str(eval(f"{registers[op]}"))
        except:
            return registers[op-4], f"{registers[op]}"
    else:
        return None, None


def adv(registers, op, pointer, formula):
    c, cs = combo_op(registers, op, formula)
    registers[0] = int(registers[0] / (2 ** c))
    if formula:
        try:
            registers[4] = str(eval(f"int({registers[4]} / (2 ** {cs}))"))
        except:
            registers[4] = f"int({registers[4]} / (2 ** {cs}))"
    return registers, pointer+2


def bxl(registers, op, pointer, formula):
    registers[1] = registers[1] ^ op
    if formula:
        try:
            registers[5] = str(eval(f"({registers[5]} ^ {op})"))
        except:
            registers[5] = f"({registers[5]} ^ {op})"
    return registers, pointer+2


def bst(registers, op, pointer, formula):
    c, cs = combo_op(registers, op, formula)
    registers[1] = c % 8
    if formula:
        try:
            registers[6] = str(eval(f"({cs} % 8)"))
        except:
            registers[6] = f"({cs} % 8)"
    return registers, pointer+2


def jnz(registers, op, pointer, formula):
    if registers[0]:
        pointer = op
    else:
        pointer = pointer + 2
    return registers, pointer


def bxc(registers, op, pointer, formula):
    registers[1] = registers[1] ^ registers[2]
    if formula:
        try:
            registers[5] = str(eval(f"({registers[5]} ^ {registers[6]})"))
        except:
            registers[5] = f"({registers[5]} ^ {registers[6]})"
    return registers, pointer+2


def out(registers, op, pointer, formula):
    c, cs = combo_op(registers, op, formula)
    registers[3].append(c % 8)
    if formula:
        try:
            registers[7].append(str(eval(f"({cs} % 8)")))
        except:
            registers[7].append(f"({cs} % 8)")

    return registers, pointer+2


def bdv(registers, op, pointer, formula):
    c, cs = combo_op(registers, op, formula)
    registers[1] = int(registers[0] / (2 ** c))
    if formula:
        try:
            registers[5] = str(eval(f"int({registers[4]} / (2 ** {cs}))"))
        except:
            registers[5] = f"int({registers[4]} / (2 ** {cs}))"
    return registers, pointer+2


def cdv(registers, op, pointer, formula):
    c, cs = combo_op(registers, op, formula)
    registers[2] = int(registers[0] / (2 ** c))
    if formula:
        try:
            registers[6] = f"int({registers[4]} / (2 ** {cs}))"
        except:
            registers[6] = str(eval(f"int({registers[4]} / (2 ** {cs}))"))
    return registers, pointer+2


def exe(program, registers, check, formula):
    pointer = 0
    if len(registers) == 3:
        # Register 3 represents the buffer (where output is stored)
        # Registers 4-6 represent the "formula" for each register
        # Register 7 represents the buffer for formulas
        registers.extend([[], "A", str(registers[1]), str(registers[2]), []])
    else:
        registers[3] = []
        registers[4] = 'A'
        registers[5] = str(registers[1])
        registers[6] = str(registers[2])
        registers[7] = []
    while pointer < (len(program) - 1):
        registers, pointer = opcodes[program[pointer]](registers, program[pointer+1], pointer, formula)
        if (registers[3] and check) and (check[:len(registers[3])] != registers[3]):
            break
    return registers


with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

opcodes = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
registers = [int(x.split(": ")[1]) for x in raw_data[:raw_data.index('')]]
program = [int(x) for x in raw_data[raw_data.index('')+1].split(": ")[1].split(",")]

output = exe(program, registers, check=False, formula=True)
formulas = output[-1]
print(f"Solution #1: {','.join([str(i) for i in output[3]])}")

# %%
lower_bound = 1
while len(exe(program, [lower_bound] + registers[1:], check=False, formula=False)[3]) < len(program):
    lower_bound *= 2
lower_bound = int(lower_bound / 2)
upper_bound = lower_bound

while len(exe(program, [upper_bound] + registers[1:], check=False, formula=False)[3]) < len(program) + 1:
    upper_bound *= 2

# This has


