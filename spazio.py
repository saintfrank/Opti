def print_matrix( tracks ):
	print "%s%s%s%s\n%s%s%s%s\n%s%s%s%s\n%s%s%s%s" % ( 
		croce(tracks[0]), croce(tracks[1]), croce(tracks[2]), croce(tracks[3]), 
		croce(tracks[4]), croce(tracks[5]), croce(tracks[6]), croce(tracks[7]), 
		croce(tracks[8]), croce(tracks[9]), croce(tracks[10]), croce(tracks[11]), 
		croce(tracks[12]), croce(tracks[13]), croce(tracks[14]), croce(tracks[15]) )




def croce( val ):
	if val is 1:
		return "x"
	else:
		return "_"

tracks = (
		1, 0, 1, 1, 
		1, 0, 1, 1, 
		1, 1, 0, 0,  
		1, 1, 0, 0)

print 'Pattern Originale:'
print_matrix(tracks)

##
## Ora vorrei fare un modello PL per il massimo split in due 
##

# Facciamo una matrice per ogni traccia

track_1 = (	0, 0, 0, 1, 
		0, 0, 1, 0, 
		0, 1, 0, 0,  
		0, 1, 0, 0)
print 'Track_1:'
print_matrix(track_1)

track_2 = (	1, 0, 0, 0, 
		1, 0, 0, 0, 
		1, 0, 0, 0,  
		1, 0, 0, 0)

print 'Track_2:'
print_matrix(track_2)

track_3 = (	0, 0, 1, 0, 
		0, 0, 1, 0, 
		0, 1, 0, 0,  
		0, 1, 0, 0)

myTracks = [track_1, track_2, track_3 ]

print 'Track_3:'
print_matrix(track_3)

# Funzione di massimo


from pymprog import *  # Import the module

import operator
import sys

N = 4
M = 4

# index and data
patternid, yid, wid, rid = range(N*M), range(N*M), range(N*M), range(2)
fid = range(N) # WARNING occhio che questo lo usero' per due variabili, non dovrebbe essere un problema 
nRange = range(N)
mRange = range(M) 

#problem definition
beginModel('basic')
verbose(True)

###
### ATTENZIONE !!!!! posso fare l'uguaglianza tra le variabili settando a = b come a - b = 0
###



# Stiamo facendo uno split, il pattern precedente e' P, e noi vogliamo creare due pattern figli Y e W
# P, Y, e W sono delle matrici NxM, rappresentate come vettori, di bit. 
# N sono i layer, mentre M sono le hit in quel layer 
P = var(patternid, 'P', bool) 	# Parent Pattern
Y = var(yid, 'Y', bool) 	# First sub-pattern
W = var(wid, 'W', bool) 	# Second sub-pattenr
Vol = var(range(2), 'Vol', int) 	# Second sub-pattenr

# AY e AW sono variabili temporanee. 
# Ognuno di queste ha N valori corrisponde all' ampiezza (apporto sul volume) per quel layer, di quel pattern.  
# TODO riscrivere meglio
AY = var(fid, 'AY', int) 
AW = var(fid, 'AW', int)

print 'Print AW:'
print AW
    
# AY    
r = st	( sum( Y[(i*N)+j] for j in mRange ) - AY[i]   == 0 for i in nRange )

# AW
r += st	( sum( W[(i*N)+j] for j in mRange ) - AW[i]   == 0 for i in nRange )



# Vogliamo controllare che Y e W abbiano lo stesso coverage di P, quindi che 

# Per ogni traccia che cade nel pattern ci sia un sub-pattern che la becchi tutta, quindi che abbia tutti i suoi punti

covY = var(range(3), 'covY', bool) 
covW = var(range(3), 'covW', bool)


# La somma del prodotto dei punti dovra
r += st	( sum( Y[i*N+j]*myTracks[k][i*N+j] for i in nRange for j in mRange ) + covY[k] *4 == 4  for k in range(3)	)


# Qui' calcolo il volume
# TODO qui' devo farlo diventare MOLTIPLICAZIONE
r += st	(   #set constraints
	sum(  AY[i] for i in nRange ) - Vol[i]   == 0 for i in range(2)
	# Questo qui' sotto funzionerebbe, ovvero, il reduce funziona bene, ma non e' supporato dal lambda generale
	# reduce( operator.mul, list( AY[i] for i in range(N)) ) - Vol[i]   == 0 for i in range(2)
	)

# Funzione obiettivo, di minimizzazione quindi
minimize(Vol[0] + Vol[1] , 'Total Volume')


sys.stdout.write("\nSolving ...")
solve()
sys.stdout.write(" done.\n\n")


print("Total Volume = %g"%vobj())





