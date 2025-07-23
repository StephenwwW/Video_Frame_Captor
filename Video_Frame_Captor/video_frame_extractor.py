# -*- coding: utf-8 -*-

"""
Video Frame Captor
A simple GUI tool to batch extract frames from video files at specified timestamps.
Now with multi-language support.

影片畫格擷取器
一個簡單的圖形介面工具，用於在指定的時間點批次擷取影片畫格。
現已支援多國語言。

Author: StephenwwW (on GitHub)
"""

import sys
import os
import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QFileDialog, QLabel, QProgressBar, QMessageBox, QComboBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont

# 1. ==== 集中化文字管理 (Internationalization Strings) ====
I18N_STRINGS = {
    'en': {
        "window_title": "Video Frame Captor",
        "target_folder_label": "Target Folder:",
        "folder_placeholder": "Select a folder containing video files...",
        "browse_button": "Browse...",
        "timestamp_label": "Capture Times (s):",
        "timestamp_placeholder": "e.g., 3, 5.5, 10 (comma-separated)",
        "start_button": "Start Capture",
        "processing_button": "Processing...",
        "initial_status": "Please select a folder and set timestamps.",
        "confirm_exit_title": "Confirm Exit",
        "confirm_exit_body": "A task is still running. Do you want to stop it and exit?",
        "error_invalid_folder_title": "Input Error",
        "error_invalid_folder_body": "Please select a valid folder.",
        "error_no_timestamp_title": "Input Error",
        "error_no_timestamp_body": "Please enter at least one timestamp.",
        "error_invalid_timestamp_title": "Input Error",
        "error_invalid_timestamp_body": "Invalid timestamp format.\nPlease use numbers separated by commas (e.g., 3, 5.5).",
        "worker_invalid_timestamp": "Error: Invalid timestamp format.",
        "worker_no_files": "No .mov or .mp4 files found.",
        "worker_stopped": "Processing stopped by user.",
        "worker_processing_status": "Processing [{i}/{total}]: {filename}",
        "worker_all_done": "All tasks completed!",
        "worker_critical_error": "A critical error occurred: {e}",
        "msg_box_success_title": "Success",
        "msg_box_info_title": "Info"
    },
    'zh_TW': {
        "window_title": "影片畫格擷取器",
        "target_folder_label": "目標資料夾:",
        "folder_placeholder": "請選擇包含影片檔案的資料夾...",
        "browse_button": "瀏覽...",
        "timestamp_label": "擷取時間點 (秒):",
        "timestamp_placeholder": "例如：3, 5.5, 10 (用逗號分隔)",
        "start_button": "開始擷取",
        "processing_button": "處理中...",
        "initial_status": "請選擇資料夾並設定時間點。",
        "confirm_exit_title": "確認退出",
        "confirm_exit_body": "任務仍在運行中。您確定要中止並退出嗎？",
        "error_invalid_folder_title": "輸入錯誤",
        "error_invalid_folder_body": "請選擇一個有效的資料夾。",
        "error_no_timestamp_title": "輸入錯誤",
        "error_no_timestamp_body": "請輸入至少一個擷取時間點。",
        "error_invalid_timestamp_title": "輸入錯誤",
        "error_invalid_timestamp_body": "時間點格式無效。\n請使用以逗號分隔的數字 (例如: 3, 5.5)。",
        "worker_invalid_timestamp": "錯誤：時間點格式無效。",
        "worker_no_files": "找不到任何 .mov 或 .mp4 檔案。",
        "worker_stopped": "處理已由使用者中止。",
        "worker_processing_status": "正在處理 [{i}/{total}]: {filename}",
        "worker_all_done": "全部任務完成！",
        "worker_critical_error": "發生嚴重錯誤：{e}",
        "msg_box_success_title": "成功",
        "msg_box_info_title": "提示"
    }
}


class Worker(QThread):
    progress_updated = pyqtSignal(int, int, str, bool)

    def __init__(self, folder_path, timestamps_str, lang):
        super().__init__()
        self.folder_path = folder_path
        self.timestamps_str = timestamps_str
        self.lang = lang
        self.i18n = I18N_STRINGS[self.lang]
        self._is_running = True

    def run(self):
        try:
            try:
                timestamps = sorted(list(set([float(t.strip()) for t in self.timestamps_str.split(',') if t.strip()])))
                if not timestamps: raise ValueError
            except ValueError:
                self.progress_updated.emit(0, 1, self.i18n["worker_invalid_timestamp"], True)
                return

            video_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.mov', '.mp4'))]
            total_files = len(video_files)

            if total_files == 0:
                self.progress_updated.emit(0, 1, self.i18n["worker_no_files"], True)
                return

            output_dir = os.path.join(self.folder_path, "images")
            os.makedirs(output_dir, exist_ok=True)

            for i, filename in enumerate(video_files):
                if not self._is_running:
                    self.progress_updated.emit(i, total_files, self.i18n["worker_stopped"], True)
                    return

                current_file_msg = self.i18n["worker_processing_status"].format(i=i+1, total=total_files, filename=filename)
                self.progress_updated.emit(i, total_files, current_file_msg, False)
                video_path = os.path.join(self.folder_path, filename)
                base_name = os.path.splitext(filename)[0]

                try:
                    cap = cv2.VideoCapture(video_path)
                    if not cap.isOpened(): continue
                    fps = cap.get(cv2.CAP_PROP_FPS) or 30

                    for ts in timestamps:
                        frame_number = int(ts * fps)
                        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                        ret, frame = cap.read()
                        if ret:
                            output_filename = f"{base_name}_sec_{ts}.png"
                            output_path = os.path.join(output_dir, output_filename)
                            is_success, buffer = cv2.imencode(".png", frame)
                            if is_success:
                                with open(output_path, 'wb') as f:
                                    f.write(buffer)
                    cap.release()
                except Exception:
                    continue

            self.progress_updated.emit(total_files, total_files, self.i18n["worker_all_done"], True)

        except Exception as e:
            self.progress_updated.emit(0, 1, self.i18n["worker_critical_error"].format(e=e), True)

    def stop(self):
        self._is_running = False

