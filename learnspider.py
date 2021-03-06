#encoding=utf-8
import urllib2
import urllib
import socket
import cookielib
import gobject
import gtk
import pygtk
import dbmanager
from parsers import CoursesParser, NoticesParser, DocumentsParser, AssignmentsParser, DiscussionsParser

cookie = None
opener = None
host = "http://learn.tsinghua.edu.cn/"
NOTICE_PRE = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/"
DOCUMENT_PRE = "http://learn.tsinghua.edu.cn"
ASSIGNMENT_PRE = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/"
DISCUSSION_PRE = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/"

quit = False
quit_succeed = False

def spidermove(username,password):
	global quit_succeed

	socket.setdefaulttimeout(5)
	quit_succeed = False

	print "正在登录..."
	login(username,password)
	print "登录成功"

	#dbmanager.connectdb()
	print "正在读取数据..."
	readcourses()
	print "数据读取完成"
	#dbmanager.closedb()
	
	cookie = None
	opener = None

	quit_succeed = True

def login(user,password):
	global cookie
	global opener

	LOGIN_PAGE_1 = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp"
	LOGIN_PAGE_2 = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher_action.jsp"
	LOGIN_PAGE_3 = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/mainteacher.jsp"
	LOGIN_PAGE_4 = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/mainstudent.jsp"

	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	opener.addheaders = [('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:17.0) Gecko/17.0 Firefox/17.0')]
	data = urllib.urlencode({"userid":user,"userpass":password})

	if not quit: 
		opener.open(LOGIN_PAGE_1,data)
	if not quit: 
		opener.open(LOGIN_PAGE_2)
	if not quit: 
		opener.open(LOGIN_PAGE_3)
	if not quit: 
		opener.open(LOGIN_PAGE_4)

def readcourses():
	global cookie
	global opener

	COURSES_PAGE = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn"
	
	print "正在读取：所有课程名称..."
	data = opener.open(COURSES_PAGE).read()
	coursesparser = CoursesParser()
	coursesparser.feed(data)
	dbmanager.refreshCoursesdb(coursesparser)

	for i in range(0,len(coursesparser.urls)):
		print '------',coursesparser.names[i],'------'
		print "正在读取：课程公告..."
		if not quit: 
			readNoticesbyCourse(coursesparser.ids[i], coursesparser.names[i]);
		print "正在读取：课程文件..."
		if not quit: 
			readDocumentsbyCourse(coursesparser.ids[i], coursesparser.names[i]);
		print "正在读取：课程作业..."
		if not quit: 
			readAssignmentsbyCourse(coursesparser.ids[i], coursesparser.names[i]);
		print "正在读取：课程讨论..."
		if not quit: 
			readDiscussionsbyCourse(coursesparser.ids[i], coursesparser.names[i]);


def readNoticesbyCourse(courseid, coursename):
	global cookie
	global opener

	NOTICE_PAGE = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id=" + courseid

	data = opener.open(NOTICE_PAGE).read()
	noticesparser = NoticesParser()
	noticesparser.feed(data)
	dbmanager.refreshNoticesdb(noticesparser, courseid, coursename)
	#for i in range(0,len(noticesparser.urls)):
	#	print noticesparser.headings[i] + ',' + noticesparser.publishers[i] + ',' + noticesparser.times[i] + ',' + noticesparser.urls[i]


def readDocumentsbyCourse(courseid, coursename):
	global cookie
	global opener

	DOCUMENT_PAGE = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id=" + courseid

	data = opener.open(DOCUMENT_PAGE).read()
	documentsparser = DocumentsParser()
	documentsparser.feed(data)
	dbmanager.refreshDocumentsdb(documentsparser, courseid, coursename)
	#for i in range(0,len(documentsparser.urls)):
	#	print documentsparser.headings[i] + ',' + documentsparser.explanations[i] + ',' + documentsparser.sizes[i] + ',' + documentsparser.times[i] + ',' + documentsparser.urls[i]


def readAssignmentsbyCourse(courseid, coursename):
	global cookie
	global opener

	ASSIGNMENT_PAGE = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_brw.jsp?course_id=" + courseid

	data = opener.open(ASSIGNMENT_PAGE).read()
	assignmentsparser = AssignmentsParser()
	assignmentsparser.feed(data)
	dbmanager.refreshAssignmentsdb(assignmentsparser, courseid, coursename)
	#for i in range(0,len(assignmentsparser.urls)):
	#	print assignmentsparser.titles[i] + ',' + assignmentsparser.startdates[i] + ',' + assignmentsparser.duedates[i] + ',' + assignmentsparser.statuses[i] + ',' + assignmentsparser.sizes[i] + ','+ assignmentsparser.urls[i]


def readDiscussionsbyCourse(courseid, coursename):
	global cookie
	global opener

	DISCUSSION_PAGE = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/gettalkid_student.jsp?course_id=" + courseid
	
	data = opener.open(DISCUSSION_PAGE).read()
	discussionsparser = DiscussionsParser()
	discussionsparser.feed(data)
	dbmanager.refreshDiscussionsdb(discussionsparser, courseid, coursename)
	#for i in range(0,len(discussionsparser.urls)):
	#	print discussionsparser.subjects[i] + ',' + discussionsparser.authors[i] + ',' + discussionsparser.replynums[i] + ',' + discussionsparser.times[i] + ',' + discussionsparser.urls[i]

#spidermove()

