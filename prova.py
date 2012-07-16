from pymprog import *  # Import the module
# index and data
xid, rid = range(3), range(3)
c = (10.0, 6.0, 4.0)
mat = [ (1.0, 1.0, 1.0),     
		        (10.0, 4.0, 5.0),   
			        (2.0, 2.0, 6.0)]   
b = (100.0, 600.0, 300.0)
#problem definition
beginModel('basic')  
verbose(True)
x = var(xid, 'X') #create variables
maximize( #set objective
  sum(c[i]*x[i] for i in xid), 'myobj'
)

print 'xid' 
print xid
print 'x' 
print x
print 'c' 
print c

r=st( #set constraints
		  sum(x[j]*mat[i][j] for j in xid) <= b[i] for i in rid
		  )
solve() #solve and report
