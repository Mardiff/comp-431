# Created by: Mike Ardiff
# Onyen: ardiff

# This parser reads in text from standard input and determines if the 
# text is a valid SMTP MAIL FROM command, prints out 200 ok if it is,
# and will print out ERROR --x if not, where x is the first token or line
# in the grammar that is incorrect. It will do so using the following
# dictionary:

# <mail-from-cmd> ::= “MAIL” <whitespace> “FROM:” <nullspace> <reverse-
#  path> <nullspace> <CRLF>
#  <whitespace> ::= <SP> | <SP> <whitespace>
#  <SP> ::= the space or tab character
#  <nullspace> ::= <null> | <whitespace>
#  <null> :== no character
# <reverse-path> ::= <path>
#  <path> ::= "<" <mailbox> ">"
#  <mailbox> ::= <local-part> "@" <domain>
#  <local-part> ::= <string>
#  <string> ::= <char> | <char> <string>
#  <char> ::= any one of the printable 128 ASCII characters, but
#  not any of <special> or <SP>
#  <domain> ::= <element> | <element> "." <domain>
#  <element> ::= <letter> | <name>
#  <name> ::= <letter> <let-dig-str>
#  <letter> ::= any one of the 52 alphabetic characters A through Z
#  in upper case and a through z in lower case
#  <let-dig-str> ::= <let-dig> | <let-dig> <let-dig-str>
#  <let-dig> ::= <letter> | <digit>
#  <digit> ::= any one of the ten digits 0 through 9
#  <CRLF> ::= the newline character
#  <special> ::= "<" | ">" | "(" | ")" | "[" | "]" | "\" | "."
#  | "," | ";" | ":" | "@" | """

import sys

for line in sys.stdin:
	print(line)
	print(checkSMTPValidity(line))

