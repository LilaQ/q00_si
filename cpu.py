import numpy as np

#	vars
INTERRUPTS_ENABLED = False
SP = np.uint16(0x0000)
PC = np.uint16(0x0000)
shiftReg = np.uint16(0x0000)
shiftOff = 0
memory = [0] * 0x10000

#	keys
L = 0
R = 0
F = 0
C = 0
ST = 0

def loadToMem(f, dest):
	with open(f, "rb") as f:
		res = f.read()
		c = 0
		for r in res:
			memory[dest + c] = r
			c = c + 1

def loadROM(file):
	with open(file, "rb") as f:
		res = f.read()
		c = 0
		for r in res:
			memory[0x100 + c] = r
			c = c + 1
	memory[0x7] = 0xc9
	memory[0x5] = 0xd3
	memory[0x6] = 0x01
	memory[0x0] = 0xd3

def loadSI():
	loadToMem("invaders.h", 0x0000)
	loadToMem("invaders.g", 0x0800)
	loadToMem("invaders.f", 0x1000)
	loadToMem("invaders.e", 0x1800)

def getVRAM():
	return memory[0x2400:0x4000]

def getPC():
	global PC
	return PC

def getSP():
	global SP
	return SP

def getREGS():
	global REGS
	return REGS

def getFLAGS():
	global FLAGS
	return FLAGS

def setKeys(_L, _R, _F, _C, _ST):
	global L, R, F, C, ST
	L = _L
	R = _R
	F = _F
	C = _C
	ST = _ST

class FLAGS:
	S = False
	Z = False
	A = False
	P = False
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

def interrupt(adr):
	global PC
	pushToStack(PC)
	PC = adr

def M():
	return memory[REGS.H<<8|REGS.L]

def NOP(len=1):
	global PC
	PC = PC + 1
	return len

def MOV_A(src, len=5):
	global PC
	REGS.A = src
	PC = PC + 1
	return len

def MOV_B(src, len=5):
	global PC
	REGS.B = src
	PC = PC + 1
	return len

def MOV_C(src, len=5):
	global PC
	REGS.C = src
	PC = PC + 1
	return len

def MOV_D(src, len=5):
	global PC
	REGS.D = src
	PC = PC + 1
	return len

def MOV_E(src, len=5):
	global PC
	REGS.E = src
	PC = PC + 1
	return len

def MOV_H(src, len=5):
	global PC
	REGS.H = src
	PC = PC + 1
	return len

def MOV_L(src, len=5):
	global PC
	REGS.L = src
	PC = PC + 1
	return len

def MOV_M(src, len=7):
	global PC
	memory[REGS.H<<8|REGS.L] = src
	PC = PC + 1
	return len

def ADD(src, len=4):
	global PC
	FLAGS.C = (REGS.A + src) > 0xFF
	FLAGS.A = ((REGS.A & 0xF) + (src & 0xF)) > 0xF
	REGS.A = (REGS.A + src) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def SUB(src, len=4):
	#ADD(~src)
	global PC
	FLAGS.C = REGS.A < src
	FLAGS.A = (REGS.A & 0xF) >= (src & 0xF)
	REGS.A = (REGS.A - src) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def ADC(src, len=4):
	global PC
	_OLD_C = FLAGS.C
	FLAGS.C = (REGS.A + src + FLAGS.C) > 0xFF
	FLAGS.A = ((REGS.A & 0xF) + (src & 0xF) + _OLD_C) > 0xF
	REGS.A =  (REGS.A + src + _OLD_C) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def SBB(src, len=4):
	global PC
	_OLD_C = FLAGS.C
	FLAGS.C = (REGS.A - src - FLAGS.C) < 0x00
	FLAGS.A = (REGS.A & 0xF) >= ((src & 0xF) + _OLD_C)
	REGS.A = (REGS.A - (src + _OLD_C)) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def ANA(src, len=4):
	global PC
	FLAGS.C = False
	FLAGS.A = ((REGS.A | src) >> 3) & 1
	REGS.A = (REGS.A & src) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def XRA(src, len=4):
	global PC
	FLAGS.C = False
	FLAGS.A = False
	REGS.A = (REGS.A ^ src) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def ORA(src, len=4):
	global PC
	FLAGS.C = False
	FLAGS.A = False
	REGS.A = (REGS.A | src) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def CMP(src, len=4):
	global PC
	FLAGS.C = REGS.A < src
	FLAGS.A = (REGS.A & 0xF) >= (src & 0xF)
	tmp = REGS.A
	REGS.A = (REGS.A - src) & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	REGS.A = tmp
	PC = PC + 1
	return len

def LDAX(src_hi, src_lo, len=7, size=1):
	global PC
	REGS.A = (memory[(src_hi << 8) | src_lo]) & 0xff
	PC = PC + size
	return len

