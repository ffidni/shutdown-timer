from timer import *

class Notification(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.line = QLineEdit()
		self.parent = parent
		self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setStyleSheet("background-color: rgba(87 ,96, 111, 90)")
		self.init_ui()

	def init_ui(self):
		self.widget_management()
		self.layout_management()

	def widget_management(self):
		self.title = QPushButton("\tShutdown Timer")
		self.info = QLabel("Shutting down in 5s")
		self.cancel_btn = QPushButton("Cancel")

		self.title.setIcon(QIcon("Assets/shutdown.png"))
		self.title.setIconSize(QSize(16, 16))
		self.title.setFont(QFont("Arial", 16, 0))
		self.info.setFont(QFont("MS Shell Dlg 2", 48))
		self.cancel_btn.setFont(QFont("Ms Shell Dlg 2", 24))
		self.cancel_btn.setFixedSize(200, 80)
		self.cancel_btn.clicked.connect(self.cancel)
		self.cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
		self.setup_stylesheet()

	def setup_stylesheet(self):
		self.title.setStyleSheet("""background: transparent;
									border: none;
									color: #ced6e0;""")
		self.info.setStyleSheet("""color: #f1f2f6;
								   background: none;""")
		self.cancel_btn.setStyleSheet("""QPushButton {
											color: rgb(58, 58, 58);
											background-color:  #dfe4ea;;
											border-radius: 12px;
											border-bottom: 16px solid #BFC4CB;
										}
										QPushButton:pressed {
											border-top: 4px solid transparent;
											border-bottom: 1px solid transparent;
										}""")

	def layout_management(self):
		main_layout = QVBoxLayout()
		spacer = QSpacerItem(0, 250, QSizePolicy.Fixed, QSizePolicy.Fixed)

		main_layout.addItem(spacer)
		main_layout.addWidget(self.title, alignment=Qt.AlignBottom)
		main_layout.addWidget(self.info, alignment=Qt.AlignHCenter)
		main_layout.addSpacing(55)
		main_layout.addWidget(self.cancel_btn, alignment=Qt.AlignHCenter)
		main_layout.addItem(spacer)
		self.setLayout(main_layout)

	def cancel(self):
		self.parent.thread.stop("Cancel")