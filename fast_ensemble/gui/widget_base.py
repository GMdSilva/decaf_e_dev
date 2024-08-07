from PyQt5.QtWidgets import QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import uuid
def merge_configs(general_options, specific_options):
    config = general_options.copy()
    config.update(specific_options)
    return config
class AnalysisWidgetBase(QWidget):
    def __init__(self, job_manager, general_options_getter=False):
        super().__init__()
        self.job_manager = job_manager
        self.job_manager.job_finished.connect(self.on_job_finished)
        self.setStyleSheet("""
            QToolBar {
                background-color: #333333;
                color: white;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                margin: 0 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #777777;
            }
        """)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_job_manager_queue)
        self.timer.start(1000)  # Check every second

    def validate_inputs(self):
        """Override this method to implement specific validation."""
        return []

    def run_analysis(self):
        errors = self.validate_inputs()
        if errors:
            self.show_error_message(errors)
            return

        try:
            g_options = self.general_options_getter()
        except Exception:
            g_options = {}

        specific_options = self.get_specific_options()
        config = merge_configs(g_options, specific_options)
        try:
            self.run_specific_analysis(config)
        except Exception as e:
            self.show_error_message([str(e)])
            
    def get_specific_options(self):
        """Override this method to return specific options."""
        return {}

    def run_specific_analysis(self, config):
        """Override this method to run specific analysis."""
        pass

    def show_error_message(self, errors):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Invalid input")
        msg.setInformativeText("\n".join(errors))
        msg.setWindowTitle("Error")
        msg.exec_()

    def show_info_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Info")
        msg.exec_()

    def on_job_finished(self, job_id, success, message):
        status = "completed" if success else "failed"
        self.show_info_message(f"Job {job_id} {status}: {message}")

    def check_job_manager_queue(self):
        # This method can be used to periodically check for updates in the job manager queue if needed
        pass