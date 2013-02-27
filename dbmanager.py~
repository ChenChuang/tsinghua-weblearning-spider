#encoding=utf-8
import MySQLdb
from parsers import CoursesParser, NoticesParser, DocumentsParser, AssignmentsParser, DiscussionsParser

conn = None
cursor = None

def connectdb():
	global conn
	global cursor

	conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="learnspiderdb",charset="utf8")  
	cursor = conn.cursor()

def closedb():
	global conn
	global cursor

	cursor.close()  
	conn.close()

def cleardb():
	global conn
	global cursor

	sql='truncate table COURSES'
	n = cursor.execute(sql)
	conn.commit()
	sql='truncate table NOTICES'
	n = cursor.execute(sql)
	conn.commit()
	sql='truncate table DOCUMENTS'
	n = cursor.execute(sql)
	conn.commit()
	sql='truncate table ASSIGNMENTS'
	n = cursor.execute(sql)
	conn.commit()
	sql='truncate table DISCUSSIONS'
	n = cursor.execute(sql)
	conn.commit()
	

def refreshCoursesdb(coursesparser):
	global conn
	global cursor

	n = cursor.execute("select CourseID from COURSES")
	results = cursor.fetchall();
	ids = coursesparser.ids;
	names = coursesparser.names;
	added = []
	for i in range(0,len(ids)):
		if results.count((ids[i],)) == 0:
			added.append([ids[i],names[i]])
			sql = "insert into COURSES(CourseID, Name) values(%s,%s)"   
			param = (ids[i],names[i])
			n = cursor.execute(sql,param)
			conn.commit()
	for item in results:
		if ids.count(item[0]) == 0:
			sql = "delete from COURSES where CourseID=%s"   
			param =(item)
			n = cursor.execute(sql,param) 
			conn.commit()
	return added   

def refreshNoticesdb(noticesparser, courseid, coursename):
	global conn
	global cursor

	n = cursor.execute("select Url from NOTICES where CourseID=%s",(courseid))
	tresults = cursor.fetchall();
	results = []
	for item in tresults:
		results.append(item[0])

	urls = noticesparser.urls;
	headings = noticesparser.headings;
	publishers = noticesparser.publishers;
	times = noticesparser.times;
	added = []
	
	for i in range(0,len(urls)):
		try:
			results.remove(unicode(urls[i],'utf8'))
			sql = "update NOTICES set Heading=%s, Publisher=%s, Time=%s, CourseID=%s where Url=%s"
			param = (headings[i],publishers[i],times[i],courseid,urls[i])
			n = cursor.execute(sql,param)
			conn.commit()
		except ValueError,e:
			added.append([headings[i],urls[i],publishers[i],times[i],coursename])
			sql = "insert into NOTICES(Heading, Url, Publisher, Time, CourseID, IsRead) values(%s,%s,%s,%s,%s,%s)"
			param = (headings[i],urls[i],publishers[i],times[i],courseid,0)
			n = cursor.execute(sql,param)
			conn.commit()
	for item in results:
		sql = "delete from NOTICES where Url=%s"   
		param =(item)
		n = cursor.execute(sql,param) 
		conn.commit()
	return added

def refreshDocumentsdb(documentsparser, courseid, coursename):
	global conn
	global cursor

	n = cursor.execute("select Url from DOCUMENTS where CourseID=%s",(courseid))
	tresults = cursor.fetchall();
	results = []
	for item in tresults:
		results.append(item[0])

	urls = documentsparser.urls;
	headings = documentsparser.headings;
	explanations = documentsparser.explanations;
	sizes = documentsparser.sizes;
	times = documentsparser.times;
	added = []

	for i in range(0,len(urls)):
		try:
			results.remove(unicode(urls[i],'utf8'))
			sql = "update DOCUMENTS set Heading=%s, Explanation=%s, DocSize=%s, Time=%s, CourseID=%s where Url=%s"
			param = (headings[i],explanations[i],sizes[i],times[i],courseid,urls[i])
			n = cursor.execute(sql,param)
			conn.commit()
		except ValueError,e:
			added.append([headings[i],urls[i],explanations[i],sizes[i],times[i],coursename])
			sql = "insert into DOCUMENTS(Heading, Url, Explanation, DocSize, Time, CourseID, IsRead) values(%s,%s,%s,%s,%s,%s,%s)"
			param = (headings[i],urls[i],explanations[i],sizes[i],times[i],courseid,0)
			n = cursor.execute(sql,param)
			conn.commit()
	for item in results:
		sql = "delete from DOCUMENTS where Url=%s"   
		param =(item)
		n = cursor.execute(sql,param) 
		conn.commit()
	return added

