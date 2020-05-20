
create database if not Exists mybook;
use mybook;

drop table if EXISTS users;
drop table if EXISTS photos;
drop table if EXISTS posts;
drop table if EXISTS groups;
drop table if EXISTS friends;
drop table if EXISTS messages;
drop table if EXISTS profiles;
drop table if EXISTS post_photos;
drop table if EXISTS post_texts;
drop table if EXISTS comments;
drop table if EXISTS group_posts;
drop table if EXISTS editors;
drop table if EXISTS members;
drop table if EXISTS userlogin;

-- relations derived from strong entities
CREATE TABLE users (
    userid int not null unique AUTO_INCREMENT,
    date_registered date not null,
    primary key (userid)
);

CREATE TABLE photos (
    photoid int not null unique AUTO_INCREMENT,
    userid int not null,
    photoname varchar(255) not null,
    primary key(photoid),
    foreign key(userid) references users(userid) on delete cascade
);

CREATE TABLE posts (
    postid int not null unique  AUTO_INCREMENT,
    postdate date not null,
    userid int not null,
    primary key(postid),
    foreign key(userid) references users(userid) on delete cascade
);

CREATE TABLE groups (
    groupid int not null unique AUTO_INCREMENT,
    creator int not null,
    groupname varchar(30) not null,
    date_created date not null,
    primary key(groupid),
    foreign key(creator) references users(userid) on delete cascade
);

-- relations derived from weak entities
CREATE TABLE userlogin (
    userid int not null unique AUTO_INCREMENT,
    email varchar(40) not null unique,
    pass varchar(255) not null,
    primary key (userid, email),
    foreign key (userid) references users(userid) on delete cascade
);

CREATE TABLE profiles (
    userid int not null unique AUTO_INCREMENT,
    firstname varchar(30),
    lastname varchar(30),
    dob date,
    gender varchar(10),
    biography varchar(255),
    photoid int,
    primary key(userid),
    foreign key(userid) references users(userid) on delete cascade
);

CREATE TABLE post_texts (
    postid int not null unique,
    caption varchar(500) not null,
    primary key(postid, caption),
    foreign key(postid) references posts(postid) on delete cascade
);

CREATE TABLE post_photos (
    postid int not null unique,
    photoid int not null,
    primary key(postid, photoid),
    foreign key(postid) references posts(postid) on delete cascade,
    foreign key(photoid) references photos(photoid) on delete cascade
);

CREATE TABLE comments (
    commentid int not null unique AUTO_INCREMENT,
    postid int not null,
    userid int not null,
    commentdate date not null,
    comment varchar(255) not null,
    primary key(commentid,postid),
    foreign key(postid) references posts(postid) on delete cascade,
    foreign key(userid) references users(userid) on delete cascade

);

--relations derived from relationships of strong entities

CREATE TABLE friends (
    fid int not null unique AUTO_INCREMENT,
    friendid1 int not null,
    friendid2 int not null,
    stat int not null,
    sender int not null,
    fgroup varchar(500) not null,
    primary key(fid),
    foreign key(friendid1) references users(userid) on delete cascade,
    foreign key(friendid2) references users(userid) on delete cascade,
    foreign key(sender) references users(userid) on delete cascade
);



CREATE TABLE messages(
    messageid int not null unique AUTO_INCREMENT,
    sender int not null,
    receiver int not null,
    messagestring varchar(255) not null,
    messagedate date, 
    messagetime time,
    primary key(messageid),
    foreign key(sender) references users(userid) on delete cascade,
    foreign key(receiver) references users(userid) on delete cascade
);

CREATE TABLE group_posts (
    postid int not null,
    groupid int not null,
    primary key(postid),
    foreign key(postid) references posts(postid) on delete cascade,
    foreign key(groupid) references groups(groupid) on delete cascade
);

CREATE TABLE editors (
    editorid int not null,
    groupid int not null,
    primary key(editorid, groupid),
    foreign key(editorid) references users(userid) on delete cascade,
    foreign key(groupid) references groups(groupid) on delete cascade
);
CREATE TABLE members (
    memberid int not null,
    groupid int not null,
    primary key(memberid,groupid),
    foreign key(memberid) references users(userid) on delete cascade,
    foreign key(groupid) references groups(groupid) on delete cascade
);

-- Stored procedures to Populate tables

