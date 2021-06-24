from notification import *
from platform import system
from subprocess import call

class ShutdownUi(QWidget):
	DEFAULT_TIME = "00:10:00"

	def __init__(self):
		super().__init__()
		self.w, self.h = 441, 286
		self.w_factor, self.h_factor = 1, 1
		self.setWindowIcon(QIcon("Assets/shutdown.png"))
		self.installEventFilter(self)
		self.setMinimumSize(self.w, self.h)
		#self.resize(self.w+10, self.h+10)
		self.setWindowTitle("Shutdown Timer")
		self.setStyleSheet("""background: #2f3542;""")
		self.init_ui()

	def init_ui(self):
		self.started = False
		self.old_input = []
		self.colon = [False, 0]
		self.reset_colon = False
		self.old_pos = False
		self.old_input_size = {}
		self.new_input_size = {}
		self.widget_management()
		self.setup_stylesheet()
		self.layout_management()

	def widget_management(self):
		self.thread = Timer(parent=self)
		self.notification = Notification(self)
		self.thread.notif_signal.connect(self.show_notification)
		self.thread.finished_signal.connect(self.shutdown)
		self.info_text = QLabel("This computer will shutdown in")
		self.timer_text = QLabel(self.DEFAULT_TIME)
		self.timer_font = QFont()
		self.timer_font.setFamily("Ms Shell Dlg 2")
		self.timer_font.setPointSize(52)
		self.input = QLineEdit(self.DEFAULT_TIME, self)
		self.change_time = QPushButton()
		self.toggle_btn = QPushButton("Start", clicked=self.on_click)
		self.invalid_dialog = QDialog(self)
		self.err_msg = QLabel("Invalid Input!")
		self.ok_btn = QPushButton("Ok")

		self.info_text.setFont(QFont("MS Shell Dlg 2", 16))
		self.info_text.setStyleSheet("color: #ced6e0;")
		self.timer_text.setAlignment(Qt.AlignHCenter)
		self.timer_text.setFont(self.timer_font)
		self.timer_text.setFixedSize(275, 83)
		self.input.setAlignment(Qt.AlignHCenter)
		self.input.textChanged.connect(self.value_changed)
		self.input.hide()
		self.change_time.setToolTip("Change current countdown")
		self.change_time.setCursor(QCursor(Qt.PointingHandCursor))
		self.change_time.setIcon(QIcon("Assets/settings.png"))
		self.change_time.setFixedSize(24, 24)
		self.change_time.setIcon(QIcon("Assets/change.png"))
		self.change_time.setIconSize(QSize(24, 24))
		self.change_time.clicked.connect(self.show_input)
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
		self.timer_layout.addWidget(self.timer_text, alignment=Qt.AlignHCenter)
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
		self.timer_text.setStyleSheet("""color: #dfe4ea;
										 background: #2D323F;
										 border-radius: 10px;""")
		self.change_time.setStyleSheet("background: transparent;")
		self.toggle_btn.setStyleSheet("""QPushButton {
											color: rgb(58, 58, 58);
											background-color:  #dfe4ea;;
											border-radius: 6px;
											border-bottom: 7px solid #BFC4CB;
										}
										QPushButton:pressed {
											border-top: 4px solid transparent;
											border-bottom: 1px solid transparent;
										}""")
		self.input.setStyleSheet("""color: #dfe4ea;
										 background: #2D323F;
										 border-radius: 10px;""")
		self.invalid_dialog.setStyleSheet("""background: #dfe4ea;
											 border-radius: 8px;""")
		self.ok_btn.setStyleSheet("""background: transparent;
									border: 2px solid #ced6e0;""")
	def show_error(self):
		QApplication.beep()
		self.invalid_dialog.show()
		self.invalid_dialog.exec_()
		self.invalid_dialog.hide()

	def show_notification(self):
		self.hide()
		self.notification.showFullScreen()

	def show_input(self):
		if self.input.isHidden():
			self.thread.stop()
			self.input.show()
			self.input.setFixedSize(self.timer_text.width(), self.timer_text.height())
			self.input.setFont(self.timer_font)
			self.input.setFocus(True)
			new_text = ''.join(self.old_input)
			if new_text:
				self.input.setText(new_text)
				self.input.setFixedSize(*self.old_input_size["Size"])
				self.timer_font.setPointSize(self.old_input_size["Font"])
				self.input.setFont(self.timer_font)
				if len(new_text) > 8:
					self.input.setCursorPosition(0)
			else:
				self.input.setText(self.timer_text.text())
			self.timer_layout.removeWidget(self.timer_text)
			self.timer_layout.insertWidget(1, self.input, alignment=Qt.AlignHCenter)
			self.old_input = list(self.input.text())
			self.timer_text.hide()
		else:
			new_text = self.input.text()
			self.old_input = list(new_text)
			self.old_input_size["Size"] = (self.timer_text.width(), self.timer_text.height())
			self.old_input_size["Font"] = self.timer_font.pointSize()
			is_valid = False
			self.timer_layout.removeWidget(self.input)
			self.timer_layout.insertWidget(1, self.timer_text, alignment=Qt.AlignHCenter)
			self.timer_text.show()
			for nums in new_text.split(":"):
				if nums.isnumeric():
					is_valid = True
				else:
					is_valid = False
			if is_valid:
				time_format = self.add_zero_leading()
				self.timer_text.setText(time_format)
			else:
				self.show_error()

			text = self.timer_text.text()
			if len(text) > 8:
				self.new_input_size["Font"] = self.timer_font.pointSize()-22
				self.new_input_size["Size"] = (self.timer_text.width(), self.timer_text.height())
				self.timer_font.setPointSize(self.new_input_size["Font"])
				fm = QFontMetrics(self.timer_font)
				width = fm.width(text)
				height = fm.height()
				main_width = self.width()
				self.timer_text.setFixedSize(width, height+15)
				self.input.setFixedSize(width, height+15)
				self.timer_text.setFont(self.timer_font)
				self.input.setFont(self.timer_font)
			self.input.hide()

	def value_changed(self, text):
		if self.colon[0] or not self.reset_colon:
			if text.count(':') != 2:
				self.reset_colon = True
				self.old_pos = self.input.cursorPosition()
				self.input.setText(''.join(self.old_input[:self.colon[1]+len(self.old_input)]))
				self.input.setCursorPosition(self.old_pos+1)
			else:
				try:
					if self.old_input and self.old_input[2] == ':':
						if len(text) != 5:
							self.old_input = list(text)
				except:
					if len(text) != 5:
						self.old_input = list(text)
		else:
			if len(text) != 5:
				self.old_input = list(text)
			if self.colon:
				self.colon = [False, 0]
				self.reset_colon = False

	def add_zero_leading(self, s=None):
		time_format = str(timedelta(seconds=self.get_time(self.input.text()) if not s else s))
		if 'days' not in time_format or 'day' not in time_format:
			if len(time_format.split(":") [0]) == 1:
				time_format = f"0{time_format}"
		else:
			old = time_format.split(",")
			if len(old[1][1:][:-6]) == 1:
				time_format = f"{old[0]}, 0{old[1][1:]}"

		return time_format

	def get_time(self, text):
		values = []
		for index, nums in enumerate(text.split(":")):
			if nums[0] == "0":
				nums = int(nums[1:])
			else:
				nums = int(nums)

			values.append(nums)

		return sum([values[0]*60*60, values[1]*60, values[2]])

	@pyqtSlot()
	def shutdown(self):
		self.started = False
		self.toggle_btn.setText("Start")
		self.notification.hide()
		if system() == 'Windows':
			call("shutdown /s")
		elif system() == 'Linux':
			call("sudo ")
		elif system() == 'Darwin':
			pass

	def on_click(self):
		if not self.input.isHidden():
			self.show_input()
		if self.started:
			QTimer.singleShot(50, self.thread.stop)
		else:
			self.started = True
			self.thread.seconds = self.get_time(self.input.text())
			QTimer.singleShot(50, self.thread.start)
			self.toggle_btn.setText("Stop")

	def eventFilter(self, obj, event):
		if (event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton):
			if obj != self.input:
				if not self.input.isHidden():
					self.show_input()
		return super().eventFilter(obj, event)

	def resizeEvent(self, event):
		self.w_factor = self.width() / self.w
		self.h_factor = self.height() / self.h

		if 'day' in self.timer_text.text() or 'day' in self.input.text():

			self.timer_font.setPointSize(self.new_input_size["Font"]*self.h_factor)
			fm = QFontMetrics(self.timer_font)
			width = fm.width(self.timer_text.text())
			height = fm.height()
			main_width = self.width()
			self.timer_text.setFixedSize(width, height+15)
			self.input.setFixedSize(width, height+15)
			self.timer_text.setFont(self.timer_font)
			self.input.setFont(self.timer_font)
				
		else:
			self.input.setFixedSize(275*self.w_factor, 83*self.h_factor)
			self.timer_text.setFixedSize(275*self.w_factor, 83*self.h_factor)
			self.timer_font.setPointSize(52*self.h_factor)

		self.timer_text.setFont(self.timer_font)
		self.input.setFont(self.timer_font)
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

if __name__ == '__main__':
	app = QApplication(argv)
	win = ShutdownUi()
	win.show()
	exit(app.exec_())


