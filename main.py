import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("student_info.ui", self)  # Pastikan nama file UI kamu benar
        
        # Koneksi ke database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",          # Ganti jika username MySQL kamu berbeda
            password="",          # Ganti jika ada password MySQL
            database="student_info_db"
        )
        self.cursor = self.db.cursor()
        
        # Tombol
        self.pushButton.clicked.connect(self.tambah_data)
        self.pushButton_2.clicked.connect(self.ubah_data)
        self.pushButton_3.clicked.connect(self.hapus_data)
        self.pushButton_4.clicked.connect(self.clear_form)
        
        self.tampilkan_data()

    def tambah_data(self):
        sql = "INSERT INTO mahasiswa (npm, nama_lengkap, nama_panggilan, telepon, email, kelas, mata_kuliah, lokasi_kampus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            self.lineEdit.text(),
            self.lineEdit_2.text(),
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
            self.comboBox.currentText(),
            self.comboBox_2.currentText(),
            self.lineEdit_8.text()
        )
        self.cursor.execute(sql, val)
        self.db.commit()
        self.tampilkan_data()

    def ubah_data(self):
        row = self.tableWidget.currentRow()
        npm = self.tableWidget.item(row, 0).text()
        sql = """UPDATE mahasiswa SET nama_lengkap=%s, nama_panggilan=%s, telepon=%s, email=%s, kelas=%s, mata_kuliah=%s, lokasi_kampus=%s
                 WHERE npm=%s"""
        val = (
            self.lineEdit_2.text(),
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
            self.comboBox.currentText(),
            self.comboBox_2.currentText(),
            self.lineEdit_8.text(),
            npm
        )
        self.cursor.execute(sql, val)
        self.db.commit()
        self.tampilkan_data()

    def hapus_data(self):
        row = self.tableWidget.currentRow()
        npm = self.tableWidget.item(row, 0).text()
        sql = "DELETE FROM mahasiswa WHERE npm = %s"
        val = (npm,)
        self.cursor.execute(sql, val)
        self.db.commit()
        self.tampilkan_data()

    def tampilkan_data(self):
        self.cursor.execute("SELECT * FROM mahasiswa")
        result = self.cursor.fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(8)
        for row_num, row_data in enumerate(result):
            for col_num, data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def clear_form(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.lineEdit_8.clear()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
sys.exit(app.exec_())