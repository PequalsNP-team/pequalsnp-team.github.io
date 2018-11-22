class CictroHash:
	def __init__(self):
		self.initialize_state()

	def initialize_state(self):
		self.S = [[31, 56, 156, 167], [38, 240, 174, 248]]

	def r(self):
		return self.S[0]

	def c(self):
		return self.S[1]

	def hash(self, text):
		text = self.pad(self.prepare(text))
		blocks = [text[i:i + 4] for i in range(0, len(text), 4)]
		for b in blocks:
			self.absorb(b)
		return self.squeeze()

	def pad(self, t):
		t.extend([0] * (4 - len(t) % 4))
		return t

	def prepare(self, text):
		return [ord(i) for i in text]

	def absorb(self, P):
		self.S[0] = self.xor(P, self.S[0])
		for i in range(50):
			self.round()

	def squeeze(self):
		return ''.join(['{:02x}'.format(b) for b in self.S[0]])

	def xor(self, a, b):
		return [c ^ p for c, p in zip(a, b)]

	def round(self):
		self.alfa()
		self.beta()
		self.gamma()
		self.delta()
		return self.S

	def alfa(self):
		self.S[0], self.S[1] = self.S[1], self.S[0]

	def beta(self):
		for i in range(0, len(self.S[1])):
			self.S[0][i] ^= self.S[1][len(self.S[1]) - 1 - i]

	def gamma(self):
		S1 = [
			[self.S[1][3], self.S[1][0], self.S[1][2], self.S[0][0]],
			[self.S[1][1], self.S[0][3], self.S[0][1], self.S[0][2]]
		]
		self.S = S1

	def delta(self):
		self.S[0][0] = self.rol(self.S[0][0])
		self.S[1][0] = self.rol(self.S[1][0])
		self.S[0][2] = self.rol(self.S[0][2])
		self.S[1][2] = self.rol(self.S[1][2])

		self.S[0][1] = self.ror(self.S[0][1])
		self.S[1][1] = self.ror(self.S[1][1])
		self.S[0][3] = self.ror(self.S[0][3])
		self.S[1][3] = self.ror(self.S[1][3])

	def rol(self, c):
		return ((c << 1) | (c >> 7)) & 0xff

	def ror(self, c):
		return ((c >> 1) | (c << 7)) & 0xff


# Testing
for w in [
	("HELLOWORLD", "91f1c05e"),
	("HELLOWORLD0", "91f1005e"),
]:
	h = CictroHash()
	assert(h.hash(w[0]) == w[1])

# "Differential" analysis
XOR = [0b00000001, 0b00000010, 0b00001000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]
seed = ["H", "E", "L", "L", "O", "W", "O", "R", "L", "D"]
found = {}

for x in XOR:
	for i in range(len(seed)):
		tmp = seed.copy()
		h = CictroHash()
		tmp[i] = chr(ord(seed[i]) ^ x)
		chash = h.hash("".join(tmp))
		if found.get(chash):
			print(chash, found[chash], "".join(tmp))
			exit()
		found[chash] = "".join(tmp)
