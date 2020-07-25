import numpy as np

SP = 0x00
PC = 0x00

class FLAGS:
	S = False,
	Z = False,
	A = False,
	P = False,
	C = False

class REGS:
	H = np.uint8(0x12)
	L = np.uint8(0x55)


def NOP():
	print("NOP")
	return

def MOV(src, dst):
	print("MOV " + str(src) + " - " + str(dst))
	return

cpu_8080 = {
	0x00 : NOP,
	0x08 : NOP,
	0x10 : NOP,
	0x18 : NOP,
	0x20 : NOP,
	0x28 : NOP,
	0x30 : NOP,
	0x38 : NOP,

	0x40 : lambda : MOV(REGS.H, REGS.L)
}