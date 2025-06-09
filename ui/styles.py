MAIN_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
}

QLabel {
    color: #2c3e50;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:disabled {
    background-color: #bdc3c7;
}

QTableWidget {
    background-color: white;
    alternate-background-color: #f9f9f9;
    selection-background-color: #3498db;
    selection-color: white;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 4px;
}

QTableWidget::item {
    padding: 4px;
}

QHeaderView::section {
    background-color: #34495e;
    color: white;
    padding: 8px;
    border: none;
}

QComboBox {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 4px;
    min-width: 100px;
}

QComboBox:hover {
    border-color: #3498db;
}

QSpinBox, QDateEdit, QLineEdit {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 4px;
}

QSpinBox:hover, QDateEdit:hover, QLineEdit:hover {
    border-color: #3498db;
}

QDialog {
    background-color: #f0f0f0;
}

/* Custom classes */
.header-label {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
    margin: 10px;
}

.section-label {
    font-size: 16px;
    font-weight: bold;
    color: #34495e;
    margin-top: 10px;
}

.stats-good {
    color: #27ae60;
}

.stats-medium {
    color: #f39c12;
}

.stats-poor {
    color: #c0392b;
}
"""