def refreshAssignmentsdb(assignmentsparser, courseid, coursename):
	global conn
	global cursor

	n = cursor.execute("select Url from ASSIGNMENTS where CourseID=%s",(courseid))
	tresults = cursor.fetchall();
	results = []
	for item in tresults:
		results.append(item[0])

	urls = assignmentsparser.urls;
	titles = assignmentsparser.titles;
	startdates = assignmentsparser.startdates;
	duedates = assignmentsparser.duedates;
	statuses = assignmentsparser.statuses;
	sizes = assignmentsparser.sizes;
	added = []

	for i in range(0,len(urls)):
		try:
			results.remove(unicode(urls[i],'utf8'))
			sql = "update ASSIGNMENTS set Title=%s, StartDate=%s, DueDate=%s, Status=%s, AttSize=%s, CourseID=%s where Url=%s"
			param = (titles[i],startdates[i],duedates[i],statuses[i],sizes[i],courseid,urls[i])
			n = cursor.execute(sql,param)
			conn.commit()
		except ValueError,e:
			added.append([titles[i],urls[i],startdates[i],duedates[i],statuses[i],sizes[i],coursename])
			sql = "insert into ASSIGNMENTS(Title, Url, StartDate, DueDate, Status, AttSize, CourseID, IsRead) values(%s,%s,%s,%s,%s,%s,%s,%s)"
			param = (titles[i],urls[i],startdates[i],duedates[i],statuses[i],sizes[i],courseid,0)
			n = cursor.execute(sql,param)
			conn.commit()
	for item in results:
		sql = "delete from ASSIGNMENTS where Url=%s"   
		param =(item)
		n = cursor.execute(sql,param) 
		conn.commit()
	return added

def refreshDiscussionsdb(discussionsparser, courseid, coursename):
	global conn
	global cursor

	n = cursor.execute("select Url from DISCUSSIONS where CourseID=%s",(courseid))
	tresults = cursor.fetchall();
	results = []
	for item in tresults:
		results.append(item[0])

	urls = discussionsparser.urls;
	subjects = discussionsparser.subjects;
	authors = discussionsparser.authors;
	replynums = discussionsparser.replynums;
	times = discussionsparser.times;
	added = []

	for i in range(0,len(urls)):
		try:
			results.remove(unicode(urls[i],'utf8'))
			sql = "update DISCUSSIONS set Subject=%s, Author=%s, ReplyNum=%s, Time=%s, CourseID=%s where Url=%s"
			param = (subjects[i],authors[i],replynums[i],times[i],courseid,urls[i])
			n = cursor.execute(sql,param)
			conn.commit()
		except ValueError,e:
			added.append([subjects[i],urls[i],authors[i],replynums[i],times[i],coursename])
			sql = "insert into DISCUSSIONS(Subject, Url, Author, ReplyNum, Time, CourseID, IsRead) values(%s,%s,%s,%s,%s,%s,%s)"
			param = (subjects[i],urls[i],authors[i],replynums[i],times[i],courseid,0)
			n = cursor.execute(sql,param)
			conn.commit()
	for item in results:
		sql = "delete from DISCUSSIONS where Url=%s"   
		param =(item)
		n = cursor.execute(sql,param) 
		conn.commit()
	return added

