from tools import *
import pymprog      # Import the module

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



def split ( myTracks ):
    
    
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
    pymprog.beginModel('basic')
    pymprog.verbose(True)
    
    # Stiamo facendo uno split, il pattern precedente e' P, e noi vogliamo creare due pattern figli Y e W
    # P, Y, e W sono delle matrici NxM, rappresentate come vettori, di bit. 
    # N sono i layer, mentre M sono le hit in quel layer 
    P = pymprog.var(patternid, 'P', bool)       # Parent Pattern
    Y = pymprog.var(range(3), 'Y', bool)        # First sub-pattern
    W = pymprog.var(range(3), 'W', bool)        # Second sub-pattenr
    
    
    # Queste tre relazioni logiche impongono che per ogni traccia k, questa venga riconosciuta da almeno un sub-pattern 
    # e traducono la relazione 
    #   covered[k] = coveredY[k] V coveredW[k]      |  k = {1,2,3} 
    # con
    #   covered[k] = 1                              |  k = {1,2,3} 
    covered = pymprog.var(range(3), 'covSubTot', bool)
    
    r  = pymprog.st( covered[k] >= Y[k]  for k in range(3) )
    r += pymprog.st( covered[k] >= W[k]  for k in range(3) )
    r += pymprog.st( covered[k] <= Y[k] + W[k]  for k in range(3) )
    r += pymprog.st( covered[k] == 1  for k in range(3) )
    #
    # # # # # # #
    
    totY = pymprog.var( range(1), 'totY', bounds=(1, 3) )
    totW = pymprog.var( range(1), 'totW', bounds=(1, 3) )
    
    r += pymprog.st( sum ( Y[k] for k in range(3) ) == totY[i] for i in range(1) )
    r += pymprog.st( sum ( W[k] for k in range(3) ) == totW[i] for i in range(1) )
    
    
    
    AY = pymprog.var(range(N*M), 'AY', int) 
    AW = pymprog.var(range(N*M), 'AW', int)
    
    ## Ora voglio fare che *per ogni punto* nella griglia 2D,                                       
    r += pymprog.st	(  AY[ i ] >= Y[k] * myTracks[k][ i ] for i in range(N*M)  for k in range(3) )
    r += pymprog.st	(  AY[ i ] <= sum( Y[k] * myTracks[k][ i ]  for k in range(3)  )  for i in range(N*M)  )
    
    r += pymprog.st	(  AW[ i ] >= W[k] * myTracks[k][ i ] for i in range(N*M)  for k in range(3) )
    r += pymprog.st	(  AW[ i ] <= sum( W[k] * myTracks[k][ i ]  for k in range(3)  )  for i in range(N*M)  )
    
    # Le ampiezze nei vari layer ... poi si potra' semplificare
    AmpY = pymprog.var(range(N), 'AmpY', int)
    AmpW = pymprog.var(range(N), 'AmpW', int)
    
    
    r += pymprog.st	(   sum(  AY[i*N+j] for j in mRange ) == AmpY[i] for i in nRange )
    r += pymprog.st	(   sum(  AW[i*N+j] for j in mRange ) == AmpW[i] for i in nRange )
    
    
    VolTotY = pymprog.var(range(1), 'VolTotY', int)        # Second sub-pattenr
    VolTotW = pymprog.var(range(1), 'VolTotW', int)        # Second sub-pattenr
    
    
    #r += st	(   sum(  AY[i*N+j] for j in mRange ) == AmpY[i] for i in nRange )
    r += pymprog.st	(   sum(  AmpY[j] for j in nRange ) == VolTotY[i] for i in range(1) )
    r += pymprog.st	(   sum(  AmpW[j] for j in nRange ) == VolTotW[i] for i in range(1) )
    
    
    pymprog.minimize( VolTotY[0] + VolTotW[0]  , 'Total Volume')
    
    
    sys.stdout.write("\nSolving ...")
    pymprog.solve()
    sys.stdout.write(" done.\n\n")
    
    
    print("Total Volume = %g"% pymprog.vobj())
   
    print 'Y'
    print Y 
    print 'W'
    print W
    
    print AmpY
    print AmpW
    
    print 'AY'
    print_variables_matrix_primal(AY)
    print 'AW'
    print_variables_matrix_primal(AW)
 
    print 'Y'
    print_variables_matrix_cross(AY)
    print 'W'
    print_variables_matrix_cross(AW)

    print 'Volume Y : ' 
    print VolTotY[0].primal
    print 'Volume W : ' 
    print VolTotW[0].primal
    print 'Volume Tot : ' 
    print sum( tracks[i] for i in range(N*M) )



# test code


tracks = (
		1, 0, 1, 1, 
		1, 0, 1, 1, 
		1, 1, 0, 0,  
		1, 1, 0, 0)

print 'Pattern Originale:'
print_values_matrix(tracks)

##
## Ora vorrei fare un modello PL per il massimo split in due 
##

# Facciamo una matrice per ogni traccia

track_1 = (	0, 0, 0, 1, 
		0, 0, 1, 0, 
		0, 1, 0, 0,  
		0, 1, 0, 0)
print 'Track_1:'
print_values_matrix(track_1)

track_2 = (	1, 0, 0, 0, 
		1, 0, 0, 0, 
		1, 0, 0, 0,  
		1, 0, 0, 0)

print 'Track_2:'
print_values_matrix(track_2)

track_3 = (	0, 0, 0, 1, 
		0, 0, 0, 1, 
		0, 0, 0, 1,  
		0, 0, 0, 1)


print 'Track_3:'
print_values_matrix(track_3)



myTracks = [track_1, track_2, track_3 ]
split(myTracks)

# Funzione di massimo


