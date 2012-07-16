from pymprog import *  # Import the module

# index and data
xid, rid = range(10), range(2)

# Funzione obiettivo
coverage = (6, 6, 4, 12, 7, 3, 5, 2, 2, 5) 

## Mi faccio una matrice che mi fa selezionare
mat = 	[
		(5, 3, 9, 2, 6, 4, 1, 1, 8, 6), # Modellazione della somma dei volumi
		(0, 0, 0, 0, 1, 0, 1, 0, 0, 0), # Ogni riga mi rappresenta un costraint di mutua esclusione(padre/figlio) 
		(0, 1, 0, 0, 0, 0, 1, 0, 0, 0), # ...
		(0, 0, 0, 1, 0, 0, 1, 0, 0, 0),
		(1, 0, 0, 0, 0, 0, 1, 0, 0, 0)
	]   

b = (30.0, 1)

#problem definition
beginModel('basic')
verbose(True)
x = var(xid, 'X', bool) #create variables

# Funzione di massimo 
maximize( #set objective
  sum(coverage[i]*x[i] for i in xid), 'myobj'
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

# Stampa del risultato
print "Solver status:", status()
print 'Z = %g;' % vobj()  # print obj value
#Print variable names and primal values
print ';\n'.join('%s = %g {dual: %g}' % (
	   x[i].name, x[i].primal, 10) 
	                       for i in xid)
print ';\n'.join('%s = %g {dual: %g}' % (
	   r[i].name, r[i].primal, 10) 
	                       for i in rid)

