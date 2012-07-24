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

def print_values_matrix( tracks ):
	print "%s%s%s%s\n%s%s%s%s\n%s%s%s%s\n%s%s%s%s" % ( 
		croce(tracks[0]),  croce(tracks[1]),  croce(tracks[2]),  croce(tracks[3]), 
		croce(tracks[4]),  croce(tracks[5]),  croce(tracks[6]),  croce(tracks[7]), 
		croce(tracks[8]),  croce(tracks[9]),  croce(tracks[10]), croce(tracks[11]), 
		croce(tracks[12]), croce(tracks[13]), croce(tracks[14]), croce(tracks[15]) )

def print_variables_matrix_cross( tracks ):
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


def print_variables_matrix_primal( tracks ):
    print"%s %s %s %s\n%s %s %s %s\n%s %s %s %s\n%s %s %s %s" % ( 
         (tracks[0].primal),  (tracks[1].primal),  (tracks[2].primal),  (tracks[3].primal), 
         (tracks[4].primal),  (tracks[5].primal),  (tracks[6].primal),  (tracks[7].primal), 
         (tracks[8].primal),  (tracks[9].primal),  (tracks[10].primal), (tracks[11].primal), 
         (tracks[12].primal), (tracks[13].primal), (tracks[14].primal), (tracks[15].primal) )




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
    
    
    #r += pymprog.st( sum ( Y[k] for k in range(3) ) >= 1 )
    #r += pymprog.st( sum ( W[k] for k in range(3) ) >= 1 )
    
    
    
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
    
    print Y 
    print W
    
    print AmpY
    print AmpW
    
    print_variables_matrix_primal(AY)
    print_variables_matrix_primal(AW)
    
    print_variables_matrix_cross(AY)
    print_variables_matrix_cross(AW)




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

track_3 = (	0, 0, 1, 0, 
		0, 0, 1, 0, 
		0, 1, 0, 0,  
		0, 1, 0, 0)

myTracks = [track_1, track_2, track_3 ]

print 'Track_3:'
print_values_matrix(track_3)

split(myTracks)

# Funzione di massimo


