import sys

def isMailFromCMD(line):
	if len(line) < 4:
		return -13
	if line[0:4] != 'MAIL':
		return -13

	index = 4
	wsLenTested = 0
	isW = 0

	while isW >= 0:
		wsLenTested += 1
		isW = isWhitespace(line[index:index+wsLenTested])

	if wsLenTested == 1:
		return isW

	# FROM:
	index = index + wsLenTested - 1

	if len(line) < (index + 5):
		return -13
	if line[index:index+5] != 'FROM:':
		return -13

	# <nullspace>: Goal is to just go as afar as there is whitespace
	line = line[index + 5:]
	index = 0

	line = line.lstrip()

	if line[0] != '<':
		return -9

	# <reverse-path>
	index = 0

	rightArrowIndex = line.find('>')

	if(rightArrowIndex == -1):
		return isReversePath(line[index:])
	
	# There is a right arrow, wahoo
	isRP = isReversePath(line[index:rightArrowIndex+1])

	if isRP < 0:
		return isRP

	# <nullspace>
	line = line[rightArrowIndex + 1:]
	index = 0

	line = line.lstrip()

	# newlineIndex = line.find('\n')

	if len(line) != 0:
		return -16

	# Sender ok
	return -14


# <whitespace> ::= <SP> | <SP> <whitespace>
def isWhitespace(strng):
	if len(strng) <= 1:
		return isSP(strng)

	isSpace = isSP(strng[:1])

	if isSpace < 0:
		return isSpace

	isW = isWhitespace(strng[1:])

	if isW < 0:
		return isW

	return isSpace + isW

# <SP> ::= the space or tab character
def isSP(char):
	return (1 if (char == ' ' or char == '\t') else -12)


# <nullspace> ::= <null> | <whitespace>
def isNullSpace(strng):
	isN = isNull(strng)

	if isN == 0:
		return isN

	isW = isWhitespace(strng)

	if isW > 0:
		return isW

	return -11

# <null> :== no character
def isNull(strng):
	return (0 if strng == '' else -10)

# <reverse-path> ::= <path>
def isReversePath(strng):
	return isPath(strng)
 
# <path> ::= "<" <mailbox> ">"
def isPath(strng):
	if len(strng) < 1:
		return -9

	if strng[:1] != '<':
		return -9

	if len(strng) == 1:
		return -7

	mailboxStr = strng[1:]
	if isMailbox(mailboxStr) > 0:
		return -9

	mailboxStr = strng[1:-1]
	isM = isMailbox(mailboxStr)

	if isM < 0:
		if startsWithMailbox(mailboxStr):
			return -9
		else:
			return isM

	if strng[-1:] != '>':
		return -9

	return 1 + isM + 1

# Tells me if the string starts with a valid mailbox
def startsWithMailbox(strng):
	foundMailbox = False

	lenChecked = 0

	while foundMailbox == False and lenChecked < len(strng):
		lenChecked += 1

		if isMailbox(strng[0:lenChecked]) > 0:
			foundMailbox = True

	return foundMailbox


# <mailbox> ::= <local-part> "@" <domain>: Find whole applicable Local Part, then check if @ is next, then find whole Domain?
def isMailbox(strng):
	index = 0
	isLP = 0

	if len(strng) == 0:
		return -7

	while isLP >= 0 and index < len(strng):
		index += 1
		isLP = isLocalPart(strng[0:index])
	
	index -= 1

	if index == 0:
		return -7

	if index == len(strng):
		return -8

	if strng[index] != '@':
		return -8

	domainStr = strng[index+1:]

	isD = isDomain(domainStr)

	if isD < 0:
		return isD

	return index + isD 

# <local-part> ::= <string>
def isLocalPart(strng):
	return isString(strng)

# <string> ::= <char> | <char> <string>
def isString(strng):
	if len(strng) <= 1:
		return isChar(strng)

	isC = isChar(strng[:1])

	if isC < 0:
		return isC

	isS = isString(strng[1:])

	if isS < 0:
		return isS

	return isC + isS

# <char> ::= any one of the printable 128 ASCII characters, but not any of <special> or <SP>
def isChar(char):
	if isSpecial(char) > 0:
		return -7
	if isSP(char) > 0:
		return -7
	if isNull(char) == 0:
		return -7

	return 1 if (ord(char) < 128) else 0

# <domain> ::= <element> | <element> "." <domain>
def isDomain(strng):
	isE = isElement(strng)

	if isE > 0:
		return isE

	dotIndex = strng.find('.')

	if(dotIndex < 0):
		return isE

	isStartE = isElement(strng[:dotIndex])

	if isStartE < 0:
		return isStartE

	isD = isDomain(strng[dotIndex+1:])

	if isD < 0:
		return isD

	return isStartE + 1 + isD


