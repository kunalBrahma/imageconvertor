import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QCheckBox, QLabel, QListWidget, QFileDialog, QMessageBox,
                             QProgressBar, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PIL import Image

class ImageConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to WebP Converter")
        self.setGeometry(100, 100, 500, 650)
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon("icon.icns"))

        self.output_folder = None
        self.current_preview_index = -1

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.header_label = QLabel("Image to WebP Converter")
        self.header_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #1D2521;")
        self.layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.format_label = QLabel("Input Image Format:")
        self.layout.addWidget(self.format_label)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG"])
        self.format_combo.currentTextChanged.connect(self.update_file_filter)
        self.layout.addWidget(self.format_combo)

        self.preview_label = QLabel("No image selected")
        self.preview_label.setFixedSize(200, 200)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid #D3D3D3; border-radius: 8px; background: #FFFFFF;")
        self.layout.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignCenter)

        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("◄")
        self.prev_button.setFixedWidth(50)
        self.prev_button.clicked.connect(self.show_previous_image)
        nav_layout.addWidget(self.prev_button)
        self.next_button = QPushButton("►")
        self.next_button.setFixedWidth(50)
        self.next_button.clicked.connect(self.show_next_image)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(100)
        self.file_list.itemClicked.connect(self.preview_selected_image)
        self.layout.addWidget(self.file_list)

        self.quality_label = QLabel("WebP Quality (0-100, ignored for lossless):")
        self.layout.addWidget(self.quality_label)
        self.quality_input = QLineEdit("80")
        self.quality_input.setMaximumWidth(100)
        self.layout.addWidget(self.quality_input)

        self.lossless_check = QCheckBox("Lossless WebP")
        self.layout.addWidget(self.lossless_check)

        self.output_folder_label = QLabel("Output Folder: Not set")
        self.output_folder_label.setStyleSheet("color: #555; font-style: italic;")
        self.layout.addWidget(self.output_folder_label)
        self.change_folder_button = QPushButton("Set/Change Output Folder")
        self.change_folder_button.clicked.connect(self.set_output_folder)
        self.layout.addWidget(self.change_folder_button)

        button_layout = QHBoxLayout()
        self.select_button = QPushButton("Select Images")
        self.select_button.clicked.connect(self.select_images)
        button_layout.addWidget(self.select_button)

        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.clicked.connect(self.clear_selection)
        button_layout.addWidget(self.clear_button)

        self.convert_button = QPushButton("Convert to WebP")
        self.convert_button.clicked.connect(self.convert_images)
        button_layout.addWidget(self.convert_button)
        self.layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Select images to convert")
        self.status_label.setStyleSheet("color: #555;")
        self.layout.addWidget(self.status_label)

        self.selected_files = []
        self.current_filter = "*.png"

        self.setStyleSheet("""
            QMainWindow { background-color: #F5F5F5; }
            QPushButton {
                background-color: #007AFF;
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                border: none;
            }
            QPushButton:hover { background-color: #005BBB; }
            QPushButton:disabled { background-color: #CCCCCC; }
            QLineEdit, QListWidget {
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                padding: 6px;
                font-size: 14px;
                background: #FFFFFF;
            }
            QComboBox {
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                padding: 6px;
                font-size: 14px;
                background: #FFFFFF;
                color: #1D2521;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #D3D3D3;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                background: #FFFFFF;
                color: #1D2521;
                selection-background-color: #E0E7FF;
                selection-color: #1D2521;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px;
                background: #FFFFFF;
                color: #1D2521;
            }
            QComboBox QAbstractItemView::item:hover {
                background: #E0E7FF;
                color: #1D2521;
            }
            QComboBox QAbstractItemView::item:selected {
                background: #E0E7FF;
                color: #1D2521;
            }
            QLabel { font-size: 14px; color: #1D2521; font-family: system-ui; }
            QProgressBar {
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                text-align: center;
                background: #FFFFFF;
            }
            QProgressBar::chunk { background-color: #007AFF; border-radius: 6px; }
            QListWidget::item:selected { background-color: #E0E7FF; color: #1D2521; }
        """)

    def update_file_filter(self):
        format_map = {"PNG": "*.png", "JPEG": "*.jpg *.jpeg"}
        self.current_filter = format_map[self.format_combo.currentText()]
        self.selected_files = []
        self.file_list.clear()
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText("No image selected")
        self.current_preview_index = -1
        self.update_navigation_buttons()
        self.status_label.setText(f"Selected format: {self.format_combo.currentText()}")

    def set_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Output Folder: {os.path.basename(folder)}")
            self.status_label.setText(f"Output folder set to: {folder}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()
                 if url.toLocalFile().lower().endswith(tuple(self.current_filter.split()))]
        self.selected_files.extend(files)
        self.update_file_list()

    def select_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "", f"Images ({self.current_filter})"
        )
        self.selected_files.extend(files)
        self.update_file_list()

    def update_file_list(self):
        self.file_list.clear()
        for file in self.selected_files:
            self.file_list.addItem(os.path.basename(file))
        self.status_label.setText(f"Selected {len(self.selected_files)} image(s)")
        if self.selected_files:
            self.current_preview_index = 0
            self.update_preview()
            self.file_list.setCurrentRow(0)
        else:
            self.current_preview_index = -1
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("No image selected")
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self.prev_button.setEnabled(self.current_preview_index > 0)
        self.next_button.setEnabled(self.current_preview_index < len(self.selected_files) - 1)

    def show_previous_image(self):
        if self.current_preview_index > 0:
            self.current_preview_index -= 1
            self.update_preview()
            self.file_list.setCurrentRow(self.current_preview_index)

    def show_next_image(self):
        if self.current_preview_index < len(self.selected_files) - 1:
            self.current_preview_index += 1
            self.update_preview()
            self.file_list.setCurrentRow(self.current_preview_index)

    def preview_selected_image(self, item):
        self.current_preview_index = self.file_list.row(item)
        self.update_preview()

    def update_preview(self):
        if 0 <= self.current_preview_index < len(self.selected_files):
            try:
                pixmap = QPixmap(self.selected_files[self.current_preview_index]).scaled(
                    200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(pixmap)
            except:
                self.preview_label.setText("Preview not available")
        else:
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("No image selected")
        self.update_navigation_buttons()

    def clear_selection(self):
        self.selected_files = []
        self.file_list.clear()
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText("No image selected")
        self.current_preview_index = -1
        self.update_navigation_buttons()
        self.status_label.setText("Selection cleared")

    def convert_images(self):
        if not self.selected_files:
            QMessageBox.critical(self, "Error", "Please select at least one image!")
            return

        if not self.output_folder:
            self.set_output_folder()
            if not self.output_folder:
                return

        try:
            quality = int(self.quality_input.text())
            if not 0 <= quality <= 100:
                raise ValueError("Quality must be between 0 and 100")
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid quality value!")
            return

        self.convert_button.setEnabled(False)
        self.select_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.selected_files))
        self.progress_bar.setValue(0)

        for i, file_path in enumerate(self.selected_files):
            try:
                img = Image.open(file_path)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(self.output_folder, f"{base_name}.webp")
                img.save(
                    output_path,
                    "WEBP",
                    quality=quality if not self.lossless_check.isChecked() else 100,
                    lossless=self.lossless_check.isChecked(),
                    method=6
                )
                img.close()
                self.progress_bar.setValue(i + 1)
            except Exception as e:
                self.progress_bar.setVisible(False)
                self.convert_button.setEnabled(True)
                self.select_button.setEnabled(True)
                self.clear_button.setEnabled(True)
                QMessageBox.critical(self, "Error", f"Failed to convert {file_path}: {str(e)}")
                return

        self.progress_bar.setVisible(False)
        self.convert_button.setEnabled(True)
        self.select_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        QMessageBox.information(self, "Success", f"Converted {len(self.selected_files)} image(s) to WebP!")
        self.status_label.setText("Conversion complete")
        self.clear_selection()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.icns"))
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec())