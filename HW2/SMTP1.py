import sys, os
from SMTP_Validity import isMailFromCMD, isRCPTToCMD, isData, isEndData, responseCodes

def main():
	# State will be 0 if waiting for MAIL FROM: cmd, 1 if waiting for RCPT TO: cmd, and 2 if waiting for end of data cmd
	
	state = 0
	sender = ''
	recipients = []
	messages = []


	for line in sys.stdin:

		sys.stdout.write(line)

		if state == 0:
			fromCode = responseCodes(isMailFromCMD(line))

			# If its a valid mail from cmd
			if fromCode == '250 OK':
				state = 1
				sender = extractAddress(line)
				sys.stdout.write(fromCode + '\n')

			# Check syntax errors, then out of order, then parameter error
			else:
				state = 0
				sender = ''
				recipients = []
				messages = []

				rcptToCode = responseCodes(isRCPTToCMD(line))
				dataCode = responseCodes(isData(line))

				# Syntax Error: Command name is unrecognizable
				if isSyntaxError(fromCode, rcptToCode, dataCode):
					sys.stdout.write(getFullMessage(500))

				#Parameter Error: it's the correct order
				elif fromCode != 'ERROR -- mail-from-cmd':
					sys.stdout.write(getFullMessage(501))

				else:
					sys.stdout.write(getFullMessage(503))

		elif state == 1:
			toCode = responseCodes(isRCPTToCMD(line))

			if toCode == '250 OK':
				recipients.append(extractAddress(line))
				sys.stdout.write(fromCode + '\n')

			else:
				dataCode = responseCodes(isData(line))

				if dataCode == '250 OK':
					state = 2
					sys.stdout.write(getFullMessage(354))

				# Error
				else:
					state = 0
					sender = ''
					recipients = []
					messages = []

					fromCode = responseCodes(isMailFromCMD(line))

					# Syntax Error: Command name is unrecognizable
					if isSyntaxError(fromCode, toCode, dataCode):
						sys.stdout.write(getFullMessage(500))

					# Order Error: only out of order if MAIL FROM: is good
					elif fromCode == 'ERROR -- mail-from-cmd':
						sys.stdout.write(getFullMessage(503))
						
					# Parameter error for either a data or RCPT cmd
					else:
						sys.stdout.write(getFullMessage(501))

		# Waiting for text: Just appending messages until the line is a .<CRLF>
		elif state == 2:
			endDataCode = responseCodes(isEndData(line))

			# print(endDataCode)

			if endDataCode == '250 OK':
				logMessage(sender, recipients, messages)
				sys.stdout.write(endDataCode + '\n')
				state = 0
				sender = ''
				recipients = []
				messages = []

			else:
				messages.append(line)


		else:
			sys.stdout.write("I'm broke"+'\n')


def extractAddress(line):
	leftArrowIndex = line.find('<')
	rightArrowIndex = line.find('>')

	return line[leftArrowIndex+1:rightArrowIndex]

def isSyntaxError(fromCode, toCode, dataCode):
	print('FROM: ' + fromCode + ', TO: ' + toCode + ', DATA: ' + dataCode)
	if fromCode == 'ERROR -- mail-from-cmd' and toCode == 'ERROR - rcpt-to-cmd' and dataCode == 'ERROR - data-cmd':
		return True

	return False


def getFullMessage(code):
	if code == 354:
		return '354 Start mail input; end with <CRLF>.<CRLF>\n'
	elif code == 500:
		return '500 Syntax error: command unrecognized\n'
	elif code == 501:
		return '501 Syntax error in parameters or arguments\n'
	elif code == 503:
		return '503 Bad sequence of commands\n'



def logMessage(senderEmail, recipientEmails, messageParts):
	# sys.stdout.write('COMPLETED IT'+'\n')

	msg = 'From: <' + senderEmail + '>\n'

	for recipient in recipientEmails:
		msg += 'To: < ' + recipient + '>\n'

	for part in messageParts:
		msg += part

	for recipient in recipientEmails:
		with open('forward/' + recipient, 'a') as f:
			f.write(msg)


# Run it
main()