DELIMITER $$
CREATE PROCEDURE createUser(
	IN date_registered date, email varchar(40), pass varchar(255), firstname varchar(30),lastname varchar(30), dob date, gender varchar(10), biography varchar(255),photoid int
)
BEGIN
	INSERT INTO users (date_registered) VALUES (date_registered);
    INSERT INTO userlogin (email, pass) VALUES (email,password(pass));
    INSERT INTO profiles (firstname, lastname, dob, gender, biography,photoid) VALUES (firstname, lastname, dob, gender, biography,photoid);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createFriends(
	IN friendid1 int,friendid2 int,stat int, sender int, fgroup varchar(500)
)
BEGIN
	INSERT INTO friends (friendid1,friendid2,stat,sender,fgroup) VALUES (friendid1,friendid2,stat,sender,fgroup);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createGroups(
	IN creator int,groupname varchar(30),date_created date
)
BEGIN
	INSERT INTO groups (creator,groupname ,date_created ) VALUES (creator,groupname ,date_created);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createMembers(
	IN memberid int, groupid int
)
BEGIN
	INSERT INTO members (memberid ,groupid) VALUES (memberid ,groupid);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createPhotos(
	IN userid int,photoname varchar(255)
)
BEGIN
	INSERT INTO photos (userid,photoname ) VALUES (userid,photoname);
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE createEditors(
	IN editorid int,groupid int
)
BEGIN
	INSERT INTO editors (editorid,groupid ) VALUES (editorid,groupid );
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE createPosts(
	IN postdate date,userid int
)
BEGIN
	INSERT INTO posts (postdate,userid) VALUES (postdate,userid );
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createPostPhotos(
	IN postid int,photoid int
)
BEGIN
	INSERT INTO post_photos (postid,photoid) VALUES (postid,photoid );
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createPostTexts(
	IN postid int, caption varchar(500)
)
BEGIN
	INSERT INTO post_texts(postid, caption) VALUES (postid, caption );
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createComments(
	IN postid int,userid int,commentdate date,comment varchar(255)
)
BEGIN
	INSERT INTO comments(postid ,userid ,commentdate ,comment) VALUES (postid ,userid ,commentdate ,comment);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createMessages(
	IN sender int,receiver int,messagestring varchar(255),messagedate date,messagetime time
)
BEGIN
	INSERT INTO messages(sender ,receiver ,messagestring ,messagedate ,messagetime) VALUES (sender ,receiver ,messagestring ,messagedate ,messagetime);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createGroupPosts(
	IN postid int,groupid int
)
BEGIN
	INSERT INTO group_posts (postid,groupid) VALUES (postid,groupid );
END$$
DELIMITER ;



-- Stored procedures to access data

DELIMITER $$
CREATE PROCEDURE getAllUsers()
BEGIN
	SELECT users.userid, profiles.firstname, profiles.lastname, userlogin.email
    FROM users JOIN profiles ON users.userid = profiles.userid
    JOIN userlogin ON users.userid = userlogin.userid;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE userDetails(
    IN userid int
)
BEGIN
	SELECT users.userid, profiles.firstname, profiles.lastname, userlogin.email, profiles.biography, profiles.dob,profiles.gender, photos.photoname
    FROM users JOIN profiles ON users.userid = profiles.userid
    JOIN userlogin ON users.userid = userlogin.userid
    JOIN photos on photos.photoid = profiles.photoid
    WHERE users.userid = userid;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getFriends(
    IN userid int
)
BEGIN
	SELECT (f.friendid1) friendship, firstname, lastname FROM friends f join profiles on f.friendid1 = profiles.userid WHERE f.friendid2 = userid
    UNION 
    SELECT (f.friendid2) friendship, firstname, lastname FROM friends f join profiles on f.friendid2 = profiles.userid WHERE f.friendid1 = userid;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE getGroups(
    IN userid int
)
BEGIN
	SELECT groups.groupid, groups.groupname, profiles.firstname, profiles.lastname from groups
    join profiles on creator = profiles.userid
    join (select members.groupid from members where memberid = userid) as m on groups.groupid = m.groupid;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getPosts(
    IN userid int
)
BEGIN
	SELECT postid, postdate from posts
    WHERE posts.userid = userid;
END$$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE getUserDetails(
    IN email varchar(40), pass varchar(255) 
)
BEGIN
	SELECT userid, email from userlogin
    WHERE userlogin.email = email and userlogin.pass = password(pass);
END$$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE getUserPersonalPosts(
    IN userid int
)
BEGIN
	SELECT posts.postid, profiles.firstname, profiles.lastname, photos.photoname, post_texts.caption, posts.postdate
    FROM posts 

    JOIN profiles ON posts.userid = profiles.userid
    left JOIN post_photos on posts.postid = post_photos.postid 
    left JOIN post_texts on posts.postid = post_texts.postid 
    left JOIN photos on post_photos.photoid = photos.photoid
    
    WHERE posts.postid NOT IN 
    (SELECT group_posts.postid FROM group_posts) and 
    posts.userid IN 
        (
            SELECT (f.friendid1) friendship FROM friends f JOIN profiles on f.friendid1 = profiles.userid WHERE f.friendid2 = userid
            UNION 
            SELECT (f.friendid2) friendship FROM friends f JOIN profiles on f.friendid2 = profiles.userid WHERE f.friendid1 = userid
        )
    ORDER BY posts.postdate
    ;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE getUserFriends(
    IN userid int
)
BEGIN
	SELECT (f.friendid1) friendship, firstname, lastname, photos.photoname FROM friends f join profiles on f.friendid1 = profiles.userid 
    join photos on profiles.photoid = photos.photoid
    WHERE f.friendid2 = userid
    UNION 
    SELECT (f.friendid2) friendship, firstname, lastname, photos.photoname FROM friends f join profiles on f.friendid2 = profiles.userid 
    join photos on profiles.photoid = photos.photoid
    WHERE f.friendid1 = userid;
END$$
DELIMITER ;







