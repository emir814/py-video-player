import sys
import vlc
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMessageBox, QMainWindow, QPushButton, QHBoxLayout, QFrame, QSlider, QLabel, QSpacerItem, QSizePolicy, QGridLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QFrame):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player")
        
        # Karanlık tema uygulaması
        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                color: #dddddd;
            }
            QPushButton {
                background-color: #444444;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QSlider::groove:horizontal {
                border: 1px solid #444444;
                height: 8px;
                background: #333333;
            }
            QSlider::handle:horizontal {
                background: #888888;
                border: 1px solid #444444;
                width: 14px;
                margin: -2px 0;
            }
            QLabel {
                color: #dddddd;
            }
        """)

        self.video_widget = QVideoWidget()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.time_label = QLabel("00:00:00")

        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_media(self.instance.media_new(video_path))
        self.player.set_hwnd(int(self.video_widget.winId()))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)

        layout.addLayout(control_layout)

        time_slider_layout = QGridLayout()
        time_slider_layout.addWidget(self.time_label, 0, 0)
        time_slider_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum), 0, 1)
        time_slider_layout.addWidget(self.position_slider, 0, 2)

        layout.addLayout(time_slider_layout)
        self.setLayout(layout)

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()

    def set_position(self, position):
        self.player.set_position(position / 100.0)

    def update_ui(self):
        if self.player.is_playing():
            self.position_slider.setValue(int(self.player.get_position() * 100))
            current_time = self.player.get_time() // 1000
            self.time_label.setText(self.format_time(current_time))

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def resizeEvent(self, event):
        self.video_widget.setGeometry(0, 0, self.width(), self.height() - 100)
        super().resizeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player")
        
        self.player = VideoPlayer(video_path)
        self.setCentralWidget(self.player)
        
        self.settings = QSettings("MyCompany", "VideoPlayerApp")
        self.restoreGeometry(self.settings.value("geometry", b""))
        self.restoreState(self.settings.value("windowState", b""))

        self.resize(800, 600)

        # Set icon
        self.setWindowIcon(QIcon('icon.png'))  # Path to your icon file

        # Karanlık tema uygulaması
        app_palette = QPalette()
        app_palette.setColor(QPalette.Window, QColor(43, 43, 43))
        app_palette.setColor(QPalette.WindowText, Qt.white)
        app_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        app_palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
        app_palette.setColor(QPalette.ToolTipBase, Qt.white)
        app_palette.setColor(QPalette.ToolTipText, Qt.white)
        app_palette.setColor(QPalette.Text, Qt.white)
        app_palette.setColor(QPalette.Button, QColor(43, 43, 43))
        app_palette.setColor(QPalette.ButtonText, Qt.white)
        app_palette.setColor(QPalette.BrightText, Qt.red)
        app_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        app_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        app_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(app_palette)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if len(sys.argv) < 2:
        QMessageBox.critical(None, "Error", "Usage: video.py <video-path>")
        sys.exit(1)

    video_path = sys.argv[1]

    try:
        viewer = MainWindow(video_path)
        viewer.show()
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        sys.exit(1)

    sys.exit(app.exec_())
