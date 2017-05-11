# Analyzing report by dividing report into each word.
import PyPDF2
import sys

def writeCountToCSV(word_dir, filename):
    outfile = open(filename +".csv","w")
    outfile.write("WORD"+",")
    outfile.write("COUNT"+"\n")
    for key in list(word_dir.keys()):
        outfile.write(key+",")
        outfile.write(str(word_dir[key])+"\n")

def MakeWordDir(word_dir, page_content):
    usable_char = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,r,x,y,z'.split(",")
    usable_char.append("\n")
    usable_char.append(" ")
    temp='';
    for c in page_content.lower():
        if c in usable_char:
            temp = temp +c
    splitedList = temp.split()
    
    for sample in splitedList:
        if sample not in list(word_dir.keys()):
            word_dir[sample] = 1
        else:
            word_dir[sample] = word_dir[sample]+1
    return word_dir

#예외상황 처리
def deleteUselessWord(word_dir):
    #동사 중에서 be동사는 의미 없으므로 삭제
    BeVerb = ['am', 'is', 'are', 'were', 'was', 'be','it','they','you','we'];
    #그외 분석에 필요없는 단어
    OtherWord = ['the', 'a', 'an', 'on', 'or', 'th', 'this', 'them', 'in', 'as', 'their', 'by', 'with', 'on', 'at', 'up', 'down', 'out', 'of', 'away', 'when', 'where', 'which', 'that', 'what', 'to', 'and', 'our', 'my', 'for', 'upon', 'ours', 'her', 'his', 'him', 'hers', 'whose', 'how', 'why']
    OtherWord = OtherWord +['who','wherever','whether', 'these','then', 'than','might','me','could','shall']
    for sample in list(word_dir.keys()):
        if sample in (BeVerb+OtherWord):
            del(word_dir[sample])

    return word_dir

def makePluralOne(word_dir):
    #복수형 표현은 단수형으로 뭉치기
    for sample in sorted(list(word_dir.keys())):
        if(sample[-1]=='y' and ((sample[:-1]+'ies' in list(word_dir.keys())))):
            word_dir[sample] += word_dir[sample[:-1]+'ies']
            del(word_dir[sample[:-1]+'ies'])
        elif (sample+'s' in list(word_dir.keys())):
            print(sample)
            word_dir[sample] += word_dir[sample+'s']
            del(word_dir[sample+'s'])
        elif (sample+'es' in list(word_dir.keys())):
            word_dir[sample] += word_dir[sample+'es']
            del(word_dir[sample+'es'])
        else:
            pass
    return word_dir
    

def openFile(filename):
    pdf_file = open(filename+'.pdf','rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)   
    page_number = read_pdf.getNumPages()
    word_dir = {}
    for i in range (0,page_number):
        page = read_pdf.getPage(i)
        try:
            page_content = page.extractText()
            word_dir = MakeWordDir(word_dir, page_content)
        except:
             print("Error_Page : "+str(i));   

    word_dir = deleteUselessWord(word_dir)
    word_dir = makePluralOne(word_dir)
    writeCountToCSV(word_dir, filename)
        

def main():
    openFile('C:\\Users\\GWONSOO\Desktop\\졸업논문\\references\\source\\4. Coca-Cola\\2016-AR-10-K');
main()
