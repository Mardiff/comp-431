import sys, os
from Dict import *

def main():
	if len(sys.argv) == 2:
		forwardPath = sys.argv[1]

		f = None
		# Waiting for Mail From Command
		state = 0

		# Verify the file exists
		try:
			f = open(forwardPath, "r");
		except IOError:
			print("File " + forwardPath + " does not exist. Exiting...")
			sys.exit()

		for line in f:
			# Check if it's a valid MAIL FROM? Then convert it.
			if state == 0:
				if isValidFromStatement(line):
					sys.stdout.write("MAIL FROM" + line[4:])

					# Wait for 1 RCTP
					state = 1
				else:
					sys.exit()

			# Check if it's a valid RCPT then convert it
			elif state == 1:
				if isValidToStatement(line):
					sys.stdout.write("RCPT TO" + line[2:])

					# Wait for 1 RCPT
					state = 2
				else:
					sys.exit()

			# Decide if it's an RCPT or DATA
			elif state == 2:
				# Have to actually check if it's a valid RCPT TO
				if isValidToStatement(line):
					sys.stdout.write("RCPT TO" + line[2:])
				else:
					sys.stdout.write("DATA\n")
					# Wait for 354
					responseTo354 = sys.stdin.readline()
					sys.stderr.write(responseTo354)
					isValidResponseCode(354, responseTo354)

					state = 3
					

			# Check if it's a valid MAIL FROM to see if it should end
			# Not an elif because the state changing to 3 in the previous if statement leads into this if
			if state == 3:
				# Check MAIL FROM validity to reset state machine
				if isValidFromStatement(line):
					sys.stdout.write(".\n")

					responseToPeriod = sys.stdin.readline()
					sys.stderr.write(responseToPeriod)
					isValidResponseCode(250, responseToPeriod)

					sys.stdout.write("MAIL FROM" + line[4:])

					state = 1
				else:
					sys.stdout.write(line)

			# Need a 250 OK for every situation except when just printing the email body out
			if state != 3:
				responseCode = sys.stdin.readline()
				sys.stderr.write(responseCode)
				isValidResponseCode(250, responseCode)

		# Reached EOF: Test for ending situations
		# Ended on a From: need to print data and pass the new state to the next if statement
		if state == 2:
			sys.stdout.write("DATA\n")
			
			responseTo354 = sys.stdin.readline()
			sys.stderr.write(responseTo354)
			isValidResponseCode(354, responseTo354)

			state = 3


		# Need to deal with an email with no body
		if state == 3:
			sys.stdout.write(".\n")
			responseCode = sys.stdin.readline()
			sys.stderr.write(responseCode)
			isValidResponseCode(250, responseCode)

		SMTPQuit()

	else:
		print("Was expecting 2 command line arguments, received " + str(len(sys.argv)) + ".");

# Run it
main()