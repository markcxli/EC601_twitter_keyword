import matplotlib.pyplot as plt
f = open("result.txt", "r")
line = f.readline()
data = line.split(' ')
for e in data:
	print e
f.close()

def plotPieChart(positive, negative, neutral, searchTerm, noOfSearchTerms):
    
    labels = ['Positive [' + str(positive) + '%]','Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'gold', 'darkred']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('The Twitter Reflection on ' + searchTerm + ' after analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()

    plt.show()


plotPieChart(float(data[0]), float(data[1]), float(data[2]), data[3], data[4])


   