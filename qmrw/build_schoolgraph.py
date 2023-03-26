import json
fo=open(r"./data/school.csv","r",encoding='gbk')  #打开csv文件
ls=[]
for line in fo:
    line=line.replace('\n','').replace('\r\n','').replace('\\r','').replace('\"','').replace('\\','').replace('\r','') #将换行换成空
    ls.append(line.split(","))  #以，为分隔符
fo.close()  #关闭文件流
# print(ls)
new_ls = []
# fw=open("./all.json","w",encoding="utf-8")  #打开json文件
for i in range(1,len(ls)):  #遍历文件的每一行内容，除了列名
    ls[i]=dict(zip(ls[0],ls[i]))  #ls[0]为列名，所以为key,ls[i]为value,
    #zip()是一个内置函数，将两个长度相同的列表组合成一个关系对
print(ls)
with open(".data/entry.json","w",encoding="utf-8") as fw:
    for j in range(1,len(ls)):
        fw.write(json.dumps(ls[j], ensure_ascii=False) + '\n')

