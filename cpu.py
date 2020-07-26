import numpy as np

SP = np.uint16(0x0000)
PC = np.uint16(0x0000)

memory = [0] * 0x3ffff

def getVRAM():
	return memory[0x2400:]

class FLAGS:
	S = False,
	Z = False,
	A = False,
	P = False,
	C = False

class REGS:
	A = np.uint8(0x00)
	F = np.uint8(0x00)
	B = np.uint8(0x00)
	C = np.uint8(0x00)
	D = np.uint8(0x00)
	E = np.uint8(0x00)
	H = np.uint8(0x00)
	L = np.uint8(0x00)

def M():
	return memory[REGS.H<<8|REGS.L]

def NOP():
	print("NOP")
	return

def MOV(dst, src, len=5):
	dst = src
	return len

def MOV_M(src, len=7):
	memory[REGS.H<<8|REGS.L] = src
	return len

def ADD(src, len=4):
	FLAGS.C = (REGS.A + src) > 0xFF
	FLAGS.A = ((REGS.A & 0xF) + (src & 0xF)) > 0xF
	REGS.A += src
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	return len

def SUB(src, len=4):
	ADD(~src)
	return len

def ADC(src, len=4):
	FLAGS.C = (REGS.A + src + FLAGS.C) > 0xFF
	FLAGS.A = ((REGS.A & 0xF) + (src & 0xF) + FLAGS.C) > 0xF
	REGS.A += src + FLAGS.C
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	return len

def SBB(src, len=4):
	ADC(~src)
	return len

def ANA(src, len=4):
	FLAGS.C = False
	FLAGS.A = False
	REGS.A = REGS.A & src
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	return len

def XRA(src, len=4):
	FLAGS.C = False
	FLAGS.A = False
	REGS.A = REGS.A ^ src
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	return len

def ORA(src, len=4):
	FLAGS.C = False
	FLAGS.A = False
	REGS.A = REGS.A | src
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	return len

def CMP(src, len=4):
	FLAGS.C = False
	FLAGS.A = False
	tmp = REGS.A
	REGS.A = REGS.A - src
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	REGS.A = trmp
	return len

def DAD(src_hi, src_lo, len=10):
	FLAGS.C = (memory[REGS.H<<8|REGS.L] + memory[src_hi<<8|src_lo]) > 0xffff
	memory[REGS.H<<8|REGS.L] = memory[REGS.H<<8|REGS.L] + memory[src_hi<<8|src_lo]
	return len

def HLT():
	print("HLT")
	exit(1)

