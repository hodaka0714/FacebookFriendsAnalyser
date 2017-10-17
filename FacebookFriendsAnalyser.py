from graphics import *
import operator
import unicodedata
from time import gmtime, strftime

TOP_FRIEND_RANK = 10
TOP_NAME_LENGTH_RANK = 10
TOP_NAME_RANK = 10

def extract_div(number,text):
    str = text[number:]
    index = 0
    ans = ''
    for i in range(len(str)):
        div = str.find('<div') if ('<div' in str) else len(text)
        ediv = str.find('</div>')
        if div < ediv:
            index = index + 1
            ans = ans + str[:div+4]
            str = str[div+4:]
        else:
            index = index - 1
            ans = ans + str[:ediv+6]
            str = str[ediv+6:]
        if index == 0:
            return ans
#extract_div(44,"<div>a<div>bc123456789</div>efg<div>hijklmno<div>p</div>qrs</div></div>")

def before_blacket(number,text):
    text = text[:number][::-1]
    text = text[:text.find('>')]
    text = text[::-1]
    return text
##before_blacket("akn>That's right!</a>".find("</a>"),"akn>That's right!</a>") -> That's right!

##Split <div class="_5h60 _30f" id="pagelet_timeline ...></div> into
##<ul class="uiList _262m _4kg" data-pnref="friends"> so that to make
##collections of <li class="_698"> ... </li>
def mk_li_list(friends_div):
    friends_div = friends_div.replace('<ul class="uiList _262m _4kg" data-pnref="friends">','@')
    friends_div = friends_div.replace('</ul><ul class="uiList _262m expandedList _4kg" data-pnref="friends">','@')
    li_collection = friends_div.split('@')
    li_collection[-1] = li_collection[-1][:-11]   #cut the last </ul></div> 
    del li_collection[0]
    return li_collection

def mk_each_list(li_collection):
    each_list = []
    for each in li_collection:
        each = each.replace('<li class="_698">','@')
        each = each.replace('</li><li class="_698">','@')
        tem_each_list = each.split('@')
        del tem_each_list[0]
        for each in tem_each_list:
            each_list.append(each)
    return each_list

def extract_fslfwbfcb(each_list):
    for i in range(len(each_list)):
        each_list[i] = extract_div(each_list[i].find('<div class="_6a _6b"><div class="fsl fwb fcb">'),each_list[i])
    return each_list

def extract_info(each_list):
    infolist = []
    for each in each_list:
        info = []
        info.append(before_blacket(each.find('</a>'),each))
        each = each[each.find('</a>') + 4:]
        first = '-1' if 'friends' not in before_blacket(each.find('</a>'),each) else before_blacket(each.find('</a>'),each)
        info.append(first)
        infolist.append(info)
    return infolist

def makeList(x):
    infile = open(x,"r")
    complete_code = infile.read()
    friends_div = extract_div(complete_code.find('<div class="_5h60 _30f" id="pagelet_timeline_app_collection_'), complete_code)
    li_collection = mk_li_list(friends_div)
    each_list = mk_each_list(li_collection)
    each_list = extract_fslfwbfcb(each_list)
    infolist = extract_info(each_list)
    return infolist



def topFriendsRank(infolist):
    whole = []
    ans = ''
    sum = 0
    for i in range(len(infolist)):
        if ('friends' in infolist[i][1]) and ('mutual' not in infolist[i][1]):
            whole.append([infolist[i][0], int(infolist[i][1][:-8].replace(',',''))])
            sum = sum + int(infolist[i][1][:-8].replace(',',''))
    whole.sort(key=lambda x: x[1], reverse=True)
    for i in range(TOP_FRIEND_RANK):
        ans = ans + whole[i][0] + '\t' + str(whole[i][1]) + '\n'
    num = len(whole)
    mid = whole[round(len(whole)/2)][1]
    avrg = round(sum / num, 2)
    ##print(ans,avrg,mid,num)
    return ans,avrg,mid,num

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    return False

