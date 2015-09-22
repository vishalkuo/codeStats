import json
def writeLanguageStats(name, percentages, individual, weights,total):
    with open('report.txt', 'w') as outfile:
        outfile.write('Total bytes: ' + str(total))
        outfile.write('\n\nOverall code usage for '+name+':\n')
        outfile.write(json.dumps(percentages, indent=1))
        outfile.write('\n\nLanguage weights, this is avg(langPercentPerProject)/sum(allAvgs): ')
        outfile.write(json.dumps(weights, indent=1))
        outfile.write('\n\nBreakdown by repo including weights:\n')
        outfile.write(json.dumps(individual, indent=1))
        outfile.write('\n')
    print('Generated report.txt')
