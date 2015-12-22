import sqlite3_db
import string


def get_question(kind):
    query = 'select title,score from choice_question order by score desc'
    cur = sqlite3_db.connect_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

def jimo(query):
    #query = 'select title,score from choice_question order by score desc'
    cur = sqlite3_db.connect_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

def addqc(title, score, A, B, C, D, answer):
    query = "insert into choice_question(title, score, A, B, C, D, answer)values ('{title}', {score}, '{A}', '{B}', '{C}', '{D}', '{answer}')".format(title=title, score=score, A=A, B=B, C=C, D=D, answer=answer)
    print query
    t = sqlite3_db.connect_db()
    cur = t.execute(query)
    rv = cur.fetchall()
    t.commit()
    cur.close()
    return rv

def addqt(title, score, true_or_false):
    query = "insert into true_or_false_question(title, score, true_or_false)values ('{title}', {score}, '{true_or_false}')".format(title=title, score=score, true_or_false=true_or_false)
    print query
    t = sqlite3_db.connect_db()
    cur = t.execute(query)
    rv = cur.fetchall()
    t.commit()
    cur.close()
    return rv

def addqtk(title, score, answer):
    query = "insert into fill(title, score, answer)values ('{title}', {score}, '{answer}')".format(title=title, score=score, answer=answer)
    print query
    t = sqlite3_db.connect_db()
    cur = t.execute(query)
    rv = cur.fetchall()
    t.commit()
    cur.close()
    return rv
