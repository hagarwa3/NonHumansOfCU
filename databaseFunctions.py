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
	qu = qu.replace('\'',"")
	print qu
	#tags = [tag]
	tags = request.args.get('tags')
	tags = tags.replace("%22","")
	tags = tags.replace('"',"")
	print tags
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
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
	addToFeed(qu,userId,tag,conn)
	return "success i believe"

def updateKarma(postId,add,conn):
	cursor = conn.cursor()
	stringIn = "UPDATE Posts SET karma = karma + "+str(add)+" Where PostId = "+str(postId)+";"
	cursor.execute(stringIn)
	stringIn = "UPDATE Users SET karma = karma + "+str(add)+"  Where Users.UserId= (Select UserId From Posts Where PostId = "+str(postId)+");"
	cursor.execute(stringIn)
	conn.commit()
# @app.route("/deletequote/", methods=['GET', 'POST'])
# def deleteQuote():
# 	#cursor = conn.cursor()
# 	print "delete starts"
# 	print str(request)
# 	qu = request.args.get('quote')
# 	qu = qu.replace("%22","")
# 	qu = qu.replace('"',"")
# 	print str(qu)
# 	find = "SELECT * FROM Quotes WHERE Quotes.Quote = \'"+str(qu)+"\'"
# 	conn.ping(True)
# 	cursor.execute(find)
# 	qId =0
# 	if cursor:
# 		count = 0
# 		for row in cursor.fetchall():
# 			count +=1
# 			qId = row[0]
# 			if count ==1:
# 				break
# 		delete = "DELETE FROM Quotes WHERE Quotes.QuoteID= "+str(qId)
# 		conn.ping(True)
# 		cursor.execute(delete)
# 		delete = "DELETE FROM Tags WHERE Tags.QuoteID= "+str(qId)
# 		conn.ping(True)
# 		cursor.execute(delete)
# 	conn.commit()
# 	return "success i hope in delete"

# def deleteTag(tag, conn):
# 	cursor = conn.cursor()
# 	delete = "DELETE FROM Tags WHERE Tags.Tag =\'"+str(tag) +"\'"
# 	cursor.execute(delete)
# 	conn.commit()

# @app.route("/updatequote/", methods=['GET', 'POST'])
# def updateQuote():
# 	#cursor = conn.cursor()
# 	quo = request.args.get('quote')
# 	quo = quo.replace("%22","")
# 	quo = quo.replace('"',"")
# 	print str(quo)
# 	newqu = request.args.get('newquote')
# 	newqu = newqu.replace("%22","")
# 	newqu = newqu.replace('"',"")
# 	print str(newqu)
# 	update = "UPDATE Quotes SET Quote =\'" + str(newqu)+"\'WHERE Quote =\'"+str(quo)+"\'"
# 	print update
# 	conn.ping(True)
# 	cursor.execute(update)
# 	conn.commit()
# 	return "kinda worked"

@app.route("/getquote/", methods=['GET'])
def getQuote():
	#cursor = conn.cursor()
	print "here"
	print "hi "+ str(request)
	#data = json.loads(request.data)
	tag = str(request.args.get('tags'))
	tag = tag.replace("%22","")
	tag = tag.replace('"',"")
	tags = tag.split(',')
	print tags
	#tags = [tag]
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
	elements = []
	# many = ''
	for row in cursor:
		elements.append(row[0])
	starter = elements[num]
	w1 = starter.split()[0]+" "+starter.split()[1]
	starter = w1.lower()
	print starter
	#starter = u"can't do"

	combine = ' '.join(elements)
	#print combine
	combine = combine.split()
	for i in xrange(len(combine)):
		combine[i]=combine[i].lower()
	triplet = []
	for i in xrange(len(combine)-3):
		triplet.append([combine[i],combine[i+1],combine[i+2]])

	doubledict = {}

	for l in triplet:
		duet = l[0]+" "+l[1]
		if duet in doubledict:
			doubledict[duet].append(str(l[2]))
		else:
			doubledict[duet]=[str(l[2])]

	#print doubledict

	length = randint(3,20)
	print length
	listsofar = starter.split()
	while len(listsofar)<=length:
	    prev = listsofar[-2]+" "+ listsofar[-1]
	    #print prev
	    get = doubledict[prev]
	    toget = randint(0,len(get)-1)
	    #print get
	    #print toget
	    string = get[toget]
	    listsofar.append(string)
	    if len(listsofar)==length and ("." != listsofar[-1][-1] and length<40):
	        length+=1
	listsofar.pop()
	listsofar = ' '.join(listsofar)
	print "here"
	message = listsofar
	print message

	conn.commit()
	return message


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
	stringIn = "SELECT * FROM Posts WHERE karma > -3 AND DATEINSERT >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND tag = \""+tagname+"\" ORDER BY karma DESC;"
	conn.ping(True)
	cursor.execute(stringIn)
	lists = []
	somedict = {}
	for row in cursor:
