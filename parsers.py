#encoding=utf-8
from sgmllib import SGMLParser

class CoursesParser(SGMLParser):
	def __init__(self):
		self.PRE_COURSE_HREF = '/MultiLanguage/lesson/student/course_locate.jsp?course_id'
		self.PRE_ID = 'course_id='
		SGMLParser.__init__(self)
	def reset(self):
		self.urls = []
		self.names = []
		self.ids = []
		self.is_course = False
		SGMLParser.reset(self)
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href' and (self.PRE_COURSE_HREF in v)]
		if href and len(href) == 1:
			self.urls.extend(href)
			self.ids.append( href[0][(href[0].find(self.PRE_ID) + len(self.PRE_ID)) : ])
			self.is_course = True
	def end_a(self):
		self.is_course = False
	def handle_data(self, text):
		if self.is_course:
			self.names.append(text[:text.find('(')].strip())

class NoticesParser(SGMLParser):
	def __init__(self):
		self.PRE_NOTICE_HREF = 'note_reply.jsp?bbs_type='
		SGMLParser.__init__(self)
	def reset(self):
		self.urls = []
		self.headings = []
		self.publishers = []
		self.times = []
		self.type = 0
		self.in_td = False
		self.tmpstr = ''
		SGMLParser.reset(self)
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href' and (self.PRE_NOTICE_HREF in v)]
		if href and len(href) == 1:
			self.urls.extend(href)
			self.type = 1
	def end_a(self):
		if self.type == 1:
			self.headings.append(self.tmpstr[:].strip())
	def start_td(self, attrs):
		self.in_td = (self.type > 0)
	def end_td(self):
		self.in_td = False
		if self.type == 1:
			self.type = 2
		elif self.type == 2:
			self.publishers.append(self.tmpstr[:].strip())
			self.type = 3
		elif self.type == 3:
			self.times.append(self.tmpstr[:].strip())
			self.type = 0
		self.tmpstr = ''
	def handle_data(self, text):
		if self.in_td or self.type == 1:
			self.tmpstr += text

class DocumentsParser(SGMLParser):
	def __init__(self):
		self.PRE_DOCUMENT_HREF = '/uploadFile/downloadFile_student.jsp?'
		SGMLParser.__init__(self)
	def reset(self):
		self.urls = []
		self.headings = []
		self.explanations = []
		self.sizes = []
		self.times = []
		self.type = 0
		self.in_td = False
		self.tmpstr = ''
		SGMLParser.reset(self)
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href' and (self.PRE_DOCUMENT_HREF in v)]
		if href and len(href) == 1:
			self.urls.extend(href)
			self.type = 1
	def end_a(self):
		if self.type == 1:
			self.headings.append(self.tmpstr[:].strip())
	def start_td(self, attrs):
		self.in_td = (self.type > 0)
	def end_td(self):
		self.in_td = False
		if self.type == 1:
			self.type = 2
		elif self.type == 2:
			self.explanations.append(self.tmpstr[:].strip())
			self.type = 3
		elif self.type == 3:
			self.sizes.append(self.tmpstr[:].strip())
			self.type = 4
		elif self.type == 4:
			self.times.append(self.tmpstr[:].strip())
			self.type = 0
		self.tmpstr = ''
	def handle_data(self, text):
		if self.in_td or self.type == 1:
			self.tmpstr += text

class AssignmentsParser(SGMLParser):
	def __init__(self):
		self.PRE_ASSIGNMENT_HREF = 'hom_wk_detail.jsp?'
		SGMLParser.__init__(self)
	def reset(self):
		self.urls = []
		self.titles = []
		self.startdates = []
		self.duedates = []
		self.statuses = []
		self.sizes = []
		self.type = 0
		self.in_td = False
		self.tmpstr = ''
		SGMLParser.reset(self)
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href' and (self.PRE_ASSIGNMENT_HREF in v)]
		if href and len(href) == 1:
			self.urls.extend(href)
			self.type = 1
	def end_a(self):
		if self.type == 1:
			self.titles.append(self.tmpstr[:].strip())
	def start_td(self, attrs):
		self.in_td = (self.type > 0)
	def end_td(self):
		self.in_td = False
		if self.type == 1:
			self.type = 2
		elif self.type == 2:
			self.startdates.append(self.tmpstr[:].strip())
			self.type = 3
		elif self.type == 3:
			self.duedates.append(self.tmpstr[:].strip())
			self.type = 4
		elif self.type == 4:
			self.statuses.append(self.tmpstr[:].strip())
			self.type = 5
		elif self.type == 5:
			self.sizes.append(self.tmpstr[:].strip())
			self.type = 0
		self.tmpstr = ''
	def handle_data(self, text):
		if self.in_td or self.type == 1:
			self.tmpstr += text

class DiscussionsParser(SGMLParser):
	def __init__(self):
		self.PRE_DISCUSSION_HREF = 'talk_reply_student.jsp?'
		SGMLParser.__init__(self)
	def reset(self):
		self.urls = []
		self.subjects = []
		self.authors = []
		self.replynums = []
		self.times = []
		self.type = 0
		self.in_td = False
		self.tmpstr = ''
		SGMLParser.reset(self)
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href' and (self.PRE_DISCUSSION_HREF in v)]
		if href and len(href) == 1:
			self.urls.extend(href)
			self.type = 1
	def end_a(self):
		if self.type == 1:
			self.subjects.append(self.tmpstr[:].strip())
	def start_td(self, attrs):
		self.in_td = (self.type > 0)
	def end_td(self):
		self.in_td = False
		if self.type == 1:
			self.type = 2
		elif self.type == 2:
			self.authors.append(self.tmpstr[:].strip())
			self.type = 3
		elif self.type == 3:
			self.replynums.append(self.tmpstr[:].strip().split('/')[0])
			self.type = 4
		elif self.type == 4:
			self.times.append(self.tmpstr[:].strip())
			self.type = 0
		self.tmpstr = ''
	def handle_data(self, text):
		if self.in_td or self.type == 1:
			self.tmpstr += text
