class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)


        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_school':
                sql = self.sql_transfer(question_type, entity_dict.get('school'))

            elif question_type == 'disease_locate':
                sql = self.sql_transfer(question_type, entity_dict.get('school'))

            elif question_type == 'disease_guanwang':
                sql = self.sql_transfer(question_type, entity_dict.get('school'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('school'))

            elif question_type == 'disease_phonenum':
                sql = self.sql_transfer(question_type, entity_dict.get('school'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)


        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        #13.查询某类节点下某属性为特定值的节点 match (n:person)where n.name=”alice” return n
        # 查询学校
        if question_type == 'disease_school':
            sql = ["match(n:school) where n.schoolnames='{0}' return n.schoolnames LIMIT 1".format(i) for i in entities]

        # 查询学校地址
        elif question_type == 'disease_locate':
            sql = ["match(n:school) where n.schoolnames='{0}' return n.locations LIMIT 1".format(i) for i in entities]

        # 查询学校官网
        elif question_type == 'disease_guanwang':
            sql = ["match(n:school) where n.schoolnames='{0}' return n.webs LIMIT 1".format(i) for i in entities]

        # 查询学校简介
        elif question_type == 'disease_desc':
            sql = ["match(n:school) where n.schoolnames='{0}' return n.desc LIMIT 1".format(i) for i in entities]

        # 查询学校电话
        elif question_type == 'disease_phonenum':
            sql = ["match(n:school) where n.schoolnames='{0}' return n.phonenums LIMIT 1".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
    res_sql = {'args': {'北京大学': ['school']}, 'question_types': ['disease_locate']}
    data = handler.parser_main(res_sql)
    print(data)


