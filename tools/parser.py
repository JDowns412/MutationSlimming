# Author: Jacob Downs, Spencer Gagnon
# 
# Usage: python parser.py mutants.log killMap.csv testMap.csv out.csv
# 
# Where mutants.log is the default name of the file that Major outputs to document information about each particular 
#			mutant (ID, Mutation operator class, Description)
#       
#		killMap.csv is the default name of the file that Major outputs to document the full kill matrix of all test suites
#       
#		testMap.csv is the name of the default file name that Major gives it's mapping of test suite numbers to their 
#			actual .java file names
#
#		out.csv is the name of the output .csv file that you choose. 
#			You may change this name, but the other two previous filenames are hard-coded into Major itself and cannot be changed


import sys, csv, pprint, json

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

def parseSuites(inSuiteFile, info):
	with open(inSuiteFile, 'rb') as csvfile:
		suitereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		firstRow = True
		for row in suitereader:
			#pull out the mutant number 
			if not firstRow:
				#row is a list of length 1 (I don't know why), so we take it's 0 index which is a string that represents the row. 
				#We split that on a comma, and then take the two components that we want to extract
				#initializes the dictionary that will hold information on the test suites
				info["suites"][row[0].split(',')[0]] = {"mutantsKilled" : [], "operatorStats" : {}}
				info["suites"][row[0].split(',')[0]]["name"] = row[0].split(',')[1]
			else:
				#prevents us from parsing in the description row as numbers
				firstRow = False

def aggregateOperators(info):
	totalMutants = 0.0
	for row in info["mutants"]:
		totalMutants += 1
		operator = info["mutants"][row]["operator"]
		killedBy = info["mutants"][row]["killedBy"]
		if operator not in info["operators"]:
			info["operators"][operator] = {"count" : 1.0, "numKilled": 0, "mutants" : [row]}
		else:
			info["operators"][operator]["count"] += 1
			info["operators"][operator]["mutants"].append(row)

		# A mutant was killed if at least one test suite killed it
		if len(killedBy) > 0:
			info["operators"][operator]["numKilled"] += 1

	
	#calculate what percentage of the total number of mutants each operator takes up
	for op in info["operators"]:
		info["operators"][op]["percentageOfTotal"] = info["operators"][op]["count"]/totalMutants
		info["operators"][op]["percentageKilled"] = info["operators"][op]["numKilled"]/info["operators"][op]["count"]

def aggregateSuites(info):
	for row in info["mutants"]:
		operator = info["mutants"][row]["operator"]
		killedBy = info["mutants"][row]["killedBy"]

		for suite in killedBy:
			info["suites"][suite]["mutantsKilled"].append(row)
			if operator not in info["suites"][suite]["operatorStats"]:
				info["suites"][suite]["operatorStats"][operator] = {"count" : 0}
			
			info["suites"][suite]["operatorStats"][operator]["count"] += 1

	for suite in info["suites"]:
		for operator in info["suites"][suite]["operatorStats"]:
			suiteCount = info["suites"][suite]["operatorStats"][operator]["count"]
			totalCount = info["operators"][operator]["count"]
			info["suites"][suite]["operatorStats"][operator]["percentOfAll"] = suiteCount/totalCount


def writeOut(outFile, info):
	with open(outFile, 'wb') as csvfile:
		#declares the writer object with a comma as a delimiter (since we're using a csv output)
  		mutantWriter = csv.writer(csvfile, delimiter=',')
  		#title row
   		mutantWriter.writerow(['Mutant Number','Operator Class','Killed by','Description'])
		#iterates through all the keys in the dictionary. Used range() to numerically sort the 
		#keys (mutant ID #'s') to keep things ordered
		for num in range(len(info["mutants"])):
			mutantWriter.writerow([(num+1), info["mutants"][str(num+1)]['operator'], info["mutants"][str(num+1)]['killedBy'], info["mutants"][str(num+1)]['Description']])

	with open('results.json', 'w') as outfile:
		json.dump(info, outfile)

def helpMessage():
	print "incorrect usage, intended usage is:"
	print "[%s mutants.log killMap.csv testMap.csv out.csv]" % sys.argv[0]

if __name__=="__main__":    
	#make sure that the arguments passed in are the right possibilities to make the program run
    if len(sys.argv) != 5:
        helpMessage()
    else:
    	info = {"mutants" : {}, "suites" : {}, "operators" : {}}
        parseMutants(sys.argv[1], info)
        parseKilled(sys.argv[2], info)
        parseSuites(sys.argv[3], info)
        aggregateOperators(info)
        aggregateSuites(info)
        
		#writeOut needs to be the last method called since it also writes our results JSON file out.
        writeOut(sys.argv[4], info)
	
	#this was used to view the dictionary of mutants for debugging purposes
	pprint.pprint(info)