#encoding=utf-8
import os
import urllib2
import urllib
import webbrowser
import threading  
import gobject
import gtk
import pygtk
import dbmanager
import learnspider

gobject.threads_init()

class PyApp(gtk.Window): 
	def __init__(self):
		super(PyApp, self).__init__()

		self.open_connectdb_dialog()

		#dbmanager.setAllIsRead(True)

	def on_connectdb_succeed(self):

		self.starting = True

		self.set_size_request(800, 480)
		self.set_position(gtk.WIN_POS_CENTER)
		
		self.connect("destroy", self.onExit)
		self.set_title("清华大学网络学堂")
		if os.path.dirname(__file__) == '':
			self.set_icon_from_file("toast.png")
		else:
			self.set_icon_from_file(os.path.dirname(__file__) + "/toast.png")
		self.set_border_width(5)

		hbox = gtk.HBox(False, 5)
		hboxtools = gtk.HBox(False, 0)
		btnrefresh = gtk.Button('刷新')
		btnrefresh.set_size_request(60, 30)
		btnrefresh.connect('clicked',self.on_btnrefresh_clicked)
		btnpref = gtk.Button('选项')
		btnpref.set_size_request(60, 30)
		btnpref.connect('clicked',self.on_btnpref_clicked)
		btngoto = gtk.Button('前往')
		btngoto.set_size_request(60, 30)
		btngoto.connect('clicked',self.on_btngoto_clicked)
		hboxtools.add(btnrefresh)
		hboxtools.add(btnpref)
		hboxtools.add(btngoto)

		# Create a new notebook, place the position of the tabs
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.notebook.connect("switch-page", self.on_page_switched)

		#courses view
		self.swcourses = gtk.ScrolledWindow()
		self.swcourses.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.swcourses.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.coursesview = gtk.TreeView()
		self.coursesview.connect("cursor-changed", self.on_course_changed)
		self.coursesview.set_rules_hint(True)
		self.coursesview.set_headers_visible(False)
		self.coursesview.set_reorderable(False)
		self.create_treeview_columns(self.coursesview,['Courese'])
		self.swcourses.add(self.coursesview)
		vboxcourses = gtk.VBox(False, 0)
		vboxcourses.set_size_request(200,480)
		vboxcourses.set_homogeneous(False)
		vboxcourses.pack_start(hboxtools, False, False, 0)
		vboxcourses.pack_start(self.swcourses, True, True, 0)

		#notices view
		self.swnotices = gtk.ScrolledWindow()
		self.swnotices.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.swnotices.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.noticesview = gtk.TreeView()
		self.noticesview.connect('row-activated',self.on_notice_activated)
		self.noticesview.set_rules_hint(True)
		self.noticesview.set_reorderable(False)
		self.create_treeview_columns(self.noticesview,['R','课程','标题','发布者','发布时间','地址'])
		self.swnotices.add(self.noticesview)
		vboxnotices = gtk.VBox(False, 0)
		vboxnotices.pack_start(self.swnotices, True, True, 0)

		#documents view
		self.swdocuments = gtk.ScrolledWindow()
		self.swdocuments.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.swdocuments.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.documentsview = gtk.TreeView()
		self.documentsview.connect('row-activated',self.on_document_activated)
		self.documentsview.set_rules_hint(True)
		self.documentsview.set_reorderable(False)
		self.create_treeview_columns(self.documentsview,['R','课程','标题','说明','文件大小','上传时间','地址'])
		self.swdocuments.add(self.documentsview)
		vboxdocuments = gtk.VBox(False, 0)
		vboxdocuments.pack_start(self.swdocuments, True, True, 0)

		#assignments view
		self.swassignments = gtk.ScrolledWindow()
		self.swassignments.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.swassignments.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.assignmentsview = gtk.TreeView()
		self.assignmentsview.connect('row-activated',self.on_assignment_activated)
		self.assignmentsview.set_rules_hint(True)
		self.assignmentsview.set_reorderable(False)
		self.create_treeview_columns(self.assignmentsview,['R','课程','题目','发布时间','截止时间','提交状态','附件大小','地址'])
		self.swassignments.add(self.assignmentsview)
		vboxassignments = gtk.VBox(False, 0)
		vboxassignments.pack_start(self.swassignments, True, True, 0)

		#discussions view
		self.swdiscussions = gtk.ScrolledWindow()
		self.swdiscussions.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.swdiscussions.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.discussionsview = gtk.TreeView()
		self.discussionsview.connect('row-activated',self.on_discussion_activated)
		self.discussionsview.set_rules_hint(True)
		self.discussionsview.set_reorderable(False)
		self.create_treeview_columns(self.discussionsview,['R','课程','主题','作者','回复数','创建时间','地址'])
		self.swdiscussions.add(self.discussionsview)
		vboxdiscussions = gtk.VBox(False, 0)
		vboxdiscussions.pack_start(self.swdiscussions, True, True, 0)

		#add pages to notebook
		self.notebook.append_page(vboxnotices, gtk.Label('公告'))
		self.notebook.append_page(vboxdocuments, gtk.Label('文件'))
		self.notebook.append_page(vboxassignments, gtk.Label('作业'))
		self.notebook.append_page(vboxdiscussions, gtk.Label('讨论'))


		hbox.set_homogeneous(False)
		hbox.pack_start(vboxcourses, False, False, 0)
		hbox.pack_start(self.notebook, True, True, 0)
		self.add(hbox)
		self.show_all()

		self.createui()

		self.starting = False

	def createui(self):
		#create view content
		self.create_courses_store()
		self.coursesview.set_cursor((1,))
		
		
	def create_courses_store(self):
		store = gtk.ListStore(str)
		self.courses = dbmanager.readCoursesdb()

		store.append(['未读消息'])
		for item in self.courses:
			store.append([item[1]])
		self.coursesview.set_model(store)

	def create_notices_store(self,courseid):
		store = gtk.ListStore(str, str, str, str, str, str)
		if courseid == None:
			results = dbmanager.readUnReadNoticesdb()
		else:
			results = dbmanager.readNoticesdb(courseid)

		for item in results:
			if item[0] == 0:
				isread = 'N'
			else:
				isread = ''
			store.append([isread,item[1],item[2],item[3],item[4],item[5]])
		self.noticesview.set_model(store)
		self.noticesview.columns_autosize()

	def create_documents_store(self,courseid):
		store = gtk.ListStore(str, str, str, str, str, str, str)
		if courseid == None:
			results = dbmanager.readUnReadDocumentsdb()
		else:
			results = dbmanager.readDocumentsdb(courseid)

		for item in results:
			if item[0] == 0:
				isread = 'N'
			else:
				isread = ''
			store.append([isread,item[1],item[2],item[3],item[4],item[5],item[6]])
		self.documentsview.set_model(store)
		self.documentsview.columns_autosize()

	def create_assignments_store(self,courseid):
		store = gtk.ListStore(str, str, str, str, str, str, str, str)
		if courseid == None:
			results = dbmanager.readUnReadAssignmentsdb()
		else:
			results = dbmanager.readAssignmentsdb(courseid)

		for item in results:
			if item[0] == 0:
				isread = 'N'
			else:
				isread = ''
			store.append([isread,item[1],item[2],item[3],item[4],item[5],item[6],item[7]])
		self.assignmentsview.set_model(store)
		self.assignmentsview.columns_autosize()

	def create_discussions_store(self,courseid):
		store = gtk.ListStore(str, str, str, str, str, str, str)
		if courseid == None:
			results = dbmanager.readUnReadDiscussionsdb()
		else:
			results = dbmanager.readDiscussionsdb(courseid)

		for item in results:
			if item[0] == 0:
				isread = 'N'
			else:
				isread = ''
			store.append([isread,item[1],item[2],item[3],item[4],item[5],item[6]])
		self.discussionsview.set_model(store)
		self.discussionsview.columns_autosize()

	def create_treeview_columns(self, treeview, columns):
		i = 0
		for item in columns:
			rendererText = gtk.CellRendererText()
			column = gtk.TreeViewColumn(item, rendererText, text=i)
			column.set_sort_column_id(i)
			treeview.append_column(column)
			i+=1

	def on_course_changed(self, treeview):
		if self.coursesview == None or self.coursesview.get_cursor()[0] == None:
			return
		i = self.coursesview.get_cursor()[0][0]
		if i > 0:
			courseid = self.courses[i-1][0]
		else:
			courseid = None
		page = self.notebook.get_current_page()
		if page == 0:
			self.create_notices_store(courseid)
		elif page== 1:
			self.create_documents_store(courseid)
		elif page== 2:
			self.create_assignments_store(courseid)
		elif page== 3:
			self.create_discussions_store(courseid)

	def on_page_switched(self, notebook, page, page_num):
		if not self.starting:
			i = self.coursesview.get_cursor()[0][0]
			if i > 0:
				courseid = self.courses[i-1][0]
			else:
				courseid = None
			if page_num == 0:
				self.create_notices_store(courseid)
			elif page_num == 1:
				self.create_documents_store(courseid)
			elif page_num == 2:
				self.create_assignments_store(courseid)
			elif page_num == 3:
				self.create_discussions_store(courseid)

	def on_notice_activated(self, treeview, path, view_column):
		store = treeview.get_model()
		url = store[path[0]][5]
		if store[path[0]][0] == 'N':
			store[path[0]][0] = ''
			dbmanager.setNoticeIsRead(True,url)
		else:
			store[path[0]][0] = 'N'
			dbmanager.setNoticeIsRead(False,url)
		
	def on_document_activated(self, treeview, path, view_column):
		store = treeview.get_model()
		url = store[path[0]][6]
		if store[path[0]][0] == 'N':
			store[path[0]][0] = ''
			dbmanager.setDocumentIsRead(True,url)
		else:
			store[path[0]][0] = 'N'
			dbmanager.setDocumentIsRead(False,url)

	def on_assignment_activated(self, treeview, path, view_column):
		store = treeview.get_model()
		url = store[path[0]][7]
		if store[path[0]][0] == 'N':
			store[path[0]][0] = ''
			dbmanager.setAssignmentIsRead(True,url)
		else:
			store[path[0]][0] = 'N'
			dbmanager.setAssignmentIsRead(False,url)

	def on_discussion_activated(self, treeview, path, view_column):
		store = treeview.get_model()
		url = store[path[0]][6]
		if store[path[0]][0] == 'N':
			store[path[0]][0] = ''
			dbmanager.setDiscussionIsRead(True,url)
		else:
			store[path[0]][0] = 'N'
			dbmanager.setDiscussionIsRead(False,url)
		
	def onExit(self, b):
		dbmanager.closedb()
		gtk.main_quit()

	def on_btnrefresh_clicked(self, button):
		self.open_refresh_dialog()
	
	def start_refresh(self):
		self.set_refresh_dialog('正在更新...请勿关闭对话框')
		username = self.username.get_text()
		password = self.password.get_text()
		self.refresh_start_btn.set_sensitive(False)
		t = MyThread(self,username,password)  
		t.start()
	
	def open_refresh_dialog(self):
		self.refresh_label = gtk.Label("请输入用户名和密码")
		
		self.username = gtk.Entry()
		self.username.set_text('chenchuang12')

		self.password = gtk.Entry()
		self.password.set_visibility(False)

		self.refresh_start_btn = gtk.Button("开始")
		self.refresh_start_btn.connect('clicked',self.on_btn_startrefresh_clicked)

		valign1 = gtk.Alignment(0.5, 1, 1, 0)
		valign1.set_padding(20, 20, 0, 0)
		valign1.add(self.refresh_label)
		valign2 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign2.add(self.username)
		valign3 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign3.add(self.password)
		valign4 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign4.add(self.refresh_start_btn)

		self.dialog = gtk.Dialog("更新",self,gtk.DIALOG_MODAL)
		self.dialog.connect('destroy',self.on_dialog_refresh_close)
		self.dialog.vbox.set_size_request(300,200)
		self.dialog.vbox.pack_start(valign1)
		self.dialog.vbox.pack_start(valign2)
		self.dialog.vbox.pack_start(valign3)
		self.dialog.vbox.pack_start(valign4)
		self.dialog.show_all()	
		self.dialog.run()

	def on_btn_startrefresh_clicked(self, button):
		if self.refresh_start_btn.get_label() == '开始':
			self.start_refresh()
		else:
			self.dialog.destroy()		

	def on_dialog_refresh_close(self, dialog):
		self.set_refresh_dialog('正在停止，请稍侯...')
		print '正在停止更新，请稍侯...'
		learnspider.quit = True
		while not learnspider.quit_succeed:
			pass
		print '更新已停止'		

	def set_refresh_dialog(self,text):
		self.refresh_label.set_text(text)
		self.refresh_start_btn.set_sensitive(True)

	def on_btnpref_clicked(self, button):
		self.open_pref_dialog()

	def on_btngoto_clicked(self, button):
		page = self.notebook.get_current_page()
		if page == 0:
			path = self.noticesview.get_cursor()[0]
			store = self.noticesview.get_model()
			url = store[path[0]][5]
			pre = learnspider.NOTICE_PRE
		elif page== 1:
			path = self.documentsview.get_cursor()[0]
			store = self.documentsview.get_model()
			url = store[path[0]][6]
			pre = learnspider.DOCUMENT_PRE
		elif page== 2:
			path = self.assignmentsview.get_cursor()[0]
			store = self.assignmentsview.get_model()
			url = store[path[0]][7]
			pre = learnspider.ASSIGNMENT_PRE
		elif page== 3:
			path = self.discussionsview.get_cursor()[0]
			store = self.discussionsview.get_model()
			url = store[path[0]][6]
			pre = learnspider.DISCUSSION_PRE
		webbrowser.open_new_tab(pre + urllib.quote(url,'/?=:&%'))
		
	def on_btncleardb_clicked(self, button):
		dbmanager.cleardb()
		self.createui()

	def on_btnsetallread_clicked(self, button):
		dbmanager.setAllIsRead(True)
		self.createui()

	def open_pref_dialog(self):

		self.cleardb_btn = gtk.Button("清空数据库")
		self.cleardb_btn.connect('clicked',self.on_btncleardb_clicked)
		self.setallread_btn = gtk.Button("全部设为已读")
		self.setallread_btn.connect('clicked',self.on_btnsetallread_clicked)

		valign1 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign1.add(self.cleardb_btn)
		valign2 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign2.add(self.setallread_btn)

		self.dialog = gtk.Dialog("更新",self,gtk.DIALOG_MODAL)
		self.dialog.vbox.set_size_request(300,100)
		self.dialog.vbox.pack_start(valign1)
		self.dialog.vbox.pack_start(valign2)
		self.dialog.show_all()
		self.dialog.run()

	def open_connectdb_dialog(self):
		self.isdbconnected = False

		self.connectdb_label = gtk.Label("请输入数据库用户名和密码")
		
		self.dbip = gtk.Entry()
		self.dbip.set_text('127.0.0.1')

		self.dbusername = gtk.Entry()
		self.dbusername.set_text('root')

		self.dbpassword = gtk.Entry()
		self.dbpassword.set_visibility(False)

		self.connectdb_btn = gtk.Button("连接")
		self.connectdb_btn.connect('clicked',self.on_btn_connectdb_clicked)

		valign1 = gtk.Alignment(0.5, 1, 1, 0)
		valign1.set_padding(20, 20, 0, 0)
		valign1.add(self.connectdb_label)
		valign2 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign2.add(self.dbip)
		valign3 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign3.add(self.dbusername)
		valign4 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign4.add(self.dbpassword)
		valign5 = gtk.Alignment(0.5, 1, 0.5, 0)
		valign5.add(self.connectdb_btn)

		self.dialog = gtk.Dialog("连接数据库",self,gtk.DIALOG_MODAL)
		self.dialog.vbox.set_size_request(300,250)
		self.dialog.vbox.pack_start(valign1)
		self.dialog.vbox.pack_start(valign2)
		self.dialog.vbox.pack_start(valign3)
		self.dialog.vbox.pack_start(valign4)
		self.dialog.vbox.pack_start(valign5)
		self.dialog.connect('destroy',self.on_dialog_connectdb_close)
		self.dialog.show_all()	
		self.dialog.run()

	def on_btn_connectdb_clicked(self, button):
		try:
			dbmanager.connectdb(self.dbip.get_text(), self.dbusername.get_text(), self.dbpassword.get_text())
			self.isdbconnected = True
			self.dialog.destroy()
			self.on_connectdb_succeed()
		except Exception,e:
			print str(e)
			md = gtk.MessageDialog(self,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE, "数据库连接错误")
			md.run()
			md.destroy()

	def on_dialog_connectdb_close(self, dialog):
		if not self.isdbconnected:
			gtk.main_quit()
		

class MyThread(threading.Thread):  
	def __init__(self, pyapp, username, password):  
		super(MyThread, self).__init__()  
		self.pyapp = pyapp
		self.username = username
		self.password = password
		self.succeed = False
   
	def refreshui(self):
		if self.succeed:
			self.pyapp.createui()
			self.pyapp.set_refresh_dialog('更新完成')
			self.pyapp.refresh_start_btn.set_label('关闭')
		else:
			self.pyapp.set_refresh_dialog('错误～请检查或重启程序')
		return False
   
	def run(self):   
		try:
			learnspider.spidermove(self.username, self.password)
			self.succeed = True
		except Exception,e:
			print str(e)
			self.succeed = False
			learnspider.quit_succeed = True
		#只能在主线程中修改UI
		gobject.idle_add(self.refreshui)


PyApp()
gtk.main()

