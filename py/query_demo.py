import requests
import urllib
import json
import pdb
solr_url = "http://localhost:8983/solr/"
solr_url = "http://thsh.servehttp.com:8983/solr/"


def make_query2(q_string,  **kwargs):
    q=""

    q_dict = dict(q=q_string, start=0, rows=10, indent="on", wt="json")
    q_dict.update(kwargs)

    return urllib.urlencode(q_dict)

def parse_response(resp_string):
    ab = json.loads(resp_string)['response']
    return ab

def query_play(q_string):
    url = solr_url+ "select/?" + make_query2(q_string)
    print "url     ", url
    r = requests.get(url)
    ab = r.text
    bc = ab.encode("utf-8")
    parsed = json.loads(bc)
    print "q_string ", q_string
    print "QTime    ", parsed['responseHeader']['QTime']
    print "params   ", parsed['responseHeader']['params']
    print "numFound ", parsed['response']['numFound']
    return parsed['response']['numFound']



class Phrase(object):
    def __init__(self, phrase, field="articlePlainText"):
        self.phrase = phrase
        self.field = field
    
    def to_query(self):
        return '''_query_:"%s:\\"%s\\""''' % (self.field, self.phrase)


class And(object):
    def __init__(self, *queries):
        self.queries = queries
    
    def to_query(self):
        sub_queries_as_strings = [q.to_query() for q in self.queries]
        return " AND ".join(sub_queries_as_strings)

class Or(object):
    def __init__(self, *queries):
        self.queries = queries
    
    def to_query(self):
        sub_queries_as_strings = [q.to_query() for q in self.queries]
        return " OR ".join(escaped_subqs)


def syntax_play():
    print "-"*80
    q_string = Phrase("american").to_query()
    print q_string
    query_play(q_string)

    print "-"*80
    q_string = Or(Phrase("american"),Phrase("samoa")).to_query()
    print q_string
    query_play(q_string)

    print "-"*80
    q_string = And(Phrase("american"),Phrase("samoa")).to_query()
    print q_string
    query_play(q_string)


#query_play(And(Phrase("cybernetics"), Phrase("Gordon Pask")).to_query())
#query_play(And(Phrase("Gordon Pask"), Phrase("cybernetics")).to_query())

def query_demo():

    qp = query_play
    american = qp('''articlePlainText:"american"''')

    american_no_quote = qp('''articlePlainText:american''')

    assert american == american_no_quote

    samoa = qp('''articlePlainText:samoa''')


    american_or_samoa = qp(
        '''articlePlainText:american OR _query_:"articlePlainText:samoa"''')

    american_and_samoa = qp(
        '''articlePlainText:american AND _query_:"articlePlainText:samoa"''')

    samoa_not_american =qp(
        '''articlePlainText:samoa NOT _query_:"articlePlainText:american"''')

    american_samoa_phrase = qp('''articlePlainText:"american samoa"''')

    assert american_or_samoa == (american + samoa_not_american)

    assert american_and_samoa >= american_samoa_phrase


    double_phrase_query = qp(
        '''articlePlainText:"american samoa" AND _query_:"articlePlainText:'manifest destiny'"''')

if __name__ == "__main__":
    #query_demo()
    pass

