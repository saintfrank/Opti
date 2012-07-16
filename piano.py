from pymprog import *  # Import the module

# index and data
xid, rid = range(10), range(1)

c = (6, 6, 4, 12, 7, 3, 5, 2, 2, 5) 

mat = [ (5, 3, 9, 2, 6, 4, 1, 1, 8, 6)  ]   

b = (100.0, 600.0, 300.0)

#problem definition
beginModel('basic')
verbose(True)
x = var(xid, 'X') #create variables

# Funzione di massimo 
maximize( #set objective
  sum(c[i]*x[i] for i in xid), 'myobj'
)

#print 'xid' 
#print xid
#print 'x' 
#print x
#print 'c' 
#print c

r=st(	#set constraints
	sum(x[j]*mat[i][j] for j in xid) <= b[i] for i in rid
  )

solve() #solve and report


print "Solver status:", status()
print 'Z = %g;' % vobj()  # print obj value
#Print variable names and primal values
print ';\n'.join('%s = %g {dual: %g}' % (
	   x[i].name, x[i].primal, x[i].dual) 
	                       for i in xid)
print ';\n'.join('%s = %g {dual: %g}' % (
	   r[i].name, r[i].primal, r[i].dual) 
	                       for i in rid)

