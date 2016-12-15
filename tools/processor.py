# Author: Jacob Downs, Spencer Gagnon, Bridget Guiney, Raymond tang
# 
# Usage: python processor.py mutants.log killMap.csv testMap.csv out.csv
# 
# Where mutants.log is the default name of the file that Major outputs to document information about each particular 
#			mutant (ID, Mutation operator class, Description)
#       
#		killMap.csv is the default name of the file that Major outputs to document the full kill matrix of all test suites
#       
#		testMap.csv is the name of the default file name that Major gives it's mapping of test suite numbers to their 
#			actual .java file names. Or, if you change the "test sort option" in Major to "sort_method", it is the mapping actual test methods themselves
#
#		out.csv is the name of the output .csv file that you choose. 
#			You may change this name, but the other two previous filenames are hard-coded into Major itself and cannot be changed


import sys, csv, pprint, json

#this method parses in the .log file that contains all of the information on the mutants that Major generated
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
				info["suites"][row[0].split(',')[0]] = {"mutantsKilled" : [], "operatorStats" : {}, "mutantsRelevant" : []}
				info["suites"][row[0].split(',')[0]]["name"] = row[0].split(',')[1]
			else:
				#prevents us from parsing in the description row as numbers
				firstRow = False

def parseCoverage(inCoverageFile, info):
	with open(inCoverageFile, 'rb') as csvfile:
		coveragereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		firstRow = True
		for row in coveragereader:
			#pull out the mutant number 
			if not firstRow:
				#row is a list of length 1 (I don't know why), so we take it's 0 index which is a string that represents the row. 
				#We split that on a comma, and then take the two components that we want to extract 
				#and add them to their spots in the dictionary
				info["suites"][row[0].split(',')[0]]["mutantsRelevant"].append(row[0].split(',')[1])
			else:
				#prevents us from parsing in the description row as numbers
				firstRow = False

#this method aggregates the desired information on all of the mutation operators that Major uses 
def aggregateOperators(info):
	totalMutants = 0.0
	for row in info["mutants"]:
		totalMutants += 1
		operator = info["mutants"][row]["operator"]
		killedBy = info["mutants"][row]["killedBy"]

		#initialize the operator in the dictionary if it hasn't been done yet
		if operator not in info["operators"]:
			info["operators"][operator] = {"count" : 1.0, "numKilled": 0, "mutants" : [row], "killedMutants" : [], "subs" : {"AOR" : {"alsoKilled" : [], "ratio" :  0.0}, "LOR" : {"alsoKilled" : [], "ratio" :  0.0}, "COR" : {"alsoKilled" : [], "ratio" :  0.0}, "ROR" : {"alsoKilled" : [], "ratio" :  0.0}, "SOR" : {"alsoKilled" : [], "ratio" :  0.0}, "ORU" : {"alsoKilled" : [], "ratio" :  0.0}, "STD" : {"alsoKilled" : [], "ratio" :  0.0}, "LVR" : {"alsoKilled" : [], "ratio" :  0.0}}}
		else:
			#add the data to the already initialized operator in the dictionary
			info["operators"][operator]["count"] += 1
			info["operators"][operator]["mutants"].append(row)

		# A mutant was killed if at least one test suite killed it
		if len(killedBy) > 0:
			info["operators"][operator]["numKilled"] += 1

	#calculate what percentage of the total number of mutants each operator takes up
	for op in info["operators"]:
		info["operators"][op]["percentageOfTotal"] = info["operators"][op]["count"]/totalMutants
		info["operators"][op]["percentageKilled"] = info["operators"][op]["numKilled"]/info["operators"][op]["count"]

#this method aggregates all of the desired data on the test methods that we wish to collect
#Note the "suites" here are whatever level of test sorting that Major was set to during execution
#it can be as broad as the entire test files themselves, and as specific as the isolated test methods
#within the files if desired. This script will aggregate on both
def aggregateSuites(info):
	for s in info["suites"]:
		for op in info["operators"]:
			#initializes the particular test suite/method
			info["suites"][s]["operatorStats"][op] = {"killCount" : 0, "relevantCount" : 0.0, "percentRelevantKilled" : 0.0, "killedMutantList" : []}

	for row in info["mutants"]:
		operator = info["mutants"][row]["operator"]
		killedBy = info["mutants"][row]["killedBy"]

		#aggregate data on the mutants that the test suite/method successfully killed
		for suite in killedBy:
			info["suites"][suite]["mutantsKilled"].append(row)
			info["suites"][suite]["operatorStats"][operator]["killCount"] += 1

	#calculate what each fraction these specific mutants were for each operator
	for suite in info["suites"]:
		for operator in info["suites"][suite]["operatorStats"]:
			suiteCount = info["suites"][suite]["operatorStats"][operator]["killCount"]
			totalCount = info["operators"][operator]["count"]
			info["suites"][suite]["operatorStats"][operator]["percentOfAll"] = suiteCount/totalCount

