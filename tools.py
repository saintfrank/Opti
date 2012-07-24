import pymprog      # Import the module

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


