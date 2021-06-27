from notification import *
from platform import system
from subprocess import call

class ShutdownUi(QWidget):
	DEFAULT_TIME = "00:10:00"
	DAYS_SIZE = 27
	DEFAULT_SIZE = 51

	def __init__(self):
		super().__init__()
		self.w, self.h = 441, 286
		self.w_factor, self.h_factor = 1, 1
		self.setWindowIcon(QIcon("Assets/shutdown.png"))
		self.installEventFilter(self)
		self.setMinimumSize(self.w, self.h)
		self.setWindowTitle("Shutdown Timer")
		self.setStyleSheet("""background: #2f3542;""")
		self.init_ui()

	def init_ui(self):
		self.text_valid = True
		self.started = False
		self.old_input = []
		self.colon = [False, 0]
		self.reset_colon = False
		self.old_pos = False
		self.old_input_size = {}
		self.new_input_size = {}
		self.new_font, self.new_size = 0, ()
		self.widget_management()
		self.setup_stylesheet()
		self.layout_management()

	def widget_management(self):
		self.thread = Timer(parent=self)
		self.notification = Notification(self)
		self.thread.notif_signal.connect(self.show_notification)
		self.thread.finished_signal.connect(self.shutdown)
		self.info_text = QLabel("This computer will shutdown in")
		self.timer_font = QFont()
		self.timer_font.setFamily("Ms Shell Dlg 2")
		self.timer_font.setPointSize(52)
		self.timer = QLineEdit(self.DEFAULT_TIME, self)
		self.change_time = QPushButton(clicked=lambda: self.on_click(change_text=True))
		self.toggle_btn = QPushButton("Start", clicked=lambda: self.on_click(change_text=False))
		self.invalid_dialog = QDialog(self)
		self.err_msg = QLabel("Invalid Input!")
		self.ok_btn = QPushButton("Ok")

		self.info_text.setFont(QFont("MS Shell Dlg 2", 16))
		self.info_text.setStyleSheet("color: #ced6e0;")
		self.timer.setAlignment(Qt.AlignHCenter)
		self.timer.textChanged.connect(self.value_changed)
		self.timer.returnPressed.connect(lambda: self.on_click(change_text=True))
		self.timer.setReadOnly(True)
		self.change_time.setToolTip("Change current countdown")
		self.change_time.setCursor(QCursor(Qt.PointingHandCursor))
		self.change_time.setIcon(QIcon("Assets/settings.png"))
		self.change_time.setFixedSize(24, 24)
		self.change_time.setIcon(QIcon("Assets/change.png"))
		self.change_time.setIconSize(QSize(24, 24))
		self.toggle_btn.setCursor(QCursor(Qt.PointingHandCursor))
		self.toggle_btn.setFont(QFont("MS Shell Dlg 2", 14))
		self.toggle_btn.setFixedSize(101, 41)
		self.invalid_dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.invalid_dialog.setFixedSize(300, 100)
		self.err_msg.setFont(QFont("MS Shell Dlg 2", 14))
		self.ok_btn.setCursor(QCursor(Qt.PointingHandCursor))
		self.ok_btn.clicked.connect(self.invalid_dialog.close)
		self.ok_btn.setFont(QFont("MS Shell Dlg 2", 10))
		self.ok_btn.setFixedSize(60, 25)

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.timer_layout = QHBoxLayout()
		self.invalid_layout = QVBoxLayout()
		self.top_spacer = QSpacerItem(0, 25, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.center_spacer = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.left_spacer = QSpacerItem(65, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.right_spacer = QSpacerItem(35, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.bottom_spacer = QSpacerItem(0, 18, QSizePolicy.Fixed, QSizePolicy.Fixed)

		self.main_layout.addItem(self.top_spacer)
		self.main_layout.addWidget(self.info_text, alignment=Qt.AlignHCenter)
		self.timer_layout.addItem(self.left_spacer)
		self.timer_layout.addWidget(self.timer, alignment=Qt.AlignHCenter)
		self.timer_layout.addWidget(self.change_time)
		self.timer_layout.addItem(self.right_spacer)
		self.main_layout.addItem(self.center_spacer)
		self.main_layout.addLayout(self.timer_layout)
		self.main_layout.addItem(self.center_spacer)
		self.main_layout.addWidget(self.toggle_btn, alignment=Qt.AlignHCenter)
		self.main_layout.addItem(self.bottom_spacer)
		self.invalid_layout.addWidget(self.err_msg, alignment=Qt.AlignHCenter)
		self.invalid_layout.addWidget(self.ok_btn, alignment=Qt.AlignHCenter)
		self.invalid_dialog.setLayout(self.invalid_layout)
		self.setLayout(self.main_layout)

	def setup_stylesheet(self):
		self.timer.setStyleSheet("""color: #dfe4ea;
										 background: #2D323F;
										 border-radius: 10px;""")
		self.change_time.setStyleSheet("background: transparent;")
		self.invalid_dialog.setStyleSheet("""background: #dfe4ea;
											 border-radius: 8px;""")
		self.ok_btn.setStyleSheet("""background: transparent;
									border: 2px solid #ced6e0;""")
	def raise_error(self):
		QApplication.beep()
		self.change_mode()
		self.invalid_dialog.show()
		self.invalid_dialog.exec_()
		self.invalid_dialog.hide()

	def show_notification(self):
		self.hide()
		self.notification.showFullScreen()

	def change_mode(self):
		self.new_input_size["Font"] = self.timer_font.pointSize()-24
		self.new_input_size["Size"] = self.timer.width(), self.timer.height()
		if self.timer.isReadOnly():
			self.timer.setReadOnly(False)
			self.timer.setFocus(True)
			self.timer.deselect()
			text = self.timer.text()
			if len(text) > 8:
				new_text = self.get_time(text, reverse=True, is_str=True)
				self.timer.setCursorPosition(0)
				self.timer.setFixedSize(275*self.w_factor, 83*self.h_factor)
				self.timer_font.setPointSize(51*self.h_factor)
				self.timer.setFont(self.timer_font)
			else:
				new_text = self.timer_format(self.get_time(text, reverse=False))

			if new_text:
				self.timer.setText(new_text)
			self.old_input = list(self.timer.text())
		else:
			if 'day' in self.timer.text():
				#print(self.timer.rect())
				self.adapt_size(old=True, origin="change_mode; else")
			self.old_input = list(self.timer.text())
			self.timer.setReadOnly(True)


	def is_valid(self, text):
		result = False
		for char in text.split(':'):
			if char.isnumeric():
				result = True
			else:
				result = False
				break
		return result

	def value_changed(self, text):
		self.text_valid = self.is_valid(text)
		if self.colon[0] or not self.reset_colon:
			if text.count(':') != 2:
				self.reset_colon = True
				self.old_pos = self.timer.cursorPosition()
				self.timer.setText(''.join(self.old_input[:self.colon[1]+len(self.old_input)]))
				self.timer.setCursorPosition(self.old_pos+1)
			else:
				try:
					if self.old_input and self.old_input[2] == ':':
						if len(text) != 5 and self.text_valid:
							self.old_input = list(text)
				except:
					if len(text) != 5 and self.text_valid:
						self.old_input = list(text)
		else:
			if len(text) != 5 and self.text_valid:
				self.old_input = list(text)
			if self.colon:
				self.colon = [False, 0]
				self.reset_colon = False

	def timer_format(self, s=None, d=None):
		time_format = str(timedelta(seconds=self.get_time(self.timer.text()) if not s else s))
		if 'days' not in time_format or 'day' not in time_format:
			if len(time_format.split(":")[0]) == 1:
				time_format = f"0{time_format}"
		else:
			old = time_format.split(",")
			if len(old[1][1:][:-6]) == 1:
				time_format = f"{old[0]}, 0{old[1][1:]}"

		return time_format

	def get_time(self, text, reverse=False, is_str=False):
		values = []
		if not reverse:
			for index, nums in enumerate(text.split(":")):
				if nums[0] == "0" and len(nums) >1:
					nums = int(nums[1:])
				else:
					nums = int(nums)

				values.append(nums)

		else:
			text = text.split()
			hours = int(text[0])*24 + int(text[2][:-6])
			try:
				minutes = int(text[2][3:5])
			except:
				minutes = int(text[2][2:4])
			seconds = int(text[2][6:])
			values.append(hours)
			values.append(minutes)
			values.append(seconds)

		if is_str:
			return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
		return sum([values[0]*60*60, values[1]*60, values[2]])

	@pyqtSlot()
	def shutdown(self):
		self.started = False
		self.toggle_btn.setText("Start")
		self.notification.hide()
		if system() == 'Windows':
			call("shutdown /s")
		elif system() == 'Linux':
			call("shutdown")
		elif system() == 'Darwin':
			pass

	def on_click(self, change_text=False):
		text = self.timer.text()
		if change_text:
			if not self.timer.isReadOnly():
				self.text_valid = self.is_valid(text)
			self.change_text(text)
		else:
			if self.started:
				QTimer.singleShot(50, self.thread.stop)
			else:
				self.started = True
				self.thread.seconds = self.get_time(self.timer.text(), reverse=True if 'day' in text else False)
				QTimer.singleShot(50, self.thread.start)
				self.toggle_btn.setText("Stop")

	def change_text(self, new):
		if self.text_valid:
			time_format = self.timer_format(self.get_time(new))
			self.timer.setText(time_format)
			if ',' in time_format and not self.old_input_size:
				self.adapt_size(origin="AXA")
			elif self.old_input_size:
				if self.new_size:
					self.timer.setFixedSize(self.new_size[0], self.new_size[1])
					self.timer_font.setPointSize(self.new_font)
				else:
					self.timer.setFixedSize(self.old_input_size["Size"][0], self.old_input_size["Size"][1])
					self.timer_font.setPointSize(self.old_input_size["Font"])
				self.timer.setFont(self.timer_font)

			self.change_mode()
		elif ',' in new:
			self.change_mode()
		else:
			self.timer.setText(''.join(self.old_input))
			self.raise_error()

	def eventFilter(self, obj, event):
		if (event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton):
			print(self.timer.rect())
			if obj != self.timer:
				if not self.timer.isReadOnly():
					text = self.timer.text()
					self.text_valid = self.is_valid(text)
					self.change_text(text)
		elif (event.type() == QEvent.WindowStateChange):
			if self.windowState() & Qt.WindowMaximized:
				print("A")
				print(self.old_input_size, self.new_size, self.new_font)
			elif event.oldState() & Qt.WindowMaximized:
				print("minimized")

		return super().eventFilter(obj, event)

	#def adapt_size(self, old=False, origin=None):
	#	if old:
	#		print(old, self.timer_font.pointSize(), origin)
	#		fm = QFontMetrics(self.timer_font)
	#		width = fm.width(self.timer.text())
	#		height = fm.height()
	#		self.timer.setFixedSize(width, height+16)
	#		self.timer.setFont(self.timer_font)
	#		self.old_input_size["Font"] = self.timer_font.pointSize()
	#		self.old_input_size["Size"] = self.timer.width(), self.timer.height()
	#	else:
	#		print(old, self.timer_font.pointSize(), origin)
	#		self.timer_font.setPointSize(self.new_input_size["Font"]*self.h_factor)
	#		self.old_input_size["Font"] = self.timer_font.pointSize()
	#		fm = QFontMetrics(self.timer_font)
	#		width = fm.width(self.timer.text())
	#		height = fm.height()
	#		self.timer.setFixedSize(width, height+15)
	#		self.old_input_size["Size"] = self.timer.width(), self.timer.height()
	#		self.timer.setFont(self.timer_font)

	def resizeEvent(self, event):
		self.w_factor = self.width() / self.w
		self.h_factor = self.height() / self.h

		if 'day' in self.timer.text():
			if self.old_input_size:
				self.new_font = self.old_input_size["Font"]*self.h_factor
				self.new_size = self.old_input_size["Size"][0]*self.w_factor, self.old_input_size["Size"][1]*self.h_factor
				self.timer_font.setPointSize(self.new_font)
				self.timer.setFixedSize(self.new_size[0], self.new_size[1])
				self.timer.setFont(self.timer_font)
			else:
				self.adapt_size(origin="resizeEvent")
		else:
			pass
			self.timer.setFixedSize(275*self.w_factor, 83*self.h_factor)
			self.timer_font.setPointSize(51*self.h_factor)

		self.timer.setFont(self.timer_font)
		self.info_text.setFont(QFont("MS Shell Dlg 2", 16*self.h_factor))
		self.toggle_btn.setFont(QFont("MS Shell Dlg 2", 14*self.h_factor))
		self.err_msg.setFont(QFont("MS Shell Dlg 2", 14*self.h_factor))
		self.ok_btn.setFont(QFont("MS Shell Dlg 2", 10*self.h_factor))
		self.ok_btn.setFixedSize(60*self.w_factor, 25*self.h_factor)
		self.change_time.setFixedSize(28*self.w_factor, 28*self.h_factor)
		self.toggle_btn.setFixedSize(101*self.w_factor, 41*self.h_factor)
		self.invalid_dialog.setFixedSize(300*self.w_factor, 100*self.h_factor)
		self.top_spacer.changeSize(0, 30*self.h_factor)
		self.center_spacer.changeSize(0, 30*self.h_factor)
		self.left_spacer.changeSize(65*self.w_factor, 0)
		self.right_spacer.changeSize(35*self.w_factor, 0)
		self.bottom_spacer.changeSize(0, 20*self.h_factor)
		self.change_time.setIconSize(QSize(28*self.w_factor, 28*self.h_factor))
		self.toggle_btn.setStyleSheet(f"""QPushButton {{
											color: rgb(58, 58, 58);
											background-color:  #dfe4ea;;
											border-radius: {5*self.h_factor}px;
											border-bottom: {7*self.h_factor}px solid #BFC4CB;
										}}
										QPushButton:pressed {{
											border-top: 4px solid transparent;
											border-bottom: 1px solid transparent;
										}}""")

if __name__ == '__main__':
	app = QApplication(argv)
	win = ShutdownUi()
	win.show()
	exit(app.exec_())


