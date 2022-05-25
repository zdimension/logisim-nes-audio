import sys
inp = sys.argv[1]
fp = open(inp, "r")
outp = open(inp + ".bin", "w")
outp.write("v2.0 raw\n")
lines = [line for line in fp if line.startswith("ROW")]

NOTES = [
	"C-",
	"C#",
	"D-",
	"D#",
	"E-",
	"F-",
	"F#",
	"G-",
	"G#",
	"A-",
	"A#",
	"B-"
]

outp.write(f"{0:08x} ")

last = [0, 0, 0, 0]
for line in lines:
	_, *cols = map(str.strip, line.split(":"))
	offset = 0
	res = 0
	for i, col in enumerate(cols[:4]):	
		(note, a, b, effect, d, e) = col.split()
		val = last[i]
		if note == "...":
			pass # mute
		elif note == "---":
			val = 0 # stop
		elif note == "===":
			pass # release
		else:
			val = 128
			name, oct = note[:2], note[2]
			if oct == "#":
				nid = 0
				oct = 4
			else:
				nid = NOTES.index(name)
				oct = int(oct)
			if i in (0, 1):
				oct += 1
			val |= (oct + 1) * 12 + nid
		last[i] = val
		res |= val << offset
		offset += 8
	outp.write(f"{res:08x} ")
outp.write("\n")