# <element> ::= <letter> | <name>
def isElement(strng):
	isL = isLetter(strng)

	if len(strng) <= 1:
		return isL
	
	if isL > 0:
		return isL

	isN = isName(strng)

	if isN > 0:
		return isN

	return isN

 
# <name> ::= <letter> <let-dig-str>
def isName(strng):
	if len(strng) == 0:
		return isLetter(strng)

	if len(strng) == 1:
		return isLetterDigitString(strng[1:])

	isL = isLetter(strng[:1])
	isLDS = isLetterDigitString(strng[1:])

	if isL < 0:
		return isL

	if isLDS < 0:
		return isLDS

	return isL + isLDS


 
# <letter> ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
def isLetter(char):
	if char.lower() == 'a':
		return 1
	if char.lower() == 'b':
		return 1
	if char.lower() == 'c':
		return 1
	if char.lower() == 'd':
		return 1
	if char.lower() == 'e':
		return 1
	if char.lower() == 'f':
		return 1
	if char.lower() == 'g':
		return 1
	if char.lower() == 'h':
		return 1
	if char.lower() == 'i':
		return 1
	if char.lower() == 'j':
		return 1
	if char.lower() == 'k':
		return 1
	if char.lower() == 'l':
		return 1
	if char.lower() == 'm':
		return 1
	if char.lower() == 'n':
		return 1
	if char.lower() == 'o':
		return 1
	if char.lower() == 'p':
		return 1
	if char.lower() == 'q':
		return 1
	if char.lower() == 'r':
		return 1
	if char.lower() == 's':
		return 1
	if char.lower() == 't':
		return 1
	if char.lower() == 'u':
		return 1
	if char.lower() == 'v':
		return 1
	if char.lower() == 'w':
		return 1
	if char.lower() == 'x':
		return 1
	if char.lower() == 'y':
		return 1
	if char.lower() == 'z':
		return 1
	return -4
 
# <let-dig-str> ::= <let-dig> | <let-dig> <let-dig-str>
def isLetterDigitString(strng):
	if len(strng) <= 1:
		return isLetterDigit(strng)

	isLD = isLetterDigit(strng[:1])

	if isLD < 0:
		return isLD

	isLDS = isLetterDigitString(strng[1:])

	if isLDS < 0:
		return isLDS

	return isLD + isLDS
 
# <let-dig> ::= <letter> | <digit>
def isLetterDigit(char):
	isD = isDigit(char)

	if isD > 0:
		return isD

	isL = isLetter(char)

	if isL > 0:
		return isL

	return -15

# <digit> ::= any one of the ten digits 0 through 9
def isDigit(char):
 	if char == '0':
 		return 1
 	if char == '1':
 		return 1
 	if char == '2':
 		return 1
 	if char == '3':
 		return 1
 	if char == '4':
 		return 1
 	if char == '5':
 		return 1
 	if char == '6':
 		return 1
 	if char == '7':
 		return 1
 	if char == '8':
 		return 1
 	if char == '9':
 		return 1

 	return -3

# <CRLF> ::= the newline character
def isCRLF(char):
	return (1 if char == '\n' else -2)

# <special> ::= "<" | ">" | "(" | ")" | "[" | "]" | "\" | "." | "," | ";" | ":" | "@" | """
def isSpecial(char):
	if char == '<':
		return 1
	if char == '>':
		return 1
	if char == '(':
		return 1
	if char == ')':
		return 1
	if char == '[':
		return 1
	if char == ']':
		return 1
	if char == '\\':
		return 1
	if char == '.':
		return 1
	if char == ',':
		return 1
	if char == ';':
		return 1
	if char == ':':
		return 1
	if char == '@':
		return 1
	if char == '\"':
		return 1
	return -1


def responseCodes(num):
	if num == -1:
		return 'ERROR -- special'
	if num == -2:
		return 'ERROR -- CRLF'
	if num == -3:
		return 'ERROR -- digit'
	if num == -4:
		return 'ERROR -- letter'
	if num == -5:
		return 'ERROR -- element'
	if num == -6:
		return 'ERROR -- domain'
	if num == -7:
		return 'ERROR -- char'
	if num == -8:
		return 'ERROR -- mailbox'
	if num == -9:
		return 'ERROR -- path'
	if num == -10:
		return 'ERROR -- null'
	if num == -11:
		return 'ERROR -- nullspace'
	if num == -12:
		return 'ERROR -- SP'
	if num == -13:
		return 'ERROR -- mail-from-cmd'
	if num == -14:
		return 'Sender ok'
	if num == -15:
		return 'ERROR - let-dig'
	if num == -16:
		return 'ERROR - CRLF'


for line in sys.stdin:
	
	sys.stdout.write(line)

	sys.stdout.write(responseCodes(isMailFromCMD(line)) + '\n')