def readNoticesdb(courseid):
	sql = "select IsRead,Name,Heading,Publisher,Time,Url from NOTICES,COURSES where NOTICES.CourseID=%s and COURSES.CourseID=%s"
	param = (courseid, courseid)
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readDocumentsdb(courseid):
	sql = "select IsRead,Name,Heading,Explanation,DocSize,Time,Url from DOCUMENTS,COURSES where DOCUMENTS.CourseID=%s and COURSES.CourseID=%s"
	param = (courseid, courseid)
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readAssignmentsdb(courseid):
	sql = "select IsRead,Name,Title,StartDate,DueDate,Status,AttSize,Url from ASSIGNMENTS,COURSES where ASSIGNMENTS.CourseID=%s and COURSES.CourseID=%s"
	param = (courseid, courseid)
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readDiscussionsdb(courseid):
	sql = "select IsRead,Name,Subject,Author,ReplyNum,Time,Url from DISCUSSIONS,COURSES where DISCUSSIONS.CourseID=%s and COURSES.CourseID=%s"
	param = (courseid, courseid)
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readUnReadNoticesdb():
	sql = "select IsRead,Name,Heading,Publisher,Time,Url from NOTICES,COURSES where NOTICES.CourseID=COURSES.CourseID and NOTICES.IsRead=0"
	param = ()
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readUnReadDocumentsdb():
	sql = "select IsRead,Name,Heading,Explanation,DocSize,Time,Url from DOCUMENTS,COURSES where DOCUMENTS.CourseID=COURSES.CourseID and DOCUMENTS.IsRead=0"
	param = ()
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readUnReadAssignmentsdb():
	sql = "select IsRead,Name,Title,StartDate,DueDate,Status,AttSize,Url from ASSIGNMENTS,COURSES where ASSIGNMENTS.CourseID=COURSES.CourseID and ASSIGNMENTS.IsRead=0"
	param = ()
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readUnReadDiscussionsdb():
	sql = "select IsRead,Name,Subject,Author,ReplyNum,Time,Url from DISCUSSIONS,COURSES where DISCUSSIONS.CourseID=COURSES.CourseID and DISCUSSIONS.IsRead=0"
	param = ()
	n = cursor.execute(sql, param)
	results = cursor.fetchall();
	return results

def readCoursesdb():
	n = cursor.execute("select CourseID,Name from COURSES")
	results = cursor.fetchall();
	return results

def setNoticeIsRead(isread,url):
	if isread:
		value = 1
	else:
		value = 0
	sql = "update NOTICES set IsRead=%s where Url=%s"
	param = (value,url)
	n = cursor.execute(sql,param)
	conn.commit()

def setDocumentIsRead(isread,url):
	if isread:
		value = 1
	else:
		value = 0
	sql = "update DOCUMENTS set IsRead=%s where Url=%s"
	param = (value,url)
	n = cursor.execute(sql,param)
	conn.commit()

def setAssignmentIsRead(isread,url):
	if isread:
		value = 1
	else:
		value = 0
	sql = "update ASSIGNMENTS set IsRead=%s where Url=%s"
	param = (value,url)
	n = cursor.execute(sql,param)
	conn.commit()

def setDiscussionIsRead(isread,url):
	if isread:
		value = 1
	else:
		value = 0
	sql = "update DISCUSSIONS set IsRead=%s where Url=%s"
	param = (value,url)
	n = cursor.execute(sql,param)
	conn.commit()

def setAllIsRead(isread):
	if isread:
		value = 1
	else:
		value = 0
	param = (value)
	sql = "update NOTICES set IsRead=%s"
	n = cursor.execute(sql,param)
	conn.commit()
	sql = "update DOCUMENTS set IsRead=%s"
	n = cursor.execute(sql,param)
	conn.commit()
	sql = "update ASSIGNMENTS set IsRead=%s"
	n = cursor.execute(sql,param)
	conn.commit()
	sql = "update DISCUSSIONS set IsRead=%s"
	n = cursor.execute(sql,param)
	conn.commit()
	 