def INR_A(len=5):
	global PC
	FLAGS.A = ((REGS.A) & 0xf) == 0xf
	FLAGS.C = (REGS.A + 1) > 0xff
	REGS.A = REGS.A + 1
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_B(len=5):
	global PC
	FLAGS.A = ((REGS.B) & 0xf) == 0xf
	FLAGS.C = (REGS.B + 1) > 0xff
	REGS.B = REGS.B + 1
	FLAGS.S = REGS.B >> 7
	FLAGS.Z = REGS.B == 0
	FLAGS.P = str(bin(REGS.B)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_C(len=5):
	global PC
	FLAGS.A = ((REGS.C) & 0xf) == 0xf
	FLAGS.C = (REGS.C + 1) > 0xff
	REGS.C = REGS.C + 1
	FLAGS.S = REGS.C >> 7
	FLAGS.Z = REGS.C == 0
	FLAGS.P = str(bin(REGS.C)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_D(len=5):
	global PC
	FLAGS.A = ((REGS.D) & 0xf) == 0xf
	FLAGS.C = (REGS.D + 1) > 0xff
	REGS.D = REGS.D + 1
	FLAGS.S = REGS.D >> 7
	FLAGS.Z = REGS.D == 0
	FLAGS.P = str(bin(REGS.D)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_E(len=5):
	global PC
	FLAGS.A = ((REGS.E) & 0xf) == 0xf
	FLAGS.C = (REGS.E + 1) > 0xff
	REGS.E = REGS.E + 1
	FLAGS.S = REGS.E >> 7
	FLAGS.Z = REGS.E == 0
	FLAGS.P = str(bin(REGS.E)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_H(len=5):
	global PC
	FLAGS.A = ((REGS.H) & 0xf) == 0xf
	FLAGS.C = (REGS.H + 1) > 0xff
	REGS.H = REGS.H + 1
	FLAGS.S = REGS.H >> 7
	FLAGS.Z = REGS.H == 0
	FLAGS.P = str(bin(REGS.H)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_L(len=5):
	global PC
	FLAGS.A = ((REGS.L) & 0xf) == 0xf
	FLAGS.C = (REGS.L + 1) > 0xff
	REGS.L = REGS.L + 1
	FLAGS.S = REGS.L >> 7
	FLAGS.Z = REGS.L == 0
	FLAGS.P = str(bin(REGS.L)).count("1") % 2 == 0
	PC = PC + 1
	return len

def INR_M(len=10):
	global PC
	FLAGS.A = (memory[REGS.H<<8|REGS.L] & 0xf) == 0xf
	FLAGS.C = (memory[REGS.H<<8|REGS.L] + 1) > 0xff
	memory[REGS.H<<8|REGS.L] += 1
	FLAGS.S = memory[REGS.H<<8|REGS.L] >> 7
	FLAGS.Z = memory[REGS.H<<8|REGS.L] == 0
	FLAGS.P = str(bin(memory[REGS.H<<8|REGS.L])).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_A(len=5):
	global PC
	FLAGS.A = REGS.A != 0x00
	FLAGS.C = (REGS.A - 1) > 0xff
	REGS.A = (REGS.A - 1) & 0xff
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_B(len=5):
	global PC
	FLAGS.A = REGS.B != 0x00
	FLAGS.C = (REGS.B - 1) > 0xff
	REGS.B = (REGS.B - 1) & 0xff
	FLAGS.S = REGS.B >> 7
	FLAGS.Z = REGS.B == 0
	FLAGS.P = str(bin(REGS.B)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_C(len=5):
	global PC
	FLAGS.A = REGS.C != 0x00
	FLAGS.C = (REGS.C - 1) > 0xff
	REGS.C = (REGS.C - 1) & 0xff
	FLAGS.S = REGS.C >> 7
	FLAGS.Z = REGS.C == 0
	FLAGS.P = str(bin(REGS.C)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_D(len=5):
	global PC
	FLAGS.A = REGS.D != 0x00
	FLAGS.C = (REGS.D - 1) > 0xff
	REGS.D = (REGS.D - 1) & 0xff
	FLAGS.S = REGS.D >> 7
	FLAGS.Z = REGS.D == 0
	FLAGS.P = str(bin(REGS.D)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_E(len=5):
	global PC
	FLAGS.A = REGS.E != 0x00
	FLAGS.C = (REGS.E - 1) > 0xff
	REGS.E = (REGS.E - 1) & 0xff
	FLAGS.S = REGS.E >> 7
	FLAGS.Z = REGS.E == 0
	FLAGS.P = str(bin(REGS.E)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_H(len=5):
	global PC
	FLAGS.A = REGS.H != 0x00
	FLAGS.C = (REGS.H - 1) > 0xff
	REGS.H = (REGS.H - 1) & 0xff
	FLAGS.S = REGS.H >> 7
	FLAGS.Z = REGS.H == 0
	FLAGS.P = str(bin(REGS.H)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_L(len=5):
	global PC
	FLAGS.A = REGS.L != 0x00
	FLAGS.C = (REGS.L - 1) > 0xff
	REGS.L = (REGS.L - 1) & 0xff
	FLAGS.S = REGS.L >> 7
	FLAGS.Z = REGS.L == 0
	FLAGS.P = str(bin(REGS.L)).count("1") % 2 == 0
	PC = PC + 1
	return len

def DCR_M(len=10):
	global PC
	FLAGS.A = memory[(REGS.H<<8|REGS.L)] != 0x00
	FLAGS.C = (memory[(REGS.H<<8|REGS.L)] - 1) > 0xff
	memory[(REGS.H<<8|REGS.L)] = (memory[(REGS.H<<8|REGS.L)] - 1) & 0xff
	FLAGS.S = memory[(REGS.H<<8)|REGS.L] >> 7
	FLAGS.Z = memory[(REGS.H<<8)|REGS.L] == 0
	FLAGS.P = str(bin(memory[(REGS.H<<8)|REGS.L])).count("1") % 2 == 0
	PC = PC + 1
	return len

def STAX(src_hi, src_lo, len=7):
	global PC
	memory[(src_hi << 8) | src_lo] = REGS.A
	PC = PC + 1
	return len

def STA(src_hi, src_lo, len=13):
	global PC
	memory[(src_hi << 8) | src_lo] = REGS.A
	PC = PC + 3
	return len

def MVI_A(src, len=7):
	global PC
	REGS.A = src
	PC = PC + 2
	return len

def MVI_B(src, len=7):
	global PC
	REGS.B = src
	PC = PC + 2
	return len

def MVI_C(src, len=7):
	global PC
	REGS.C = src
	PC = PC + 2
	return len

def MVI_D(src, len=7):
	global PC
	REGS.D = src
	PC = PC + 2
	return len

def MVI_E(src, len=7):
	global PC
	REGS.E = src
	PC = PC + 2
	return len

def MVI_H(src, len=7):
	global PC
	REGS.H = src
	PC = PC + 2
	return len

def MVI_L(src, len=7):
	global PC
	REGS.L = src
	PC = PC + 2
	return len

def MVI_M(src, len=10):
	global PC
	memory[REGS.H<<8|REGS.L] = src
	PC = PC + 2
	return len

def RRC(len=4):
	global PC
	FLAGS.C = REGS.A & 1
	REGS.A = ((REGS.A >> 1) | (FLAGS.C << 7)) & 0xff
	PC = PC + 1 
	return len

def RLC(len=4):
	global PC
	FLAGS.C = REGS.A >> 7
	REGS.A = ((REGS.A << 1) | FLAGS.C) & 0xff
	PC = PC + 1
	return len

def RAR(len=4):
	global PC
	_C = FLAGS.C
	FLAGS.C = REGS.A & 1
	REGS.A = ((REGS.A >> 1) | (_C << 7)) & 0xff
	PC = PC + 1
	return len

def RAL(len=4):
	global PC
	_C = FLAGS.C
	FLAGS.C = (REGS.A >> 7) & 1
	REGS.A = ((REGS.A << 1) | _C) & 0xff
	PC = PC + 1
	return len

def PCHL(len=5):
	global PC
	PC = (REGS.H << 8) | REGS.L
	return len

def DAA(len=4):
	global PC
	if FLAGS.A == 1 or (REGS.A & 0xf) > 9:
		if ((REGS.A & 0xf) + 6) > 0xf:
			FLAGS.A = 1
		else:
			FLAGS.A = 0
		REGS.A = REGS.A + 6
	#if FLAGS.C == 1 or val_hi > 9 or (((REGS.A & 0xf) > 9) and (val_hi >= 9)):
	if FLAGS.C == 1 or ((REGS.A >> 4) & 0xf) > 9:
		REGS.A = REGS.A + 0x60
		if REGS.A > 0xff:
			FLAGS.C = 1
	REGS.A = REGS.A & 0xff
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	FLAGS.Z = REGS.A == 0
	FLAGS.S = REGS.A >> 7
	PC = PC + 1
	return len

def CMA(len=4):
	global PC
	REGS.A = (~REGS.A) & 0xff
	PC = PC + 1
	return len

def CMC(len=4):
	global PC
	if FLAGS.C == 1:
		FLAGS.C = 0	
	else:
		FLAGS.C = 1
	PC = PC + 1
	return len

def STC(len=4):
	global PC
	FLAGS.C = 1
	PC = PC + 1
	return len

def ADI(len=7):
	global PC
	FLAGS.A = ((REGS.A & 0xF) + (memory[PC+1] & 0xF)) > 0xF
	FLAGS.C = (REGS.A + memory[PC+1]) > 0xff
	REGS.A = (REGS.A + memory[PC+1]) & 0xff
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def ACI(len=7):
	global PC
	FLAGS.A = ((REGS.A & 0xF) + (memory[PC+1] & 0xF) + FLAGS.C) > 0xF
	REGS.A = REGS.A + memory[PC+1] + FLAGS.C
	FLAGS.C = REGS.A > 0xff
	REGS.A = REGS.A & 0xff
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def SUI(len=7):
	global PC
	FLAGS.A = 0 if (REGS.A & 0xf) < (memory[PC+1] & 0xf) else 1
	FLAGS.C = memory[PC+1] > REGS.A
	REGS.A = (REGS.A - memory[PC+1]) & 0xff
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def SBI(len=7):
	global PC
	FLAGS.A = 0 if (REGS.A & 0xf) < ((memory[PC+1] & 0xf) + FLAGS.C) else 1
	_OLD_C = FLAGS.C
	FLAGS.C = (memory[PC+1] + FLAGS.C) > REGS.A
	REGS.A = (REGS.A - (memory[PC+1] + _OLD_C)) & 0xff
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def ANI(len=7):
	global PC
	FLAGS.A = ((REGS.A | memory[PC+1]) >> 3) & 1
	REGS.A = REGS.A & memory[PC+1]
	FLAGS.C = 0
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def ORI(len=7):
	global PC
	FLAGS.A = ((REGS.A & 0xF) + (~memory[PC+1] & 0xF)) > 0xF
	REGS.A = REGS.A | memory[PC+1]
	FLAGS.C = 0
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def XRI(len=7):
	global PC
	FLAGS.A = ((REGS.A & 0xF) + (~memory[PC+1] & 0xF)) > 0xF
	REGS.A = REGS.A ^ memory[PC+1]
	FLAGS.C = 0
	FLAGS.S = REGS.A >> 7
	FLAGS.Z = REGS.A == 0
	FLAGS.P = str(bin(REGS.A)).count("1") % 2 == 0
	PC = PC + 2
	return len

def CPI(len=7):
	global PC
	FLAGS.A = 0 if (REGS.A & 0xF) < (memory[PC+1] & 0xF) else 1
	FLAGS.C = REGS.A < memory[PC+1]
	FLAGS.S = ((REGS.A - memory[PC+1]) & 0xff) >> 7
	FLAGS.Z = REGS.A == memory[PC+1]
	FLAGS.P = str(bin((REGS.A - memory[PC+1]) & 0xff)).count("1") % 2 == 0
	PC = PC + 2
	return len

def EI(len=4):
	global PC
	INTERRUPTS_ENABLED = True
	PC = PC + 1
	return len

def DI(len=4):
	global PC
	INTERRUPTS_ENABLED = False
	PC = PC + 1
	return len

#	send Akku to output device #xy
def OUT(len=10):
	global PC, shiftReg, shiftOff
	val = REGS.A
	if memory[PC+1] == 2:	
		shiftOff = val & 7
	elif memory[PC+1] == 4:
		shiftReg = (shiftReg >> 8) | (val << 8)
		#print("pushing to OUT device " + str(memory[PC+1]) + " with value " + "{:02X}".format(REGS.A))
	PC = PC + 2
	return len

#	read 8bit from input device XY to Akku
def IN(len=10):
	global PC, L, R, F, C, S, shiftReg, shiftOff
	id = memory[PC+1]
	if id == 0:
		b0 = 1	#	DIP4 self-test
		b1 = 1	#	always 1
		b2 = 1	#	always 1
		b3 = 1	#	always 1
		b4 = F	#	Fire
		b5 = L	#	Left
		b6 = R	#	Right
		b7 = 0	#	? tied to demux port 7 ?
		REGS.A = (b7 << 7) | (b6 << 6) | (b5 << 5) | (b4 << 4) | (b3 << 3) | (b2 << 2) | (b1 << 1) | b0
	elif id == 1:
		b0 = C	#	CREDIT
		b1 = 0	#	2P Start
		b2 = ST	#	1P Start
		b3 = 1	#	always 1
		b4 = F	#	1P Shot
		b5 = L	#	1P left
		b6 = R	#	1P right
		b7 = 0	#	not connected
		REGS.A = (b7 << 7) | (b6 << 6) | (b5 << 5) | (b4 << 4) | (b3 << 3) | (b2 << 2) | (b1 << 1) | b0
	elif id == 2:
		b0 = 1	#	DIP3 	00 = 3 ships	10 = 5 ships
		b1 = 1	#	DIP5	01 = 4 ships	11 = 6 ships
		b2 = 0	#	Tilt
		b3 = 0	#	DIP6	0 = extra ship at 1500	1 = extra ship at 1000
		b4 = 0	#	2P Shot
		b5 = 0	#	2P left
		b6 = 0	#	2P right
		b7 = 0	#	DIP7	Coin info displayed in demo screen	0 = ON
		REGS.A = (b7 << 7) | (b6 << 6) | (b5 << 5) | (b4 << 4) | (b3 << 3) | (b2 << 2) | (b1 << 1) | b0
	elif id == 3:
		REGS.A = shiftReg >> (8 - shiftOff)
	REGS.A = REGS.A & 0xff
	PC = PC + 2
	return len

def HLT(len=7):
	print("HLT")
	#exit(1)
	return len


#
#	JUMPS / CALLS
#

#	ret
def RET(len=10):
	global PC
	PC = popFromStack()
	return len

#	ret if condition
def RET_IF(flag, val, len=5):
	global PC
	if flag == val:
		len=11
		PC = popFromStack()
	else:
		PC = PC + 1
	return len


#	jmp
def JMP(len=10):
	global PC
	PC = (memory[PC+2] << 8) | memory[PC+1]
	return len

#	jmp if condition
def JMP_IF(flag, val, len=10):
	global PC
	if flag == val:
		PC = (memory[PC+2] << 8) | memory[PC+1]
	else: 
		PC = PC + 3
	return len


#	call
def CALL(len=17):
	global PC
	pushToStack(PC+3)
	PC = (memory[PC+2] << 8) | memory[PC+1]
	return len

#	call if condition
def CALL_IF(flag, val, len=11):
	global PC
	if flag == val:
		len = CALL()
	else:
		PC = PC + 3
	return len


#	rst
def RST(exp, len=11):
	global PC
	pushToStack(PC+2)
	PC = int(getExp(exp)+"000", 2)
	return len


#
#	16 bit load / store / moves
#

def POP_BC(len=10):
	global SP, PC
	REGS.C = memory[SP]
	SP = (SP + 1) & 0xffff
	REGS.B = memory[SP]
	SP = (SP + 1) & 0xffff
	PC = PC + 1
	return len

def POP_DE(len=10):
	global SP, PC
	REGS.E = memory[SP]
	SP = (SP + 1) & 0xffff
	REGS.D = memory[SP]
	SP = (SP + 1) & 0xffff
	PC = PC + 1
	return len

def POP_HL(len=10):
	global SP, PC
	REGS.L = memory[SP]
	SP = (SP + 1) & 0xffff
	REGS.H = memory[SP]
	SP = (SP + 1) & 0xffff
	PC = PC + 1
	return len

def POP_PSW(len=10):
	global SP, PC
	REGS.A = memory[SP]
	SP = (SP + 1) & 0xffff
	FLAGS.C = memory[SP] & 1
	FLAGS.P = (memory[SP] >> 2) & 1
	FLAGS.A = (memory[SP] >> 4) & 1
	FLAGS.Z = (memory[SP] >> 6) & 1
	FLAGS.S = (memory[SP] >> 7) & 1
	SP = (SP + 1) & 0xffff
	PC = PC + 1
	return len


def PUSH_BC(len=11):
	global SP, PC
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.B
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.C
	PC = PC + 1
	return len

def PUSH_DE(len=11):
	global SP, PC
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.D
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.E
	PC = PC + 1
	return len

def PUSH_HL(len=11):
	global SP, PC
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.H
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.L
	PC = PC + 1
	return len

def PUSH_PSW(len=11):
	global SP, PC
	SP = (SP - 1) & 0xffff
	memory[SP] = (FLAGS.S << 7) | (FLAGS.Z << 6) | (FLAGS.A << 4) | (FLAGS.P << 2) | (FLAGS.C)
	SP = (SP - 1) & 0xffff
	memory[SP] = REGS.A
	PC = PC + 1
	return len


def XTHL(len=18):
	global SP, PC
	_L = memory[SP]
	_H = memory[SP+1]
	memory[SP] = REGS.L
	memory[SP+1] = REGS.H
	REGS.L = _L
	REGS.H = _H
	PC = PC + 1
	return len

def SPHL(len=5):
	global SP, PC
	SP = (REGS.H << 8) | REGS.L
	PC = PC + 1
	return len

def XCHG(len=4):
	global SP, PC
	_D = REGS.D
	_E = REGS.E 
	REGS.D = REGS.H
	REGS.E = REGS.L
	REGS.H = _D
	REGS.L = _E
	PC = PC + 1
	return len

def LHLD(len=16):
	global SP, PC
	REGS.L = memory[memory[PC+2] << 8 | memory[PC+1]]
	REGS.H = memory[memory[PC+2] << 8 | memory[PC+1] + 1]
	PC = PC + 3
	return len

def SHLD(len=16):
	global SP, PC
	memory[memory[PC+2] << 8 | memory[PC+1]] = REGS.L
	memory[memory[PC+2] << 8 | memory[PC+1] + 1] = REGS.H
	PC = PC + 3
	return len

def LXI_BC(len=10):
	global SP, PC
	REGS.B = memory[PC+2]
	REGS.C = memory[PC+1]
	PC = PC + 3
	return len

def LXI_DE(len=10):
	global SP, PC
	REGS.D = memory[PC+2]
	REGS.E = memory[PC+1]
	PC = PC + 3
	return len

def LXI_HL(len=10):
	global SP, PC
	REGS.H = memory[PC+2]
	REGS.L = memory[PC+1]
	PC = PC + 3
	return len

def LXI_SP(len=10):
	global SP, PC
	SP = memory[PC+2] << 8 | memory[PC+1]
	PC = PC + 3
	return len


#
#	16 bit arithmetic / logical ops
#

def INX_BC(len=5):
	global SP, PC
	res = (((REGS.B << 8) | REGS.C) + 1) & 0xffff
	REGS.B = res >> 8
	REGS.C = res & 0xff
	PC = PC + 1
	return len

def INX_DE(len=5):
	global SP, PC
	res = (((REGS.D << 8) | REGS.E) + 1) & 0xffff
	REGS.D = res >> 8
	REGS.E = res & 0xff
	PC = PC + 1
	return len

def INX_HL(len=5):
	global SP, PC
	res = (((REGS.H << 8) | REGS.L) + 1) & 0xffff
	REGS.H = res >> 8
	REGS.L = res & 0xff
	PC = PC + 1
	return len

def INX_SP(len=5):
	global SP, PC
	SP = (SP + 1) & 0xffff
	PC = PC + 1
	return len

def DAD(src_hi, src_lo, len=10):
	global SP, PC
	FLAGS.C = ((REGS.H<<8|REGS.L) + (src_hi<<8|src_lo)) > 0xffff
	REGS.H = (((REGS.H<<8|REGS.L) + (src_hi<<8|src_lo)) >> 8) & 0xff
	REGS.L = ((REGS.H<<8|REGS.L) + (src_hi<<8|src_lo)) & 0xff
	PC = PC + 1
	return len

def DCX_BC(len=5):
	global SP, PC
	res = (((REGS.B << 8) | REGS.C) - 1) & 0xffff
	REGS.B = res >> 8
	REGS.C = res & 0xff
	PC = PC + 1
	return len

def DCX_DE(len=5):
	global SP, PC
	res = (((REGS.D << 8) | REGS.E) - 1) & 0xffff
	REGS.D = res >> 8
	REGS.E = res & 0xff
	PC = PC + 1
	return len

def DCX_HL(len=5):
	global SP, PC
	res = (((REGS.H << 8) | REGS.L) - 1) & 0xffff
	REGS.H = res >> 8
	REGS.L = res & 0xff
	PC = PC + 1
	return len

def DCX_SP(len=5):
	global SP, PC
	SP -= 1
	PC = PC + 1
	return len


##	helpers

def pushToStack(val):
	global SP
	SP = SP - 1
	memory[SP] = (val) >> 8
	SP = SP - 1
	memory[SP] = (val) & 0xff

def popFromStack():
	global SP
	res = (memory[SP+1] << 8 | memory[SP])
	SP = SP+2
	return res


def getExp(exp):
	return "{0:b}".format(exp)[-3:]


cpu_8080 = {
	0x00 : lambda : NOP(),
	0x01 : lambda : LXI_BC(),
	0x02 : lambda : STAX(REGS.B, REGS.C),
	0x03 : lambda : INX_BC(),
	0x04 : lambda : INR_B(),
	0x05 : lambda : DCR_B(),
	0x06 : lambda : MVI_B(memory[PC+1]),
	0x07 : lambda : RLC(),
	0x08 : lambda : NOP(),
	0x09 : lambda : DAD(REGS.B, REGS.C),
	0x0a : lambda : LDAX(REGS.B, REGS.C),
	0x0b : lambda : DCX_BC(),
	0x0c : lambda : INR_C(),
	0x0d : lambda : DCR_C(),
	0x0e : lambda : MVI_C(memory[PC+1]),
	0x0f : lambda : RRC(),

	0x10 : lambda : NOP(),
	0x11 : lambda : LXI_DE(),
	0x12 : lambda : STAX(REGS.D, REGS.E),
	0x13 : lambda : INX_DE(),
	0x14 : lambda : INR_D(),
	0x15 : lambda : DCR_D(),
	0x16 : lambda : MVI_D(memory[PC+1]),
	0x17 : lambda : RAL(),
	0x18 : lambda : NOP(),
	0x19 : lambda : DAD(REGS.D, REGS.E),
	0x1a : lambda : LDAX(REGS.D, REGS.E),
	0x1b : lambda : DCX_DE(),
	0x1c : lambda : INR_E(),
	0x1d : lambda : DCR_E(),
	0x1e : lambda : MVI_E(memory[PC+1]),
	0x1f : lambda : RAR(),

	0x20 : lambda : NOP(),
	0x21 : lambda : LXI_HL(),
	0x22 : lambda : SHLD(),
	0x23 : lambda : INX_HL(),
	0x24 : lambda : INR_H(),
	0x25 : lambda : DCR_H(),
	0x26 : lambda : MVI_H(memory[PC+1]),
	0x27 : lambda : DAA(),
	0x28 : lambda : NOP(),
	0x29 : lambda : DAD(REGS.H, REGS.L),
	0x2a : lambda : LHLD(),
	0x2b : lambda : DCX_HL(),
	0x2c : lambda : INR_L(),
	0x2d : lambda : DCR_L(),
	0x2e : lambda : MVI_L(memory[PC+1]),
	0x2f : lambda : CMA(),

	0x30 : lambda : NOP(),
	0x31 : lambda : LXI_SP(),
	0x32 : lambda : STA(memory[PC+2], memory[PC+1]),
	0x33 : lambda : INX_SP(),
	0x34 : lambda : INR_M(),
	0x35 : lambda : DCR_M(),
	0x36 : lambda : MVI_M(memory[PC+1]),
	0x37 : lambda : STC(),
	0x38 : lambda : NOP(),
	0x39 : lambda : DAD(SP >> 8, SP & 0xff),
	0x3a : lambda : LDAX(memory[PC+2], memory[PC+1], 13, 3),
	0x3b : lambda : DCX_SP(),
	0x3c : lambda : INR_A(),
	0x3d : lambda : DCR_A(),
	0x3e : lambda : MVI_A(memory[PC+1]),
	0x3f : lambda : CMC(),

	0x40 : lambda : MOV_B(REGS.B),
	0x41 : lambda : MOV_B(REGS.C),
	0x42 : lambda : MOV_B(REGS.D),
	0x43 : lambda : MOV_B(REGS.E),
	0x44 : lambda : MOV_B(REGS.H),
	0x45 : lambda : MOV_B(REGS.L),
	0x46 : lambda : MOV_B(M(), 7),
	0x47 : lambda : MOV_B(REGS.A),
	0x48 : lambda : MOV_C(REGS.B),
	0x49 : lambda : MOV_C(REGS.C),
	0x4a : lambda : MOV_C(REGS.D),
	0x4b : lambda : MOV_C(REGS.E),
	0x4c : lambda : MOV_C(REGS.H),
	0x4d : lambda : MOV_C(REGS.L),
	0x4e : lambda : MOV_C(M(), 7),
	0x4f : lambda : MOV_C(REGS.A),

	0x50 : lambda : MOV_D(REGS.B),
	0x51 : lambda : MOV_D(REGS.C),
	0x52 : lambda : MOV_D(REGS.D),
	0x53 : lambda : MOV_D(REGS.E),
	0x54 : lambda : MOV_D(REGS.H),
	0x55 : lambda : MOV_D(REGS.L),
	0x56 : lambda : MOV_D(M(), 7),
	0x57 : lambda : MOV_D(REGS.A),
	0x58 : lambda : MOV_E(REGS.B),
	0x59 : lambda : MOV_E(REGS.C),
	0x5a : lambda : MOV_E(REGS.D),
	0x5b : lambda : MOV_E(REGS.E),
	0x5c : lambda : MOV_E(REGS.H),
	0x5d : lambda : MOV_E(REGS.L),
	0x5e : lambda : MOV_E(M(), 7),
	0x5f : lambda : MOV_E(REGS.A),

	0x60 : lambda : MOV_H(REGS.B),
	0x61 : lambda : MOV_H(REGS.C),
	0x62 : lambda : MOV_H(REGS.D),
	0x63 : lambda : MOV_H(REGS.E),
	0x64 : lambda : MOV_H(REGS.H),
	0x65 : lambda : MOV_H(REGS.L),
	0x66 : lambda : MOV_H(M(), 7),
	0x67 : lambda : MOV_H(REGS.A),
	0x68 : lambda : MOV_L(REGS.B),
	0x69 : lambda : MOV_L(REGS.C),
	0x6a : lambda : MOV_L(REGS.D),
	0x6b : lambda : MOV_L(REGS.E),
	0x6c : lambda : MOV_L(REGS.H),
	0x6d : lambda : MOV_L(REGS.L),
	0x6e : lambda : MOV_L(M(), 7),
	0x6f : lambda : MOV_L(REGS.A),

	0x70 : lambda : MOV_M(REGS.B),
	0x71 : lambda : MOV_M(REGS.C),
	0x72 : lambda : MOV_M(REGS.D),
	0x73 : lambda : MOV_M(REGS.E),
	0x74 : lambda : MOV_M(REGS.H),
	0x75 : lambda : MOV_M(REGS.L),
	0x76 : lambda : HLT(),
	0x77 : lambda : MOV_M(REGS.A),
	0x78 : lambda : MOV_A(REGS.B),
	0x79 : lambda : MOV_A(REGS.C),
	0x7a : lambda : MOV_A(REGS.D),
	0x7b : lambda : MOV_A(REGS.E),
	0x7c : lambda : MOV_A(REGS.H),
	0x7d : lambda : MOV_A(REGS.L),
	0x7e : lambda : MOV_A(M(), 7),
	0x7f : lambda : MOV_A(REGS.A),

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
	0xb9 : lambda : CMP(REGS.C),
	0xba : lambda : CMP(REGS.D),
	0xbb : lambda : CMP(REGS.E),
	0xbc : lambda : CMP(REGS.H),
	0xbd : lambda : CMP(REGS.L),
	0xbe : lambda : CMP(M(), 7),
	0xbf : lambda : CMP(REGS.A),

	0xc0 : lambda : RET_IF(FLAGS.Z, 0),
	0xc1 : lambda : POP_BC(),
	0xc2 : lambda : JMP_IF(FLAGS.Z, 0),
	0xc3 : lambda : JMP(),
	0xc4 : lambda : CALL_IF(FLAGS.Z, 0),
	0xc5 : lambda : PUSH_BC(),
	0xc6 : lambda : ADI(),
	0xc7 : lambda : RST(0),
	0xc8 : lambda : RET_IF(FLAGS.Z, 1),
	0xc9 : lambda : RET(),
	0xca : lambda : JMP_IF(FLAGS.Z, 1),
	0xcb : lambda : JMP(),
	0xcc : lambda : CALL_IF(FLAGS.Z, 1),
	0xcd : lambda : CALL(),
	0xce : lambda : ACI(),
	0xcf : lambda : RST(1),

	0xd0 : lambda : RET_IF(FLAGS.C, 0),
	0xd1 : lambda : POP_DE(),
	0xd2 : lambda : JMP_IF(FLAGS.C, 0),
	0xd3 : lambda : OUT(),
	0xd4 : lambda : CALL_IF(FLAGS.C, 0),
	0xd5 : lambda : PUSH_DE(),
	0xd6 : lambda : SUI(),
	0xd7 : lambda : RST(2),
	0xd8 : lambda : RET_IF(FLAGS.C, 1),
	0xd9 : lambda : RET(),
	0xda : lambda : JMP_IF(FLAGS.C, 1),
	0xdb : lambda : IN(),
	0xdc : lambda : CALL_IF(FLAGS.C, 1),
	0xdd : lambda : CALL(),
	0xde : lambda : SBI(),
	0xdf : lambda : RST(3),

	0xe0 : lambda : RET_IF(FLAGS.P, 0),
	0xe1 : lambda : POP_HL(),
	0xe2 : lambda : JMP_IF(FLAGS.P, 0),
	0xe3 : lambda : XTHL(),
	0xe4 : lambda : CALL_IF(FLAGS.P, 0),
	0xe5 : lambda : PUSH_HL(),
	0xe6 : lambda : ANI(),
	0xe7 : lambda : RST(4),
	0xe8 : lambda : RET_IF(FLAGS.P, 1),
	0xe9 : lambda : PCHL(),
	0xea : lambda : JMP_IF(FLAGS.P, 1),
	0xeb : lambda : XCHG(),
	0xec : lambda : CALL_IF(FLAGS.P, 1),
	0xed : lambda : CALL(),
	0xee : lambda : XRI(),
	0xef : lambda : RST(5),

	0xf0 : lambda : RET_IF(FLAGS.S, 0),
	0xf1 : lambda : POP_PSW(),
	0xf2 : lambda : JMP_IF(FLAGS.S, 0),
	0xf3 : lambda : DI(),
	0xf4 : lambda : CALL_IF(FLAGS.S, 0),
	0xf5 : lambda : PUSH_PSW(),
	0xf6 : lambda : ORI(),
	0xf7 : lambda : RST(6),
	0xf8 : lambda : RET_IF(FLAGS.S, 1),
	0xf9 : lambda : SPHL(),
	0xfa : lambda : JMP_IF(FLAGS.S, 1),
	0xfb : lambda : EI(),
	0xfc : lambda : CALL_IF(FLAGS.S, 1),
	0xfd : lambda : CALL(),
	0xfe : lambda : CPI(),
	0xff : lambda : RST(7),
}