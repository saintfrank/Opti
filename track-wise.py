## Ora, secondo me, non direi di farlo punto punto, ma traccia traccia. 
## Allora prendo le variabili booleane Y[0], Y[1], Y[2], 
##
## Allora, per il coverage: sicurmente Y[0] + Y[1] + Y[2] + W[0] + W[1] + W[2] <= 3 al numero di coverage
##
## Metto che Y[0] + Y[1] + Y[2] > 0  
##
## E per calcolare il volume:
## faccio semplice le somme, ma poi, certo, non posso fare il prodotto, ma la somma, ma almeno mi approssima
##
##


## TODO : 
## - devo riuscire a fare il coverage, ovvero a riuscire a capire come controllare che uno dei due sub-pattern 
## - devo riuscire anche a fare il volume
##
## NOZIONI : 
## - in generale ho un vettore di variabili x. Il problema di ottimizzazione P e' del tipo
##  min { c(x) | Ax<= b }   dove A e b sono vettori di numeri reali
##

def print_matrix( tracks ):
	print "%s%s%s%s\n%s%s%s%s\n%s%s%s%s\n%s%s%s%s" % ( 
		croce(tracks[0]),  croce(tracks[1]),  croce(tracks[2]),  croce(tracks[3]), 
		croce(tracks[4]),  croce(tracks[5]),  croce(tracks[6]),  croce(tracks[7]), 
		croce(tracks[8]),  croce(tracks[9]),  croce(tracks[10]), croce(tracks[11]), 
		croce(tracks[12]), croce(tracks[13]), croce(tracks[14]), croce(tracks[15]) )

def print_variables( tracks ):
    print"%s%s%s%s\n%s%s%s%s\n%s%s%s%s\n%s%s%s%s" % ( 
        croce(tracks[0].primal),  croce(tracks[1].primal),  croce(tracks[2].primal),  croce(tracks[3].primal), 
        croce(tracks[4].primal),  croce(tracks[5].primal),  croce(tracks[6].primal),  croce(tracks[7].primal), 
        croce(tracks[8].primal),  croce(tracks[9].primal),  croce(tracks[10].primal), croce(tracks[11].primal), 
        croce(tracks[12].primal), croce(tracks[13].primal), croce(tracks[14].primal), croce(tracks[15].primal) )


def croce( val ):
    if val >= 1  :
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

# Stiamo facendo uno split, il pattern precedente e' P, e noi vogliamo creare due pattern figli Y e W
# P, Y, e W sono delle matrici NxM, rappresentate come vettori, di bit. 
# N sono i layer, mentre M sono le hit in quel layer 
P = var(patternid, 'P', bool)       # Parent Pattern
Y = var(range(3), 'Y', bool)        # First sub-pattern
W = var(range(3), 'W', bool)        # Second sub-pattenr


# Queste tre relazioni logiche impongono che per ogni traccia k, questa venga riconosciuta da almeno un sub-pattern 
# e traducono la relazione 
#   covered[k] = coveredY[k] V coveredW[k]      |  k = {1,2,3} 
# con
#   covered[k] = 1                              |  k = {1,2,3} 
covered = var(range(3), 'covSubTot', bool)

r=st( covered[k] >= Y[k]  for k in range(3) )
r+=st( covered[k] >= W[k]  for k in range(3) )
r+=st( covered[k] <= Y[k] + W[k]  for k in range(3) )
r+=st( covered[k] == 1  for k in range(3) )
#
# # # # # # #


r=st( sum ( Y[k] for k in range(3) ) >= 1    )
r=st( sum ( W[k] for k in range(3) ) >= 1   )



AY = var(range(N*M), 'AY', int) 
AW = var(range(N*M), 'AW', int)

## Ora voglio fare che *per ogni punto* nella griglia 2D,                                       
r = st	(  AY[ i ] >= Y[k] * myTracks[k][ i ] for i in range(N*M)  for k in range(3) )
r = st	(  AY[ i ] <= sum( Y[k] * myTracks[k][ i ]  for k in range(3)  )  for i in range(N*M)  )

