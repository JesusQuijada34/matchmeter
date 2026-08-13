#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updater template for PackageMaker projects.
This template is used when creating new projects.
"""

import sys
import os
import time
import shutil
import zipfile
import subprocess
import traceback
import threading
import xml.etree.ElementTree as ET
from datetime import datetime

# requests con fallback a urllib
try:
    import requests
except ImportError:
    requests = None

# PyQt6 con fallback para entornos sin GUI
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar
    from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QObject
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False
    QApplication = None
    QMainWindow = object
    QWidget = object
    QVBoxLayout = object
    QLabel = object
    QProgressBar = object
    QFont = object
    QIcon = object
    QPixmap = object
    QColor = object
    Qt = None
    QThread = object
    class pyqtSignal:
        def __init__(self, *args): pass
        def connect(self, *args): pass
        def emit(self, *args): pass
    QTimer = object
    QObject = object

# Leviathan UI con fallback
try:
    from leviathan_ui import LeviathanDialog, WipeWindow, LeviathanProgressBar, CustomTitleBar
    HAS_LEVIATHAN = True
except (ImportError, SyntaxError):
    HAS_LEVIATHAN = False
    class LeviathanDialog:
        @staticmethod
        def launch(*args, **kwargs): print(f"[MOCK] LeviathanDialog: {args}")
    class WipeWindow:
        @staticmethod
        def create():
            class MockWipe:
                def set_mode(self, *args): return self
                def apply(self, *args): pass
            return MockWipe()
    class LeviathanProgressBar: pass
    class CustomTitleBar:
        def __init__(self, *args, **kwargs): pass
        def set_color(self, *args): pass

# --- CONFIG ---
XML_PATH = "details.xml"
LOG_PATH = "updater_log.txt"
CHECK_INTERVAL = 60
GITHUB_API = "https://api.github.com"

def log(msg):
    """Log message to file and console."""
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{ts} {msg}\n")
    except: pass
    print(f"{ts} {msg}")

def leer_xml(path):
    """Read local details.xml."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        return {
            "app": root.findtext("app", "").strip(),
            "version": root.findtext("version", "").strip(),
            "platform": root.findtext("platform", "").strip(),
            "author": root.findtext("author", "").strip(),
            "publisher": root.findtext("publisher", "").strip()
        }
    except: return {}

def leer_xml_remoto(author, app):
    """Read remote version from GitHub."""
    url = f"https://raw.githubusercontent.com/{author}/{app}/main/details.xml"
    try:
        if requests:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return ET.fromstring(r.text).findtext("version", "").strip()
        else:
            # Fallback usando urllib
            import urllib.request
            with urllib.request.urlopen(url, timeout=10) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    return ET.fromstring(content).findtext("version", "").strip()
    except: pass
    return ""

def _check_url_exists(url):
    """Check if URL exists (HEAD request)."""
    if requests:
        try:
            r = requests.head(url, timeout=15, allow_redirects=True)
            return r.status_code == 200
        except: pass
    else:
        # Fallback usando urllib
        try:
            import urllib.request
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.status == 200
        except: pass
    return False

def buscar_release(author, app, version, platform, publisher):
    """Search for .iflapp release file."""
    filename = f"{publisher}.{app}.{version}-{platform}.iflapp"
    url = f"https://github.com/{author}/{app}/releases/download/{version}/{filename}"
    if _check_url_exists(url):
        return url
    return None

def buscar_release_exe(author, app, version, platform, publisher):
    """Search for .exe setup file."""
    exe_patterns = [
        f"{publisher}.{app}-{version}-{platform}.exe",
        f"{publisher}.{app}.{version}-{platform}.exe",
        f"{publisher}-{app}-{version}-{platform}.exe",
        f"{app}-{version}-{platform}.exe",
        f"{publisher}.{app}-Setup-{version}.exe",
        f"{app}-Setup-{version}.exe",
    ]
    for filename in exe_patterns:
        url = f"https://github.com/{author}/{app}/releases/download/{version}/{filename}"
        if _check_url_exists(url):
            log(f"[EXE] Setup encontrado: {filename}")
            return url, filename
    return None, None

