import re


def convert_vietnamese_to_asscii(text):
	mapping_chars = {
		"àáảãạâầấẩẫậăằắẳẵặ": "a",
		"èéẻẽẹêềếểễệ": "e",
		"đ": "d",
		"ìíỉĩị": "i",
		"òóỏõọôồốổỗộơờớởỡợ": "o",
		"ùúủũụưừứửữự": "u",
		"ỳýỷỹỵ": "y"
	}

	for viet_chars, ascii_char in mapping_chars.items():
		text = re.sub(r"[{}]+".format(viet_chars), ascii_char, text)
	return text