def topNameLengthRank(infolist,num):
    whole = []
    ans = ''
    sum = 0
    for i in range(len(infolist)):
        if infolist[i][0].replace(' ','').replace('-','').replace("'","").isalpha() and not is_japanese(infolist[i][0]):
            whole.append([infolist[i][0], len(infolist[i][0].replace(' ','').replace('-','').replace("'",""))])
            sum = sum + len(infolist[i][0].replace(' ',''))
    whole.sort(key=lambda x: x[1], reverse=True)
    #print(whole)
    for i in range(TOP_NAME_LENGTH_RANK):
        if num == 2:
            ans = ans + whole[len(whole) - 1 - i][0] + '\t' + str(whole[len(whole) -1 - i][1]) + '\n'
        else:
            ans = ans + whole[i][0] + '\t' + str(whole[i][1]) + '\n'
    num = len(whole)
    mid = whole[round(len(whole)/2)][1]
    avrg = round(sum / num, 2)
    #print(ans,avrg,mid,num)
    return ans,avrg,mid,num

def mostCommon(infolist):
    ansFirst = ''
    ansLast = ''
    dictFirst = {}
    for i in range(len(infolist)):
        if infolist[i][0].replace(' ','').replace('-','').replace("'","").isalpha():
            a = infolist[i][0][:infolist[i][0].find(" ")]
            dictFirst[a] = dictFirst.get(a, 0) + 1
    dictFirst = sorted(dictFirst.items(), key=operator.itemgetter(1), reverse=True)
    dictLast = {}
    for i in range(len(infolist)):
        if infolist[i][0].replace(' ','').replace('-','').replace("'","").isalpha():
            a = infolist[i][0][len(infolist[i][0]) - infolist[i][0][::-1].find(" "):]
            if not a == '':
                dictLast[a] = dictLast.get(a, 0) + 1
    dictLast = sorted(dictLast.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(TOP_NAME_RANK):
        ansFirst = ansFirst + dictFirst[i][0] + '\t' + str(dictFirst[i][1]) + '\n'
        ansLast = ansLast + dictLast[i][0] + '\t' + str(dictLast[i][1]) + '\n'
    #print(ansFirst,ansLast)
    return ansFirst,ansLast

def editList(infolist):
    numbers = []
    for i in range(len(infolist)):
        if not (('mutual' in infolist[i][1]) or ('-1' in infolist[i][1])):
            a = infolist[i][1][:-8].replace(",","")
            b = int(a)
            numbers.append(b)
    numbers.sort()
##    #print(numbers)
    return numbers

def editstr(noFri_str):
    nametext = ''
    name = noFri_str.split("\n")
    for i in range(len(name)):
        name[i] = name[i][:name[i].find("\t")]
    for ele in name:
        nametext = nametext + ele + '\n'
    numtext = ''
    num = noFri_str.split("\n")
    for i in range(len(num)):
        num[i] = num[i][num[i].find("\t"):]
    for ele in num:
        numtext = numtext + ele + '\n'
    return nametext, numtext

def graphics(infolist):
    win = GraphWin("Friends Analyzer", 1020, 800)
    win.setBackground("white")

    noFri_str, noFri_avrg, noFri_mid, noFri_num = topFriendsRank(infolist)
    nameLen1_str,nameLen1_avrg, nameLen1_mid, nameLen1_num = topNameLengthRank(infolist,1)
    nameLen2_str,nameLen2_avrg, nameLen2_mid, nameLen2_num = topNameLengthRank(infolist,2)
    strFirst, strLast = mostCommon(infolist)
    numbers = editList(infolist)

    message = 'Your sourcecode is successfully analysed and  \"'+str(len(infolist))+'\"  friends\' information are extracted.\n'
    message = message + '\"' + str(len(infolist) - len(numbers)) + ' friends\" hide the information of their friends.\n'
    message = message + '\"' + str(len(infolist) - nameLen1_num) + ' friends\" don\'t register their name in alphabet. ' + strftime("%Y/%m/%d",gmtime()) + '\n'
    mainm = Text(Point(390, 50), message)
    mainm.setTextColor("green")
    mainm.draw(win)

    BELOW = 670
    ELE1_X = 150
    ELE1_Y = BELOW
    ELE2_X = 520
    ELE2_Y = BELOW
    ELE3_X = 830
    ELE3_Y = BELOW
    ELE4_X = 830
    ELE4_Y = 180
    ELE5_X = 830
    ELE5_Y = ELE4_Y + 230

    GENTEN_X = 100
    GENTEN_Y = 480
    WIDTH = 600
    HEIGHT = 350
    
    nametext, numtext = editstr(noFri_str)
    nametext2, numtext2 = editstr(nameLen1_str)
    nametext3, numtext3 = editstr(nameLen2_str)
    nametext4, numtext4 = editstr(strFirst)
    nametext5, numtext5 = editstr(strLast)
    
    Text(Point(ELE1_X, ELE1_Y), nametext).draw(win)
    Text(Point(ELE1_X + 150, ELE1_Y), numtext).draw(win)
    Text(Point(ELE2_X, ELE2_Y), nametext2).draw(win)
    Text(Point(ELE2_X + 150, ELE2_Y), numtext2).draw(win)
    Text(Point(ELE3_X, ELE3_Y), nametext3).draw(win)
    Text(Point(ELE3_X + 80, ELE3_Y), numtext3).draw(win)
    Text(Point(ELE4_X, ELE4_Y), nametext4).draw(win)
    Text(Point(ELE4_X + 80, ELE4_Y), numtext4).draw(win)
    Text(Point(ELE5_X, ELE5_Y), nametext5).draw(win)
    Text(Point(ELE5_X + 80, ELE5_Y), numtext5).draw(win)

    Text(Point(ELE1_X + 50, ELE1_Y - 130),'The number of friends TOP10\n').draw(win)
    Text(Point(ELE2_X + 40, ELE2_Y - 130),'Longest names TOP10\n').draw(win)
    Text(Point(ELE3_X + 40, ELE3_Y - 130),'Shortest names TOP10\n').draw(win)
    Text(Point(ELE4_X + 50, ELE4_Y - 120),'Most common First name TOP10\n').draw(win)
    Text(Point(ELE5_X + 50, ELE5_Y - 120),'Most common Last name TOP10\n').draw(win)
    Text(Point(ELE1_X + 50, ELE1_Y + 100),'Mean: '+ str(noFri_avrg) +', Median:'+ str(noFri_mid) +", N:"+str(noFri_num)).draw(win)
    Text(Point(ELE2_X + 40, ELE2_Y + 100),'Mean: '+ str(nameLen1_avrg) +', Median:'+ str(nameLen1_mid) +", N:"+str(nameLen1_num)).draw(win)
    Text(Point(ELE3_X + 40, ELE3_Y + 100),'Mean: '+ str(nameLen2_avrg) +', Median:'+ str(nameLen2_mid) +", N:"+str(nameLen2_num)).draw(win)

    for i in range(len(numbers)):
        bar = Rectangle(Point(GENTEN_X+WIDTH*i/len(numbers), GENTEN_Y), Point(GENTEN_X+WIDTH*(i+1)/len(numbers), GENTEN_Y-numbers[i]*HEIGHT/5000))
        bar.setFill("green")
        bar.draw(win)
    Text(Point(GENTEN_X+WIDTH, GENTEN_Y+10), len(numbers)).draw(win)

    for i in range(6):
        Text(Point(GENTEN_X-40,GENTEN_Y-HEIGHT*i/5),1000*i).draw(win)
        Line(Point(GENTEN_X,GENTEN_Y-HEIGHT*i/5),Point(GENTEN_X+WIDTH,GENTEN_Y-HEIGHT*i/5)).draw(win)
    Text(Point(GENTEN_X+WIDTH/2, GENTEN_Y-HEIGHT-35), 'The distribution of the number of friends').draw(win)

    input("Press <Enter> to quit.")
    win.close()
    
def main():
    filename = input('Type the name of a file: ')
    infolist = makeList(filename)

    graphics(infolist)
    
    simpleInfoList = editList(infolist)

main()

