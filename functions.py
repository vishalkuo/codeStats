import getpass, requests, json

API_URL = "https://api.github.com"

def authenticate():
    name = raw_input("Enter your Github username: ")
    password = getpass.getpass("Enter your Github password: ")
    r = requests.get(API_URL, auth=(name, password))
    while r.status_code != 200:
        print("Bad Credentials!")
        name = raw_input("Enter your Github username: ")
        password = getpass.getpass("Enter your Github password: ")
        r = requests.get('https://api.github.com', auth=(name, password))
    return {'name': name, 'password': password}


def getNamedRepos(repoList, name, password):
    repos = requests.get(API_URL + '/user/repos?visibility=public', auth=(name, password))
    repoJson = json.loads(repos.text)
    for x in repoJson:
        repoList.append(x['name'])


def getLanguageStats(repoList, total, language, name, password, individual):
    for x in repoList:
        repoStat = requests.get(API_URL + '/repos/' + name + '/' + x + '/languages', auth=(name, password))
        repoStatJson = json.loads(repoStat.text)
        individual[x] = repoStatJson
        for y in repoStatJson:
            if y in language:
                language[y] += repoStatJson[y]
                total += repoStatJson[y]
            else:
                language[y] = repoStatJson[y]
                total += repoStatJson[y]
    return total

def parseLanguageStats(language, percentages, total):
    for lang in language:
        percentages[lang] = "{0:.4f}".format((language[lang] / float(total)) * 100) + " %"

def parseLanguageWeights(individual, result):
    for ind in individual:
        for lang in individual[ind]:
            result.setdefault(lang, []).append(individual[ind][lang])
    print result

def writeLanguageStats(name, percentages, individual, total):
    with open('report.txt', 'w') as outfile:
        outfile.write('Total bytes: ' + str(total))
        outfile.write('Overall code usage for '+name+':\n')
        outfile.write(json.dumps(percentages, indent=1))
        outfile.write('\n\nBreakdown by repo:\n')
        outfile.write(json.dumps(individual, indent=1))
        outfile.write('\n')
    print('Generated report.txt')




