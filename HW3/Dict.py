# <rcpt-to-cmd> ::= "To: "<forward-path> <CRLF>
def isValidToStatement(line):
	# "To: "
	if len(line) < 4:
		return False

	if line[0:4] != 'To: ':
		return False

	line = line[4:]

	# <forward-path>
	rightArrowIndex = line.find('>')

	if(rightArrowIndex == -1):
		return False
	
	# There is a right arrow, wahoo
	isFP = isForwardPath(line[:rightArrowIndex+1])

	if isFP < 0:
		return False

	line = line[rightArrowIndex + 1:]
	index = 0

	line = line.lstrip()

	if len(line) != 0:
		return False
  
	# Sender ok
	return True

# <From> ::= "From: " <reverse-path> <CRLF>
def isValidFromStatement(line):
		# "From: "
	if len(line) < 6:
		return False

	if line[0:6] != 'From: ':
		return False

	line = line[6:]

	# <reverse-path>
	rightArrowIndex = line.find('>')

	if(rightArrowIndex == -1):
		return False
	
	# There is a right arrow, wahoo
	isRP = isReversePath(line[:rightArrowIndex+1])

	if isRP < 0:
		return False

	line = line[rightArrowIndex + 1:]
	index = 0

	line = line.lstrip()

	if len(line) != 0:
		return False
  
	# Sender ok
	return True

# <end-data-cmd> ::= "." <CRLF>
def isEndData(line):
	if len(line) != 2:
		return -20

	if line[0] != '.'  or line[1] != '\n':
		return -20

	return -14

# <data-cmd> ::= "DATA" <nullspace> <CRLF>
def isData(line):
	if len(line) < 4:
		return -20

	if line[0:4] != 'DATA':
		return -20

	# Checking for the stupid DATAX thing
	line = line[4:]

	if len(line) > 1:
		if isSP(line[0]) < 0:
			return -20

	line = line.lstrip()

	if len(line) > 0:
		return -16

	return -14

# <rcpt-to-cmd> ::= "RCPT" <whitespace> "TO:" <nullspace> <forward-path> <nullspace> <CRLF>
def isRCPTToCMD(line):
	# "RCPT"
	if len(line) < 4:
		return -17

	if line[0:4] != 'RCPT':
		return -17

	line = line[4:]

	# <whitespace>
	isW = 0
	wsLenTested = 0

	while isW >= 0:
		wsLenTested += 1
		isW = isWhitespace(line[0:wsLenTested])

	if wsLenTested == 1:
		return -17

	line = line[wsLenTested-1:]

	# "TO:"
	if len(line) < 3:
		return -17

	if line[0:3] != 'TO:':
		return -17

	line = line[3:]

	# <nullspace>
	line = line.lstrip()

	if len(line) == 0:
		return -9

	if line[0] != '<':
		return -9

	# <forward-path>
	rightArrowIndex = line.find('>')

	if(rightArrowIndex == -1):
		return isForwardPath(line)
	
	# There is a right arrow, wahoo
	isFP = isForwardPath(line[:rightArrowIndex+1])

	if isFP < 0:
		return isFP

	# <nullspace>
	line = line[rightArrowIndex + 1:]
	index = 0

	line = line.lstrip()

	if len(line) != 0:
		return -16

	# Sender ok
	return -14

# <forward-path> ::= <path>
def isForwardPath(strng):
	return isPath(strng)

# <mail-from-cmd> ::= "MAIL" <SP> "FROM:" <reverse-path> <CRLF>
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
		return -13

	if wsLenTested > 2 and ((wsLenTested - 1) % 4 != 0):
		return -13

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

	if len(line) == 0:
		return -9

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
		return '250 OK'
	if num == -15:
		return 'ERROR - let-dig'
	if num == -16:
		return 'ERROR - CRLF'
	if num == -17:
		return 'ERROR - rcpt-to-cmd'
	if num == -20:
		return 'ERROR - data-cmd'