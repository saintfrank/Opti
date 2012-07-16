def croce( val ):
	if val is 1:
		return "x"
	else:
		return "_"

s = (0, 1, 1, 0, 1, 0 , 1, 0, 0, 1, 1, 1,  1, 1, 0, 0, 1, 0)


print "%s%s%s%s\n%s%s%s%s\n%s%s%s%s\n%s%s%s%s" % ( croce(s[0]), croce(s[1]), croce(s[2]), croce(s[3]), croce(s[4]), croce(s[5]), croce(s[6]), croce(s[7]),  croce(s[8]), croce(s[9]), croce(s[10]), croce(s[11]), croce(s[12]), croce(s[13]), croce(s[14]), croce(s[15]) )



