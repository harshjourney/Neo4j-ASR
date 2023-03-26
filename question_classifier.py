import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.desc_path = os.path.join(cur_dir, 'D:/Python/python 3.6/ASR/期末/qmrw/prepare_data/dict/desc.txt')
        self.guanwang_path = os.path.join(cur_dir, 'D:/Python/python 3.6/ASR/期末/qmrw/prepare_data/dict/guanwang.txt')
        self.locate_path = os.path.join(cur_dir, 'D:/Python/python 3.6/ASR/期末/qmrw/prepare_data/dict/locate.txt')
        self.phonenum_path = os.path.join(cur_dir, 'D:/Python/python 3.6/ASR/期末/qmrw/prepare_data/dict/phonenum.txt')
        self.school_path = os.path.join(cur_dir, 'D:/Python/python 3.6/ASR/期末/qmrw/prepare_data/dict/school.txt')
        #self.yuanxi_path = os.path.join(cur_dir, 'E:/NEO4J/kaoyan/kaoyan/dict/yuanxi.txt')
        #self.province_path = os.path.join(cur_dir, 'E:/NEO4J/kaoyan/kaoyan/dict/province.txt')
        #self.major_path = os.path.join(cur_dir, 'E:/NEO4J/kaoyan/kaoyan/dict/major.txt')
        # 加载特征词
        self.desc_wds= [i.strip() for i in open(self.desc_path,encoding="utf-8") if i.strip()]#encoding="utf-8"
        self.guanwang_wds= [i.strip() for i in open(self.guanwang_path,encoding="utf-8") if i.strip()]
        self.locate_wds= [i.strip() for i in open(self.locate_path,encoding="utf-8") if i.strip()]
        self.phonenum_wds= [i.strip() for i in open(self.phonenum_path,encoding="utf-8") if i.strip()]
        self.school_wds= [i.strip() for i in open(self.school_path,encoding="utf-8") if i.strip()]
        #self.yuanxi_wds = [i.strip() for i in open(self.yuanxi_path, encoding="utf-8") if i.strip()]
        #self.major_wds= [i.strip() for i in open(self.major_path,encoding="utf-8") if i.strip()]
        #self.province_wds= [i.strip() for i in open(self.province_path,encoding="utf-8") if i.strip()]
        self.region_words = set(self.school_wds + self.guanwang_wds + self.locate_wds + self.phonenum_wds + self.desc_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.school_qwds = ['哪所']
        self.locate_qwds = ['在哪','哪里','什么地方','怎么去','怎么走','地址']
        self.phonenum_qwds = ['电话','号码','联络','联系']
        self.guanwang_qwds = ['官网','网址','网页']
        self.desc_qwds = ['简介','介绍']
        #self.major_qwds = ['专业']
        #self.province_qwds = ['省','在哪个省']
        #self.yuanxi_qwds = ['院系','属于','什么院']

        '''self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']'''

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        school_dict = self.check_medical(question)
        if not school_dict:                            #school——dict为空
            return {}
        data['args'] = school_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in school_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        #学校
        if self.check_words(self.school_qwds, question) and ('school' in types):
            question_type = 'disease_school'
            question_types.append(question_type)

        #地址
        if self.check_words(self.locate_qwds, question) and 'school' in types:
            question_type = 'disease_locate'
            question_types.append(question_type)


        # 官网
        if self.check_words(self.guanwang_qwds, question) and 'school' in types:
            question_type = 'disease_guanwang'
            question_types.append(question_type)

        #简介
        if self.check_words(self.desc_qwds, question) and 'school' in types:
            question_type = 'disease_desc'
            question_types.append(question_type)

        #联系电话
        if self.check_words(self.phonenum_qwds, question) and 'school' in types:
            question_type = 'disease_phonenum'
            question_types.append(question_type)

        '''#专业
        if self.check_words(self.major_qwds, question) and ('disease' in types):
            question_type = 'disease_major'
            question_types.append(question_type)

        # 省份
        if self.check_words(self.province_qwds, question) and ('disease' in types):
            question_type = 'disease_province'
            question_types.append(question_type)

        # 院系
        if self.check_words(self.yuanxi_qwds, question) and 'disease' in types:
            question_type = 'disease_yuanxi'
            question_types.append(question_type)'''
        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'school' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'school' in types:
            question_types = ['symptom_disease']
        #print(question_types)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.desc_wds:
                wd_dict[wd].append('desc')
            if wd in self.guanwang_wds:
                wd_dict[wd].append('guanwang')
            if wd in self.locate_wds:
                wd_dict[wd].append('locate')
            if wd in self.phonenum_wds:
                wd_dict[wd].append('phonenum')
            if wd in self.school_wds:
                wd_dict[wd].append('school')
            '''if wd in self.province_wds:
                wd_dict[wd].append('province')
            if wd in self.major_wds:
                wd_dict[wd].append('major')'''
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    question = '北京大学在哪'
    data = handler.classify(question)
    print(data)