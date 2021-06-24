from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSpinBox, QLabel, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QThread, QTimer
from datetime import timedelta
from time import sleep
from sys import argv, exit


class Shutdown(QWidget):

	def __init__(self):
		super().__init__()
		self.resize(441, 286)
		self.setWindowTitle("Shutdown Timer")
		self.setStyleSheet("""background: #2f3542;""")
		self.init_ui()

	def init_ui(self):
		self.started = False
		self.old_input = []
		self.colon = [False, 0]
		self.reset_colon = False
		self.old_pos = False
		self.thread = Timer(parent=self)
		self.widget_management()
		self.setup_stylesheet()
		self.layout_management()

	def widget_management(self):
		self.info_text = QLabel("This computer will shutdown in")
		self.timer_text = QLabel("00:05:00")
		self.timer_font = QFont()
		self.timer_font.setFamily("Ms Shell Dlg 2")
		self.timer_font.setPointSize(52)
		self.input = QLineEdit(self)
		self.change_time = QPushButton()
		self.toggle_btn = QPushButton("Start", clicked=self.on_click)
		self.invalid_dialog = QDialog(self)
		self.err_msg = QLabel("Invalid Input!")
		self.ok_btn = QPushButton("Ok")

		self.info_text.setFont(QFont("MS Shell Dlg 2", 16))
		self.info_text.setStyleSheet("color: #ced6e0;")

		self.timer_text.setFont(self.timer_font)
		self.timer_text.setFixedSize(275, 83)
		self.input.textChanged.connect(self.value_changed)
		self.input.hide()
		self.change_time.setIcon(QIcon("Assets/settings.png"))
		self.change_time.setFixedSize(24, 24)
		self.change_time.setIcon(QIcon("Assets/change.png"))
		self.change_time.setIconSize(QSize(24, 24))
		self.change_time.clicked.connect(self.show_input)
		self.toggle_btn.setFont(QFont("MS Shell Dlg 2", 14))
		self.toggle_btn.setFixedSize(101, 41)
		self.invalid_dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.invalid_dialog.setFixedSize(300, 100)
		self.err_msg.setFont(QFont("MS Shell Dlg 2", 14))
		self.ok_btn.clicked.connect(self.invalid_dialog.close)
		self.ok_btn.setFont(QFont("MS Shell Dlg 2", 10))
		self.ok_btn.setFixedSize(60, 25)

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.timer_layout = QHBoxLayout()
		self.invalid_layout = QVBoxLayout()
		self.top_spacer = QSpacerItem(0, 25, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.center_spacer = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.left_spacer = QSpacerItem(65, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.right_spacer = QSpacerItem(35, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.bottom_spacer = QSpacerItem(0, 18, QSizePolicy.Fixed, QSizePolicy.Fixed)

		self.main_layout.addItem(self.top_spacer)
		self.main_layout.addWidget(self.info_text, alignment=Qt.AlignHCenter)
		self.timer_layout.addItem(self.left_spacer)
		self.timer_layout.addWidget(self.timer_text, alignment=Qt.AlignHCenter)
		self.timer_layout.addWidget(self.change_time)
		self.timer_layout.addItem(self.right_spacer)
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
		#self.err_msg.setStyleSheet("color: #57606f;")
		self.ok_btn.setStyleSheet("""background: transparent;
									border: 2px solid #ced6e0;""")


	def show_error(self):
		QApplication.beep()
		self.invalid_dialog.show()
		self.invalid_dialog.exec_()
		self.invalid_dialog.hide()


	def show_input(self):
		if self.input.isHidden():
			self.input.show()
			self.input.setFixedSize(self.timer_text.width(), self.timer_text.height())
			self.input.setFont(self.timer_font)
			self.input.setFocus(True)
			new_text = self.timer_text.text()
			if 'days' in new_text or 'day' in new_text:
				new_text = new_text.split(":")
				hour = int(new_text[0])*24 + int(new_text[1][1:][:-6])
				rest = new_text[1][1:][2:]
				self.input.setText(''.join(f"{hour}:{rest}"))
			else:
				self.input.setText(self.timer_text.text())
			self.timer_layout.removeWidget(self.timer_text)
			self.timer_layout.insertWidget(1, self.input)
			self.old_input = list(self.input.text())
			self.timer_text.hide()
		else:
			new_text = self.input.text()
			is_valid = False
			self.input.hide()
			self.timer_layout.removeWidget(self.input)
			self.timer_layout.insertWidget(1, self.timer_text)
			self.timer_text.show()
			if len(new_text) > 8:
				self.show_error()
			elif len(new_text) == 8:
				for nums in new_text.split(":"):
					if nums.isnumeric():
						is_valid = True
				if is_valid:
					self.timer_text.setText(new_text)	
				else:
					self.show_error()		

	def value_changed(self, text):
		if self.colon[0] or not self.reset_colon:
			if self.input.text().count(':') != 2:
				self.reset_colon = True
				self.old_pos = self.input.cursorPosition()
				self.input.setText(''.join(self.old_input[:self.colon[1]+8]))
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

	def get_time(self):
		values = []
		for index, nums in enumerate(self.timer_text.text().split(":")):
			if nums[0] == "0":
				nums = int(nums[1:])
			else:
				nums = int(nums)

			values.append(nums)

		return sum([values[0]*60*60, values[1]*60, values[2]])


	def on_click(self):
		if self.started:
			self.started = False
			QTimer.singleShot(50, self.thread.stop)
			self.toggle_btn.setText("Start")
		else:
			self.started = True
			self.thread.seconds = self.get_time()
			QTimer.singleShot(50, self.thread.start)
			self.toggle_btn.setText("Stop")

class Timer(QThread):

	def __init__(self, seconds=None, parent=None):
		super().__init__(parent)
		self.seconds = seconds
		self.flag = False
		self.parent = parent

	def run(self):
		self.seconds += 1
		while (self.seconds > 0):
			self.seconds -= 1
			time_format = str(timedelta(seconds=self.seconds))
			if 'days' not in time_format:
				if time_format[0] == '0' and time_format[1] == ':':
					time_format = f"0{time_format}"
			else:
				old = time_format.split(",")
				time_format = f"{old[0]}, 0{old[1][1:]}"
			if not self.flag:
				self.parent.timer_font.setPointSize(self.parent.timer_font.pointSize()-25)
				self.parent.timer_text.setFont(self.parent.timer_font)
				self.parent.input.setFont(self.parent.timer_font)
				self.flag = True
			self.parent.timer_text.setText(time_format)
			sleep(1)

	def stop(self):
		self.terminate()


if __name__ == '__main__':
	app = QApplication(argv)
	win = Shutdown()
	win.show()
	exit(app.exec_())


