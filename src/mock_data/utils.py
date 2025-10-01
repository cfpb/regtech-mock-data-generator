# This file contains helper functions used by one or more classes 
# in order to generate clean and failing synthetic data files.

# Import
import os
from io import StringIO


def write_file(ts_input=None, lar_input=None, outpath=None):
	"""
	Takes a TS row and LAR data as dataframes. Writes LAR data to file and
	re-reads it to combine with TS data to make a full file.

	ts_input: DataFrame of a TS row
	lar_input: DataFrame of one or more LAR rows
	outpath: The full output path and file name/extension to write to
	"""
	
	string_buffer = StringIO() 
	ts_input.to_csv(string_buffer, index=False, header=False, sep='|')
	lar_input.to_csv(string_buffer, index=False, header=False, sep='|')
	
	with open(outpath, "w") as f:
		f.write(string_buffer.getvalue())


def check_digit_gen(valid=True, ULI=None):
	"""Generates a check digit for a ULI in accordance with
	https://www.consumerfinance.gov/eregulations/diff/1003-C/2015-26607_20170101/2015-26607_20180101?from_version=2015-26607_20170101#1003-C-1"""
	if ULI is None:
		raise ValueError("a ULI must be supplied")
	#GENERATING A CHECK DIGIT
	#Step 1: Starting with the leftmost character in the string that consists of the combination of the
	#Legal Entity Identifier (LEI) pursuant to § 1003.4(a)(1)(i)(A) and the additional characters identifying the
	#covered loan or application pursuant to § 1003.4(a)(1)(i)(B), replace each alphabetic character with numbers
	#in accordance with Table I below to obtain all numeric values in the string.
	
	
	#1: convert letters to digits
	#2: append '00' to right of string
	#3:Apply the mathematical function mod=(n, 97) where n= the number obtained in step 2 above and 97 is the divisor.
	#3a: Alternatively, to calculate without using the modulus operator, divide the numbers in step 2 above by 97.
	#   Truncate the remainder to three digits and multiply it by .97. Round the result to the nearest whole number.
	#4: Subtract the result in step 3 from 98. If the result is one digit, add a leading 0 to make it two digits.
	#5: The two digits in the result from step 4 is the check digit. Append the resulting check digit to the
	#   rightmost position in the combined string of characters described in step 1 above to generate the ULI.
	
	#digit_vals contains the conversion of numbers to letters
	digit_vals = {
	'A':10, 'H':17,'O':24,'V':31,'B':11,
	'I':18,'P':25,'W':32,'C':12,'J':19,
	'Q':26,'X':33,'D':13,'K':20,'R':27,
	'Y':34, 'E':14,'L':21,'S':28,'Z':35,
	'F':15,'M':22,'T':29,'G':16,'N':23,'U':30}
	
	uli_chars = list(ULI)
	mod_uli_chars = []
	for char in uli_chars:
		if char.upper() in digit_vals.keys():
			mod_uli_chars.append(str(digit_vals[char.upper()]))
		else:
			mod_uli_chars.append(char)
	mod_uli_chars.append('00') 
	digit_base = int("".join(mod_uli_chars))
	digit_modulo = digit_base % 97
	check_digit = 98 - digit_modulo

	if valid:
		return str(check_digit).zfill(2) #left pad check digit with 0 if length is less than 2
	else:
		return str(check_digit+6).zfill(2)[:2] #return a bad check digit (used in edit testing)
