# Encoding and Decoding functions
def decode(val):
    if val == "0000":
        return 0
    elif val == "0001":
        return 1
    elif val == "0010":
        return 2
    elif val == "0011":
        return 3
    elif val == "0100":
        return 4
    elif val == "0101":
        return 5
    elif val == "0110":
        return 6
    elif val == "0111":
        return 7
    elif val == "1000":
        return 8
    elif val == "1001":
        return 9
    elif val == "1010":
        return 10
    elif val == "1011":
        return 11
    elif val == "1100":
        return 12
    elif val == "1101":
        return 13
    elif val == "1110":
        return 14
    elif val == "1111":
        return 15
def encode(val):
    if val == 0:
        return "0000"
    elif val == 1:
        return "0001"
    elif val == 2:
        return "0010"
    elif val == 3:
        return "0011"
    elif val == 4:
        return "0100"
    elif val == 5:
        return "0101"
    elif val == 6:
        return "0110"
    elif val == 7:
        return "0111"
    elif val == 8:
        return "1000"
    elif val == 9:
        return "1001"
    elif val == 10:
        return "1010"
    elif val == 11:
        return "1011"
    elif val == 12:
        return "1100"
    elif val == 13:
        return "1101"
    elif val == 14:
        return "1110"
    elif val == 15:
        return "1111"

# Execution function
def execute(program):
    registers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for line in program:
        if len(line.strip('\n')) != 12:
            print("ERROR: ALL LINES MUST BE 12 CHARACTERS LONG")
            return
        val1 = decode(line[0:4])
        sign = decode(line[4:8])
        val2 = decode(line[8:12])

        if sign == 0:
            registers[val1] = val2
        if sign == 1:
            registers[val1] += val2
        if sign == 2:
            registers[val1] -= val2
        if sign == 3:
            registers[val1] *= val2
        if sign == 4:
            registers[val1] /= val2
        if sign == 5:
            registers[val1] = registers[val2]
        if sign == 6:
            registers[val1] += registers[val2]
        if sign == 7:
            registers[val1] -= registers[val2]
        if sign == 8:
            registers[val1] *= registers[val2]
        if sign == 9:
            registers[val1] /= registers[val2]
        if sign == 10:
            print(registers[val1])