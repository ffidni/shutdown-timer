from packages import *

class Timer(QThread):
	#Defining signal to communicate between classes
	finished_signal = pyqtSignal(bool)
	notif_signal = pyqtSignal(bool)

	def __init__(self, seconds=None, parent=None):
		super().__init__(parent)
		self.seconds = seconds
		self.parent = parent

	def run(self):
		#Timer's countdown
		self.parent.DEFAULT_TIME = self.parent.timer_format(self.seconds)
		while (self.seconds > 0):
			self.seconds -= 1
			time_format = self.parent.timer_format(self.seconds)
			#If there's 10 seconds left; show the 
			#notification to warn the user about the shutdown
			if self.seconds <= 10:
				if self.parent.notification.isHidden():
					self.notif_signal.emit(True)
				self.parent.notification.info.setText(f"Shutting down in {self.seconds}s")
			self.parent.timer.setText(time_format)
			sleep(1)

		self.parent.timer.setText(self.parent.DEFAULT_TIME)
		self.finished_signal.emit(True)

	def stop(self, value=None):
		#Stop the timer and return the current value
		self.terminate()
		if value == 'Cancel':
			self.parent.notification.hide()
			self.parent.show()
		self.parent.started = False
		self.parent.toggle_btn.setText("Start")
		self.parent.timer.setCursorPosition(len(self.parent.timer.text()))