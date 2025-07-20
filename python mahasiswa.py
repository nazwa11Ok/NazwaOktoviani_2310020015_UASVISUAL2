import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class MahasiswaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_database()
        self.init_ui()
        self.load_data()
        
    def init_database(self):
        """Inisialisasi database SQLite"""
        self.conn = sqlite3.connect('mahasiswa.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npm TEXT UNIQUE NOT NULL,
                nama_lengkap TEXT NOT NULL,
                nama_panggilan TEXT,
                telepon TEXT,
                email TEXT,
                kelas TEXT,
                mata_kuliah TEXT,
                lokasi_kampus TEXT
            )
        ''')
        self.conn.commit()
        
    def init_ui(self):
        """Inisialisasi User Interface"""
        self.setWindowTitle("Aplikasi CRUD Mahasiswa")
        self.setGeometry(100, 100, 800, 600)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4a148c, stop:1 #1a237e);
            }
            QWidget {
                background-color: transparent;
                color: white;
                font-family: Arial, sans-serif;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                margin: 10px;
            }
        """)
        header_layout = QVBoxLayout()
        header_frame.setLayout(header_layout)
        
        title_label = QLabel("MAHASISWA")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #4a148c;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                background-color: #e1f5fe;
                border-radius: 5px;
                margin: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Form input
        form_layout = QVBoxLayout()
        
        # Input fields
        fields = [
            ("NPM", "npm_input"),
            ("NAMA LENGKAP", "nama_lengkap_input"),
            ("NAMA PANGGILAN", "nama_panggilan_input"),
            ("TELEPON", "telepon_input"),
            ("EMAIL", "email_input"),
            ("KELAS", "kelas_input"),
            ("MATA KULIAH", "mata_kuliah_input"),
            ("LOKASI KAMPUS", "lokasi_kampus_input")
        ]
        
        for label_text, attr_name in fields:
            row_layout = QHBoxLayout()
            
            label = QLabel(label_text)
            label.setFixedWidth(120)
            label.setStyleSheet("""
                QLabel {
                    color: #4a148c;
                    font-weight: bold;
                    padding: 5px;
                }
            """)
            
            input_field = QLineEdit()
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 12px;
                }
                QLineEdit:focus {
                    border: 2px solid #4a148c;
                }
            """)
            setattr(self, attr_name, input_field)
            
            row_layout.addWidget(label)
            row_layout.addWidget(input_field)
            form_layout.addLayout(row_layout)
        
        header_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.tambah_btn = QPushButton("TAMBAH")
        self.ubah_btn = QPushButton("UBAH")
        self.hapus_btn = QPushButton("HAPUS")
        self.batal_btn = QPushButton("BATAL")
        
        buttons = [self.tambah_btn, self.ubah_btn, self.hapus_btn, self.batal_btn]
        button_colors = ["#4CAF50", "#2196F3", "#F44336", "#FF9800"]
        
        for i, btn in enumerate(buttons):
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {button_colors[i]};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {button_colors[i]}dd;
                }}
                QPushButton:pressed {{
                    background-color: {button_colors[i]}aa;
                }}
            """)
            button_layout.addWidget(btn)
        
        header_layout.addLayout(button_layout)
        main_layout.addWidget(header_frame)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        headers = ["ID", "NPM", "NAMA LENGKAP", "NAMA PANGGILAN", "TELEPON", 
                  "EMAIL", "KELAS", "MATA KULIAH", "LOKASI KAMPUS"]
        self.table.setHorizontalHeaderLabels(headers)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 10px;
                margin: 10px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
            QHeaderView::section {
                background-color: #4a148c;
                color: white;
                padding: 8px;
                border: 1px solid #ccc;
                font-weight: bold;
            }
        """)
        
        # Hide ID column
        self.table.setColumnHidden(0, True)
        
        # Adjust column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(self.table)
        
        # Connect buttons
        self.tambah_btn.clicked.connect(self.tambah_data)
        self.ubah_btn.clicked.connect(self.ubah_data)
        self.hapus_btn.clicked.connect(self.hapus_data)
        self.batal_btn.clicked.connect(self.batal)
        
        # Connect table selection
        self.table.itemSelectionChanged.connect(self.on_table_select)
        
        self.selected_id = None
        
    def load_data(self):
        """Load data dari database ke table"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mahasiswa")
        data = cursor.fetchall()
        
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
    
    def clear_form(self):
        """Clear semua input field"""
        inputs = [self.npm_input, self.nama_lengkap_input, self.nama_panggilan_input,
                 self.telepon_input, self.email_input, self.kelas_input,
                 self.mata_kuliah_input, self.lokasi_kampus_input]
        for input_field in inputs:
            input_field.clear()
        self.selected_id = None
    
    def tambah_data(self):
        """Tambah data mahasiswa baru"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO mahasiswa (npm, nama_lengkap, nama_panggilan, telepon, 
                                     email, kelas, mata_kuliah, lokasi_kampus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.npm_input.text(),
                self.nama_lengkap_input.text(),
                self.nama_panggilan_input.text(),
                self.telepon_input.text(),
                self.email_input.text(),
                self.kelas_input.text(),
                self.mata_kuliah_input.text(),
                self.lokasi_kampus_input.text()
            ))
            self.conn.commit()
            self.load_data()
            self.clear_form()
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan!")
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "NPM sudah ada!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
    
    def ubah_data(self):
        """Update data mahasiswa yang dipilih"""
        if not self.selected_id:
            QMessageBox.warning(self, "Warning", "Pilih data yang akan diubah!")
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE mahasiswa SET npm=?, nama_lengkap=?, nama_panggilan=?, 
                                   telepon=?, email=?, kelas=?, mata_kuliah=?, lokasi_kampus=?
                WHERE id=?
            ''', (
                self.npm_input.text(),
                self.nama_lengkap_input.text(),
                self.nama_panggilan_input.text(),
                self.telepon_input.text(),
                self.email_input.text(),
                self.kelas_input.text(),
                self.mata_kuliah_input.text(),
                self.lokasi_kampus_input.text(),
                self.selected_id
            ))
            self.conn.commit()
            self.load_data()
            self.clear_form()
            QMessageBox.information(self, "Sukses", "Data berhasil diubah!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
    
    def hapus_data(self):
        """Hapus data mahasiswa yang dipilih"""
        if not self.selected_id:
            QMessageBox.warning(self, "Warning", "Pilih data yang akan dihapus!")
            return
            
        reply = QMessageBox.question(self, "Konfirmasi", 
                                   "Apakah Anda yakin ingin menghapus data ini?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM mahasiswa WHERE id=?", (self.selected_id,))
                self.conn.commit()
                self.load_data()
                self.clear_form()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
    
    def batal(self):
        """Batal / Clear form"""
        self.clear_form()
        self.table.clearSelection()
    
    def on_table_select(self):
        """Handle ketika baris tabel dipilih"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.selected_id = int(self.table.item(current_row, 0).text())
            
            # Fill form dengan data yang dipilih
            self.npm_input.setText(self.table.item(current_row, 1).text())
            self.nama_lengkap_input.setText(self.table.item(current_row, 2).text())
            self.nama_panggilan_input.setText(self.table.item(current_row, 3).text())
            self.telepon_input.setText(self.table.item(current_row, 4).text())
            self.email_input.setText(self.table.item(current_row, 5).text())
            self.kelas_input.setText(self.table.item(current_row, 6).text())
            self.mata_kuliah_input.setText(self.table.item(current_row, 7).text())
            self.lokasi_kampus_input.setText(self.table.item(current_row, 8).text())
    
    def closeEvent(self, event):
        """Handle ketika aplikasi ditutup"""
        self.conn.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set aplikasi style
    app.setStyle('Fusion')
    
    window = MahasiswaApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()