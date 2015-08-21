import functions

auth = {'name':None, 'password':None}
repoList = []
language = {}
total = 0
percentages = {}
individual = {}

auth = functions.authenticate()
functions.getNamedRepos(repoList, auth['name'], auth['password'])
total = functions.getLanguageStats(repoList, total, language, auth['name'], auth['password'], individual)
functions.parseLanguageStats(language, percentages, total)
functions.writeLanguageStats(auth['name'], percentages, individual)








