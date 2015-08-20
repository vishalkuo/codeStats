import requests, getpass, json

API_URL = "https://api.github.com"

name = raw_input("Enter your Github username: ")
password = getpass.getpass("Enter your Github password: ")
r = requests.get(API_URL, auth=(name, password))
while r.status_code != 200:
    print("Bad Credentials!")
    name = raw_input("Enter your Github username: ")
    password = getpass.getpass("Enter your Github password: ")
    r = requests.get('https://api.github.com', auth=(name, password))

repos = requests.get(API_URL + '/users/' + name + '/repos', auth=(name, password))
repoJson = json.loads(repos.text)
repoList = []
for x in repoJson:
    repoList.append(x['name'])

language = {}
total = 0
for x in repoList:
    repoStat = requests.get(API_URL + '/repos/' + name + '/' + x + '/languages', auth=(name, password))
    repoStatJson = json.loads(repoStat.text)
    for y in repoStatJson:
        if y in language:
            language[y] += repoStatJson[y]
            total += repoStatJson[y]
        else:
            language[y] = repoStatJson[y]
            total += repoStatJson[y]

percentages = {}
for lang in language:
    percentages[lang] = "{0: .4f}".format((language[lang] / float(total)) * 100) + " %"
print json.dumps(percentages, indent=1)