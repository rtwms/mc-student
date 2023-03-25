import sys
from datalayer_sqlite3 import DatalayerSqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QComboBox, QToolBar, QStatusBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student App')
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon('icons/add.png'), '&Add Student', self)
        add_student_action.triggered.connect(self.insert_dlg)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction(QIcon('icons/search.png'), '&Search for a Student', self)
        search_student_action.triggered.connect(self.search_dlg)
        file_menu_item.addAction(search_student_action)

        edit_student_action = QAction('&Edit', self)
        edit_student_action.triggered.connect(self.edit_dlg)
        # file_menu_item.addAction(search_student_action)

        delete_student_action = QAction('&Delete Student', self)
        delete_student_action.triggered.connect(self.delete_dlg)
        # file_menu_item.addAction(search_student_action)

        action_about = QAction('&About', self)
        action_about.setMenuRole(QAction.MenuRole.NoRole)
        help_menu_item.addAction(action_about)

        """
        add a table
        """
        self.table = QTableWidget()

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self.cell_clicked)
        self.setCentralWidget(self.table)

        tbar = QToolBar()
        tbar.setMovable(True)
        self.addToolBar(tbar)

        tbar.addAction(add_student_action)
        tbar.addAction(search_student_action)

        sbar = QStatusBar()
        record_text = QLabel('hi')
        sbar.addWidget(record_text)
        self.setStatusBar(sbar)

    def cell_clicked(self):
        row = self.table.currentRow()
        name = self.table.item(row, 1).text()

        children = self.findChildren(QPushButton)
        if children:
            for ch in children:
                self.statusBar().removeWidget(ch)

        edit_btn = QPushButton(f'Edit {name}')
        edit_btn.clicked.connect(self.edit_dlg)
        self.statusBar().addWidget(edit_btn)

        dele_btn = QPushButton(f'Delete {name}')
        dele_btn.clicked.connect(self.delete_dlg)

        self.statusBar().addWidget(dele_btn)

    def load_data(self):
        dbc, cursor = dl.connect()
        result = dbc.execute('SELECT * from students s order by s.id')
        # clear any existing data after an add
        self.table.setRowCount(0)
        for row_idx, row in enumerate(result):
            self.table.insertRow(row_idx)
            for col_idx, item in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
                # print('%s %s' % (col_idx, item))
        dbc.close()

    def insert_dlg(self):
        dlg = InsertDialog()
        dlg.exec()

    def search_dlg(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit_dlg(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_dlg(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search for a Student')
        self.setFixedWidth(200)
        self.setFixedHeight(250)
        layout = QVBoxLayout()

        row = home.table.currentRow()
        sid = home.table.item(row, 0).text()
        name = home.table.item(row, 1).text()
        course = home.table.item(row, 2).text()
        mobile = home.table.item(row, 3).text()

        i_label_id = QLabel(f'id: {sid}')
        self.i_edit_id = QLineEdit(sid)
        self.i_edit_id.setReadOnly(True)

        i_label_name = QLabel('Name')
        self.i_edit_name = QLineEdit(name)

        i_label_course = QLabel('Course')
        self.i_edit_course = QComboBox()
        self.i_edit_course.addItems(['Astronomy', 'Biology', 'Math', 'English', 'Physics'])
        self.i_edit_course.setCurrentText(course)
        # self.i_edit_course = QLineEdit(course)

        i_label_mobile = QLabel('Mobile')
        self.i_edit_mobile = QLineEdit(mobile)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_student)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.cancel)

        layout.addWidget(i_label_id)
        layout.addWidget(self.i_edit_id)
        layout.addWidget(i_label_name)
        layout.addWidget(self.i_edit_name)
        layout.addWidget(i_label_course)
        layout.addWidget(self.i_edit_course)
        layout.addWidget(i_label_mobile)
        layout.addWidget(self.i_edit_mobile)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def cancel(self):
        self.close()

    def save_student(self):
        s_id = self.i_edit_id.text()
        s_name = self.i_edit_name.text()
        s_course = self.i_edit_course.itemText(self.i_edit_course.currentIndex())
        s_mobile = self.i_edit_mobile.text()

        sql_update = f'UPDATE students set ' + \
                     f" name = \"{s_name}\", course = \"{s_course}\", mobile = \"{s_mobile}\"" + \
                     f' WHERE id = \"{s_id}\"'

        dl.update(sql_update)

        home.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search for a Student')
        self.setFixedWidth(200)
        self.setFixedHeight(250)
        layout = QVBoxLayout()

        row = home.table.currentRow()
        sid = home.table.item(row, 0).text()
        name = home.table.item(row, 1).text()

        i_delete_label = QLabel('Id')
        layout.addWidget(i_delete_label)
        self.i_delete_id = QLineEdit(sid)
        self.i_delete_id.setReadOnly(True)
        layout.addWidget(self.i_delete_id)
        self.i_delete_name = QLabel(name)
        layout.addWidget(self.i_delete_name)

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(self.delete_one)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.cancel)
        layout.addWidget(delete_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def cancel(self):
        self.close()

    def delete_one(self):
        d_id = self.i_delete_id.text()
        sql_update = f'DELETE FROM students' + \
                     f' WHERE id = \"{d_id}\"'

        result = dl.delete(sql_update)

        home.load_data()
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search for a Student')
        self.setFixedWidth(200)
        self.setFixedHeight(250)
        layout = QVBoxLayout()

        self.i_search_edit = QLineEdit('Name')
        layout.addWidget(self.i_search_edit)

        self.i_error_text = QLabel('')
        layout.addWidget(self.i_error_text)

        b_search = QPushButton('Search')
        b_search.clicked.connect(self.search)
        layout.addWidget(b_search)

        self.setLayout(layout)
        print('finished setting up insert dialog')

    def search(self):
        print('searching')
        name = self.i_search_edit.text()
        result = dl.search(f"SELECT * FROM students where name like '%{name}%'")
        kount = 0
        for row_idx, row in result:
            kount = kount + 1
            print(f'looped:  {type(row)}')
            sn = row[1]
            print(f'found {sn}')
            items = home.table.findItems(sn, Qt.MatchFlag.MatchFixedString)
            for item in items:
                home.table.item(item.row(), 1).setSelected(True)
        if kount == 0:
            self.i_error_text.setText('Not Found')


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Student')
        self.setFixedWidth(200)
        self.setFixedHeight(250)
        layout = QVBoxLayout()

        self.i_name_edit = QLineEdit('Name')
        self.i_name_edit.setPlaceholderText('Name')
        layout.addWidget(self.i_name_edit)

        self.i_course_edit = QComboBox()
        self.i_course_edit.addItems(['Astronomy', 'Biology', 'Math', 'English', 'Physics'])
        layout.addWidget(self.i_course_edit)

        self.i_mobile_edit = QLineEdit('Mobile')
        self.i_mobile_edit.setPlaceholderText('Mobile #')
        layout.addWidget(self.i_mobile_edit)

        b_add = QPushButton('Add')
        b_add.clicked.connect(self.registered)
        layout.addWidget(b_add)

        self.setLayout(layout)
        print('finished setting up insert dialog')

    def registered(self):
        print(f'inserting {self.i_name_edit}')
        name = self.i_name_edit.text()
        course = self.i_course_edit.itemText(self.i_course_edit.currentIndex())
        mobile = self.i_mobile_edit.text()

        statement = f"INSERT INTO students (name, course, mobile) VALUES ('{name}', '{course}', '{mobile}')"
        dl.insert(statement)

        home.load_data()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dl = DatalayerSqlite3('database.db')
    home = MainWindow()
    home.setMinimumSize(600, 400)
    home.show()
    home.load_data()
    sys.exit(app.exec())
