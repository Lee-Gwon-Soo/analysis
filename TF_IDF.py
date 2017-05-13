import sys
import math

def getWordCount(corpname):
    flag=False;
    infile = open('Source\\'+corpname+'.csv','r')
    wordDict={}
    for line in infile:
        tempList = line.replace("\n","").split(",")            
        if( flag and (int(tempList[1]) >= 70)): #일정 갯수 이상 나온 경우만 조사.
            wordDict[tempList[0]]=int(tempList[1])
        flag = True
    infile.close()

    return wordDict

def doAnalzyingFD_IDF(corpGroup, wordInfo_byCompany, i):
    
    wordDict = wordInfo_byCompany[i];
    tfidfDict = {}
    outfile = open('result\\'+corpGroup[i]+".csv","w")
    
    outfile.write("WORD"+",")
    outfile.write("FD value"+",")
    outfile.write("IDF value"+",")
    outfile.write("FD-IDF " +"\n")
    for sampleKey in wordDict.keys():
        #FD 값 구하기
        temp_FD = 0.5 + 0.5*(int(wordDict[sampleKey])/getMax(wordDict.values()))
        #IDF 값 구하기
        temp_IDF = IDF(len(corpGroup),sampleKey, wordInfo_byCompany, i)

        temp_TFIDF = temp_FD * temp_IDF
        outfile.write(sampleKey+",")
        outfile.write(str(temp_FD)+",")
        outfile.write(str(temp_IDF)+",")
        outfile.write(str(temp_TFIDF) +"\n")
        
        tfidfDict[sampleKey] = temp_TFIDF

    outfile.close()
    return tfidfDict

def getMax(valueList):
    return sorted(valueList)[-1]


def IDF(total_number_of_document, term, wordInfo_byCompany, i):
    count = 0
    for j in range (0, len(wordInfo_byCompany)):
        tempList = wordInfo_byCompany[j].keys()
        if term in tempList:
            count+=1

    return math.log10(total_number_of_document/(1+count))


def main():
    corpname = ['cocacola', 'disney','facebook', 'ge', 'ibm', 'mcdonalds', 'microsoft', 'toyota']
    #일단 파일에서 단어 정보 불러오기.
    wordInfo_byCompany = []
    for comp in corpname :
        wordInfo_byCompany.append(getWordCount(comp))

    #TFIDF 구하기
    tfidfInfo_byCompany = []
    for i in range (0, len(corpname)):
         tfidfInfo_byCompany.append(doAnalzyingFD_IDF(corpname, wordInfo_byCompany, i))


    print("End Analyzing")
    
    

    #결과를 통해서 분석하기.
main()
