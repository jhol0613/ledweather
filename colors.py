from enum import Enum
class Colors(Enum):
	# GRB order
	VFR = (50,0,0)
	MVFR = (0,0,50)
	IFR = (0,50,0)
	LIFR = (0,25,25)
	ERROR = (20,20,20)