class VideoFrameCaptor(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.current_lang = 'zh_TW' # 預設語言
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 520, 280) # 稍微加寬加高以容納新元件
        self.setFont(QFont("Microsoft JhengHei UI", 10))

        # 2. ==== 新增語言切換開關 ====
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("繁體中文", "zh_TW")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)

        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        lang_layout.addWidget(self.lang_combo)

        # 主要佈局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addLayout(lang_layout) # 將語言開關放在最上面

        # --- Folder Selection ---
        self.folder_label = QLabel()
        self.folder_path_edit = QLineEdit()
        self.browse_button = QPushButton()
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_path_edit)
        folder_layout.addWidget(self.browse_button)
        main_layout.addLayout(folder_layout)

        # --- Timestamp Input ---
        self.timestamp_label = QLabel()
        self.time_edit = QLineEdit()
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.timestamp_label)
        time_layout.addWidget(self.time_edit)
        main_layout.addLayout(time_layout)

        # --- Start Button ---
        self.start_button = QPushButton()
        self.start_button.setStyleSheet(
            "QPushButton { background-color: #28a745; color: white; font-weight: bold; padding: 8px; border-radius: 5px; }"
            "QPushButton:hover { background-color: #218838; }"
            "QPushButton:disabled { background-color: #5a6268; }"
        )
        self.start_button.clicked.connect(self.start_processing)
        main_layout.addWidget(self.start_button)

        # --- Progress & Status ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet("QProgressBar { height: 18px; border-radius: 5px; }")
        main_layout.addWidget(self.progress_bar)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)
        self.retranslate_ui(self.current_lang) # 初始化UI文字

    # 3. ==== 建立翻譯函式 ====
    def retranslate_ui(self, lang):
        """Updates all UI text elements to the selected language."""
        self.current_lang = lang
        i18n = I18N_STRINGS[lang]

        self.setWindowTitle(i18n["window_title"])
        self.folder_label.setText(i18n["target_folder_label"])
        self.folder_path_edit.setPlaceholderText(i18n["folder_placeholder"])
        self.browse_button.setText(i18n["browse_button"])
        self.timestamp_label.setText(i18n["timestamp_label"])
        self.time_edit.setPlaceholderText(i18n["timestamp_placeholder"])
        self.start_button.setText(i18n["start_button"])
        self.status_label.setText(i18n["initial_status"])

    def on_language_changed(self):
        """Slot for handling language change."""
        lang_code = self.lang_combo.currentData()
        self.retranslate_ui(lang_code)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.windowTitle())
        if folder:
            self.folder_path_edit.setText(folder)

    def start_processing(self):
        i18n = I18N_STRINGS[self.current_lang]
        folder_path = self.folder_path_edit.text()
        time_str = self.time_edit.text()

        if not folder_path or not os.path.isdir(folder_path):
            QMessageBox.warning(self, i18n["error_invalid_folder_title"], i18n["error_invalid_folder_body"])
            return

        if not time_str:
            QMessageBox.warning(self, i18n["error_no_timestamp_title"], i18n["error_no_timestamp_body"])
            return

        try:
            [float(t.strip()) for t in time_str.split(',') if t.strip()]
        except ValueError:
            QMessageBox.warning(self, i18n["error_invalid_timestamp_title"], i18n["error_invalid_timestamp_body"])
            return

        self.set_controls_enabled(False)
        self.worker = Worker(folder_path, time_str, self.current_lang)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def update_progress(self, current, total, message, is_finished):
        i18n = I18N_STRINGS[self.current_lang]
        self.status_label.setText(message)
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)

        if is_finished:
            title = i18n["msg_box_success_title"]
            if "錯誤" in message or "Error" in message or "找不到" in message or "No" in message or "中止" in message or "stopped" in message:
                title = i18n["msg_box_info_title"]
            QMessageBox.information(self, title, message)

    def set_controls_enabled(self, enabled):
        i18n = I18N_STRINGS[self.current_lang]
        self.start_button.setEnabled(enabled)
        self.browse_button.setEnabled(enabled)
        self.folder_path_edit.setEnabled(enabled)
        self.time_edit.setEnabled(enabled)
        self.lang_combo.setEnabled(enabled)
        self.start_button.setText(i18n["start_button"] if enabled else i18n["processing_button"])

    def on_finished(self):
        self.set_controls_enabled(True)
        self.progress_bar.setValue(0)

    def closeEvent(self, event):
        i18n = I18N_STRINGS[self.current_lang]
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(self, i18n["confirm_exit_title"], i18n["confirm_exit_body"],
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                           QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoFrameCaptor()
    ex.show()
    sys.exit(app.exec())