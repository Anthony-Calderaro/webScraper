#! oscarsAPI.py
import json, requests, re

# Download the JSON data from API.
url = "http://oscars.yipitdata.com"
response = requests.get(url)
response.raise_for_status()

# Load JSON data into a Python variable.
oscarData = json.loads(response.text)
x = oscarData["results"] # x is an array of 87 years

# iterate over each of the 87 years
# send each year to the years array
years = []
yearsIndex = 0
while yearsIndex < len(x):
    for item in x[yearsIndex]:
        if item == "year":
            encodedYear = str(x[yearsIndex][item])
            years.append(encodedYear)
            yearsIndex += 1

# Go through the Years Array with a REGEX to get the first 4 digits
# Send the formatted year to the yearsMasterArray. Encode it
yearMasterArray = []
yearPattern = re.compile(r"\d{4}") 
for year in years:
    matches = yearPattern.findall(year)
    yearMasterArray.append(matches[0].encode("utf-8"))

# Check
# print(len(years)) # Should be 87
# print("\n".join(years)) # this returns the raw data
# print("\n".join(yearMasterArray)) # returns the 4-digit date

# iterate over each of the 87 years
# Grab the winning film where winner is True 
# Push to the winners array
winners = []
winnersIndex = 0
while winnersIndex < len(x):
    for item in x[winnersIndex]["films"]:
        if item["Winner"] == True:
            winningMovie = str(item["Film"])
            winners.append(winningMovie)
            winnersIndex += 1

# Go through winners array with with a REGEX to get the proper title
# Push it to the winnerMasterArray
winnerMasterArray = []
winnerPattern = re.compile(r"[\w -.!()!:;]*[^\[]") 
for winner in winners:
    matches = winnerPattern.findall(winner)
    winnerMasterArray.append(matches[0].encode("utf-8"))

# Check
# print(len(winners)) # Should be 87 
# print(len(winnerMasterArray)) # Should be 87 
# print("\n".join(winners)) # this returns the raw data
# print("\n".join(winnerMasterArray)) # this returns the formatted data

# Iterate over each winning film 
# Grab the url from the Detail URL key:value pair
# Push to winningURLArray
winningURLArray = []
winningURLIndex = 0
while winningURLIndex < len(x):
    for item in x[winningURLIndex]["films"]:
        if item["Winner"] == True:
            winningURL = str(item["Detail URL"])
            winningURLArray.append(winningURL)
            winningURLIndex += 1

# Check
# print(len(winningURLArray)) # Should be 87
# print("\n".join(winningURLArray)) # Prints Raw URL from Detail URL Key

# Iterate over each url in the winningURLArray
# Take the url, go to the url, load it as JSON data  
# Search the JSON data, find the budget key
# Push it to the budget array
budgetArray = []
budgetArrayIndex = 0
while budgetArrayIndex < len(winningURLArray):
    winnerData = winningURLArray[budgetArrayIndex]
    winningRes = requests.get(winnerData)
    winningRes.raise_for_status()
    winningBudgets = json.loads(winningRes.text)
    if "Budget" in winningBudgets:
        cost = winningBudgets["Budget"]
        budgetArray.append(cost)
    budgetArrayIndex += 1

# Check 
# print(len(budgetArray)) # Should be 87, getting 82. Need to Grab Wiki URL for 
# print("\n".join(budgetArray)) # Raw data

budgetMasterArray = []
budgetMasterArrayNum = []
budgetPattern = re.compile(r"\d[0-9]*")
for item in budgetArray:
    matches = budgetPattern.findall(item)
    for match in matches:
        m = str(match.encode("UTF-8"))
        if len(m) == 3:
            budgetMasterArray.append("%s000" % m)
        elif len(m) < 3:
            budgetMasterArray.append("%s000000" % m)
        else:
            budgetMasterArray.append(m)

for item in budgetMasterArray:
    budgetMasterArrayNum.append(int(item))

total = 0
count = 0
avg = 0
for number in budgetMasterArrayNum:
    total += number
    count += 1
    if count == len(budgetMasterArrayNum):
        avg += total / count

counter = 0
while counter < len(yearMasterArray):
    a = yearMasterArray[counter] 
    b = winnerMasterArray[counter]
    if budgetMasterArrayNum > 0:
        c = ("$%s" % (budgetMasterArrayNum[counter]))
    else:
        c = 0
    print("In %s, %s won with a budget of %s." % (a, b, c)) 
    counter += 1

print("In total, there were 87 oscar awards, with an average budget of approximately $%s" % (avg))

