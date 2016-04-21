from flask import Flask, request
from flask.ext.mysql import MySQL
from random import randint
from flask.ext.cors import CORS
import os
import json
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={"/*": {"origins": "*"}})
#cors2 = CORS(app, resources={"/insert/": {"origins": "*"}})
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'b42d5429495ba1'
app.config['MYSQL_DATABASE_PASSWORD'] = '8bd2e75a'
app.config['MYSQL_DATABASE_DB'] = 'heroku_b089831d5b9fbdc'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-03.cleardb.net'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
tagssss = ['meme','cartoon','politics']
quote = 'Wombo Combo.'
newquote = 'lalalala'


@app.route("/insertquote/", methods=['GET', 'POST'])
def insertQuote():
	#cursor = conn.cursor()
	print "here we go"
	print str(request)
	qu = request.args.get('quote')
	qu = qu.replace("%22","")
	qu = qu.replace('"',"")
	print qu
	#tags = [tag]
	tags = request.args.get('tags')
	tags = tags.replace("%22","")
	tags = tags.replace('"',"")
	print tags
	tag = [tags]
	stringIn = "INSERT INTO Quotes(Quote) Values(\'"+qu+"\')"
	conn.ping(True)
	cursor.execute(stringIn)
	find = "SELECT * FROM Quotes WHERE Quotes.Quote = \'"+qu+"\'"
	conn.ping(True)
	cursor.execute(find)
	count = 0
	qId = 0
	for row in cursor.fetchall():
		count +=1
		qId = row[0]
		if count ==1:
			break
	for line in tag:
		add = "INSERT INTO Tags(QuoteID, Tag) Values ("+str(qId)+", \'"+str(line)+"\')"
		conn.ping(True)
		cursor.execute(add)
	conn.commit()
	return "success i believe"


@app.route("/deletequote/", methods=['GET', 'POST'])
def deleteQuote():
	#cursor = conn.cursor()
	print "delete starts"
	print str(request)
	qu = request.args.get('quote')
	qu = qu.replace("%22","")
	qu = qu.replace('"',"")
	print str(qu)
	find = "SELECT * FROM Quotes WHERE Quotes.Quote = \'"+str(qu)+"\'"
	conn.ping(True)
	cursor.execute(find)
	qId =0
	if cursor:
		count = 0
		for row in cursor.fetchall():
			count +=1
			qId = row[0]
			if count ==1:
				break
		delete = "DELETE FROM Quotes WHERE Quotes.QuoteID= "+str(qId)
		conn.ping(True)
		cursor.execute(delete)
		delete = "DELETE FROM Tags WHERE Tags.QuoteID= "+str(qId)
		conn.ping(True)
		cursor.execute(delete)
	conn.commit()
	return "success i hope in delete"

# def deleteTag(tag, conn):
# 	cursor = conn.cursor()
# 	delete = "DELETE FROM Tags WHERE Tags.Tag =\'"+str(tag) +"\'"
# 	cursor.execute(delete)
# 	conn.commit()

@app.route("/updatequote/", methods=['GET', 'POST'])
def updateQuote():
	#cursor = conn.cursor()
	quo = request.args.get('quote')
	quo = quo.replace("%22","")
	quo = quo.replace('"',"")
	print str(quo)
	newqu = request.args.get('newquote')
	newqu = newqu.replace("%22","")
	newqu = newqu.replace('"',"")
	print str(newqu)
	update = "UPDATE Quotes SET Quote =\'" + str(newqu)+"\'WHERE Quote =\'"+str(quo)+"\'"
	print update
	conn.ping(True)
	cursor.execute(update)
	conn.commit()
	return "kinda worked"

@app.route("/getquote/", methods=['GET'])
def getQuote():
	#cursor = conn.cursor()
	print "here"
	print "hi "+ str(request)
	#data = json.loads(request.data)
	tag = str(request.args.get('tags'))
	tag = tag.replace("%22","")
	tag = tag.replace('"',"")
	print tag
	tags = [tag]
	find = "SELECT DISTINCT q.Quote FROM Quotes AS q, Tags As t WHERE "
	count = 0
	for line in tags:
		if count >0:
			find += " OR "
		find += " t.Tag =\'"+str(line)+"\'"
		count+=1
	find += " AND q.QuoteID = t.QuoteID"
	print find
	conn.ping(True)
	cursor.execute(find)
	top = cursor.rowcount
	num = randint(1,top)
	count =1
	many = ''
	for row in cursor:
		if count == num:
			many = row[0]
			break
		print row[0]
		count +=1
	conn.commit()
	return many


