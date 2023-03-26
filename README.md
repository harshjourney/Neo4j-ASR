# Neo4j-ASR
基于Neo4j知识图谱的语音问答实践（项目改编自刘焕勇的医疗问答知识图谱项目）

简介


通过开源项目(刘焕勇，中国科学院软件研究所)的医药问答项目，互网
上爬取的数据，在neo4j上建立知识图谱，然后进行数据的处理并进行问题
解析，最后用语音技术实现问题的录入和回答

Neo4j上手指南


安装教程：https://blog.csdn.net/zeroheitao/article/details/122925845
一些常用的命令：

1.创建结点
create(节点名称：节点标签{属性名：属性值，。。。。})
//可以创建没有属性的节点，create总是创建节点

2.删除数据库里所有内容
match(n) detach DELETE n

3.删除
match(节点名称：节点标签{节点属性:"属性值"}) delete 节点名称

删除关系：
match(p:person{name:"",})-[x:gxx]-(n:person{name:'zx"}) delete x,n,p 

添加标签：
match(p:Person) where id(p)=2 set p:善良的富二代 return p

修添属性：
match(p:Person) where id(p)=2 set p.能力="波纹疾走" return p

查找关系：
match(n:Person)-[:死敌]->(p:Person) return n,p

建立关系
create(p:person{name:"",})-[x:gxx]-(n:person{name:'zx"})

网络爬虫


暂时就不过多介绍了，我这里用的是xpath的方式进行的爬取，不会的话建议去CSDN上面看看


语音识别模块

注意一下：我这个代码里面的API试用期已经过期了所以跑不出来，你可以去注册一个号然后它会免费给你玩一段时间
