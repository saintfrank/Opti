import pymprog

patterns = [ (6, 5), (3,6) , (7,3), (12, 3), (2, 43), (1,10), (2,8),(3,3),(12,65),(4,2) ]

cov = []
vol = []

for co,vo in patterns:
	cov.append(co)
	vol.append(vo)

print 'cov '
print cov
print 'len '
print vol

p = pymprog.model("am")
pymprog.beginModel('am')

#xi = range(len(patterns))
xi = range(4)

x = p.var( range(len (patterns) ) , 'x', bool) # x created over index set E.

print 'x ' 
print x
print 'xi ' 
print xi

g = sum(cov[i]*x[i] for i in xi)

print ' g : ' 
print g

pymprog.maximize( 
		#sum(cov[i]*x[i] for i in xi), 'prova'
	sum([cov[0]*x[0],cov[1]*x[1]]), 'prova'
)

r=st( #set constraints
	sum(vol[j]*x[j] for j in xi) <= 100
)

x = p.var( ( v  for (x,v) in patterns) , 'x', int) 
# x created over index set E.

print x
#minize the total travel distance
#p.min(sum(c[t]*x[t] for t in E), 'tiotaldist')
