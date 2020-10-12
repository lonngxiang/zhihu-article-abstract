import requests
import json
import time
import csv
import pymysql
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import hashlib
# import time
import random
import http.client
from lxml import etree
import urllib
import datetime
import re

from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib as mpl  # 配置字体
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"] #配置字体，不然汉字有的显示不正常
path = r'/Users/lonng/Desktop/v+/呆萌的停用词表.txt'


lists = []
def zhihu():
    

    headers={
        "accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",

    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "upgrade-insecure-requests":"1"
    }

    

    #&sort_by=updated  按时间更新排序 ；default 默认排序

    for i in range(15):
        print("第%d页"%i)
        url="https://www.zhihu.com/api/v4/questions/424604443/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&limit=5&offset={}&sort_by=default&platform=desktop".format(i*5)

        html=requests.get(url,headers=headers).text
        print(html)
        html = json.loads(html)
        for i in range(len(html["data"])):
            # print(html["data"][i]["content"])
            title = html["data"][i]["question"]['title']
            title_url = 'https://www.zhihu.com/question/'+str(html["data"][i]["question"]['id'])
            author = html["data"][i]["author"]['name']
            author_url = "https://www.zhihu.com/people/"+ str(html["data"][i]["author"]['id'])
            answer_url = "https://www.zhihu.com/question/{}/answer/{}".format(str(html["data"][i]["question"]['id']),str(html["data"][i]["id"]))
            if html["data"][i]["author"]['gender'] == 0:
                gender = "女"
            else:
                gender = "男"
            dtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(html["data"][i]["created_time"]))
            content = html["data"][i]["content"]
            voteup_count = html["data"][i]["voteup_count"]
            comment_count = html["data"][i]["comment_count"]
            print([title,title_url,author,gender,author_url,answer_url,dtime,voteup_count,comment_count,content])
            lists.append([title,title_url,author,gender,author_url,answer_url,dtime,voteup_count,comment_count,content])

    #         hot = "insert into zhihu_copy(title,title_url,author,gender,author_url,answer_url,dtime,voteup_count,comment_count,content) values('%s','%s','%s','%s','%s','%s','%s','%d','%d','%s')" % (
    #             title, title_url, author, gender, author_url, answer_url, dtime, voteup_count, comment_count, content)
    #         curor.execute(hot)
    #         conn.commit()


zhihu()

import jieba
import jieba.analyse
jieba.analyse.set_stop_words(path)
jieba.add_word('Jackeylove')
jieba.add_word('jklove')
# tags = jieba.analyse.extract_tags(" ".join(contents), topK=50 ,withWeight=True)
tags = jieba.analyse.extract_tags(" ".join(lists1).replace("https","").replace("www","").replace("zhihu","")\
                                  .replace("http","").replace("cn","").replace("video","").replace("知乎","").replace("question","").replace("answer",""), topK=100)


print(tags,"人工智能提取前100核心关键词："+','.join(tags))


#词云
text=' '.join(tags)
wc = WordCloud(font_path="/Users/lonng/Library/Fonts/msyh.ttf",background_color='black',max_words=100,max_font_size=120,scale=10)
word_cloud = wc.generate(text)
# word_cloud.to_file('3.png')
plt.figure(figsize=(26,26))
plt.imshow(word_cloud)
plt.axis("off")
plt.show()



#摘要
ss = []
tr4s1 = TextRank4Sentence()
tr4s1.analyze(text="".join(lists1), lower=True, source = 'all_filters')
# print( str(n+1)+'.摘要：' )
for item in tr4s1.get_key_sentences(num=20):
    print(item.sentence+"\n")
    ss.append(item.sentence)
    
    
sss = '人工智能NLP自动提取：\n'
for ii,jj in enumerate(ss[:20]):
    sss = sss + "{}、{}".format(ii+1,jj) + "\n\n\n"
    
print(sss)
