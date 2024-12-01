import argparse


class MorseCode:
	def __init__(self):

		# this dictionary stores the conversion between english characters and morse code
		self.morse_code = {
			"A": "._",
			"N": "_.",
			"B": "_...",
			"O": "___",
			"C": "_._.",
			"P": ".__.",
			"D": "_..",
			"Q": "__._",
			"E": ".",
			"R": "._.",
			"F": ".._.",
			"S": "...",
			"G": "__.",
			"T": "_",
			"H": "....",
			"U": ".._",
			"I": "..",
			"V": "..._",
			"J": ".___",
			"W": ".__",
			"K": "_._",
			"X": "_.._",
			"L": "._..",
			"Y": "_.__",
			"M": "__",
			"Z": "__..",
			"1": ".____",
			"6": "_....",
			"2": "..___",
			"7": "__...",
			"3": "...__",
			"8": "___..",
			"4": "...._",
			"9": "____.",
			"5": ".....",
			"0": "_____",
			" ": "/",
			"?": "..__..",
			";": "_._._.",
			":": "___...",
			"/": "_.._.",
			"-": "_...._",
			"\'": ".____.",
			"\"": "._.._.",
			"(": "_.__.",
			")": "_.__._",
			"=": "_..._",
			"+": "._._.",
			"*": "_.._",
			"@": ".__._.",
			"Á": ".__._",
			"Ä": "._._",
			"É": ".._..",
			"Ñ": "__.__",
			"Ö": "___.",
			"Ü": "..__",
			".": " "}

	def to_morsecode(self, string):
		return ' '.join([self.morse_code[char.upper()] for char in string])

	def to_english(self, morse_code_str):

		morse_code_list = morse_code_str.split(" ")

		output = ""

		for sub_sequence in morse_code_list:
			for key in self.morse_code.keys():
				if self.morse_code[key] == sub_sequence:
					output += key
					break

		return output


if __name__ == '__main__':
	print(MorseCode().to_morsecode('Phan anh Tu'))
	print(MorseCode().to_english('.__. .... ._ _. / ._ _. .... / _ .._'))