#This method aggregates our first attempt at a conclusive data point.
#At the time, our group was still restricted to the broad test-file granularity of test sorting in Major
#After development of this method, our Professor taught us how to achieve a finer granularity of test sorting
#thus deeming this stat to be obsolete. However, it is left here just in case it is useful later.
#The idea behind this stat was to try and determine (as close as we possibly could) how much one operator
#subsumed another one at the test-file level. To do this, the average of the killed/relevant mutants for each operator
#in each file were computed and stored in the info dictionary
def calculateRelevantMutantsKilled(info):
	for row in info["suites"]:
		for mutant in info["suites"][row]["mutantsRelevant"]:
			mutantCategory = info["mutants"][mutant]["operator"]
			info["suites"][row]["operatorStats"][mutantCategory]["relevantCount"] += 1
			if mutant in info["suites"][row]["mutantsKilled"]:
				info["suites"][row]["operatorStats"][mutantCategory]["killedMutantList"].append(mutant)
				if mutant not in info["operators"][mutantCategory]["killedMutants"]:
					info["operators"][mutantCategory]["killedMutants"].append(mutant)

		for op in info["suites"][row]["operatorStats"]:
			killCount = info["suites"][row]["operatorStats"][op]["killCount"]
			relevantCount = info["suites"][row]["operatorStats"][op]["relevantCount"]

			if info["suites"][row]["operatorStats"][op]["relevantCount"] > 0:
				info["suites"][row]["operatorStats"][op]["percentRelevantKilled"] = killCount/relevantCount

#this method's runtime complexity may be a nightmare, but it gets the job done. 
# to calculate the ratio that one operate subsumes another, this method compares every operator against 
# every other operator since the subsumptions aren't reversible (op1 subsumes 2 != op2 subsumes 1). 
# This method goes through every suite that mutants from op1 were killed in, and it finds mutants from op2
# that were also killed in the same test case. Since both are killed at the same time, the op1 mutant that was killed
# therefore subsumes the op2 mutant (in this test case). This method checks for all possible occurrences of this 
# scenario and totals them up, making sure not to count duplicates. After everything is tallied and aggregated into the
# the respective spots within the "info" dictionary, the number of subsumed op2 mutants are divided by the total
# number of op2 mutants to be killed in general (this includes mutants in op2 that weren't subsumed by an op1 mutant)
# This is where we derive our ratios from, and these ratios are what we will use to draw conclusions on the data
def calcSubsumptionPercentages(info):
	#iterate through all possible combinations of mutation operator groups
	for op1 in info["operators"]:
		for op2 in info["operators"]:
			#this will be used to keep track of how many mutants within op2 are subsumed by "killed" 
			#in the next loop
			killedCount = 0

			#avoid unnecessary computing
			if op1 != op2:	
				#iterate through the op1 mutants that were killed anywhere in the test suite
				for killed in info["operators"][op1]["killedMutants"]:
					#iterate through all of the test methods
					for suite in info["suites"]:
						# only do the following computations if that test actually killed this particular mutant
						if killed in info["suites"][suite]["mutantsKilled"]:
							#iterate through all the other mutants that were killed in this test.
							#this list is essentially all of the mutants that are subsumed by the mutant from op1
							for alsoKilled in info["suites"][suite]["mutantsKilled"]:
								#don't add a duplicate to the list of mutants from op2 that were previously determined to be subsumed
								if alsoKilled in info["operators"][op2]["mutants"] and alsoKilled not in info["operators"][op1]["subs"][op2]["alsoKilled"]:
									info["operators"][op1]["subs"][op2]["alsoKilled"].append(alsoKilled)
									#increment the counter of non-repeated subsumed op2 mutants
									killedCount += 1

				print("Finished {0} sub -> {1}".format(op1, op2))

				#calculate and set the subsumption percentage for this combo of ops (op1 subsumes op2 by this ratio)
				info["operators"][op1]["subs"][op2]["ratio"] = float(killedCount) / info["operators"][op2]["numKilled"]

