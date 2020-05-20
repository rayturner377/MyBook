import random, csv, datetime
from os import listdir
from app import app, mysql
from os.path import isfile, join
from faker.providers.person.en import Provider
from itertools import product
from faker import Faker  

def generate_users():
    faker = Faker()
    #---------Creating Unique Users-----------------
    # getting Unique female and male first names
    male = list(set(Provider.first_names_male))[:710]
    female = list(set(Provider.first_names_female) - set(male))[:710]
 
    #getting unique last names
    last_name = list(set(Provider.last_names))[:710]

    #Associating Lastname with first name
    female = list(set(["{} {}".format(f, l) for f, l in product(female, last_name) if f != l]))
    male = list(set(["{} {}".format(f, l) for f, l in product(male, last_name) if f != l]))
    #shuffling lists
    random.shuffle(female)
    random.shuffle(male)
    #seperating name into first and last name
    female = [f.split(" ") for f in female]
    male = [m.split(" ") for m in male]
    #----------------------------------------------------

    
    #---------Used to generate Random Password------------
    #characters to use in password
    characters = [x for x in range(48,57)] + [x for x in range(65,91)] +  [x for x in range(97,123)]+[33,35,36,37,64]
    #Function to generate password
    def getPass(x=8):
        if x == 0:
            return ''
        else:
            return chr(characters[random.randint(0,len(characters)-1)]) + getPass(x-1)
    #----------------------------------------------------
     #-------Creating Date of Birth-----------------
    #Start date for random DOB
    start = datetime.date(1970, 1, 1)
    #Function to create DOB
    def getDOB():
        return str(start + datetime.timedelta(days=random.randint(1,12775)))
    #----------------------------------------------------
    #----------------------------------------------------
     #-------Creating Date Registered-----------------
    #Start date
    startDate = datetime.date(2019, 1, 1)
    #Function to create Registered Function
    def registered():
        return str(startDate + datetime.timedelta(days=random.randint(1,485)))
    #----------------------------------------------------
    #------Creating Email--------------------------
    #email provider
    def getEmail(fname,lname):
        extensions = ["@google.com","@yahoo.com","@icloud.com","@live.com"]
        server = extensions[random.randint(0,3)]
        return fname+lname+server
    #----------------------------------------------------
    def biography():
        bio =["I am a user", "I love to dance","Reading is my hobby","I like cars","socialmedia is my 2nd love","Drama and entertainment"]
        return bio[random.randint(0,len(bio)-1)]


    #creating Female Users
    female = [ [f[0], f[1] ,"female" , getDOB(), getEmail(f[0],f[1]), getPass(), registered(),biography()] for f in female ]
    #creating Male Users
    male = [ [m[0], m[1] ,"male" , getDOB(), getEmail(m[0],m[1]), getPass(), registered(), biography() ] for m in male ]
    #----------------------------------------------------
    
    all_users = female + male
    random.shuffle(all_users)

    usercsv= csv.writer(open('users.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    profilecsv= csv.writer(open('profiles.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    userlogincsv = csv.writer(open('userlogin.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    pic = 1
    for u in all_users[:8000]:
        prof = [u[0],u[1],u[3],u[2],u[7],pic]
        ux = [u[6]]
        ul = [u[4],u[5]]
        usercsv.writerow(ux)
        profilecsv.writerow(prof)
        userlogincsv.writerow(ul)
        pic+=1
    

    print("done")
    #########################################################################################

def generate_friends():
    '''
    User with smaller user ID goes first
    '''
    def swap(a,b):
        if b<a:
            return (b,a)
        return (a,b)

    '''
    create a list of friend tuples eg, (uid =1, uid=30)
    '''
    with open('users.csv', newline='') as f:
        numusers = len(list(csv.reader(f)))

    def userList(lst):
        ulist = []
        #each user has a max of 300 friends
        maxfriends = 100
        #set number of users to assign random friends to
        assignTo = len(lst) // 10
        for user in lst[:assignTo]:
            friendsnumber = random.choice(lst[:maxfriends])
            for x in range(friendsnumber):
                friend = random.choice(lst)
                if friend == user:
                    x-=1
                else:
                    ulist.append(swap(user,friend))
        return(ulist)

    #request section

    def assignStat_Sender_Type(friends):
        nlst =[]
        groups = ["Relatives","School","Work"]
        for f in friends:
            sender = f[random.randint(0,1)]
            group = groups[random.randint(0,2)]
            status = 0
            s = random.randint(1,10)
            if(s>7):
                status = 1
            nlst.append((f[0],f[1],status,sender,group))
        return nlst


    def generateFriends(users):
        users = [x for x in range(1,users+1)]
        friends = userList(users)
        #remove duplicates
        friends_min = set(friends)
        friends_min=list(friends_min)
        friends_min.sort()
        
        return assignStat_Sender_Type(friends_min)


    def allFriends(users):
        relations = generateFriends(users)

        f= csv.writer(open('friends.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for _list in relations:
            f.writerow(_list)
    
    allFriends(numusers)

##########################################################################################

def generate_groups():
    def dateCreated():
        start = datetime.date(2020, 1, 1)
        return str(start + datetime.timedelta(days=random.randint(1,120)))

    groupNames = ["myfamily", "comp3161", "businessDept", "alpha Hall","trackTeam", "hype Squad", "Late Nighters", "random group"]
    def creatGroups(allusers):
        groups = []
        lst = groupNames
        numCreators = len(lst)

        for x in range(numCreators):
            creator = random.choice([y for y in range(1,len(allusers)+1)])
            groups.append([creator, lst[x], dateCreated()])
        return groups

    with open('users.csv', newline='') as f:
        userIDs = [x+1 for x in range(len(list(csv.reader(f))))]

    groups = creatGroups(userIDs)
    f= csv.writer(open('groups.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in groups:
        f.writerow(_list)
    #_________________________________________________________________________________________________
    #generate members

    def memberlist(userids,groups):
        maxNumber = 25
        groupIDs = [x+1 for x in range(len(groups)+1)]
        members = []
        for group in range(0,len(groups)):
            numMembers = random.choice([y for y in range(1,maxNumber+1)])
            creator = groups[group][0]
            members.append((creator,group+1))
            for x in range(numMembers):
                memberID = random.choice([y for y in range(1,len(userids)+1)])
                if(memberID == creator):
                    x-=1
                else:
                    members.append((memberID,group+1))
        return members



    with open('users.csv', newline='') as f:
        userIDs = [x+1 for x in range(len(list(csv.reader(f))))]
        print("\n\n len uid is: ", len(userIDs))

    members = memberlist(userIDs,groups)
    members = list(set(members))
    members.sort()
    membercsv= csv.writer(open('members.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in members:
        membercsv.writerow(_list)

    #________________________________________________________________________________________________________________________
    # Generate Editors
    def getGroupID(member):
        return member[1]
    def getMemberID(member):
        return member[0]

    def getMembers(groupID,membersList):
        memberIDs =[]
        for x in membersList:
            if getGroupID(x) == groupID:
                memberIDs.append(getMemberID(x))
        return memberIDs

    def generateEditors(groupNames,members):
        editors = []
        for group in range(len(groupNames)):
            groupMembers = getMembers(group+1,members)
            maxEditor = int(0.33* len(groupMembers)-1)
            creator = groups[group][0]
            editors.append((creator, group+1))
            for x in range(maxEditor):
                editor = groupMembers[random.choice([y for y in range(len(groupMembers))])]
                if editor == creator:
                    x-=1
                else:
                    editors.append((editor, group+1))
        return editors

    editors = generateEditors(groupNames,members)
    editors = list(set(editors))
    editors.sort()
    editorcsv= csv.writer(open('editors.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in editors:
        editorcsv.writerow(_list)

######################################################################################################
def generate_posts():
    #Posts(postid, postDate, UID)
    def _posts(number_of_posts):
        posts = []
        with open('editors.csv', newline='') as e:
            editors = list(set([x[0] for x in csv.reader(e)]))

        for post in range(number_of_posts):
            poster = random.choice(editors)
            posts.append((datetime.date.today(),poster))
        return posts
    
    def generate_post_text(posts):
        textslist = ["Be a Warrior, not a Worrier.","Go wild for a while.","Rolling with the homies.","When you are Downie, eat a brownie.",
            "All we have is NOW.","Just keep making those baby steps every day.","You think you are not moving but when you look back, you will realize how far you have come",
            "We got that Friday feeling.","Catch flights, not Feelings.","Disappointed but not surprised.","How I feel when there is no Coffee. DEPRESSO!"
            "50% Savage. 50% Sweetness.","You can’t do epic stuff with basic people."]
        posttexts = []
        total_post_texts = int(len(posts)/1)
        lstpostids = list(set([random.choice([y for y in range(1,len(posts))]) for x in range(total_post_texts)]))
        for x in lstpostids:
            text= random.choice(textslist)
            posttexts.append((x,text))
        posttextcsv= csv.writer(open('post_texts.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for _list in posttexts:
            posttextcsv.writerow(_list)

    with open('users.csv', newline='') as f:
        userIDs = [x+1 for x in range(len(list(csv.reader(f))))]

    number_of_posts = int(0.33 * len(userIDs))
    
    posts = _posts(number_of_posts)
    generate_post_text(posts)
    postscsv= csv.writer(open('posts.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in posts:
        postscsv.writerow(_list)

def generate_group_posts():

    def geteditor(poster,editors):
        editor = []
        for e in editors:
            if e[0] == poster:
                return e

    def _group_posts(posts, editors,number_of_gposts):
        groupposts = []
        for post in range(number_of_gposts):
            postid =random.choice ([x+1 for x in range(len(posts))])
            p = posts[postid-1]
            poster = p[1]
            editor=geteditor(poster,editors)
            groupid = editor[1]
            gp = (postid,groupid)
            if gp in groupposts:
                post -=1
            else:
                groupposts.append(gp)
        return groupposts


    with open('posts.csv', newline='') as f:
        posts = list(csv.reader(f))
    
    with open('editors.csv', newline='') as e:
        editors = list(csv.reader(e))
        

    number_of_gposts = int(0.1 * len(posts))
    group_posts = _group_posts(posts, editors,number_of_gposts)
    
    group_postscsv= csv.writer(open('group_posts.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in group_posts:
        group_postscsv.writerow(_list)
    
def generate_photos():
    def profile_photos(users):
        profiles = []
        for x in range(users):
            if x%2 == 0:
                profiles.append((x+1,"female.webp"))
            else:
                profiles.append((x+1,"male.webp"))
        return profiles
    
    def posts_photos(posts,allprofiles):
        mypath = app.config['POST_PICS'] #mypath links to folder with photos
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        total_post_pics = int(len(posts)*0.4)
        photos = []
        postpics = []
        lstpostids = list(set([random.choice([y for y in range(1,len(posts))]) for x in range(total_post_pics)]))
        x=1
        
        for pid in lstpostids:
            photoid = allprofiles + x
            photos.append((pid,photoid))
            postpics.append(( posts[pid][1], random.choice(onlyfiles)))
            x+=1
        postphotoscsv= csv.writer(open('post_photos.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
        postpics
        for _list in photos:
            postphotoscsv.writerow(_list)
        return postpics

    with open('posts.csv', newline='') as p:
        total_posts = list(csv.reader(p))
    with open('users.csv', newline='') as u:
        allprofiles = len(list(csv.reader(u)))

    photos = profile_photos(allprofiles)+ posts_photos(total_posts,allprofiles)
    photoscsv= csv.writer(open('photos.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in photos:
        photoscsv.writerow(_list)

def generate_comments():
    commentlist = [ 
    "That's right. Good for you. You're really moving.","That's the right answer. You're right on target.","That's very perceptive. You've come a long way with this one.",
    "The results were worth all your hard work. You've got it now.","This demonstrates your knowledge of the ____. You've made my day.",
    "This gets a four-star rating. You've put in a full day today.","This is a moving scene. You've really been paying attention.","This is a winner! You've shown a lot of patience with this.","This is fun, isn't it? Your hard work has paid off.","This is prize-winning work. Your remark shows a lot of sensitivity."
    ,"This is quite an accomplishment. Your style has spark.","This is something special. Your work has such personality.","This kind of work pleases me very much.",
    "This paper has pizzazz!","This really has flair."
    ]
    comments = []

    with open('posts.csv', newline='') as p:
        allposts = list(csv.reader(p))
    with open('members.csv', newline='') as m:
        members = list(csv.reader(m))
    with open('group_posts.csv', newline='') as gp:
        groupposts = list(csv.reader(gp))
    
    def getMembers(members,groupid):
        memberset = []
        for x in members:
            if groupid == x[1]:
                memberset.append(x[0])
        return memberset
    
    postids = [str(x+1) for x in range(len(allposts))]
    grouppostids = []
    for post in groupposts:
        groupmembers= getMembers(members,post[1]) # getmembers accepts a 
        maxcomments = 4
        for x in range(random.randint(1,4)):
            post_id = post[0]
            commenter = random.choice(groupmembers)
            day = str(datetime.date.today())
            comment = commentlist[random.randint(0,len(commentlist)-1)]
            comments.append((post_id, commenter, day, comment))
        grouppostids.append((post[0]))

    remainingpostsID = list(set(postids) - set(grouppostids))
    
    for post in postids:
        if post in remainingpostsID:
            post_id = post
            commenter = allposts[int(post)-1][1]
            day = str(datetime.date.today())
            comment = commentlist[random.randint(0,len(commentlist)-1)]
            comments.append((post_id, commenter, day, comment))
    
    
    commentscsv= csv.writer(open('comments.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in comments:
        commentscsv.writerow(_list)

def generate_messages():
    messagetemplate = ["Hi","Hello"," How are you?","I'm fine, thanks for asking","You?","What time did you get in?","Can you wake me up at 8 tomorrow?",
    "Sure thing", "whateder you wan to do","I'm going to buy a house","What are you doing tomorrow"]
      
    def create_messages(users):
        numMessages = int(users/4)
        messages =[]
        for message in range(numMessages):
            participants = getSenderReceiver()
            sender = participants[0]
            messagetext = random.choice(messagetemplate)
            receiver = participants[1]
            day = str(datetime.date.today())
            time = str(datetime.datetime.now().time())[:8]
            messages.append((sender,receiver,messagetext, day,time))
        return messages
    def getSenderReceiver():
        with open('friends.csv', newline='') as f:
            allfriends = list(csv.reader(f))
        friendship = random.choice(allfriends)
        order = random.choice([0,1])
        if order == 0:
            return (friendship[0],friendship[1])
        return (friendship[1],friendship[0])

    with open('users.csv', newline='') as f:
            users = list(csv.reader(f))

    messages =create_messages(len(users))
    messagescsv= csv.writer(open('messages.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for _list in messages:
        messagescsv.writerow(_list)

############# Populate Tables with data ##########################

def populateUsers():
    with open('users.csv', newline='') as u:
        users = list(csv.reader(u))
    with open('userlogin.csv', newline='') as ul:
        userlogins = list(csv.reader(ul))

    with open('profiles.csv', newline='') as prof:
        profiles = list(csv.reader(prof))
    for row in range(len(users)):

        email = userlogins[row][0]
        password = userlogins[row][1]
        day = users[row][0]
        #profile format
        #Felipa,Spinka,1989-02-06,female,I like cars,1
        firstname =profiles[row][0]
        lastname = profiles[row][1]
        dob = profiles[row][2]
        gender = profiles[row][3]
        bio = profiles[row][4]
        picid = profiles[row][5]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (day,email,password,firstname,lastname,dob,gender,bio,picid)
            cur.callproc('createUser', args)
            mysql.connection.commit()
            cur.close()
    
    return "populated tables"

def populate_friends():
    with open('friends.csv', newline='') as fr:
        friends = list(csv.reader(fr))
    for row in range(len(friends)):
        friendid1,friendid2,stat,sender,fgroup = friends[row][0], friends[row][1], friends[row][2], friends[row][3], friends[row][4]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (friendid1,friendid2,stat,sender,fgroup)
            cur.callproc('createFriends', args)
            mysql.connection.commit()
            cur.close()
    

def populate_groups():
    with open('groups.csv', newline='') as gr:
        groups = list(csv.reader(gr))
    for row in range(len(groups)):
        creator,groupname ,date_created = groups[row][0],groups[row][1],groups[row][2]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (creator,groupname ,date_created)
            cur.callproc('createGroups', args)
            mysql.connection.commit()
            cur.close()

    with open('members.csv', newline='') as me:
        members = list(csv.reader(me))
    for row in range(len(members)):
        memberid ,groupid = members[row][0],members[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (memberid ,groupid)
            cur.callproc('createMembers', args)
            mysql.connection.commit()
            cur.close()

    with open('editors.csv', newline='') as ed:
        editors = list(csv.reader(ed))
    for row in range(len(editors)):
        editorid, groupid = editors[row][0],editors[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (editorid,groupid)
            cur.callproc('createEditors', args)
            mysql.connection.commit()
            cur.close()

def populate_photos():
    with open('photos.csv', newline='') as ph:
        photos = list(csv.reader(ph))
    for row in range(len(photos)):
        userid, photoname = photos[row][0], photos[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (userid, photoname)
            cur.callproc('createPhotos', args)
            mysql.connection.commit()
            cur.close()

def populate_posts():
       
    with open('posts.csv', newline='') as po:
        posts = list(csv.reader(po))
    for row in range(len(posts)):
        postdate,userid = posts[row][0], posts[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (postdate,userid)
            cur.callproc('createPosts', args)
            mysql.connection.commit()
            cur.close()
    
    with open('post_photos.csv', newline='') as pp:
        post_photos = list(csv.reader(pp))
    for row in range(len(post_photos)):
        postid,photoid = post_photos[row][0], post_photos[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (postid,photoid)
            cur.callproc('createPostPhotos', args)
            mysql.connection.commit()
            cur.close()

    with open('post_texts.csv', newline='') as pt:
        post_texts = list(csv.reader(pt))
    for row in range(len(post_texts)):
        postid, caption = post_texts[row][0], post_texts[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (postid, caption)
            cur.callproc('createPostTexts', args)
            mysql.connection.commit()
            cur.close()
    
    with open('comments.csv', newline='') as co:
        comments = list(csv.reader(co))
    for row in range(len(comments)):
        postid ,userid ,commentdate ,comment = comments[row][0], comments[row][1], comments[row][2], comments[row][3]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (postid ,userid ,commentdate ,comment)
            cur.callproc('createComments', args)
            mysql.connection.commit()
            cur.close()
    
def populate_messages():
    with open('messages.csv', newline='') as ms:
        messages = list(csv.reader(ms))
    for row in range(len(messages)):
        sender ,receiver ,messagestring ,messagedate ,messagetime = messages[row][0], messages[row][1], messages[row][2], messages[row][3],messages[row][4]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (sender ,receiver ,messagestring ,messagedate ,messagetime)
            cur.callproc('createMessages', args)
            mysql.connection.commit()
            cur.close()

def populate_groupPosts():
    with open('group_posts.csv', newline='') as gp:
        group_posts = list(csv.reader(gp))
    for row in range(len(group_posts)):
        postdate,userid = group_posts[row][0], group_posts[row][1]
        with app.app_context():
            cur = mysql.connection.cursor()
            if cur:
                print("\n\n Connection\n")
            args = (postdate,userid)
            cur.callproc('createGroupPosts', args)
            mysql.connection.commit()
            cur.close()

def populate():
    generate_users()
    generate_friends()
    generate_groups()
    generate_posts()
    generate_group_posts()
    generate_photos()
    generate_comments()
    generate_messages()

    populateUsers()
    populate_friends()
    populate_groups()
    populate_photos()
    populate_posts()
    populate_messages()
    populate_groupPosts()
    pass
    