#		thislist = [row[0], row[1], row[2], row[3], row[5]]
		cursor2 = conn.cursor()
		stringIn = "SELECT username FROM Users Where userId = " +str(row[2])+";"
		cursor2.execute(stringIn)
		username = "hello"
		for name in cursor2:
			username = name[0]
		lists.append([row[0],row[1],username,row[3],row[5]] )
		#somedict[row[0]] = {"post":row[1], "userID":username, "tagname":row[3], "karma":row[5]}
#	 	lists.append(thislist)
	lists.sort(key=lambda x: x[4],reverse = True)
	print lists
	for row in lists:
		somedict[row[0]] = {"post":row[1], "userID":row[2], "tagname":row[3], "karma":row[4]}
	#somedict = sorted(somedict.items(), key=lambda x: x[1]['karma'], reverse = True)
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
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "UPDATE Posts SET karma = karma + "+str(add)+" Where PostId = "+str(postID)+";"
	cursor.execute(stringIn)
	cursor.execute("SELECT karma From Posts Where PostId = "+str(postID)+";")
	sum = 0
	for row in cursor:
		sum = row[0]
	print sum
	if sum <=-3:
		cursor.execute("DELETE FROM Posts Where PostId = "+str(postID)+";")
	stringIn = "UPDATE Users SET karma = karma + "+str(add)+"  Where Users.UserId= (Select UserId From Posts Where PostId = "+str(postID)+");"
	cursor.execute(stringIn)
	conn.commit()
	return "hahaha"
# @app.route("/createuser/", methods=['POST'])
# def createUser():


# 	print "here we go"
# 	print str(request)
# 	username = request.args.get('username')
# 	username = username.replace("%22","")
# 	username = username.replace('"',"")
# 	print username

# 	password = request.args.get('password')
# 	password = password.replace("%22","")
# 	password = password.replace('"',"")
# 	print password


# 	cursor = conn.cursor()
# 	stringIn = "INSERT INTO Users(Username, Pass) Values(\'"+username+"\',\'"+password+"\');"
# 	cursor.execute(stringIn)
# 	conn.commit()

@app.route("/loginuser/", methods=['GET','POST'])
def loginUser():
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
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "SELECT * FROM Users WHERE username = \""+username+"\""
	cursor.execute(stringIn)
	print "here it is"
	count = 0
	for row in cursor:
		count+=1
	print "oh"
	if(count == 0):
		print "count was 0"
		stringIn = "INSERT INTO Users(Username, Pass) Values(\'"+username+"\',\'"+password+"\');"
		cursor.execute(stringIn)
		conn.commit()
		return "created"
	else:
		print "hmmmmmm"
		stringIn = "SELECT * FROM Users WHERE username = \""+username+"\" AND pass = \""+password+"\";"
		cursor.execute(stringIn)
		conn.commit()
		counter = 0
		for row in cursor:
			counter+=1
		if(counter<1):
			print "rip"
			return "not found"
		else:
			for row in cursor:
				print row
				print "yoooo"
				return str(row[0])





@app.route("/getuserfeed/", methods=['GET','POST'])
def getUserFeed():
	print str(request)
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "Select * FROM Posts Where Posts.userId = " +str(userId)+ ";"
	cursor.execute(stringIn)
	conn.commit()
	print stringIn
	somedict = {}
	for row in cursor:
#		thislist = [row[0], row[1], row[2], row[3], row[5]]
		cursor2 = conn.cursor()
		stringIn = "SELECT username FROM Users Where userId = " +str(row[2])+";"
		cursor2.execute(stringIn)
		username = "hello"
		for name in cursor2:
			username = name[0]
		word = (row[1].decode("utf-8"))
		other = word.encode("ascii","ignore")
		somedict[row[0]] = {"post":word, "userID":username, "tagname":row[3], "karma":row[5]}
#	 	lists.append(thislist)
	haha = json.dumps(somedict)
	return haha

