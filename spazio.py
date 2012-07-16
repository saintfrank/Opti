def croce( val ):
	if val is 1:
		return "x"
	else:
		return "_"

tracks = (
		1, 0, 1, 1, 
		1, 0, 1, 0, 
		1, 1, 0, 0,  
		1, 1, 0, 0)


print "%s%s%s%s\n%s%s%s%s\n%s%s%s%s\n%s%s%s%s" % ( 
		croce(tracks[0]), croce(tracks[1]), croce(tracks[2]), croce(tracks[3]), croce(tracks[4]), 
		croce(tracks[5]), croce(tracks[6]), croce(tracks[7]), croce(tracks[8]), croce(tracks[9]), 
		croce(tracks[10]), croce(tracks[11]), croce(tracks[12]), croce(tracks[13]), croce(tracks[14]), croce(tracks[15]) )


##
## Ora vorrei fare un modello PL per il massimo split in due 
##

# Facciamo una matrice per ogni traccia

track_1 = (	0, 0, 0, 1, 
		0, 0, 1, 0, 
		0, 1, 0, 0,  
		0, 1, 0, 0)

track_2 = (	1, 0, 0, 0, 
		1, 0, 0, 0, 
		1, 0, 0, 0,  
		1, 0, 0, 0)

track_3 = (	0, 0, 1, 0, 
		0, 0, 1, 0, 
		0, 1, 0, 0,  
		0, 1, 0, 0)


#somma(Yi + Wi) = x      # for every i 0..16

#Fi = somma (Yj) 	# per ogni j del vettore orizzontale (layer)   - Fj indica la componente del volume nel layer j - F ha due vettori, uno per Y e uno per W

#Vj = produttoria( Fi )   # Per Y e W

# Funzione di massimo


from pymprog import *  # Import the module

# index and data
patternid, yid, wid, rid = range(16), range(16), range(16), range(2)
fid = range(4)

#problem definition
beginModel('basic')
verbose(True)

###
### ATTENZIONE !!!!! posso fare l'uguaglianza tra le variabili settando a = b come a - b = 0
###

P = var(patternid, 'P', bool) #create variables
Y = var(yid, 'Y', bool) #create variables
W = var(wid, 'W', bool) #create variables

F = var(fid, 'F', int) #create variables
     
r = st(   #set constraints
	 sum(  for j in yid) - Y[i]  <= b[i] for i in fid
	)

# Funzione di massimo 
#minimize( #set objective
#   	sum( coverage[i]*x[i] for i in xid), 'myobj'
#	)



