import sys
import requests
import warnings
import time
import os
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox,
                           QPushButton, QProgressBar, QTextEdit, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

warnings.filterwarnings("ignore", category=DeprecationWarning)

class ViewerWorker(QThread):
    progress = pyqtSignal(str)
    viewer_started = pyqtSignal(int)
    finished = pyqtSignal()
    
    def __init__(self, proxy_url, channel, viewer_count, headless, rapid_mode):
        super().__init__()
        self.proxy_url = proxy_url
        self.channel = channel
        self.viewer_count = viewer_count
        self.headless = headless
        self.rapid_mode = rapid_mode
        self.drivers = []
        self.running = True

    def simulate_viewer_activity(self, driver, viewer_index):
        try:
            scroll_amount = random.randint(100, 500)
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            time.sleep(random.uniform(2, 4))
            
            # Simulate mouse movement
            driver.execute_script("""
                var event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': arguments[0],
                    'clientY': arguments[1]
                });
                document.dispatchEvent(event);
            """, random.randint(100, 800), random.randint(100, 600))
            
            # Occasionally change quality
            if random.random() < 0.3:
                try:
                    quality_button = driver.find_element(By.CSS_SELECTOR, '[data-a-target="player-settings-button"]')
                    quality_button.click()
                    time.sleep(1)
                    quality_menu = driver.find_element(By.CSS_SELECTOR, '[data-a-target="player-settings-menu"]')
                    quality_menu.click()
                except:
                    pass
            
            # Video interaction
            if random.random() < 0.2:
                driver.execute_script("""
                    var video = document.querySelector('video');
                    if(video) {
                        if(video.paused) {
                            video.play();
                        } else {
                            video.currentTime += Math.random() * 10;
                        }
                    }
                """)
                
            time.sleep(random.uniform(8, 20))
        except Exception as e:
            self.progress.emit(f"Activity simulation error for viewer {viewer_index}: {str(e)}")

    def setup_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        
        # Anti-detection measures
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Performance options
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--mute-audio')
        
        # Additional stability options
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-background-networking')
        
        # Random window size
        width = random.randint(1024, 1920)
        height = random.randint(768, 1080)
        chrome_options.add_argument(f'--window-size={width},{height}')
        
        # Random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        return chrome_options

    def run(self):
        try:
            service = Service(ChromeDriverManager().install())
            
            for i in range(self.viewer_count):
                if not self.running:
                    break
                    
                chrome_options = self.setup_chrome_options()
                
                try:
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    self.drivers.append(driver)
                    
                    driver.get(self.proxy_url)
                    
                    wait = WebDriverWait(driver, 20)
                    text_box = wait.until(EC.presence_of_element_located((By.ID, 'url')))
                    
                    twitch_url = f'https://www.twitch.tv/{self.channel}'
                    text_box.send_keys(twitch_url)
                    text_box.send_keys(Keys.RETURN)
                    
                    self.progress.emit(f"Viewer {i + 1}/{self.viewer_count} initialized successfully")
                    self.viewer_started.emit(i + 1)
                    
                    if not self.rapid_mode:
                        time.sleep(random.uniform(3, 7))
                        self.simulate_viewer_activity(driver, i)
                    
                except Exception as e:
                    self.progress.emit(f"Error initializing viewer {i + 1}: {str(e)}")
                    continue
            
            while self.running:
                for i, driver in enumerate(self.drivers):
                    if not self.running:
                        break
                    try:
                        self.simulate_viewer_activity(driver, i)
                        time.sleep(random.uniform(1, 3))
                    except:
                        continue
                        
        except Exception as e:
            self.progress.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()

    def stop(self):
        self.running = False
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                continue

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twitch Viewer Bot - Enhanced GUI Version")
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit, QSpinBox, QComboBox {
                padding: 8px;
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #9147ff;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #772ce8;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                font-family: monospace;
            }
            QProgressBar {
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                text-align: center;
                background-color: #2a2a2a;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #9147ff;
            }
        """)
        
        # Title
        title = QLabel("Twitch Viewer Bot")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(title)
        
        # Form layout
        form_layout = QVBoxLayout()
        
        # Channel input
        channel_layout = QHBoxLayout()
        channel_label = QLabel("Channel Name:")
        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("Enter Twitch channel name")
        channel_layout.addWidget(channel_label)
        channel_layout.addWidget(self.channel_input)
        form_layout.addLayout(channel_layout)
        
        # Viewer count
        viewers_layout = QHBoxLayout()
        viewers_label = QLabel("Number of Viewers:")
        self.viewers_spin = QSpinBox()
        self.viewers_spin.setRange(1, 50)
        self.viewers_spin.setValue(5)
        viewers_layout.addWidget(viewers_label)
        viewers_layout.addWidget(self.viewers_spin)
        form_layout.addLayout(viewers_layout)
        
        # Proxy selection
        proxy_layout = QHBoxLayout()
        proxy_label = QLabel("Proxy Server:")
        self.proxy_combo = QComboBox()
        self.proxy_combo.addItems([
            "CroxyProxy.com (Recommended)",
            "CroxyProxy.rocks",
            "Croxy.network",
            "Croxy.org",
            "CroxyProxy.net",
            "Blockaway.net",
            "YoutubeUnblocked.live"
        ])
        proxy_layout.addWidget(proxy_label)
        proxy_layout.addWidget(self.proxy_combo)
        form_layout.addLayout(proxy_layout)
        
        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Launch Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Stealth Mode (stable)", "Rapid Mode (faster)"])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        form_layout.addLayout(mode_layout)
        
        # Headless mode
        self.headless_check = QCheckBox("Run in Headless Mode (no visible windows)")
        self.headless_check.setStyleSheet("color: white;")
        form_layout.addWidget(self.headless_check)
        
        layout.addLayout(form_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Viewers")
        self.stop_button = QPushButton("Stop Viewers")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # Connect signals
        self.start_button.clicked.connect(self.start_viewers)
        self.stop_button.clicked.connect(self.stop_viewers)
        
        self.viewer_thread = None

    def log(self, message):
        self.log_output.append(message)
        
    def update_progress(self, value):
        progress = int((value / self.viewers_spin.value()) * 100)
        self.progress_bar.setValue(progress)
        
    def start_viewers(self):
        if not self.channel_input.text():
            self.log("Please enter a channel name")
            return
            
        if self.viewers_spin.value() > 15:
            self.log("Warning: Running more than 15 viewers might cause instability")
            
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.log_output.clear()
        
        proxy_urls = [
            "https://www.croxyproxy.com",
            "https://www.croxyproxy.rocks",
            "https://www.croxy.network",
            "https://www.croxy.org",
            "https://www.croxyproxy.net",
            "https://www.blockaway.net",
            "https://www.youtubeunblocked.live"
        ]
        
        self.viewer_thread = ViewerWorker(
            proxy_urls[self.proxy_combo.currentIndex()],
            self.channel_input.text(),
            self.viewers_spin.value(),
            self.headless_check.isChecked(),
            self.mode_combo.currentIndex() == 1
        )
        
        self.viewer_thread.progress.connect(self.log)
        self.viewer_thread.viewer_started.connect(self.update_progress)
        self.viewer_thread.finished.connect(self.on_viewers_finished)
        self.viewer_thread.start()
        
    def stop_viewers(self):
        if self.viewer_thread:
            self.log("Stopping viewers...")
            self.viewer_thread.stop()
            
    def on_viewers_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.log("Viewer session ended")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()