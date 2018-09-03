# Created by: Mike Ardiff
# Onyen: ardiff

# This parser reads in text from standard input and determines if the 
# text is a valid SMTP MAIL FROM command, prints out 200 ok if it is,
# and will print out ERROR --x if not, where x is the first token or line
# in the grammar that is incorrect. It will do so using the dictionary in
# dictionary.txt

import sys
from SMTP_Validity import isMailFromCMD, responseCodes

for line in sys.stdin:
	
	print(line)

	print(responseCodes(checkSMTPValidity(line)))