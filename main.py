import functions, signal, sys, utils.writer as writer

auth = {'name':None, 'password':None}
repoList = []
language = {}
total = 0
percentages = {}
individual = {}
weights = {}

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

auth = functions.authenticate()
functions.getNamedRepos(repoList, auth['name'], auth['password'])
total = functions.getLanguageStats(repoList, total, language, auth['name'], auth['password'], individual)
functions.parseLanguageStats(language, percentages, total)
functions.parseProjectWeights(individual, total)
functions.parseLanguageWeights(individual,  weights)
writer.writeLanguageStats(auth['name'], percentages, individual, weights ,total)







