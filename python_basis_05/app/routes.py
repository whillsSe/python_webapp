from flask import abort, redirect, render_template, request,session, url_for
from sqlalchemy import desc
from app import app,db
from app.models import User,Tag,Article
import hashlib
@app.route('/')
@app.route('/index')
def index():
    user_id = session.get('user_id')
    if user_id is not None:
        #自身以外の投稿かつ最新順かつトップ5を読み込む
        entries = db.session.query(Article).filter(Article.user_id != user_id).order_by(desc(Article.created_at)).limit(8)
        return render_template('home.html',entries=entries)
    else:
        return render_template('index.html')

@app.route('/register')
def show_regiter():
    return render_template('register.html',title="pb5_register")

@app.route('/register',methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['pass']
    username = request.form['username']
    user = User()
    user.email = email
    user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user.username = username

    db.session.add(user)
    db.session.commit()

    return render_template('register_succeed.html',title="pb5_register_succeed")

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        user = User.query.filter_by(email=email).first()
        if(user.password == hashlib.sha256(password.encode('utf-8')).hexdigest()):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', title="pb5_login",error=error)

@app.route('/drafts/new',methods=['GET','POST'])
def writeNewArticle():
    if request.method == 'GET':
        base=None
        return render_template('draft.html',base=base)
    elif request.method == 'POST':
        newArticle = Article()
        title = request.form['title']
        content = request.form['content']

        newArticle.title = title
        newArticle.content = content
        newArticle.user_id = session['user_id']

        tags_str = request.form['tags']
        tags_list = tags_str.split(',')

        for tag_str in tags_list[:5]:
            tag_str = tag_str.strip()
            tag = Tag.query.filter_by(tag=tag_str).first()
            if not tag:
                tag = Tag(tag=tag_str)
                db.session.add(tag)
            newArticle.tags.append(tag)

        db.session.add(newArticle)
        db.session.commit()
        return redirect(url_for('index'))
    
@app.route('/drafts/edit/<article_id>',methods=['GET','POST'])
def editArticle(article_id):
    article = Article.query.filter_by(id=article_id, user_id=session['user_id']).first()
    if request.method == 'GET':
        if article is None:
            abort(404)
        return render_template('draft.html',base=article)
    elif request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            title = request.form['title']
            content = request.form['content']

            tags_str = request.form['tags']
            tags_list = [tag.strip() for tag in tags_str.split(',')]

            # remove old tags that are not in the new list
            for tag in article.tags:
                if tag.tag not in tags_list:
                    article.tags.remove(tag)

            # add new tags from the list
            for tag_str in tags_list[:5]:
                tag = Tag.query.filter_by(tag=tag_str).first()
                if not tag:
                    tag = Tag(tag=tag_str)
                    db.session.add(tag)
                if tag not in article.tags:
                    article.tags.append(tag)
            
            article.title = title
            article.content = content
            db.session.commit()
            return redirect(url_for('index'))

@app.route('/article/<article_id>')
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    return render_template('article.html',article=article)