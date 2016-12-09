# Author: Jacob Downs
# 
# Usage: python parser.py mutants.log killMap.csv out.csv
# 
# Where mutants.log is the default name of the file that Major outputs to document information about each particular 
#			mutant (ID, Mutation operator class, Description)
#       
#		killMap.csv is the default name of the file that Major outputs to document the full kill matrix of all test suites
#       
#		out.csv is the name of the output .csv file that you choose. 
#			You may change this name, but the other two previous filenames are hard-coded into Major itself and cannot be changed


import sys, csv, pprint

def parseMutants(inMutatantsFile, info):
	with open(inMutatantsFile, 'rb') as mutantFile:
		for line in mutantFile:
			#if this line is too short to possibly be a mutant (to eliminate empty lines)
			if (len(line) > 1):
				#the descriptions are nicely separated by colons
				colons = line.split(':')
				#builds the dictionary for later
				info["mutants"][colons[0]] = {"operator" : colons[1], "Description" : ":".join(colons[2:]), "killedBy" : []}

def parseKilled(inKilleldFile, info):
	with open(inKilleldFile, 'rb') as csvfile:
		killreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		firstRow = True
		for row in killreader:
			#pull out the mutant number 
			if not firstRow:
				#row is a list of length 1 (I don't know why), so we take it's 0 index which is a string that represents the row. 
				#We split that on a comma, and then take the two components that we want to extract
				info["mutants"][row[0].split(',')[1]]["killedBy"].append(row[0].split(',')[0])
			else:
				#prevents us from parsing in the description row as numbers
				firstRow = False

def writeCsv(outFile, info):
	with open(outFile, 'wb') as csvfile:
		#declares the writer object with a comma as a delimiter (since we're using a csv output)
  		mutantWriter = csv.writer(csvfile, delimiter=',')
  		#title row
   		mutantWriter.writerow(['Mutant Number','Operator Class','Killed by','Description'])
		#iterates through all the keys in the dictionary. Used range() to numerically sort the 
		#keys (mutant ID #'s') to keep things ordered
		for num in range(len(info["mutants"])):
			mutantWriter.writerow([(num+1), info["mutants"][str(num+1)]['operator'], info["mutants"][str(num+1)]['killedBy'], info["mutants"][str(num+1)]['Description']])

def helpMessage():
	print "incorrect usage, intended usage is:"
	print "%s [mutants.log, killMap.csv, out.csv]" % sys.argv[0]

if __name__=="__main__":    
	#make sure that the arguments passed in are the right possibilities to make the program run
    if len(sys.argv) != 4:
        helpMessage()
    else:
    	info = {"mutants" : {}, "suites" : {}, }
        parseMutants(sys.argv[1], info)
        parseKilled(sys.argv[2], info)
        writeCsv(sys.argv[3], info)
	
	print ("hi")
	#this was used to view the dictionary of mutants for debugging purposes
	pprint.pprint(info)