@app.route("/addfeed/", methods=['GET'])
def addToFeed():
	#cursor = conn.cursor()

	print "here we go"
	print str(request)
	post = request.args.get('post')
	post = post.replace("%22","")
	post = post.replace('"',"")
	print post
	userID = request.args.get('userID')
	userID = userID.replace("%22","")
	userID = userID.replace('"',"")
	print userID
	tag = request.args.get('tag')
	tag = tag.replace("%22","")
	tag = tag.replace('"',"")
	print tag

	stringIn = "INSERT INTO Posts(Post,UserID,Tag) Values(\'"+post+"\',"+str(userID)+",\'"+tag+"\');"
	print stringIn
	conn.ping(True)
	cursor.execute(stringIn)
	conn.commit()
	return "hahahahaha"


#this returns the cursor that can be used to get the feeds
@app.route("/getfeed/", methods=['GET'])
def fillfeed():
	print "here we go"
	print str(request)
	tagname = request.args.get('tagname')
	tagname = tagname.replace("%22","")
	tagname = tagname.replace('"',"")
	print tagname
	stringIn = "SELECT * FROM Posts WHERE karma > -3 AND DATEINSERT >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND tag = \""+tagname+"\";"
	conn.ping(True)
	cursor.execute(stringIn)
#	lists = []
	somedict = {}
	for row in cursor:
#		thislist = [row[0], row[1], row[2], row[3], row[5]]
		cursor2 = conn.cursor()
		stringIn = "SELECT username FROM Users Where userId = " +str(row[2])+";"
		cursor2.execute(stringIn)
		username = "hello"
		for name in cursor2:
			username = name[0]
		somedict[row[0]] = {"post":row[1], "userID":username, "tagname":row[3], "karma":row[5]}
#	 	lists.append(thislist)
	haha = json.dumps(somedict)
	return haha



@app.route("/updatekarma/", methods=['GET','POST'])
def updateKarma():

	print "here we go"
	print str(request)
	postID = request.args.get('postID')
	print postID
	postID = postID.replace("%22","")
	postID = postID.replace('"',"")
	print postID

	add = request.args.get('add')
	add = add.replace("%22","")
	add = add.replace('"',"")
	print add

	cursor = conn.cursor()
	stringIn = "UPDATE Posts SET karma = karma + "+str(add)+" Where PostId = "+str(postID)+";"
	cursor.execute(stringIn)
	stringIn = "UPDATE Users SET karma = karma + "+str(add)+"  Where Users.UserId= (Select UserId From Posts Where PostId = "+str(postID)+");"
	cursor.execute(stringIn)
	conn.commit()
	return "hahaha"
@app.route("/createuser/", methods=['POST'])
def createUser():


	print "here we go"
	print str(request)
	username = request.args.get('username')
	username = username.replace("%22","")
	username = username.replace('"',"")
	print username

	password = request.args.get('password')
	password = password.replace("%22","")
	password = password.replace('"',"")
	print password


	cursor = conn.cursor()
	stringIn = "INSERT INTO Users(Username, Pass) Values(\'"+username+"\',\'"+password+"\');"
	cursor.execute(stringIn)
	conn.commit()

def getUserFeed(userId, conn):
	cursor = conn.cursor()
	stringIn = "Select * FROM Posts Where Posts.userId = " +str(userId)+ ";"
	cursor.execute(stringIn)
	conn.commit();
	return cursor

def getUniqueTagsFromUser(userId,conn):
	cursor = conn.cursor()
	stringIn = "Select DISTINCT Posts.Tag FROM Posts Where Posts.userId = " +str(userId)+ ";"
	cursor.execute(stringIn)
	conn.commit();
	return cursor

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port, debug = True)
    app.run(debug = True)
 
# MySQL configurations

#insertQuote(quote,tags,conn)
#deleteEntry(quote,conn)
#deleteTag('meme',conn)
# updateQuote(quote,newquote,conn)
# cursor.execute("SELECT * FROM Quotes")
# for row in cursor:
# 	print str(row[0])+ " "+str(row[1])
