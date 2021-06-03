data = {
	"a":False,
	"b":False,
	"c":False,
	"d":False,
	"e":False,
	"f":False,
	"g":False,
	"h":False,
	"i":False
}
marks = {}
ARRAY_MAX = 255
array = [False] * ARRAY_MAX
pointer = 0
line_num = 0
word_num = 0
truth_line = -1

def get_data(name):
	if name == "0" or name == "false":
		return False
	elif name == "1" or name == "true":
		return True
	elif name == "ptd":
		return array[pointer]
	try:
		return data[name]
	except:
		raise NameError("Line {0}: {1} doesn't exist".format(line_num, name))

filename = input("Enter a filepath : ")

with open(filename) as program_file:
	program = program_file.readlines()

	line_num_max = len(program)

	for i in range(line_num_max):
		program[i] = program[i].replace('\n', '').split(' ')

	while line_num < line_num_max:
		word = program[line_num][word_num].lower()

		if word == "print":
			word_num += 1
			word = program[line_num][word_num].lower()
			print(get_data(word))
		elif word == "change":
			word_num += 1
			word = program[line_num][word_num].lower()
			if not word in data.keys():
				if word == "ptd":
					array[pointer] = not array[pointer]
				else:
					raise NameError("Line {0}: {1} isn't a variable name".format(line_num, word))
			else:
				data[word] = not get_data(word)
		elif word == "truth":
			word_num += 1
			word = program[line_num][word_num].lower()
			if get_data(word):
				truth_line = line_num
		elif word == "return":
			if truth_line != -1:
				line_num = truth_line
				word_num = -1
		elif word == "jump":
			word_num += 1
			word = program[line_num][word_num].lower()
			old_line_num = line_num
			try:
				line_num = int(word)
				if line_num >= line_num_max:
					break
			except:
				if word in marks.keys():
					line_num = marks[word]
				else:
					mark_line_num = line_num
					mark_word_num = word_num
					found = False
					while mark_line_num < line_num_max:
						mark_word = program[mark_line_num][mark_word_num].lower()
						
						if mark_word == "mark":
							mark_word_num += 1
							mark_word = program[mark_line_num][mark_word_num].lower()
							marks[mark_word] = mark_line_num
							if mark_word == word:
								found = True						
								line_num = marks[mark_word]
						mark_word_num += 1
						if mark_word_num == len(program[mark_line_num]):
							mark_word_num = 0
							mark_line_num += 1
					if not found:
						mark_line_num = 0
						mark_word_num = 0
						while mark_line_num < line_num:
							mark_word = program[mark_line_num][mark_word_num].lower()
							
							if mark_word == "mark":
								mark_word_num += 1
								mark_word = program[mark_line_num][mark_word_num].lower()
								marks[mark_word] = mark_line_num
								if mark_word == word:
									found = True						
									line_num = marks[mark_word]

							mark_word_num += 1
							if mark_word_num == len(program[mark_line_num]):
								mark_word_num = 0
								mark_line_num += 1
						if not found: break
			program[old_line_num][word_num-1] = "usedjump"
			word_num = -1
		elif word == "input":
			word_num += 1
			word = program[line_num][word_num].lower()
			if not word in data.keys():
				if word == "ptd":
					inpu = None
					msg = "Enter true or false : "
					while inpu != "true" and inpu != "false":
						inpu = input(msg).lower()
						msg = "Sorry, please enter true or false : "
					if inpu == "true":
						array[pointer] = True
					else:
						array[pointer] = False
				else:
					raise NameError("Line {0}: {1} isn't a variable name".format(line_num, word))
			else:
				inpu = None
				msg = "Enter true or false : "
				while inpu != "true" and inpu != "false":
					inpu = input(msg).lower()
					msg = "Sorry, please enter true or false : "
				if inpu == "true":
					data[word] = True
				else:
					data[word] = False
		elif word == "ascii":
			code = 0
			for i in range(7, 0, -1):
				word_num += 1
				code += get_data(program[line_num][word_num]) * pow(2, i)
			word_num += 1
			code += get_data(program[line_num][word_num])
			print(chr(code), end='')
		elif word == "mark":
			word_num += 1
			word = program[line_num][word_num].lower()
			marks[word] = line_num
		elif word == "incptr":
			pointer = (pointer + 1) % ARRAY_MAX
		elif word == "decptr":
			pointer = (pointer - 1) % ARRAY_MAX

		word_num += 1
		if word_num == len(program[line_num]):
			word_num = 0
			line_num += 1