#this method writes out all of the desired output files
def writeOut(outFile, outRatios, info):
	with open(outFile, 'wb') as csvfile:
		#declares the writer object with a comma as a delimiter (since we're using a csv output)
  		mutantWriter = csv.writer(csvfile, delimiter=',')
  		#title row
   		mutantWriter.writerow(['Mutant Number','Operator Class','Killed by','Description'])
		#iterates through all the keys in the dictionary. Used range() to numerically sort the 
		#keys (mutant ID #'s') to keep things ordered
		for num in range(len(info["mutants"])):
			mutantWriter.writerow([(num+1), info["mutants"][str(num+1)]['operator'], info["mutants"][str(num+1)]['killedBy'], info["mutants"][str(num+1)]['Description']])

	with open("subsumptions.csv", 'wb') as csvfile:
		#declares the writer object with a comma as a delimiter (since we're using a csv output)
  		subWriter = csv.writer(csvfile, delimiter=',')
  		#title row
   		subWriter.writerow(['Operator Pair','Subsumption ratio'])

   		for op1 in info["operators"]:
   			for op2 in info["operators"][op1]["subs"]:
   				if info["operators"][op1]["subs"][op2]["ratio"] > 0.5:
   					subWriter.writerow([("{0} v. {1}".format(op1, op2)), info["operators"][op1]["subs"][op2]["ratio"]])

	#Write out the csv file that will be used for graphing our preliminary results 
	#(The multi-line graph that Spencer and I were talking about)
	with open(outRatios, 'wb') as ratioFile:
		#declares the writer object with a comma as a delimiter (since we're using a csv output)
  		ratioWriter = csv.writer(ratioFile, delimiter=',')
  		#title row
   		ratioWriter.writerow(['Suite', 'AOR','LOR','COR','ROR', 'SOR', 'ORU', 'STD', 'LVR'])
		#iterates through all the keys in the dictionary. Used range() to numerically sort the 
		#keys (mutant ID #'s') to keep things ordered
		aor = ""
		lor = ""
		cor = ""
		ror = ""
		sor = ""
		oru = ""
		std = ""
		lvr = ""

		#this loop is quite redundant and non-elegant, 
		#but at the time it was the only way that I could think to accomplish the desired task
		#the percentages need to be initialized to 0 in order to prevent a 
		#"key does not exist" error later in the program
		for suit in info["suites"]:
			if "AOR" in info["suites"][suit]["operatorStats"]:
				aor = info["suites"][suit]["operatorStats"]["AOR"]["percentRelevantKilled"]
			else:
				aor = 0

			if "LOR" in info["suites"][suit]["operatorStats"]:
				lor = info["suites"][suit]["operatorStats"]["LOR"]["percentRelevantKilled"]
			else:
				lor = 0

			if "COR" in info["suites"][suit]["operatorStats"]:
				cor = info["suites"][suit]["operatorStats"]["COR"]["percentRelevantKilled"]
			else:
				cor = 0

			if "ROR" in info["suites"][suit]["operatorStats"]:
				ror = info["suites"][suit]["operatorStats"]["ROR"]["percentRelevantKilled"]
			else:
				ror = 0

			if "SOR" in info["suites"][suit]["operatorStats"]:
				sor = info["suites"][suit]["operatorStats"]["SOR"]["percentRelevantKilled"]
			else:
				sor = 0

			if "ORU" in info["suites"][suit]["operatorStats"]:
				oru = info["suites"][suit]["operatorStats"]["ORU"]["percentRelevantKilled"]
			else:
				oru = 0

			if "STD" in info["suites"][suit]["operatorStats"]:
				std = info["suites"][suit]["operatorStats"]["STD"]["percentRelevantKilled"]
			else:
				std = 0

			if "LVR" in info["suites"][suit]["operatorStats"]:
				lvr = info["suites"][suit]["operatorStats"]["LVR"]["percentRelevantKilled"]
			else:
				lvr = 0

			ratioWriter.writerow([suit, aor, lor, cor, ror, sor, oru, std, lvr])

	#dump the info dictionary to a json file so it can be used in outside programs/analyses
	with open('results.json', 'w') as outfile:
		json.dump(info, outfile, indent=5, sort_keys=True)

def helpMessage(argNum):
	print ("incorrect usage, intended usage is for 5 operators, not %d:" % argNum)
	print "[%s mutants.log killMap.csv testMap.csv coverageMap.csv out.csv ratios.csv]" % sys.argv[0]

if __name__=="__main__":    
	#make sure that the arguments passed in are the right possibilities to make the program run
    if len(sys.argv) != 7:
        helpMessage(len(sys.argv))
    else:
    	#this info dictionary will be the basis for all the data parsed and aggregated in this experiment
    	#note: at the time of this script's creation, we were unaware of how to change the test granularity 
    	#of Major from the test file level down to the test method (within every file) level
    	info = {"mutants" : {}, "suites" : {}, "operators" : {}}
        parseMutants(sys.argv[1], info)
        parseKilled(sys.argv[2], info)
        parseSuites(sys.argv[3], info)
        parseCoverage(sys.argv[4], info)
        aggregateOperators(info)
        aggregateSuites(info)
        calculateRelevantMutantsKilled(info)
        calcSubsumptionPercentages(info)
        
		#writeOut needs to be the last method called since it also writes our results JSON file out.
        writeOut(sys.argv[5], sys.argv[6], info)
	
	#this was used to view the dictionary of mutants for debugging purposes
	#pprint.pprint(info)