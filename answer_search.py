from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.gg = Graph("http://localhost:7474", username="neo4j", password="z5896347")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.gg.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_school':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_locate':
            subject = answers[0]['n.locations']
            final_answer = '它的地址在：{0}'.format(subject)

        elif question_type == 'disease_guanwang':
            subject = answers[0]['n.webs']
            final_answer = '它的官网是：{0}'.format(subject)

        elif question_type == 'disease_desc':
            subject = answers[0]['n.desc']
            final_answer = '简介：{0}'.format(subject)

        elif question_type == 'disease_phonenum':
            subject = answers[0]['n.phonenums']
            final_answer = '它的联系电话是：{0}'.format(subject)

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    res_sql = [{'question_type': 'disease_locate', 'sql': ["MATCH (n:school) where n.schoolnames='北京大学' return n.locations LIMIT 1"]}]
    data = searcher.search_main(res_sql)
    print(data)