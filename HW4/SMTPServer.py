import sys, os
from Dict import *

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

		# Only had MAIL FROM so far
		elif state == 1:
			toCode = responseCodes(isRCPTToCMD(line))

			if toCode == '250 OK':
				recipients.append(extractAddress(line))
				state = 2
				sys.stdout.write(fromCode + '\n')


			else:
				dataCode = responseCodes(isData(line))
				fromCode = responseCodes(isMailFromCMD(line))
			
				state = 0
				sender = ''
				recipients = []
				messages = []

				# Syntax Error: Command name is unrecognizable
				if isSyntaxError(fromCode, toCode, dataCode):
					sys.stdout.write(getFullMessage(500))

				# Parameter Error: Rest of RCPTtoCMD is invalid
				elif toCode != 'ERROR - rcpt-to-cmd':
					sys.stdout.write(getFullMessage(501))

				# OOO Error: 
				else:
					sys.stdout.write(getFullMessage(503))


		elif state == 2:
			toCode = responseCodes(isRCPTToCMD(line))

			if toCode == '250 OK':
				recipients.append(extractAddress(line))
				sys.stdout.write(fromCode + '\n')

			else:
				dataCode = responseCodes(isData(line))

				if dataCode == '250 OK':
					state = 3
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
					elif fromCode != 'ERROR -- mail-from-cmd':
						sys.stdout.write(getFullMessage(503))
						
					# Parameter error for either a data or RCPT cmd
					else:
						sys.stdout.write(getFullMessage(501))

		# Waiting for text: Just appending messages until the line is a .<CRLF>
		elif state == 3:
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



# Run it
main()