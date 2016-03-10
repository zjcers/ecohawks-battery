#!/usr/bin/python
#Original Author: Zane J Cersovsky
#Original Date: Mar 6 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 7 2016
def reverse_word(word):
	r"""
	Takes in a int and reverse its bytes
	"""
	assert type(word) == int
	assert word >= 0 and word < 65536
	msb = word >> 8
	lsb = word & 255
	return (lsb << 8) | msb
def twocomplement(word):
	r"""
	Switches between 2's complement binary and python signed integers
	"""
	assert type(word) == int
	assert word >= 0 and word < 65536
	if (isNegative2c(word)):
		return ~word+1
	else:
		return word
def isNegative2c(word):
	r"""
	Returns a bool of the leading bit
	"""
	assert type(word) == int
	assert word >= 0 and word < 65536
	return bool(word >> 15)
