import getpass, requests, json, utils.imports as imports, sys

API_URL = "https://api.github.com"

def authenticate():
    secret = None
    try:
        if imports.module_exists("secret"):
            secret = __import__("secret")
            name = secret.username
            password = secret.password
            print ("Found secret.py. Attempting to login using these credentials")
        else:
            name = raw_input("Enter your Github username: ")
            password = getpass.getpass("Enter your Github password: ")
        print("Authenticating...")
        r = requests.get(API_URL, auth=(name, password))
        while r.status_code != 200:
            print("Bad Credentials!")
            name = raw_input("Enter your Github username: ")
            password = getpass.getpass("Enter your Github password: ")
            r = requests.get('https://api.github.com', auth=(name, password))
        return {'name': name, 'password': password}
    except EOFError:
        print "\n"
        sys.exit(0)

def getNamedRepos(repoList, name, password):
    repos = requests.get(API_URL + '/user/repos?visibility=public', auth=(name, password))
    repoJson = json.loads(repos.text)
    print("Grabbing all repos...")
    for x in repoJson:
        repoList.append(x['name'])
    sys.stdout.flush()

def getLanguageStats(repoList, total, language, name, password, individual):
    print ("Getting language stats for repos...")
    n = len(repoList)
    for i in range(0,n):
        x = repoList[i]
        repoStat = requests.get(API_URL + '/repos/' + name + '/' + x + '/languages', auth=(name, password))
        repoStatJson = json.loads(repoStat.text)
        individual.update({x:{}})
        individual[x].update({'Breakdown':repoStatJson})
        individual[x]['Total'] = 0
        indTotal = 0
        for y in repoStatJson:
            if y in language:
                language[y] += repoStatJson[y]
            else:
                language[y] = repoStatJson[y]
            total += repoStatJson[y]
            indTotal += repoStatJson[y]
        individual[x]['Total'] = indTotal
    return total

def parseLanguageStats(language, percentages, total):
    for lang in language:
        percentages[lang] = "{0:.4f}".format((language[lang] / float(total)) * 100) + " %"

def parseProjectWeights(individual, total):
    testList = []
    for ind in individual:
        ind_total = individual[ind]['Total']
        individual[ind]['Weight'] = formatZero((ind_total / float(total)), 4)

def parseLanguageWeights(individual, result):
    print('Guessing (language) weights...')
    total = None
    for ind in individual:
        total = individual[ind]['Total']
        weight = individual[ind]['Weight']
        for lang in individual[ind]['Breakdown']:
            result.setdefault(lang, []).append((float(individual[ind]['Breakdown'][lang]) / total) * float(weight) * 100)
    for key in result:    
        avg = average(result[key])
        result[key] = avg * 100
    result_sum = sum(map(float, result.values()))
    for key in result:
        result[key] = formatZero(result[key]/float(result_sum) * 100, 4)

def average(list):
    return float(sum(list))/len(list) if len(list) > 0 else float('nan')

def writeLanguageStats(name, percentages, individual, weights,total):
    with open('report.txt', 'w') as outfile:
        outfile.write('Total bytes: ' + str(total))
        outfile.write('\n\nOverall code usage for '+name+':\n')
        outfile.write(json.dumps(percentages, indent=1))
        outfile.write('\n\nLanguage weights, this is avg(langPercentPerProject)/sum(allAvgsFromNumerator): ')
        outfile.write(json.dumps(weights, indent=1))
        outfile.write('\n\nBreakdown by repo including weights:\n')
        outfile.write(json.dumps(individual, indent=1))
        outfile.write('\n')
    print('Generated report.txt')

def formatZero(exp, zero):
    return ("{0:." + str(zero) + "f}").format(exp)