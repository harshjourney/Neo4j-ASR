import os
import json
from py2neo import Graph,Node

class Schoolgraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.d_p = os.path.join(cur_dir,'./data/entry2.json')
        self.gg = Graph("http://localhost:7474", username="neo4j", password="z5896347")
 #读取文件
    def read_nodes(self):
        descs = [] #学校简介
        webs = [] #学校官网
        locations = [] #地址
        phonenums = [] #电话号码
        schoolnames = [] #学校名

        school_infos = [] #学校的信息
        '''装结点'''
        rels_phonenum = []#学校名与电话号码关系
        rels_descs = [] #学校名与学校简介的关系
        rels_locations = [] #学校名与地址的关系
        rels_webs = []  # 学校名与学校官网的关系

        count=0
        for data in open(self.d_p,encoding='utf-8'):  # 遍历文件中的数据 按行取数据  data 就是每一行的数据
            school_dict = {}
            count += 1
            print (count)
            entry_json = json.loads(data)
            school = entry_json['name']  # 获取学校的名称
            school_dict['name'] = school# 将json里的学校名放字典里
            schoolnames.append(school)
            school_dict['desc'] = ''
            school_dict['location'] = ''
            school_dict['tel_num'] = ''
            school_dict['website'] = ''

            if 'tel' in entry_json:
                phonenums.append(entry_json['tel'])
                school_dict['tel_num'] = entry_json['tel']
                for pname in phonenums:  # 提取每一个校名
                    rels_phonenum.append([school,pname])

            if 'desc' in entry_json:
                descs.append(entry_json['desc'])
                school_dict['desc'] = entry_json['desc']
                for desc in descs:  # 提取每一个校名
                    rels_descs.append([school,desc])

            if 'loc' in entry_json:
                locations.append(entry_json['loc'])
                school_dict['location'] = entry_json['loc']
                for location in locations:  # 提取每一个校名
                    rels_locations.append([school,location])

            if 'web' in entry_json:
                webs.append(entry_json['web'])
                school_dict['website'] = entry_json['web']
                for web in webs:  # 提取每一个校名
                    rels_webs.append([school, web])

            school_infos.append(school_dict)
        return set(schoolnames),set(descs),set(locations),set(phonenums),set(webs),school_infos,\
               rels_descs,rels_locations,rels_phonenum,rels_webs

    '''建立节点'''
    def create_node(self,label,nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.gg.create(node)
            count += 1
            print(count, len(nodes))
        return

    def create_school_nodes(self, school_infos):
        count = 0
        for school_dict in school_infos:  # 取出每一个学校信息（字典）
             node = Node("school", schoolnames=school_dict['name'], desc=school_dict['desc'],
                         locations=school_dict['location'], phonenums=school_dict['tel_num'],
                            webs=school_dict['website'])  # 创建每一个学校结点
             self.gg.create(node)
             count += 1
             print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        schoolnames,descs,locations,phonenums,webs,school_infos, rels_descs,rels_phonenums,rels_locations,rels_webs= self.read_nodes()
        self.create_school_nodes(school_infos)
        self.create_node('学校名称',schoolnames)
        print(len(schoolnames))
        self.create_node('学校简介', descs)
        print(len(descs))
        self.create_node('学校地址', locations)
        print(len(locations))
        self.create_node('学校电话', phonenums)
        print(len(phonenums))
        self.create_node('学校官网', webs)
        print(len(webs))
        return
    '''创建实体关系边'''
    def create_graphrels(self):
        schoolnames,descs,locations,phonenums,webs,school_infos, rels_descs,rels_phonenums,rels_locations,rels_webs= self.read_nodes()
        self.create_relationship('school', '学校简介', rels_descs, 'basic_info', '简介')
        self.create_relationship('school', '学校电话', rels_phonenums, 'call', '联系电话')
        self.create_relationship('school', '学校地址', rels_locations, 'where', '在哪')
        self.create_relationship('school', '学校官网', rels_webs,'where_web','官网是什么')
    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
         # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.gg.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

        '''导出数据'''

    def export_data(self):
        schoolnames,descs,locations,phonenum,webs,school_infos, rels_webs,rels_phonenum,rels_descs,rels_locations = self.read_nodes()
        f_schoolnames = open('schoolnames.txt', 'w+')
        f_locations= open('locations.txt', 'w+')
        f_phonenums = open('phonenums.txt', 'w+')
        f_webs = open('webs.txt', 'w+')
        f_descs= open('descs.txt', 'w+')


        f_schoolnames.write('\n'.join(list(schoolnames)))
        f_locations.write('\n'.join(list(locations)))
        f_phonenums.write('\n'.join(list(phonenum)))
        f_webs.write('\n'.join(list(webs)))
        f_descs.write('\n'.join(list(descs)))

        f_schoolnames.close()
        f_locations.close()
        f_phonenums.close()
        f_webs.close()
        f_descs.close()
        return

if __name__ == '__main__':
    handler = Schoolgraph()
    handler.create_graphnodes()
    handler.create_graphrels()
