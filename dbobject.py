import sqlite3
from random import shuffle

db = sqlite3.connect('ark.db')
##Fetchib andmebaasist andmed sõnastikuna
db.row_factory = sqlite3.Row

class DatabaseObject:
    '''Laiendab Question ja Answer klassi'''
    
    def __init__(self, properties):
        '''Muudab andmebaasist saadud sõnastiku objekti muutujateks
        nt siis saab küsimuse id poole pöörduda question.id'''
        self.__dict__.update(properties)
    
    @classmethod
    def findByID(caller, ID):
        query='SELECT * FROM {} WHERE id={} LIMIT 1'.format(caller.tableName, ID)
        return caller.findBySQL(query)[0]
    
    @classmethod
    def findAll(caller, addSQL=''):
        query='SELECT * FROM {} {}'.format(caller.tableName, addSQL)
        return caller.findBySQL(query)
        
    @classmethod
    def findBySQL(caller, query):
        results=list()
        cursor = db.execute(query)
        for row in cursor: results.append(caller(dict(row)))
        return results

class Question(DatabaseObject):
    tableName='questions'

    @classmethod
    def nullStats(self):
        '''Nullib kõigi küsimuste statistika'''
        query = "UPDATE {} SET tries=0, correct=0".format(self.tableName)
        db.execute(query)
        db.commit()
        
    @classmethod
    def getNextN(self,n):
        '''Leiab andmebaasist järgmised n küsimust sorteerib õigesti vastamise
        protsendi järgi'''
        a=self.findAll('ORDER BY correct/tries ASC LIMIT {}'.format(n*2))
        shuffle(a)
        return a[:n]

        
    def __getattribute__(self, var):
        '''Tagastab objekti muutuja, kui päritakse protsenti, arvutab kohapeal välja'''
        if var=='percentage':
            return round(self.correct/self.tries, 2) if self.tries!=0 else 0
        else:
            return DatabaseObject.__getattribute__(self, var)

    def getAnswers(self):
        '''Tagastab küsimuse vastused objektide listina'''
        return Answer.findAll('WHERE question_id={}'.format(self.id))

    def update(self):
        '''Uuendab küsimuse vastamiste ja õigesti vastamiste arvu'''
        query = "UPDATE questions SET tries={}, correct={} WHERE id={}".format(self.tries, self.correct, self.id)
        db.execute(query)
        db.commit()
        
class Answer(DatabaseObject):
    tableName='answers'


    
