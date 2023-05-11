from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt
import sys

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Name")
		self.setWindowIcon(QIcon("icon.png"))
		self.setGeometry(350, 100, 1000, 800)
		self.setStyleSheet("background-color: #303022;")
		
		# p = self.palette()
		# p.setColor(QPalette.Window, Qt.red)
		# self.setPalette(p)
	
	def create_player(self):

		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

		videoWidget = QVideoWidget()

		openButton = QPushButton("Open Video")
		

app = QApplication(sys.argv)
window = Window() 
window.show()
sys.exit(app.exec_())
