import re
import sys
import spacy
import matplotlib as mpl

## todo -- tune spacy to be a bit faster
## todo -- make some kind of a UI?
## todo -- maybe use numpy or matplotlib or whatever to make a graph from this

class wordCount:
    nlp = spacy.load('en_core_web_sm')
    excluded_pos = {"ADP", "AUX", "PRON", "DET", "PART", "PUNCT", "SCONJ", "PREPN", "CCONJ"}
    defaultFile = "thegreatgatsby.txt"
    currentFile = ""
    textArray = []
    totalLength = 0
    runningTotalCnt = 0
    runningTotalPct = 0
    totalRelevantLength = 0
    relevantTotalPct = 0
    
    def __init__(self):
        print("Python-based data tool for text files")


    def fileToArray(s):
        s.textArray = [line.strip() for line in s.currentFile.readlines()]
        s.stripUnwantedPOS()


    def stripUnwantedPOS(s):
        sentences = s.textArray
        new_sentences = []
        for sentence in sentences:
                new_sentence = []
                for token in s.nlp(sentence):
                    if token.pos_ not in s.excluded_pos:
                        s.totalRelevantLength = s.totalRelevantLength + 1
                        new_sentence.append(token.text)
                new_sentences.append(" ".join(new_sentence))
        s.textArray = new_sentences


    def printCounts(s, dc):
        i = 0
        for key in list(dc.keys()):
            if (len(key) < 2 or key.strip() == ""):
                del dc[key]
                
        sortD = sorted(dc.items(), key=lambda x:x[1], reverse=True)
        
        for key in sortD:
            i += 1
            if(i < 21):
                pre = ")" if i > 9 else " )"
                pctOfTotal = '{:.1%}'.format(key[1] / s.totalLength)

                s.runningTotalCnt = int(s.runningTotalCnt) + int(key[1])
                s.runningTotalPct = float(s.runningTotalPct) + float(key[1] / s.totalLength)
                s.relevantTotalPct = float(s.relevantTotalPct) + float(key[1] / s.totalRelevantLength)

                print(i, pre, key[0], ":", key[1], "(", pctOfTotal, ")")
            else:
                break


    def countWords(s):
        data = s.currentFile.read()
        words = data.split()
        s.totalLength = len(words)


    def buildDict(s):
        d = dict()
        for line in s.textArray:
            line = line.lower()
            words = line.split(" ")
                
            for word in words:
                word = re.sub('[^A-Za-z0-9]+', '', word)
                if word in d:
                    d[word] = d[word] + 1
                else:
                    d[word] = 1             
        return d


    def makeChart(s, words):
        labels = words.keys()
        sizes = words.values()
        
        
        pass


    def main(s):
        n = len(sys.argv) 
        if(n < 2):
            print("File Path:", s.defaultFile)
            s.currentFile = open(s.defaultFile, encoding="utf8")
            s.countWords()
            print("Word Count:", s.totalLength)
            s.currentFile.seek(0)
            s.fileToArray()
            dc = s.buildDict()
            s.printCounts(dc)
        else:
            for arg in range(1, n):
                print("File Path:", sys.argv[arg])
                s.currentFile = open(sys.argv[arg], encoding="utf8")
                s.countWords()
                print("Word Count:", s.totalLength)
                s.currentFile.seek(0)
                s.fileToArray()
                dc = s.buildDict()
                s.printCounts(dc)
        print("Relevant Total: ", s.totalRelevantLength, "(", '{:.1%}'.format(s.relevantTotalPct), ")")        
        print("Total:", s.runningTotalCnt, "(", '{:.1%}'.format(s.runningTotalPct), ")")
        

w = wordCount()
w.main()