class InstallerWorker(QObject):
    """Worker thread for downloading and installing updates."""
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self, url, app_data):
        super().__init__()
        self.url = url
        self.app = app_data["app"]
        self._running = True

    def run(self):
        temp_zip = "pending_update.zip"
        ext_dir = "update_temp_extracted"
        try:
            self.status.emit("Conectando con el servidor...")
            
            if requests:
                r = requests.get(self.url, stream=True)
                total = int(r.headers.get("content-length", 0))
                down = 0
                with open(temp_zip, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if not self._running: return
                        f.write(chunk)
                        down += len(chunk)
                        if total: self.progress.emit(int(down * 100 / total))
            else:
                # Fallback usando urllib
                import urllib.request
                with urllib.request.urlopen(self.url, timeout=60) as response:
                    total = int(response.headers.get("Content-Length", 0))
                    down = 0
                    with open(temp_zip, "wb") as f:
                        while True:
                            chunk = response.read(8192)
                            if not chunk or not self._running: break
                            f.write(chunk)
                            down += len(chunk)
                            if total: self.progress.emit(int(down * 100 / total))

            self.status.emit("Descomprimiendo actualización...")
            if os.path.exists(ext_dir): shutil.rmtree(ext_dir)
            with zipfile.ZipFile(temp_zip, "r") as z:
                z.extractall(ext_dir)

            self.status.emit("Cerrando aplicación principal...")
            self._kill_target(self.app)
            time.sleep(2)

            self.status.emit("Sobrescribiendo sistema...")
            for root, dirs, files in os.walk(ext_dir):
                rel = os.path.relpath(root, ext_dir)
                dest_fold = rel if rel != "." else "."
                if dest_fold != "." and not os.path.exists(dest_fold):
                    os.makedirs(dest_fold)
                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(dest_fold, file)
                    if os.path.abspath(dst) == os.path.abspath(sys.argv[0]): continue
                    if os.path.exists(dst):
                        try: os.remove(dst)
                        except:
                            try: os.rename(dst, dst + f".old.{int(time.time())}")
                            except: continue
                    try: shutil.move(src, dst)
                    except: pass

            # Sincronizar plantillas
            self._sync_templates()

            try: shutil.rmtree(ext_dir)
            except: pass
            try: os.remove(temp_zip)
            except: pass
            
            self.status.emit("Finalizando...")
            self.finished.emit(True, "OK")

        except Exception as e:
            log(traceback.format_exc())
            self.finished.emit(False, str(e))

    def _kill_target(self, target_name):
        """Kill processes by name."""
        log(f"Matando procesos de: {target_name}")
        try:
            if sys.platform == "win32":
                subprocess.call(f"taskkill /F /IM {target_name}.exe", shell=True)
                subprocess.call(f"taskkill /F /IM {target_name}", shell=True)
            else:
                subprocess.call(f"pkill -9 -f {target_name}", shell=True)
        except Exception as e:
            log(f"Kill error: {e}")

    def _sync_templates(self):
        """Sync templates from extracted update."""
        src = os.path.join("update_temp_extracted", "src", "templates")
        tgt = os.path.join("src", "templates")
        if os.path.isdir(src):
            try:
                for root, dirs, files in os.walk(src):
                    for file in files:
                        src_file = os.path.join(root, file)
                        rel = os.path.relpath(src_file, src)
                        tgt_file = os.path.join(tgt, rel)
                        os.makedirs(os.path.dirname(tgt_file), exist_ok=True)
                        shutil.copy2(src_file, tgt_file)
                log("[TEMPLATE SYNC] Plantillas sincronizadas")
            except Exception as e:
                log(f"[TEMPLATE SYNC] Error: {e}")

class ModernUpdaterWindow(QMainWindow):
    """Main updater window with modern UI."""
    
    def __init__(self, app_data, url):
        super().__init__()
        self.app_data = app_data
        self.url = url
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(480, 320)
        if HAS_LEVIATHAN:
            WipeWindow.create().set_mode("ghostBlur").apply(self)
        self.init_ui()
        self.center()
        QTimer.singleShot(500, self.start_install)

    def center(self):
        if QApplication.instance():
            screen = QApplication.primaryScreen()
            if screen:
                self.move(screen.availableGeometry().center() - self.rect().center())

    def init_ui(self):
        central = QWidget()
        central.setObjectName("Central")
        central.setStyleSheet("QWidget#Central { background: rgba(18, 24, 34, 0.85); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; }")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if HAS_LEVIATHAN:
            self.title_bar = CustomTitleBar(self, title="System Updater", is_main=True)
            self.title_bar.set_color(QColor(0,0,0,0))
            layout.addWidget(self.title_bar)

        content = QWidget()
        c_lay = QVBoxLayout(content)
        c_lay.setContentsMargins(30, 10, 30, 30)
        c_lay.setSpacing(15)
        
        self.icon_lbl = QLabel("🔄")
        self.icon_lbl.setStyleSheet("font-size: 48px; color: #2486ff;")
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_lay.addWidget(self.icon_lbl)
        
        self.lbl_main = QLabel(f"Actualizando {self.app_data['app']}")
        self.lbl_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_main.setStyleSheet("font-family: 'Segoe UI'; font-weight: 700; font-size: 18px; color: white;")
        c_lay.addWidget(self.lbl_main)
        
        self.lbl_status = QLabel("Preparando...")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet("color: #aaa; font-size: 13px;")
        c_lay.addWidget(self.lbl_status)
        
        if HAS_LEVIATHAN:
            self.pbar = LeviathanProgressBar(self)
        else:
            self.pbar = QProgressBar()
            self.pbar.setStyleSheet("QProgressBar { background: #333; border: none; height: 6px; } QProgressBar::chunk { background: #2486ff; }")
            self.pbar.setTextVisible(False)
        c_lay.addWidget(self.pbar)
        
        layout.addWidget(content)

    def start_install(self):
        self.thread = QThread()
        self.worker = InstallerWorker(self.url, self.app_data)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.pbar.setValue)
        self.worker.status.connect(self.lbl_status.setText)
        self.worker.finished.connect(self.on_fin)
        self.thread.start()

    def on_fin(self, ok, msg):
        self.thread.quit()
        if ok:
            self.lbl_status.setText("¡Actualización completada!")
            exe = f"{self.app_data['app']}.exe"
            if os.path.exists(exe): subprocess.Popen(exe)
            QTimer.singleShot(1500, self.close)
        else:
            self.lbl_status.setText(f"Error: {msg}")
            self.lbl_status.setStyleSheet("color: #ff5252;")

def ciclo_embestido():
    """Background update checker."""
    def verificar():
        while True:
            datos = leer_xml(XML_PATH)
            if datos:
                remoto = leer_xml_remoto(datos["author"], datos["app"])
                if remoto and remoto != datos["version"]:
                    # Buscar .exe primero, luego .iflapp
                    exe_url, exe_file = buscar_release_exe(
                        datos["author"], datos["app"], remoto,
                        datos["platform"], datos["publisher"]
                    )
                    if exe_url:
                        log(f"[UPDATE] Nueva versión disponible: {remoto}")
                        # Por ahora solo .iflapp para descarga directa
                    
                    url = buscar_release(datos["author"], datos["app"], remoto, datos["platform"], datos["publisher"])
                    if url:
                        if PYQT6_AVAILABLE:
                            app = QApplication(sys.argv)
                            w = ModernUpdaterWindow(datos, url)
                            w.show()
                            app.exec()
                        return 
            time.sleep(CHECK_INTERVAL)
    threading.Thread(target=verificar, daemon=True).start()

if __name__ == "__main__":
    ciclo_embestido()
    while True: time.sleep(100)
