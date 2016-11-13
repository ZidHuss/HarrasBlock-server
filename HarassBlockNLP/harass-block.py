import nltk
from nltk.tag import pos_tag, map_tag
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import re

class HarassBlock:
    url=''
    
    def analyze(self, url):
        req = requests.get(url)                                 # Get the page
        soup = BeautifulSoup(req.content, 'html.parser')        # Parse Text from HTML
        for script in soup(["script","style"]):
            script.extract()
        text = soup.find('body').get_text()
        text = re.sub(r'\n\s*\n', r'\n', text.strip(), flags=re.M) 
       
        textLines = text.split('\n')                            # Split text into lines array
 
        sid = SentimentIntensityAnalyzer()
        i=0
        lineScoreMap = dict()
        for line in textLines:
            # print(textLines[i])
            scores = sid.polarity_scores(line)
            # print('line' + str(i) + ' - {0}: {1}, '.format('compound', scores['compound']), end='') 
            lineScoreMap[textLines[i]] = scores['compound']
            i+=1
        
        harassmentScores = []
        uniqueBadWordsDetected = set([])
        for c in range(len(textLines)):
            # print('line ' + str(c) + ' - ' + textLines[c])
        




            # print(textLine[0])
            tokenizedText = nltk.word_tokenize(textLines[c])    # Tokenize the line into words
            posTagged = pos_tag(tokenizedText)                  # Tag pronouns... ect
            simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
    
            badWords = self.readBadWords()                      # Read list of badwords
            # print(badWords)
            
            # print(simplifiedTags)

            for i in range(len(simplifiedTags) - 1):            # loop through word,tag array
                if simplifiedTags[i][1] == 'PRON' and simplifiedTags[i+1][0] in badWords:
                    print('Harassment Detected (PRONOUN BADWORD) - ' + simplifiedTags[i+1][0])
                    uniqueBadWordsDetected.add(simplifiedTags[i+1][0])
                    harassmentScores.append(lineScoreMap[textLines[c]])
                    # print(lineScoreMap[textLines[c]])
                elif simplifiedTags[i][0] in badWords and simplifiedTags[i+1][1] == 'PRON':
                    print('Harassment Detected (BADWORD PRONOUN) - ' + simplifiedTags[i][0])
                    uniqueBadWordsDetected.add(simplifiedTags[i][0])
                    harassmentScores.append(lineScoreMap[textLines[c]])
                elif simplifiedTags[i][1] == 'PRON':
                    print (simplifiedTags[i+2:])
                    for j in simplifiedTags[i+2:]:
                        if j[0] in badWords:
                            print('Harassment Detected (PRONOUN ... BADWORD) - ' + j[0])
                            uniqueBadWordsDetected.add(j[0])
                            harassmentScores.append(lineScoreMap[textLines[c]])
                print(harassmentScores)
                
        totalHarassmentRating = sum(harassmentScores)
        print(totalHarassmentRating)
        return totalHarassmentRating

    def readBadWords(self):
        with open('google_badlist.txt', 'r') as badWords:
            return [badWord.rstrip() for badWord in badWords.readlines()]



def main():
    instance = HarassBlock()
    # instance.analyze('http://www.urbandictionary.com/define.php?term=fuck%20you')
    instance.analyze('https://ghostbin.com/paste/7yhn5')

if __name__ == '__main__':
    main()