cpu_8080 = {
	0x00 : NOP,
	0x08 : NOP,
	0x09 : lambda : DAD(REG.B, REG.C)
	0x10 : NOP,
	0x18 : NOP,
	0x19 : lambda : DAD(REG.D, REG.E)
	0x20 : NOP,
	0x28 : NOP,
	0x29 : lambda : DAD(REG.H, REG.L)
	0x30 : NOP,
	0x38 : NOP,
	0x39 : lambda : DAD(SP >> 8, SP & 0xff)

	0x40 : lambda : MOV(REGS.B, REGS.B),
	0x41 : lambda : MOV(REGS.B, REGS.C),
	0x42 : lambda : MOV(REGS.B, REGS.D),
	0x43 : lambda : MOV(REGS.B, REGS.E),
	0x44 : lambda : MOV(REGS.B, REGS.H),
	0x45 : lambda : MOV(REGS.B, REGS.L),
	0x46 : lambda : MOV(REGS.B, M(), 7),
	0x47 : lambda : MOV(REGS.B, REGS.A),
	0x48 : lambda : MOV(REGS.C, REGS.B),
	0x49 : lambda : MOV(REGS.C, REGS.C),
	0x4a : lambda : MOV(REGS.C, REGS.D),
	0x4b : lambda : MOV(REGS.C, REGS.E),
	0x4c : lambda : MOV(REGS.C, REGS.H),
	0x4d : lambda : MOV(REGS.C, REGS.L),
	0x4e : lambda : MOV(REGS.C, M(), 7),
	0x4f : lambda : MOV(REGS.C, REGS.A),

	0x50 : lambda : MOV(REGS.D, REGS.B),
	0x51 : lambda : MOV(REGS.D, REGS.C),
	0x52 : lambda : MOV(REGS.D, REGS.D),
	0x53 : lambda : MOV(REGS.D, REGS.E),
	0x54 : lambda : MOV(REGS.D, REGS.H),
	0x55 : lambda : MOV(REGS.D, REGS.L),
	0x56 : lambda : MOV(REGS.D, M(), 7),
	0x57 : lambda : MOV(REGS.D, REGS.A),
	0x58 : lambda : MOV(REGS.E, REGS.B),
	0x59 : lambda : MOV(REGS.E, REGS.C),
	0x5a : lambda : MOV(REGS.E, REGS.D),
	0x5b : lambda : MOV(REGS.E, REGS.E),
	0x5c : lambda : MOV(REGS.E, REGS.H),
	0x5d : lambda : MOV(REGS.E, REGS.L),
	0x5e : lambda : MOV(REGS.E, M(), 7),
	0x5f : lambda : MOV(REGS.E, REGS.A),

	0x60 : lambda : MOV(REGS.H, REGS.B),
	0x61 : lambda : MOV(REGS.H, REGS.C),
	0x62 : lambda : MOV(REGS.H, REGS.D),
	0x63 : lambda : MOV(REGS.H, REGS.E),
	0x64 : lambda : MOV(REGS.H, REGS.H),
	0x65 : lambda : MOV(REGS.H, REGS.L),
	0x66 : lambda : MOV(REGS.H, M(), 7),
	0x67 : lambda : MOV(REGS.H, REGS.A),
	0x68 : lambda : MOV(REGS.L, REGS.B),
	0x69 : lambda : MOV(REGS.L, REGS.C),
	0x6a : lambda : MOV(REGS.L, REGS.D),
	0x6b : lambda : MOV(REGS.L, REGS.E),
	0x6c : lambda : MOV(REGS.L, REGS.H),
	0x6d : lambda : MOV(REGS.L, REGS.L),
	0x6e : lambda : MOV(REGS.L, M(), 7),
	0x6f : lambda : MOV(REGS.L, REGS.A),

	0x70 : lambda : MOV_M(REGS.B),
	0x71 : lambda : MOV_M(REGS.C),
	0x72 : lambda : MOV_M(REGS.D),
	0x73 : lambda : MOV_M(REGS.E),
	0x74 : lambda : MOV_M(REGS.H),
	0x75 : lambda : MOV_M(REGS.L),
	0x76 : HLT,
	0x77 : lambda : MOV_M(REGS.A),
	0x78 : lambda : MOV(REGS.A, REGS.B),
	0x79 : lambda : MOV(REGS.A, REGS.C),
	0x7a : lambda : MOV(REGS.A, REGS.D),
	0x7b : lambda : MOV(REGS.A, REGS.E),
	0x7c : lambda : MOV(REGS.A, REGS.H),
	0x7d : lambda : MOV(REGS.A, REGS.L),
	0x7e : lambda : MOV(REGS.A, M(), 7),
	0x7f : lambda : MOV(REGS.A, REGS.A),

	0x80 : lambda : ADD(REGS.B),
	0x81 : lambda : ADD(REGS.C),
	0x82 : lambda : ADD(REGS.D),
	0x83 : lambda : ADD(REGS.E),
	0x84 : lambda : ADD(REGS.H),
	0x85 : lambda : ADD(REGS.L),
	0x86 : lambda : ADD(M(), 7),
	0x87 : lambda : ADD(REGS.A),

	0x88 : lambda : ADC(REGS.B),
	0x89 : lambda : ADC(REGS.C),
	0x8a : lambda : ADC(REGS.D),
	0x8b : lambda : ADC(REGS.E),
	0x8c : lambda : ADC(REGS.H),
	0x8d : lambda : ADC(REGS.L),
	0x8e : lambda : ADC(M(), 7),
	0x8f : lambda : ADC(REGS.A),

	0x90 : lambda : SUB(REGS.B),
	0x91 : lambda : SUB(REGS.C),
	0x92 : lambda : SUB(REGS.D),
	0x93 : lambda : SUB(REGS.E),
	0x94 : lambda : SUB(REGS.H),
	0x95 : lambda : SUB(REGS.L),
	0x96 : lambda : SUB(M(), 7),
	0x97 : lambda : SUB(REGS.A),

	0x98 : lambda : SBB(REGS.B),
	0x99 : lambda : SBB(REGS.C),
	0x9a : lambda : SBB(REGS.D),
	0x9b : lambda : SBB(REGS.E),
	0x9c : lambda : SBB(REGS.H),
	0x9d : lambda : SBB(REGS.L),
	0x9e : lambda : SBB(M(), 7),
	0x9f : lambda : SBB(REGS.A),

	0xa0 : lambda : ANA(REGS.B),
	0xa1 : lambda : ANA(REGS.C),
	0xa2 : lambda : ANA(REGS.D),
	0xa3 : lambda : ANA(REGS.E),
	0xa4 : lambda : ANA(REGS.H),
	0xa5 : lambda : ANA(REGS.L),
	0xa6 : lambda : ANA(M(), 7),
	0xa7 : lambda : ANA(REGS.A),

	0xa8 : lambda : XRA(REGS.B),
	0xa9 : lambda : XRA(REGS.C),
	0xaa : lambda : XRA(REGS.D),
	0xab : lambda : XRA(REGS.E),
	0xac : lambda : XRA(REGS.H),
	0xad : lambda : XRA(REGS.L),
	0xae : lambda : XRA(M(), 7),
	0xaf : lambda : XRA(REGS.A),

	0xb0 : lambda : ORA(REGS.B),
	0xb1 : lambda : ORA(REGS.C),
	0xb2 : lambda : ORA(REGS.D),
	0xb3 : lambda : ORA(REGS.E),
	0xb4 : lambda : ORA(REGS.H),
	0xb5 : lambda : ORA(REGS.L),
	0xb6 : lambda : ORA(M(), 7),
	0xb7 : lambda : ORA(REGS.A),

	0xb8 : lambda : CMP(REGS.B),
	0xb8 : lambda : CMP(REGS.C),
	0xb8 : lambda : CMP(REGS.D),
	0xb8 : lambda : CMP(REGS.E),
	0xb8 : lambda : CMP(REGS.H),
	0xb8 : lambda : CMP(REGS.L),
	0xb8 : lambda : CMP(M(), 7),
	0xb8 : lambda : CMP(REGS.A),
}