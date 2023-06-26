import requests
import bs4
from lxml import etree
import pandas as pd
useragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3514.0 Safari/537.36'
cookie=''#cookie
headers = {'User-Agent':useragent,'Cookie':cookie}
url=''
r = requests.get(url,headers=headers)
r.encoding = 'utf-8'
tree = etree.HTML(r.text)
soup=bs4.BeautifulSoup(r.text,'html.parser')
total=int(tree.xpath('//*[@id="fanyaMarking"]/div[1]/div[1]/div[1]/span[1]/text()')[0].split('：')[1])
attr=[]
for i in range(total):
    i=i+1
    dicmm={'questionId':str(i),'question':'','A':'','B':'','C':'','D':'','answer':''}
    dataid=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']')[0].get('data')
    ids='question'+str(dataid)
    question=soup.find(id=ids).find('h3').get_text('\n')
    print('i:'+str(i),end='')
    try:
        isRight=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']/div/div[2]/div[1]/div/span/@aria-label')[0]
    except:    
        isRight=tree.xpath('//*[@id="'+ids+'"]/div/div[3]/div[1]/div/span/@aria-label')[0]
    if isRight=='答案错误':
        ass=[]
        divaa=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']/ul/li[1]/text()')
        divbb=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']/ul/li[2]/text()')
        divcc=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']/ul/li[3]/text()')
        divdd=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']/ul/li[4]/text()')
        divc=tree.xpath('/html/body/div[3]/div[1]/div[2]/div/div['+str(i)+']/div/div/span[1]/text()')
        print(ass)
        Gid=str(str(i)+'.')
        dicmm['question']=question.replace(Gid,'')[12:]
        dicmm['A']=divaa[0][2:]
        dicmm['B']=divbb[0][2:]
        dicmm['C']=divcc[0][2:]
        dicmm['D']=divdd[0][2:]
        dicmm['answer']=divc[0]
        attr.append(dicmm)
        print("q:"+str(ass)+"A:"+str(divaa)+"B:"+str(divbb)+"C:"+str(divcc)+"D:"+str(divdd)+"答案:"+str(divc))
db=pd.DataFrame(attr)
db.to_csv('test.csv',encoding='utf-8-sig')
