# -*- coding: utf-8 -*-
from app import app
import getQuestion
import user

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os, json
from flask import Flask, session, render_template, url_for, redirect, request, flash
app.secret_key = os.urandom(24)

yanzhengti, yztdaan = (u"你最喜欢的人是？  (这是一道验证题，为了验证你有答题的资格) ", u"王八蛋")

def update_question():
    global questions
    questions  = []
    query = "select title,A,B,C,D,answer from choice_question"
    rv = getQuestion.jimo(query)
    for num, itemq in enumerate(rv):
        questions.append( {"type": "xuanze", "question" : itemq[0], "answer" : itemq[-1], "xuanzetilist": itemq[1:5]} )
    query = "select title,true_or_false from true_or_false_question"
    rv = getQuestion.jimo(query)
    for num, itemq in enumerate(rv):
        questions.append( {"type": "panduan", "question" : itemq[0], "answer" : itemq[1] } )
    query = "select title,answer from fill"
    rv = getQuestion.jimo(query)
    for num, itemq in enumerate(rv):
        questions.append( {"type": "tiankong", "question" : itemq[0], "answer" : itemq[1] } )
    #print questions
    return

def render_success( sessionScore, failn ):
    try:
        a, b, c = str(sessionScore).zfill(3)
    except:
        a, b, c = '999'
    return render_template("success.html", hund=a, deca=b, unit=c, failnum=failn)

@app.route('/', methods=['GET', 'POST'])
def index():
    tfs = {"xuanze":"xuanzeti.html", "panduan":"panduanti.html", "tiankong":"quiz.html"}
    update_question()
    xuanzetixuanxiang = ''
    if "current_question" not in session:
        session["current_question"] = -1
    if "score" not in session:
        session["score"] = 0
        session["scuccnum"] = 0

    cq = session["current_question"]
    if 0 <= cq < len(questions):
        qtype = questions[cq]["type"]
        #print "qtype", qtype
        if qtype == "xuanze":
            xuanzetilist = questions[cq]["xuanzetilist"]
            xuanzetixuanxiang = repr(list(xuanzetilist))
    if request.method == "POST" and cq < len(questions):
        try:
            if cq == -1:
                entered_answer = request.form.get("answer", '')
            elif qtype == "xuanze":
                entered_answer = json.loads(list(request.form)[0])[0]["id"]
                #print "entered_answer", entered_answer
                #print "xuanzetilist", xuanzetilist
                entered_answer = "ABCD"[xuanzetilist.index(entered_answer)]
                #print "xuanzetixuanxiang, entered_answer", xuanzetixuanxiang, entered_answer
                #print "realan", questions[session["current_question"]]["answer"]
            elif qtype == "panduan":
                entered_answer = list(request.form)[0]
                entered_answer = {"true": "1", "false": "0"}[entered_answer]
                #print entered_answer
            elif qtype == "tiankong":
                entered_answer = request.form.get("answer", '')
        except:
            entered_answer = ""
        #print entered_answer

        if not entered_answer:
            flash(u"请输入一个答案！", "error")
        elif session["current_question"] == -1:
            if yztdaan == entered_answer:
                session["current_question"] = 0
            else:
                flash(u"答案错误！思想觉悟不高，你不是人类吗？", "error")
        elif entered_answer != questions[session["current_question"]]["answer"]:
            session["current_question"] += 1# next
            flash(u"回答错误！下一题", "error")
        else:
            session["current_question"] += 1
            session["score"] += 1
            session["scuccnum"] += 1
            flash(u"恭喜，答对了！下一题", "right")

    cq = session["current_question"]
    if 0 <= cq < len(questions):
        qtype = questions[cq]["type"]
        #print "qtype", qtype
        if qtype == "xuanze":
            xuanzetilist = questions[cq]["xuanzetilist"]
            xuanzetixuanxiang = repr(list(xuanzetilist))
    #print 'cq, lenques', cq, len(questions)
    if cq >= len(questions):
        return render_success( sessionScore=session["score"], failn=len(questions)-session["scuccnum"] )
    #print "Current", questions[cq]["question"] , xuanzetixuanxiang
    tf = tfs[questions[cq]["type"]] if cq != -1 else "quiz.html"
    #print "xuanzetilist", xuanzetixuanxiang
    return render_template(
        tf,
        question=questions[cq]["question"] if cq != -1 else yanzhengti,
        question_number=cq+1 if cq != -1 else -1,
        xuanzetixuanxiang = xuanzetixuanxiang.replace("u'", "'").replace('u"', '"'),
        quesnum=len(questions) if cq != -1 else u"1，微电，版图设计"
                          )

