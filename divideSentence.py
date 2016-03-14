#coding=utf-8
import obtainKeywords
import sys, re
import chardet 
reload(sys)
sys.setdefaultencoding("utf-8")
# sys.setdefaultencoding('gb18030') 


#判断 文本(字符串)的类型
def obtainTextType(ff):
    # import chardet 
    enc = chardet.detect(ff) 
    return enc['encoding']  #返回文件类型

################################################################################################

#文件编码类型判断
def obtainFileType(filepath):
    # import chardet 
    tt = open(filepath, 'rb') 
    ff = tt.readline()        #这里试着换成read(5)也可以，但是换成readlines()后报错 
    tt.close() 
    return obtainTextType(ff)  #返回文件类型

################################################################################################

#读取文件, 返回去掉空格和空白的字符串 
def ReadFile(url):		#url文件的路径
    # print obtainFileType(url)
    if obtainFileType(url) == 'GB2312':
        #.decode("gbk").encode('utf-8') 以gbk编码格式读取字符串（因为他就是gbk编码的）并转换为utf-8格式输出
        content = open(url, "rb").read().decode("gbk").encode('utf-8')
        # print obtainTextType(content)

    elif obtainFileType(url) == 'ascii':
        content = open(url, "rb").read().encode('utf-8')
        # print obtainTextType(content)

    else:
        # print obtainFileType(url)
        content = open(url, "rb").read()
        # print obtainTextType(content)

    strRe = re.sub('\s', '', content)   #用正则干掉所有的空白
    return strRe

################################################################################################


# 清除函数中多余的分句字符.---'？。！',如果连续出现,次序不限,只保留一次, 
# 并且,在列表头部, 不存在以上述字符开头的情况,有则删除.
# 参数: 1 分词以后的一个词的链表 2:要删除的 特殊字符
def remove_special_characters_InText(word_list, special_characters):
    punt_list = special_characters          # 作为句子结束的判断

    #在词表开头, 判断是否是以正文开头,还是以句子结束符开头.
    while True:
        if word_list[0] not in punt_list:
            break
        else:
            del word_list[0]

    singal = False                  # 标记, 如果前面存在了句尾结束符, 那么下一个必须不是, 如果还是,就不保存
    ReWords = []                    # 保留词表    
    for word in word_list:
        if word not in punt_list:
            singal = True
            ReWords.append(word)
        if word in punt_list:
            if singal == True:
                ReWords.append(word)
                singal = False
    
    # i = 1000
    # for w in ReWords:
    #     i = i - 1
    #     if i < 0:
    #         break
    #     print w,

    return ReWords

################################################################################################

# 处理一个句子中的连续符号的问题, 比如 ,.相连...
def remove_special_characters_InSentence(divide_sentence_Map, special_characters):
    punt_list = special_characters          # 作为句子结束的判断
    sentences_Map = {0:[]}
    # 还没有想好怎么处理, 有待商榷.......
    pass

################################################################################################

#根据分词之后的列表,进行分句
def divide_sentence_for_Map(strReContent):
    word_list = obtainKeywords.divide_text_words(strReContent)                                  #  对文本进行分词
    
    # 这里需要说明一下,  ？。！ 只处理中文字符.就这三个做为结束符号.
    ReWordsList = remove_special_characters_InText(word_list, '？。！'.decode('utf8'))           #  删除文章开头部分 和 文章中重复的, 连在一起的--- 句尾结束标记词

    # 分句, 将文章, 根据句子结束符, 分句.
    punt_list = '？。！'.decode('utf8')                          # 作为分句的判断
    divide_sentence_Map = {0:[]}                                # 保存分句的字典, key: 句子的顺序, value: 是一个列表, 保存了该句子被分词后的 词组.
    countNum = 0                                                # 计数, 作为字典的key
    text_head_singal = False                                    # 标记, 当被标记为True时, 字典key加1, 进入下一个句
    newline_singal = False                                      # 开始新的一行

    for word in ReWordsList:                                    # 遍历分词之后的磁链
        if word not in punt_list:                               # 如果这个分词, 是句尾标记词, 就进入下一句
            divide_sentence_Map[countNum].append(word)
        
        else:
            divide_sentence_Map[countNum].append(word)
            countNum = countNum + 1                             # 存储分句的字典 key 进行跟新
            divide_sentence_Map[countNum] = []                  # 初始化


#这里有待商榷.
    # # 处理分句中的符号问题, 比如 ,, 连在一起, 或者 ,. 连在一起.这种. 消除,保证句子的紧凑. 这样便于统计真是的句子长度和分词个数.
    # special_characters = "[。,?、|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:".decode('utf8')
    # divide_sentence_Map = remove_special_characters_InSentence(divide_sentence_Map, special_characters)

    return divide_sentence_Map


################################################################################################

#程序进行中文分句, 返回分组之后的列表 
def cut_sentence(words):		#words是中文字符串
    words = (words).decode('utf8')
    start = 0
    i = 0
    sents = []
    token = ''
    punt_list = '？。！'.decode('utf8')
    for word in words:
        if word in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sents.append(words[start:i+1])
            start = i+1
            i += 1
        else:
            i += 1
            token = list(words[start:i + 2]).pop() 		# 取下一个字符
    if start < len(words):
        sents.append(words[start:])
    return sents

################################################################################################

#先读取文章中的数据,然后进行分句,返回分句之后的列表
def divideSentence(url):
	strRe = ReadFile(url)
	sentences = cut_sentence(strRe)
	return sentences
	

    
# ------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    # sentences = divideSentence('foo.txt')

    # print type(sentences)

    strRe = ReadFile('10.txt')
    divide_sentence_Map = divide_sentence_for_Map(strRe)       #进行分词

    print len(divide_sentence_Map)
    for i in divide_sentence_Map[0]:
        print i, "-",


    # print len(divideSentence('foo.txt'))
	# for s in sentences:
	# 	print s.decode('utf-8')


