from datetime import date
from app import app, mysql
from flask import render_template, request, redirect, url_for
from app import generatedata
import random, datetime, csv
from flask_wtf import FlaskForm
from wtforms import StringField

class searchbox(FlaskForm):
    item = StringField('item')


@app.route('/')
def home():
    with app.app_context():
            cur = mysql.connection.cursor()     
            cur.execute("SELECT COUNT(posts.postid) FROM posts")
            total_posts = cur.fetchall()
            cur.execute("SELECT COUNT(groups.groupid) FROM groups")
            total_groups = cur.fetchall()
            cur.execute("SELECT COUNT(users.userid) FROM users")
            total_users = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            
    return render_template("index.html", total_users=total_users[0][0], total_posts=total_posts[0][0],total_groups=total_groups[0][0])


@app.route('/users', methods = ["GET","POST"])
def users():
    form = searchbox()
    if request.method == "POST":
        return userdetails(form.item.data)
    elif request.method == "GET":
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.callproc('getAllUsers')
            user_list = cur.fetchall()
    return render_template("users.html",form = form, user_list=user_list)

@app.route('/users/<userid>', methods=['GET','POST'])
def userdetails(userid):
    with app.app_context():
        cur = mysql.connection.cursor()
        args = []
        args.append(userid)
        cur.callproc('userDetails',args)
        user = cur.fetchall()
    if user:
        user = user[0]
        posts, groups, friends, gt, pt, ft = [0],[0],[0],0,0,0
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.callproc('getFriends',args)
            friends = cur.fetchall()
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.callproc('getGroups',args)
            groups = cur.fetchall()
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.callproc('getPosts',args)
            posts = cur.fetchall()
        gt, pt, ft = len(groups) , len(posts) , len(friends)
        print(len(groups))
        return render_template('userDetails.html',user=user,posts = posts, friends = friends, groups = groups, pt=pt,gt=gt,ft=ft )
    return render_template('users.html')

@app.route('/groups', methods=['GET','POST'])
def groups():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT groupid, groupname,  profiles.firstname,profiles.lastname FROM groups join profiles on groups.creator = profiles.userid")
    if resultValue >0:
        groups = cur.fetchall()
        print(groups[0])
        return render_template('groups.html', group_list = groups)

@app.route('/groups/<groupid>', methods=['GET','POST'])
def groupdetails(groupid):
    with app.app_context():
        args=[groupid]
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT groupid, groupname, date_created, profiles.firstname,profiles.lastname FROM groups join profiles on groups.creator = profiles.userid where groups.groupid = %s",args)
        group = cur.fetchall()

        resultValue = cur.execute("select count(memberid) from members join profiles on memberid = profiles.userid join groups on members.groupid = groups.groupid where profiles.gender = 'female' and members.groupid = %s",args)
        females = cur.fetchall()[0][0]

        resultValue = cur.execute("select count(memberid) from members join profiles on memberid = profiles.userid join groups on members.groupid = groups.groupid where profiles.gender = 'male' and members.groupid = %s",args)
        males = cur.fetchall()[0][0]

        resultValue = cur.execute("select members.memberid, profiles.firstname, profiles.lastname, groups.groupname from members join profiles on members.memberid = profiles.userid join groups on groups.groupid = members.groupid where members.groupid = %s", args)
        members = cur.fetchall()
        group = group[0]
        return render_template('groupDetails.html',group=group,males = males, females = females, total = males+females, members = members)
    return render_template('groups.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT postid, postdate, firstname, lastname FROM posts JOIN profiles ON posts.userid = profiles.userid")
    if resultValue >0:
        posts = cur.fetchall()
        return render_template('posts.html', post_list = posts)
    
@app.route('/posts/<postid>', methods=['GET','POST'])
def postdetails(postid):
    with app.app_context():
        cur = mysql.connection.cursor()
        args=[postid]
        resultValue = cur.execute("SELECT postid, postdate, firstname, lastname FROM posts JOIN profiles ON posts.userid = profiles.userid where posts.postid = %s", args)
        post = cur.fetchall()[0]
    with app.app_context():
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT commentid, firstname, lastname, commentdate, comment FROM comments JOIN profiles ON comments.userid = profiles.userid where comments.postid = %s", args)
        comments = cur.fetchall()
        print(comments)
        return render_template('postDetails.html',post = post, comments = comments)
    return render_template('posts.html')

generatedata.populate()

