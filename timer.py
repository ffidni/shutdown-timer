from packages import *

class Timer(QThread):
	finished_signal = pyqtSignal(bool)
	notif_signal = pyqtSignal(bool)

	def __init__(self, seconds=None, parent=None):
		super().__init__(parent)
		self.seconds = seconds
		self.flag = False
		self.parent = parent

	def run(self):
		self.parent.DEFAULT_TIME = self.parent.timer_format(self.seconds)
		while (self.seconds > 0):
			self.seconds -= 1
			time_format = self.parent.timer_format(self.seconds)
			if self.seconds <= 10:
				if self.parent.notification.isHidden():
					self.notif_signal.emit(True)
				self.parent.notification.info.setText(f"Shutting down in {self.seconds}s")
			self.parent.timer.setText(time_format)
			sleep(1)

		self.parent.timer.setText(self.parent.DEFAULT_TIME)
		self.finished_signal.emit(True)

	def stop(self, value=None):
		self.terminate()
		if value == 'Cancel':
			self.parent.notification.hide()
			self.parent.show()
		self.parent.started = False
		self.parent.toggle_btn.setText("Start")
		self.parent.timer.setCursorPosition(len(self.parent.timer.text()))