@app.route("/getuniquetagsfromuser/", methods=['GET','POST'])
def getUniqueTagsFromUser():
	print str(request)
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "Select DISTINCT Posts.Tag FROM Posts Where Posts.userId = " +str(userId)+ ";"
	cursor.execute(stringIn)
	count =0
	romp= cursor.fetchall()
	res = ""
	amount = romp[0]
	for row in cursor:
#		mostFrequent = str(row[1])
		if count+1 == amount:
			res += str(row[0])
		else:
			res += str(row[0])+","
		count+=1
	return res[:-1]

@app.route("/getquotesaddedbyuser/", methods=['GET','POST'])
def getQuotesAddedByUser():
	print str(request)
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "SELECT DISTINCT Posts.Post FROM Posts INNER JOIN Quotes ON Posts.userId = " +str(userId)+ " AND Posts.post = Quotes.Quote ;"
	cursor.execute(stringIn)
	conn.commit()
	romp= cursor.fetchall()
	res = ""
	count =0 
	amount = romp[0]
	for row in cursor:
#		mostFrequent = str(row[1])
		if count+1 == amount:
			res += str(row[0])
		else:
			res += str(row[0])+","
		count+=1
	return res[:-1]

#gets the frequency of each tag and sorts them from most frequent to least frequent
@app.route("/getmostfrequenttag/", methods=['GET','POST'])
def getMostFrequentTag():
	print str(request)
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "Select COUNT(tag), tag FROM Posts Where Posts.userId = " +str(userId)+ " GROUP BY tag  ORDER BY COUNT(tag) DESC;"
	cursor.execute(stringIn)
	conn.commit()
	count = 0
	mostFrequent = ""
	res = ""
	romp = cursor.fetchone()
	amount = romp[0]-1
	for row in cursor:
#		mostFrequent = str(row[1])
		if count == amount:
			res += str(row[1])
		else:
			res += str(row[1])+","
		count+=1
	return res[:-1]

@app.route("/getuniqueuserfeed/", methods=['GET','POST'])
def getUniqueUserFeed():
	print str(request)
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "Select COUNT(tag), tag FROM Posts Where Posts.userId = " +str(userId)+ " GROUP BY tag  ORDER BY COUNT(tag) DESC;"
	cursor.execute(stringIn)
	conn.commit();
	frequent = ""
	count =0
	somedict =  {}
	for row in cursor:
		if count == 1:
			break;
		frequent= row[1]
		count+=1
	print frequent
	cursor1 = conn.cursor()
	stringIn = "Select * FROM Posts Where Posts.userId = " +str(userId)+ " AND Posts.Tag = \'"+frequent+"\';"
	cursor1.execute(stringIn)
	conn.commit();
	for row in cursor1:
#		thislist = [row[0], row[1], row[2], row[3], row[5]]
		cursor2 = conn.cursor()
		stringIn = "SELECT username FROM Users Where userId = " +str(row[2])+";"
		cursor2.execute(stringIn)
		username = "hello"
		for name in cursor2:
			username = name[0]
		word = (row[1].decode("utf-8"))
		other = word.encode("ascii","ignore")
		somedict[row[0]] = {"post":word, "userID":username, "tagname":row[3], "karma":row[5]}#	 	lists.append(thislist)
	haha = json.dumps(somedict)
	return haha

@app.route("/getpostbykarma/", methods=['GET','POST'])
def getPostByKarma():
	print str(request)
	userId = request.args.get('userid')
	userId = userId.replace("%22","")
	userId = userId.replace('"',"")
	print userId
	conn.ping(True)
	cursor = conn.cursor()
	stringIn = "Select * FROM Posts Where Posts.userId = " +str(userId)+ " ORDER BY karma DESC;"
	cursor.execute(stringIn)
	conn.commit();
	somedict = {}
	for row in cursor:
#		thislist = [row[0], row[1], row[2], row[3], row[5]]
		cursor2 = conn.cursor()
		stringIn = "SELECT username FROM Users Where userId = " +str(row[2])+";"
		cursor2.execute(stringIn)
		username = "hello"
		for name in cursor2:
			username = name[0]
		print row[5]
		word = (row[1].decode("utf-8"))
		other = word.encode("ascii","ignore")
		somedict[row[0]] = {"post":word, "userID":username, "tagname":row[3], "karma":row[5]}
#	 	lists.append(thislist)
	haha = json.dumps(somedict)
	return haha

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
