import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic

class NilaiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form_nilai.ui", self)  # Pastikan nama file UI-nya sesuai

        # Daftar untuk menyimpan data input
        self.data_nilai = []

        # Event handler tombol
        self.pushButton.clicked.connect(self.tambah_data)

        # Inisialisasi header tabel
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "ID Mahasiswa", "Nilai Harian", "Nilai UTS", "Nilai UAS"
        ])

    def tambah_data(self):
        id_ = self.lineEdit.text()
        id_mhs = self.lineEdit_2.text()
        harian = self.lineEdit_3.text()
        tugas = self.lineEdit_4.text()  # ditampilkan kalau mau tambahkan kolom tugas
        uts = self.lineEdit_5.text()
        uas = self.lineEdit_6.text()

        # Simpan data ke list
        data = [id_, id_mhs, harian, uts, uas]
        self.data_nilai.append(data)

        # Update tabel
        self.tableWidget.setRowCount(len(self.data_nilai))
        for row_idx, row_data in enumerate(self.data_nilai):
            for col_idx, value in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(value))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NilaiWindow()
    window.setWindowTitle("Form Input Nilai Mahasiswa")
    window.show()
    sys.exit(app.exec_())