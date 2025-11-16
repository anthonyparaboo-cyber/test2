def get_register(register):
    return int(register.replace("X", ""))


def instruction(line):
    parts = line.replace(",", "").split()
    opcode = parts[0].upper()

    # R-type instructions
    if opcode in ["ADD", "SUB", "AND", "ORR", "EOR", "MUL"]:
        rd = get_register(parts[1])
        rn = get_register(parts[2])
        rm = get_register(parts[3])
        opcodes = {
            "ADD": "10001011000",
            "SUB": "11001011000",
            "AND": "10001010000",
            "ORR": "10101010000",
            "EOR": "11001010000",
            "MUL": "10011011000",
        }
        opcode_bin = int(opcodes[opcode], 2)
        instruction_bin = (opcode_bin << 21) | (int(rm) << 16) | (rn << 5) | rd
        return instruction_bin
    # Shift instructions
    if opcode in ["LSL", "LSR"]:
        rd = get_register(parts[1])
        rn = get_register(parts[2])
        rm = 0
        shamt = int(parts[3].replace("#", "")) & 0x3F
        opcodes = {
            "LSL": "11010011011",
            "LSR": "11010011010",
        }
        opcode_bin = int(opcodes[opcode], 2)
        instruction_bin = (
            (opcode_bin << 21) | (rm << 16) | (shamt << 10) | (rn << 5) | rd
        )
        return instruction_bin

    # I-type instructions
    if opcode in ["ADDI", "SUBI"]:
        rd = get_register(parts[1])
        rn = get_register(parts[2])
        imm = int(parts[3].replace("#", "")) & 0xFFF
        opcodes = {
            "ADDI": "1001000100",
            "SUBI": "1101000100",
        }
        opcode_bin = int(opcodes[opcode], 2)
        instruction_bin = (opcode_bin << 22) | (imm << 10) | (rn << 5) | rd
        return instruction_bin

    # D-type instructions
    if opcode in ["LDUR", "STUR"]:
        rt = get_register(parts[1])
        rn = get_register(parts[2])
        offset = int(parts[3].replace("#", "")) & 0x1FF
        opcodes = {
            "LDUR": "11111000010",
            "STUR": "11111000000",
        }
        opcode_bin = int(opcodes[opcode], 2)
        instruction_bin = (opcode_bin << 21) | (offset << 12) | (rn << 5) | rt
        return instruction_bin
    # CB-Format instructions
    if opcode in ["CBZ", "CBNZ"]:
        rt = get_register(parts[1])
        imm = int(parts[2].replace("#", "")) & 0x7FFFF
        opcodes = {
            "CBZ": "10110100",
            "CBNZ": "10110101",
        }
        opcode_bin = int(opcodes[opcode], 2)
        instruction_bin = (opcode_bin << 24) | (imm << 5) | rt
        return instruction_bin
    # B-format instructions
    if opcode == "B":
        imm = int(parts[1].replace("#", "")) & 0x3FFFFFF
        opcode_bin = int("000101", 2)
        instruction_bin = (opcode_bin << 26) | imm
        return instruction_bin


program = [
    "ADDI X1, X0, #5",
    "ADD X2, X1, X3",
    "LDUR X4, X5, #8",
    "STUR X6, X7, #16",
    "SUB X10, X11, X12",
    "CBZ X13, #32",
    "CBNZ X14, #64",
    "B #128",
    "LSL X15, X16, #2",
    "LSR X17, X18, #3",
]

for line in program:
    print(line, " --> ", f"{instruction(line):08X}")
    print(line, " --> ", f"{instruction(line):032b}")
