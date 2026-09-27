#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    
    # initialize the session for page views
    session['page_views'] = session.get('page_views') or 0
    
    # increment the session on each request
    session['page_views'] += 1
    
    # send a response based on session data
    if session['page_views'] <= 3:
        # Look up the single article whose id matches the id in the URL
        article = Article.query.filter(Article.id == id).first()
        # Convert the Article object to a dictionary and send it as JSON with 200 OK
        return make_response(ArticleSchema().dump(article), 200)
    # Over 3, send an error message with 401 code
    return make_response({'message': 'Maximum pageview limit reached'}, 401)


if __name__ == '__main__':
    app.run(port=5555)
