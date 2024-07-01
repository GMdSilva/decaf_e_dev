from pathlib import Path

from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QListWidget, QListWidgetItem

ICON_ROOT = Path(__file__).parent / "icons"
STYLES = r"""
    QListWidget {
        min-width: 294px;
        background: none;
        font-size: 13pt;
        color: #333333;
    }
    QListWidget::item {
        width: 80px;
        height: 110px;
        border-radius: 4px;
        margin: 10px;
        padding: 10px;
        background: #f5f5f5;
        color: #333333;
    }
    QListWidget::item:hover {
        background: #e7f3ff;
    }
    QListWidget::item:selected {
        background: #007BFF;
        color: white;
    }
"""

def _get_icon(name):
    path = ICON_ROOT / f'{name.lower().replace(" ", "_")}.png'
    if not path.exists():
        return ""
    return str(path)


class Icons(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMovement(self.Static)  # The items cannot be moved by the user.
        self.setViewMode(self.IconMode)  # make items icons
        self.setResizeMode(self.Adjust)  # re-layout when view is resized.
        self.setUniformItemSizes(True)  # better performance
        self.setIconSize(QSize(100, 100))
        self.setWordWrap(True)
        self.setStyleSheet(STYLES)

    def addItem(self, label: str, tool_tip: str = None):
        if isinstance(label, QListWidgetItem):
            super().addItem(label)

        item = QListWidgetItem(QIcon(_get_icon(label)), label)
        if tool_tip is not None:
            item.setToolTip(tool_tip)
        super().addItem(item)

    def addItems(self, labels: dict) -> None:
        for label in labels:
            if hasattr(labels[label], "tool_tip"):
                self.addItem(label, labels[label].tool_tip)
            else:
                self.addItem(label)