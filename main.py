import sys
import os
import json
import re
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QTabWidget, QMessageBox, QLabel, QSizePolicy, QComboBox, QLineEdit,
    QSpinBox
)
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QPalette, QColor

# ==========================================
# سیستم مدیریت زبان با اسکن پوشه محلی
# ==========================================
class LangManager(QObject):
    lang_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.available_langs = {}
        self.translations = {}
        self.current_lang = "fa"
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.locales_dir = os.path.join(base_dir, "locales")
        
        self.scan_languages()
        self.load_language(self.current_lang)

    def scan_languages(self):
        if not os.path.exists(self.locales_dir):
            os.makedirs(self.locales_dir)
            return

        for filename in os.listdir(self.locales_dir):
            if filename.endswith(".json"):
                lang_code = filename[:-5]
                filepath = os.path.join(self.locales_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        lang_name = data.get("lang_name", lang_code.upper())
                        self.available_langs[lang_code] = lang_name
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    def load_language(self, lang_code):
        filepath = os.path.join(self.locales_dir, f"{lang_code}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
                self.current_lang = lang_code
            except Exception as e:
                print(f"Error loading {filepath}: {e}")

    def set_lang(self, lang_code):
        if lang_code != self.current_lang:
            self.load_language(lang_code)
            direction = Qt.RightToLeft if lang_code in ["fa", "ar", "he"] else Qt.LeftToRight
            QApplication.instance().setLayoutDirection(direction)
            self.lang_changed.emit(self.current_lang)

    def t(self, key):
        return self.translations.get(key, key)

lang_mgr = LangManager()

# ==========================================
# تب اول: تکه‌تکه کردن (Split Tab)
# ==========================================
class SplitTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file_path = ""
        self.setAcceptDrops(True)
        self.setup_ui()
        lang_mgr.lang_changed.connect(self.update_texts)
        self.update_texts()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(self.title)
        
        self.desc = QLabel()
        self.desc.setStyleSheet("font-size: 11px; color: #888888;")
        main_layout.addWidget(self.desc)
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #3d3d3d; border-radius: 6px; padding: 8px; font-size: 13px;
            }
        """)
        
        self.load_btn = QPushButton()
        self.load_btn.setCursor(Qt.PointingHandCursor)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border: none;
                padding: 10px 20px; font-size: 13px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        
        input_layout.addWidget(self.path_input, 4)
        input_layout.addWidget(self.load_btn, 1)
        main_layout.addLayout(input_layout)

        # --- باکس تعداد خطوط ---
        chunk_layout = QHBoxLayout()
        chunk_layout.setSpacing(8)

        self.chunk_label = QLabel()
        self.chunk_label.setStyleSheet("font-size: 13px;")

        self.chunk_spinbox = QSpinBox()
        self.chunk_spinbox.setMinimum(1)
        self.chunk_spinbox.setMaximum(100000)
        self.chunk_spinbox.setValue(500)
        self.chunk_spinbox.setFixedWidth(110)
        self.chunk_spinbox.setStyleSheet("""
            QSpinBox {
                border: 2px solid #3d3d3d; border-radius: 6px;
                padding: 6px 8px; font-size: 13px; font-weight: bold;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
        """)

        chunk_layout.addWidget(self.chunk_label)
        chunk_layout.addWidget(self.chunk_spinbox)
        chunk_layout.addStretch()
        main_layout.addLayout(chunk_layout)
        # --- پایان باکس ---

        self.process_btn = QPushButton()
        self.process_btn.setCursor(Qt.PointingHandCursor)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white; border: none;
                padding: 12px; font-size: 14px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #d35400; }
        """)
        main_layout.addWidget(self.process_btn)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3d3d3d; border-radius: 6px; padding: 8px; font-size: 13px;
                background-color: rgba(0, 0, 0, 0.03);
            }
        """)
        main_layout.addWidget(self.log_area, 1)
        
        self.setLayout(main_layout)
        self.load_btn.clicked.connect(self.load_file_dialog)
        self.process_btn.clicked.connect(self.execute_split)

    def update_texts(self):
        self.title.setText(lang_mgr.t("split_title"))
        self.desc.setText(lang_mgr.t("split_desc"))
        self.load_btn.setText(lang_mgr.t("open_file_btn"))
        self.process_btn.setText(lang_mgr.t("process_split_btn"))
        self.path_input.setPlaceholderText(lang_mgr.t("split_placeholder"))
        self.chunk_label.setText(lang_mgr.t("chunk_size_label"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path.lower().endswith(('.txt', '.json')):
                self.selected_file_path = file_path
                self.path_input.setText(file_path)
                break

    def load_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, lang_mgr.t("open_file_btn"), "", "Text Files (*.txt *.json);;All Files (*)"
        )
        if path:
            self.selected_file_path = path
            self.path_input.setText(path)

    def execute_split(self):
        if not self.selected_file_path or not os.path.exists(self.selected_file_path):
            QMessageBox.warning(self, lang_mgr.t("warning_title"), lang_mgr.t("no_file"))
            return
        
        try:
            self.log_area.clear()
            base_dir = os.path.dirname(self.selected_file_path)
            file_name, file_ext = os.path.splitext(os.path.basename(self.selected_file_path))
            
            output_dir = os.path.join(base_dir, f"{file_name}_parts")
            os.makedirs(output_dir, exist_ok=True)
            
            with open(self.selected_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            chunk_size = self.chunk_spinbox.value()   # ← مقدار از SpinBox
            part_num = 1
            
            for i in range(0, total_lines, chunk_size):
                chunk = lines[i : i + chunk_size]
                part_name = f"{file_name}_part_{part_num:03d}{file_ext}"
                part_path = os.path.join(output_dir, part_name)
                
                with open(part_path, "w", encoding="utf-8") as pf:
                    pf.writelines(chunk)
                
                self.log_area.append(f"Created: {part_name}")
                part_num += 1
                
            msg = lang_mgr.t("split_done").format(part_num - 1, output_dir)
            QMessageBox.information(self, lang_mgr.t("success_title"), msg)
        except Exception as e:
            QMessageBox.critical(self, lang_mgr.t("error_title"), lang_mgr.t("error_msg").format(str(e)))


# ==========================================
# تب دوم: چسباندن هوشمند (Merge Tab)
# ==========================================
class MergeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_dir_path = ""
        self.setAcceptDrops(True)
        self.setup_ui()
        lang_mgr.lang_changed.connect(self.update_texts)
        self.update_texts()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(self.title)
        
        self.desc = QLabel()
        self.desc.setStyleSheet("font-size: 11px; color: #888888;")
        main_layout.addWidget(self.desc)
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #3d3d3d; border-radius: 6px; padding: 8px; font-size: 13px;
            }
        """)
        
        self.load_btn = QPushButton()
        self.load_btn.setCursor(Qt.PointingHandCursor)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c; color: white; border: none;
                padding: 10px 20px; font-size: 13px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #16a085; }
        """)
        
        input_layout.addWidget(self.path_input, 4)
        input_layout.addWidget(self.load_btn, 1)
        main_layout.addLayout(input_layout)
        
        self.process_btn = QPushButton()
        self.process_btn.setCursor(Qt.PointingHandCursor)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; color: white; border: none;
                padding: 12px; font-size: 14px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #8e44ad; }
        """)
        main_layout.addWidget(self.process_btn)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3d3d3d; border-radius: 6px; padding: 8px; font-size: 13px;
                background-color: rgba(0, 0, 0, 0.03);
            }
        """)
        main_layout.addWidget(self.log_area, 1)
        
        self.setLayout(main_layout)
        self.load_btn.clicked.connect(self.load_dir_dialog)
        self.process_btn.clicked.connect(self.execute_merge)

    def update_texts(self):
        self.title.setText(lang_mgr.t("merge_title"))
        self.desc.setText(lang_mgr.t("merge_desc"))
        self.load_btn.setText(lang_mgr.t("open_dir_btn"))
        self.process_btn.setText(lang_mgr.t("process_merge_btn"))
        self.path_input.setPlaceholderText(lang_mgr.t("merge_placeholder"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            dir_path = url.toLocalFile()
            if os.path.isdir(dir_path):
                self.selected_dir_path = dir_path
                self.path_input.setText(dir_path)
                break

    def load_dir_dialog(self):
        path = QFileDialog.getExistingDirectory(self, lang_mgr.t("open_dir_btn"), "")
        if path:
            self.selected_dir_path = path
            self.path_input.setText(path)

    def execute_merge(self):
        if not self.selected_dir_path or not os.path.isdir(self.selected_dir_path):
            QMessageBox.warning(self, lang_mgr.t("warning_title"), lang_mgr.t("no_dir"))
            return
        
        try:
            self.log_area.clear()
            pattern = re.compile(r".*_part_(\d+)\.(txt|json)$", re.IGNORECASE)
            valid_files = []
            
            for f in os.listdir(self.selected_dir_path):
                match = pattern.match(f)
                if match:
                    part_index = int(match.group(1))
                    full_path = os.path.join(self.selected_dir_path, f)
                    valid_files.append((part_index, full_path, f))
            
            if not valid_files:
                QMessageBox.warning(self, lang_mgr.t("warning_title"), lang_mgr.t("no_parts_found"))
                return
            
            valid_files.sort(key=lambda x: x[0])
            _, first_ext = os.path.splitext(valid_files[0][2])
            
            output_file_name = f"Merged_Result{first_ext}"
            output_file_path = os.path.join(self.selected_dir_path, output_file_name)
            
            with open(output_file_path, "w", encoding="utf-8") as out_f:
                for index, path, name in valid_files:
                    self.log_area.append(lang_mgr.t("reading_part").format(name, index))
                    with open(path, "r", encoding="utf-8") as in_f:
                        out_f.write(in_f.read())
            
            msg = lang_mgr.t("merge_done").format(output_file_path)
            QMessageBox.information(self, lang_mgr.t("success_title"), msg)
        except Exception as e:
            QMessageBox.critical(self, lang_mgr.t("error_title"), lang_mgr.t("error_msg").format(str(e)))


# ==========================================
# پنجره اصلی
# ==========================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(750, 550)
        self.is_dark_mode = True
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(15, 10, 15, 0)
        top_bar.setSpacing(10)
        
        self.theme_btn = QPushButton("☀️ Light")
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        self.lang_combo = QComboBox()
        self.lang_combo.setCursor(Qt.PointingHandCursor)
        
        for code, name in lang_mgr.available_langs.items():
            self.lang_combo.addItem(name, code)
            
        index = self.lang_combo.findData(lang_mgr.current_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
            
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        
        top_bar.addStretch()
        top_bar.addWidget(self.theme_btn)
        top_bar.addWidget(self.lang_combo)
        main_layout.addLayout(top_bar)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(SplitTab(), "")
        self.tabs.addTab(MergeTab(), "")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
        lang_mgr.lang_changed.connect(self.update_texts)
        self.update_texts()
        self.apply_theme()

    def change_language(self, index):
        lang_code = self.lang_combo.itemData(index)
        if lang_code:
            lang_mgr.set_lang(lang_code)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_btn.setText("🌙 Dark" if not self.is_dark_mode else "☀️ Light")
        self.apply_theme()

    def apply_theme(self):
        palette = QPalette()
        if self.is_dark_mode:
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor("#1e1e1e"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor("#2d2d2d"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor("#ffffff"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor("#3d3d3d"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            
            tab_bg, tab_fg, pane_bg = "#2d2d2d", "#b0b0b0", "#1e1e1e"
            self.lang_combo.setStyleSheet("QComboBox { background-color: #2d2d2d; color: #ffffff; border: 1px solid #3498db; border-radius: 4px; padding: 4px 10px; font-weight: bold; min-width: 100px; } QComboBox::drop-down { border: none; }")
            self.theme_btn.setStyleSheet("QPushButton { background-color: transparent; color: #ffffff; border: 1px solid #7f8c8d; border-radius: 4px; padding: 4px 10px; font-weight: bold; } QPushButton:hover { background-color: #7f8c8d; color: white; }")
        else:
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor("#f5f5f5"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor("#000000"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor("#ffffff"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor("#e0e0e0"))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor("#000000"))
            
            tab_bg, tab_fg, pane_bg = "#e0e0e0", "#555555", "#f5f5f5"
            self.lang_combo.setStyleSheet("QComboBox { background-color: #ffffff; color: #000000; border: 1px solid #3498db; border-radius: 4px; padding: 4px 10px; font-weight: bold; min-width: 100px; } QComboBox::drop-down { border: none; }")
            self.theme_btn.setStyleSheet("QPushButton { background-color: transparent; color: #000000; border: 1px solid #7f8c8d; border-radius: 4px; padding: 4px 10px; font-weight: bold; } QPushButton:hover { background-color: #7f8c8d; color: white; }")

        QApplication.instance().setPalette(palette)
        
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: none; background-color: {pane_bg}; }}
            QTabBar::tab {{
                background-color: {tab_bg}; color: {tab_fg};
                padding: 12px 25px; font-size: 13px; font-weight: bold;
                border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 3px;
            }}
            QTabBar::tab:selected {{
                background-color: {pane_bg}; color: #3498db; border-bottom: 3px solid #3498db;
            }}
        """)

    def update_texts(self):
        self.setWindowTitle(lang_mgr.t("app_title"))
        self.tabs.setTabText(0, lang_mgr.t("tab_extract"))
        self.tabs.setTabText(1, lang_mgr.t("tab_replace"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    initial_direction = Qt.LayoutDirection.RightToLeft if lang_mgr.current_lang in ["fa", "ar", "he"] else Qt.LayoutDirection.LeftToRight
    app.setLayoutDirection(initial_direction)
    
    window = MainWindow()
    window.resize(850, 600)
    window.show()
    sys.exit(app.exec())