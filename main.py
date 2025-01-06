import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import threading
import time

# Simulated OCR function
def simulate_ocr_process():
    time.sleep(5)
    return {"success": 10, "failure": 2}

# Main App Class
class OCRApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCR Process App")
        self.setGeometry(100, 100, 600, 400)

        layout = QtWidgets.QVBoxLayout()

        # Create Bucket Section
        bucket_group = QtWidgets.QGroupBox("1. Create Bucket and Folders")
        bucket_layout = QtWidgets.QHBoxLayout()

        self.bucket_name_input = QtWidgets.QLineEdit()
        self.bucket_name_input.setPlaceholderText("Enter bucket name")
        bucket_layout.addWidget(self.bucket_name_input)

        create_bucket_btn = QtWidgets.QPushButton("Create Bucket")
        create_bucket_btn.clicked.connect(self.create_bucket)
        bucket_layout.addWidget(create_bucket_btn)

        bucket_group.setLayout(bucket_layout)
        layout.addWidget(bucket_group)

        # Upload Images Section
        upload_group = QtWidgets.QGroupBox("2. Upload Images")
        upload_layout = QtWidgets.QVBoxLayout()

        self.upload_btn = QtWidgets.QPushButton("Upload Images")
        self.upload_btn.clicked.connect(self.upload_files)
        upload_layout.addWidget(self.upload_btn)

        self.upload_list = QtWidgets.QListWidget()
        upload_layout.addWidget(self.upload_list)

        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)

        # Run OCR Section
        ocr_group = QtWidgets.QGroupBox("3. Run OCR Process")
        ocr_layout = QtWidgets.QVBoxLayout()

        self.ocr_btn = QtWidgets.QPushButton("Run OCR")
        self.ocr_btn.clicked.connect(self.run_ocr)
        ocr_layout.addWidget(self.ocr_btn)

        ocr_group.setLayout(ocr_layout)
        layout.addWidget(ocr_group)

        # Logs Section
        log_group = QtWidgets.QGroupBox("Logs")
        log_layout = QtWidgets.QVBoxLayout()

        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Status Section
        self.status_label = QtWidgets.QLabel("Status: Waiting for user action.")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def create_bucket(self):
        bucket_name = self.bucket_name_input.text()
        if not bucket_name:
            QtWidgets.QMessageBox.critical(self, "Error", "Bucket name cannot be empty!")
            return

        # Simulate bucket creation
        time.sleep(1)
        self.status_label.setText(f"Bucket '{bucket_name}' created with folders for Raw Images, Successful OCRs, and Failed OCRs.")

    def upload_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Images")
        if files:
            self.upload_list.clear()
            self.upload_list.addItems(files)
            self.status_label.setText("Files selected for upload.")

    def run_ocr(self):
     def task():
        start_time = time.time()
        self.update_status("Running OCR process...")
        result = simulate_ocr_process()
        end_time = time.time()
        completion_time = end_time - start_time

        log_message = (
            f"OCR Completed:\n"
            f"Success: {result['success']}\n"
            f"Failures: {result['failure']}\n"
            f"Time Taken: {completion_time:.2f} seconds"
        )
        self.update_log(log_message)
        self.update_status("OCR process completed.")

        # Run the task in a separate thread
        threading.Thread(target=task).start()

    def update_status(self, message):
     # Use QMetaObject.invokeMethod to ensure thread-safe UI updates
     QtCore.QMetaObject.invokeMethod(
        self.status_label, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, message)
    )

    def update_log(self, message):
     # Use QMetaObject.invokeMethod for thread-safe updates to QTextEdit
     QtCore.QMetaObject.invokeMethod(
        self.log_output, "append", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, message)
    )


# Main execution
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
