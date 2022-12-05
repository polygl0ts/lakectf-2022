from flask import Blueprint, abort, escape
from flask import flash, render_template, redirect, url_for, request
import os
from . import db, limiter, q
from .models import Post
from .bot import visit
import codecs
import ipaddress
import time
import uuid
import unicodedata
import re
import time
import random

adminToken = os.environ["adminToken"]

main = Blueprint('main', __name__)


@main.before_app_first_request
def setup_lore():
    welcome = Post(post_id=str(uuid.uuid4()),
                author="pilvar",
                title="Welcome! :D",
                body="Thanks for visiting my forum! I hope you have fun there :)",
                deleted="False",
                ts="1666285716")
    db.session.add(welcome)
    leaked_flag = Post(post_id=str(uuid.uuid4()),
                    author="sam.ninja",
                    title="Nice forum you got there pilvar!",
                    body="I was wondering about the flag tho, I think that \""+os.environ["FLAG"]+"\" is a bit inappropriate for a very serious and professional team like polygl0ts. I'm sure you could find a better idea!",
                    deleted="True",
                    ts="1666288821")
    db.session.add(leaked_flag)
    db.session.commit()

@main.route('/')
def index():
    try:
      page = request.args.get('page')
      if page:
        page = int(page)
      else:
        page = 1
      posts = []
      query = request.args.get('query')
      if query:
        time.sleep(random.random()/2) #my friend told me about "security through inconsistency", no idea what it means, but he told me to add this here!
        antiReDOS = re.compile("[a-zA-Z0-9 .|]+") #regex DOS? Not on MY forum!
        if re.fullmatch(antiReDOS, query) and len(query) < 200:
          query = ".*"+query+".*"
          for post in Post.query.all():
            if post.deleted == "False" or request.cookies.get('adminToken') == adminToken:
              if re.match(query, post.body) or re.match(query, post.title) or re.match(query, post.author):
                posts.append(post)
      else:
        for post in Post.query.all():
          if post.deleted == "False" or request.cookies.get('adminToken') == adminToken:
            posts.append(post)
      posts = sorted(posts, key=lambda d: int(d.ts))
      posts.reverse()
      npages = 1
      if len(posts) == 0:
        return render_template('homepage.html')
      if len(posts) > 10:
        npages = 1+((len(posts)-1)//10)
      posts = posts[10*(page-1):10*page]
      if len(posts) == 0:
        return redirect("/")
      pages = [page for page in range(1,npages+1)]
      return render_template('homepage.html', posts=posts, pages=pages)
    except Exception as e:
        return {"error":str(e)}


@main.route('/new_post', methods=['POST'])
@limiter.limit("50/minute") #This rate-limit will apply to all teams because you're all sharing the same public ip, please don't spam my forum!
def new_post():
  try:
    username = escape(request.form.get('username'))
    title = escape(request.form.get('title'))
    body = escape(request.form.get('body'))
    body = body.replace("\\n","\n")
    if "EPFL" in body or "EPFL" in title or "EPFL" in username:
        abort(403) #We had a case where a user leaked the flag from our CTF, we don't want this to happen again!!
    if len(username) > 32 or len(title) > 64 or len(body) > 4096:
        return {"error":"No flooding plz"}
    id = str(uuid.uuid4()) #I learnt to never let the user control the ID, I already lost 7 clob-mates because of this! >.>
    new_post = Post(post_id=id,
                    author=username,
                    title=title,
                    body=body,
                    deleted="False",
                    ts=str(int(time.time()))) #I love python.
    db.session.add(new_post)
    db.session.commit()
    return redirect("/"+id)
  except Exception as e:
    return(str(e))

@main.route('/report', methods=['POST'])
@limiter.limit("8/minute") #This rate-limit will apply to all teams because you're all sharing the same public ip, you shouldn't need more than 1 report/minute!
def report():
    try:
        path = request.form.get('path')
        if "." in path:  #I learnt ppl could inject an arbitrary URL using @ or ., but they can't send a valid url using . so here's the fix!
            return {"success":False,"message":"plz no hack"}
        path = unicodedata.normalize("NFKD", path).encode('ascii','ignore').decode('ascii') #UPDATE: just learnt about unicode, now it should be good.
        if "." in path:
            return {"success":False,"message":"plz no hack!"}
        if "[" in path or "]" in path: #UPDATE 2: ipv6 now!? wtf is even this!?!!?! Urls are so weird man...
            return {"success":False,"message":"plz no hack!!"}
        post_id = path[-36:]
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return {"success":False,"message":"There's no such post!"}
        if post.deleted == "True":
            return {"success":False,"message":"The post has already been deleted."}
        else:
            q.enqueue(visit, path)
            return {"success":True,"message":"Post succesfully reported"}
    except Exception as e:
        return {"success":False,"message":str(e)}

@main.route('/delete', methods=['POST'])
def delete():
    if request.cookies.get('adminToken') == adminToken and request.headers.get('Origin').startswith("http://web:8080/"): # this should prevent CSRF, right?
      try:
        post = request.form.get('post')
        Post.query.filter_by(post_id=post).update({
        'deleted': "True"
        })
      except Exception as e:
        return {"success":"false","error":str(e)}
    return redirect("/")

@main.route('/<post_id>')
def see_post(post_id=None):
    post = Post.query.filter_by(post_id=post_id).first()
    if post.deleted == "False" or request.cookies.get('adminToken') == adminToken:
      return render_template('post.html', post=post)
    else:
      return "Post deleted, or does not exist"