r = st	(  AW[ i ] >= W[k] * myTracks[k][ i ] for i in range(N*M)  for k in range(3) )
r = st	(  AW[ i ] <= sum( W[k] * myTracks[k][ i ]  for k in range(3)  )  for i in range(N*M)  )

# Le ampiezze nei vari layer ... poi si potra' semplificare
AmpY = var(range(N), 'AmpY', int)
AmpW = var(range(N), 'AmpW', int)


r += st	(   sum(  AY[i*N+j] for j in mRange ) == AmpY[i] for i in nRange )
r += st	(   sum(  AW[i*N+j] for j in mRange ) == AmpW[i] for i in nRange )





## AY e AW sono variabili temporanee. 
## Ognuno di queste ha N valori corrisponde all' ampiezza (apporto sul volume) per quel layer, di quel pattern.  
## TODO riscrivere meglio
#AY = var(fid, 'AY', int) 
#AW = var(fid, 'AW', int)
#
#print 'Print AW : ' 
#print AW
#
#
#
## AY    
#r = st	( sum( [(i*N)+j] * Y[0]  for j in miRange ) == AY[i]  for i in nRange )
#
## AW
#r += st	( sum( W[(i*N)+j] for j in mRange ) == AW[i]  for i in nRange )
#
#
#
## Vogliamo controllare che Y e W abbiano lo stesso coverage di P, quindi che 
## Per ogni traccia che cade nel pattern ci sia un sub-pattern che la becchi tutta, quindi che abbia tutti i suoi punti
##
## CovY[k] sara' 1 se il sub-pattern Y riconosce la traccia k. Sara' 0 altrimenti 
#
#coveredY = var(range(3), 'covY', bool) 
#
#r+=st( sum( myTracks[k][i*N+j] * ( myTracks[k][i*N+j] - Y[i*N+j])  for i in nRange for j in mRange ) == coveredY[k]  for k in range(3) )
#
#
## CovW[k] sara' 1 se il sub-pattern W riconosce la traccia k. Sara' 0 altrimenti 
#
#coveredW = var(range(3), 'covW', bool)
#
#r+=st(  sum( myTracks[k][i*N+j] * ( myTracks[k][i*N+j] - W[i*N+j]) for i in nRange for j in mRange ) == coveredW[k]  for k in range(3) )
#
## TODO qui ora dovrei moltiplicarle per vedere se Una delle due e' zero !!!
#
#
##
## # # # # # # 


#
#Vol = var(range(2), 'Vol', int)     # Volume
#
#
## Qui' calcolo il volume @TODO qui' devo farlo diventare MOLTIPLICAZIONE
## Questo qui' sotto funzionerebbe, ovvero, e' la produttoria, ma non si puo fare:  reduce( operator.mul, list( AY[i] for i in range(N)) )
#r += st	(   sum(  AY[i] for i in nRange ) - Vol[i]   == 0 for i in range(2) )
#
#
#
## Funzione obiettivo, di minimizzazione quindi
#minimize( (3 *Y[0]) + (20* Y[1]) + (2* Y[2]) + (10* W[0]) + (1* W[1]) + (7* W[2])   , 'Total Volume')

VolTotY = var(range(1), 'VolTotY', int)        # Second sub-pattenr
VolTotW = var(range(1), 'VolTotW', int)        # Second sub-pattenr


#r += st	(   sum(  AY[i*N+j] for j in mRange ) == AmpY[i] for i in nRange )
r += st	(   sum(  AmpY[j] for j in nRange ) == VolTotY[i] for i in range(1) )
r += st	(   sum(  AmpW[j] for j in nRange ) == VolTotW[i] for i in range(1) )


minimize( VolTotY[0] + VolTotW[0]  , 'Total Volume')


sys.stdout.write("\nSolving ...")
solve()
sys.stdout.write(" done.\n\n")


print("Total Volume = %g"%vobj())

print Y 
print W

print AmpY
print AmpW

print AY
print AW

print_variables(AY)
print_variables(AW)






