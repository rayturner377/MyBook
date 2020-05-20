from datetime import date
from app import app, mysql
from flask import render_template, request, redirect, url_for, session
from app import generatedata
import random, datetime, csv
from .forms import searchbox, LoginForm

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        print("user is logged in")
        return redirect(url_for('dashboard'))
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        args = []
        args.append(username)
        args.append(password)
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.callproc('getUserDetails',args)
            account = cur.fetchall()

        # If account exists in accounts table in out database
        
        if account:
            account = account[0]
            print("\n\n",account)
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            print(session['id'], session['username'])
        
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', form= form)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    with app.app_context():
            args = []
            args.append(session['id'])
            cur = mysql.connection.cursor()
            cur.callproc('getUserPersonalPosts',args)
            postFeed = cur.fetchall()
    return render_template('dashboard.html', postFeed = postFeed)

@app.route('/comments/<postid>',methods=['GET','POST'])
def comments(postid):
    print(postid)
    with app.app_context():
        args = []
        args.append(postid)
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT commentid, firstname, lastname, commentdate, comment FROM comments JOIN profiles ON comments.userid = profiles.userid where comments.postid = %s", args)
        comment = cur.fetchall()
        resultValue = cur.execute("SELECT postid, postdate, firstname, lastname FROM posts JOIN profiles ON posts.userid = profiles.userid where posts.postid = %s", args)
        post = cur.fetchall()[0]
        resultValue = cur.execute("select posts.postid, photos.photoname, post_texts.caption from posts left join post_photos on posts.postid = post_photos.postid left join post_texts on posts.postid = post_texts.postid left join photos on post_photos.photoid = photos.photoid where posts.postid = %s", args)
        postbody = cur.fetchall()[0]
    return render_template('comments.html', comment= comment, postbody = postbody, post=post)

@app.route('/about2')
def about2():
    """Render the website's about page."""
    return render_template('about2.html')

@app.route('/profiler',methods=['GET','POST'])
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        with app.app_context():
            args = []
            args.append(session['id'])
            cur = mysql.connection.cursor()
            cur.callproc('userDetails',args)
            user = cur.fetchall()[0]
            print(user)
    return render_template('profile.html', user=user )

@app.route('/friends',methods=['GET','POST'])
def friends():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        with app.app_context():
            args = []
            args.append(session['id'])
            cur = mysql.connection.cursor()
            cur.callproc('getUserFriends',args)
            friends = cur.fetchall()
            print(friends)
    return render_template('friends.html', friends=friends )

@app.route('/usergroups',methods=['GET','POST'])
def usergroups():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        with app.app_context():
            args = []
            userid = session['id']
            args.append(session['id'])
            cur = mysql.connection.cursor()
            cur.callproc('getGroups',args)
            groups = cur.fetchall()
            print(groups)
    return render_template('usergroups.html', groups=groups )


@app.route('/usergroupdetails/<groupid>',methods=['GET','POST'])
def userGroupDetails(groupid):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        with app.app_context():
            args = []
            userid = session['id']
            args.append(groupid)
            cur = mysql.connection.cursor()
            resultValue = cur.execute("select posts.postid, posts.postdate, firstname, lastname from posts join group_posts on group_posts.postid = posts.postid join profiles on posts.userid = profiles.userid where groupid = %s", args)
            posts = cur.fetchall()
            print(posts)
    return render_template('userGroupDetails.html', posts=posts )

@app.route('/grouppostdetails/<postid>',methods=['GET','POST'])
def groupPostDetail(postid):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        with app.app_context():
            args = []
            args.append(postid)
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT commentid, firstname, lastname, commentdate, comment FROM comments JOIN profiles ON comments.userid = profiles.userid where comments.postid = %s", args)
            comment = cur.fetchall()
            resultValue = cur.execute("SELECT postid, postdate, firstname, lastname FROM posts JOIN profiles ON posts.userid = profiles.userid where posts.postid = %s", args)
            post = cur.fetchall()[0]
            resultValue = cur.execute("select posts.postid, photos.photoname, post_texts.caption from posts left join post_photos on posts.postid = post_photos.postid left join post_texts on posts.postid = post_texts.postid left join photos on post_photos.photoid = photos.photoid where posts.postid = %s", args)
            postbody = cur.fetchall()[0]
    return render_template('groupPostDetails.html', comment= comment, postbody = postbody, post=post)


@app.route("/logout")
def logout():
    # Logout the user and end the session
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))



#admin section
############################################################

@app.route('/admin')
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

@app.route('/about')
def about():
            
    return render_template("about2.html")


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

            cur.execute("select messageid, receiver, firstname, lastname, messagedate, messagestring from messages join profiles on receiver = profiles.userid where sender = %s",args)
            sentMessages = cur.fetchall()
            cur.execute("select messageid, sender, firstname, lastname, messagedate, messagestring from messages join profiles on receiver = profiles.userid where receiver = %s",args)
            receivedMessages = cur.fetchall()
            gt, pt, ft = len(groups) , len(posts) , len(friends)
            
        return render_template('userDetails.html',user=user,posts = posts, friends = friends, groups = groups, pt=pt,gt=gt,ft=ft,sentMessages= sentMessages, receivedMessages=receivedMessages)
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

        resultValue = cur.execute("select posts.postid, posts.postdate, firstname, lastname from posts join group_posts on group_posts.postid = posts.postid join profiles on posts.userid = profiles.userid where groupid = %s", args)
        posts = cur.fetchall()
        
        resultValue = cur.execute("select editorid, firstname, lastname from editors join profiles on editorid = profiles.userid join groups on groups.groupid = editors.groupid where editors.groupid = %s", args)
        editors = cur.fetchall()
        print(editors)
        return render_template('groupDetails.html',group=group,males = males, females = females, total = males+females, members = members,posts=posts, editors = editors)
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

        resultValue = cur.execute("select posts.postid, photos.photoname, post_texts.caption from posts left join post_photos on posts.postid = post_photos.postid left join post_texts on posts.postid = post_texts.postid left join photos on post_photos.photoid = photos.photoid where posts.postid = %s", args)
        postbody = cur.fetchall()
        postbody = postbody[0]
        return render_template('postDetails.html',post = post, comments = comments, total_comments = len(comments), postbody=postbody)
    return render_template('posts.html')

generatedata.populate()



###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404