@app.route('/addqc', methods=['GET', 'POST'])
def add_questions1():
    if request.method == 'GET':
        return render_template('add_cques.html')
    if request.method == 'POST':
        title, score, A, B, C, D, answer = request.form['title'], request.form['score'], request.form['A'], request.form['B'], request.form['C'], request.form['D'], request.form['answer']
        print title, score, A, B, C, D, answer
        getQuestion.addqc(title=title, score=score, A=A, B=B, C=C, D=D, answer=answer)
        return render_template('add_cques.html', success=True)

@app.route('/addqt', methods=['GET', 'POST'])
def add_questions2():
    if request.method == 'GET':
        return render_template('add_tques.html')
    if request.method == 'POST':
        title, score, true_or_false = request.form['title'], request.form['score'], request.form['true_or_false']
        print title, score, true_or_false
        getQuestion.addqt(title=title, score=score, true_or_false=true_or_false)
        return render_template('add_tques.html', success=True)

@app.route('/addqtk', methods=['GET', 'POST'])
def add_questions3():
    if request.method == 'GET':
        return render_template('add_tkques.html')
    if request.method == 'POST':
        title, score, answer = request.form['title'], request.form['score'], request.form['answer']
        print title, score, answer
        getQuestion.addqtk(title=title, score=score, answer=answer)
        return render_template('add_tkques.html', success=True)

'''
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        if request.form['username']:
            if user.login(request.form['username'], request.form['password']):
                return user_dash_view()
            else:
                return render_template("index.html", error=True)
        else:
            return 'Fail'


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if request.form['password'] != request.form['password-repeat']:
            return render_template('register.html', error='passwords are not same')
        else:
            if user.register(request.form['username'], request.form['password']):
                return 'success'
            else:
                return render_template('register.html', error='the username has been registered')

'''

@app.route('/user_dash', methods=['GET', 'POST'])
def user_dash_view():
    data = user.rank()
    if request.method == 'GET':
        return render_template('user_dashboard.html', users=data)
    if request.method == 'POST':
        return render_template('user_dashboard.html', users=data)


@app.route('/question/<int:kind>', methods=['GET', 'POST'])
def question(kind):
    data = getQuestion.get_question('%d' % kind)
    print data
    if request.method == 'GET':
        return render_template('question_list.html', question_kind='题目' + '%d' % kind, questions=data, kind=kind)


@app.route('/question/id/<int:id>', methods=['GET', 'POST'])
def show_questions(id):
    data = getQuestion.get_question('', False, '%d' % id)
    if request.method == 'GET':
        return render_template('add_cques.html', question_title=data[0], question_content=data[1], kind=data[3])
    if request.method == 'POST':
        if user.login(request.form['username'], request.form['password']):
            if data[2] != unicode(request.form['answer']):
                return render_template('question.html', question_title=data[0], question_content=data[1], kind=data[3], error=True)
            else:
                user.add_score(request.form['username'], data[4])
                return render_template('question.html', question_title=data[0], question_content=data[1], kind=data[3], success=True)
        else:
            return render_template('question.html', question_title=data[0], question_content=data[1], kind=data[3], loginError=True)
