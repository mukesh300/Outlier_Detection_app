import sys
import os

from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from db_helper import *

welcome_screen = CWD + config["ui"]["welcome_screen"]
login_screen = CWD + config["ui"]["loginscreen"]
create_account_screen = CWD + config["ui"]["signup_screen"]
window_title = CWD + config["ui"]["signup_screen"]
thumbnail_path = CWD + config["data"]["thumbnail_path"]


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi(welcome_screen, self)
        # self.setWindowTitle(window_title)
        self.login.clicked.connect(self.gotologin)
        self.new_account.clicked.connect(self.createaccount)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def createaccount(self):
        new = CreateAccountScreen()
        widget.addWidget(new)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi(login_screen, self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button.clicked.connect(self.login_func)
        self.signup_button.clicked.connect(self.createaccount)

    def createaccount(self):
        new = CreateAccountScreen()
        widget.addWidget(new)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def login_func(self):
        user = self.email_field.text()
        password = self.password_field.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all the fields")

        else:
            result_pass = None
            conn = None
            try:
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                query = f"SELECT password FROM user_data WHERE username = '{user}'"
                cur.execute(query)
                result_pass = cur.fetchone()[0]
            except Exception as e:
                print(e)
            finally:
                if conn:
                    conn.close()
            if result_pass == password:
                self.gotogallery()
                print("logged in successfuly!")
            else:
                self.error.setText("Invalid username or password")

    def gotogallery(self):
        gallery = Gallery()
        gallery.disp_all()
        widget.addWidget(gallery)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAccountScreen(QDialog):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi(create_account_screen, self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_button.clicked.connect(self.signup_func)
        self.login_button.clicked.connect(self.gotologin)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def signup_func(self):
        user = self.username_field.text()
        password = self.password_field.text()
        confirm_password = self.confirmpassword_field.text()
        if len(user) == 0 or len(password) == 0 or len(confirm_password) == 0:
            self.error.setText("Please input all the fields")
        else:
            result_pass = None
            conn = None
            try:
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                query = f"SELECT password FROM user_data WHERE username = '{user}'"
                cur.execute(query)
                result_pass = cur.fetchone()
            except Exception as e:
                print(e)
            finally:
                if conn:
                    conn.close()
            if result_pass is not None:
                self.error.setText("User already exists, please login")
            else:
                if password != confirm_password:
                    self.error.setText("Passwords doesn't match!")
                else:
                    try:
                        conn = sqlite3.connect(DB)
                        cur = conn.cursor()
                        query = f'INSERT INTO user_data VALUES ("{user}", "{password}")'
                        cur.execute(query)
                        conn.commit()
                    except Exception as e:
                        print(e)
                    finally:
                        if conn:
                            conn.close()
                    self.error.setStyleSheet("color : rgb(114, 159, 207)")
                    self.error.setText("User created Successfully!")


class Gallery(QDialog):
    def __init__(self):
        super(Gallery, self).__init__()
        self.units = get_all()
        self.good_units = get_good()
        self.bad_units = get_bad()
        self.n_units = len(get_all())
        self.n_gunits = len(get_good())
        self.n_bunits = len(get_bad())
        self.current_range = (0, 28)
        self.current_sel = "all"
        self.init_gallery()
        self.logout_button.clicked.connect(self.logout)
        self.left_button.clicked.connect(self.get_prev)
        self.right_button.clicked.connect(self.get_next)
        self.sel_all.clicked.connect(self.disp_all)
        self.sel_good.clicked.connect(self.disp_good)
        self.sel_bad.clicked.connect(self.disp_bad)

    def disp_all(self, init=True):
        self.current_sel = "all"
        if init:
            self.current_range = (0, 28)
        first_val, last_val = self.current_range
        last_val = self.n_units if last_val > self.n_units else last_val
        self.fill_img(self.units[first_val:last_val])

    def disp_good(self, init=True):
        self.current_sel = "good"
        if init:
            self.current_range = (0, 28)
        first_val, last_val = self.current_range
        last_val = self.n_gunits if last_val > self.n_gunits else last_val
        first_val, last_val = (0, 28) if first_val > last_val else (first_val, last_val)
        self.fill_img(self.good_units[first_val:last_val])

    def disp_bad(self, init=True):
        self.current_sel = "bad"
        if init:
            self.current_range = (0, 28)
        first_val, last_val = self.current_range
        last_val = self.n_bunits if last_val > self.n_bunits else last_val
        first_val, last_val = (0, 28) if first_val > last_val else (first_val, last_val)
        self.fill_img(self.bad_units[first_val:last_val])

    def get_prev(self):
        if self.current_range != (0, 28):
            first_val, last_val = self.current_range
            self.current_range = (first_val - 28, first_val)
            if self.current_sel == "good":
                self.disp_good(init=False)
            elif self.current_sel == "bad":
                self.disp_bad(init=False)
            else:
                self.disp_all(init=False)

    def get_next(self):
        if self.current_sel == "all":
            if self.current_range[1] <= self.n_units:
                first_val, last_val = self.current_range
                self.current_range = (last_val, last_val + 28)
                self.disp_all(init=False)
        elif self.current_sel == "good":
            if self.current_range[1] <= self.n_gunits:
                first_val, last_val = self.current_range
                self.current_range = (last_val, last_val + 28)
                self.disp_good(init=False)
        elif self.current_sel == "bad":
            if self.current_range[1] <= self.n_bunits:
                first_val, last_val = self.current_range
                self.current_range = (last_val, last_val + 28)
                self.disp_bad(init=False)

    def logout(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def init_gallery(self):
        self.setObjectName("Dialog")
        self.resize(1200, 700)
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1200, 700))
        self.widget.setMinimumSize(QtCore.QSize(1200, 700))
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "    background-color: rgb(164, 0, 0);\n"
                                  "background-color: qlineargradient(spread:pad, x1:0.487562, y1:0, x2:0.493, y2:1, stop:0 rgba(67, 204, 160, 255), stop:1 rgba(255, 255, 255, 255))}")
        self.widget.setObjectName("widget")

        self.sel_all = QtWidgets.QPushButton(self.widget)
        self.sel_all.setGeometry(QtCore.QRect(40, 10, 61, 31))
        self.sel_all.setStyleSheet("QPushButton#sel_all {\n"
                                   "    background-color: rgb(238, 238, 236);\n"
                                   "    border-style: outset;\n"
                                   "    border-width: 1px;\n"
                                   "    border-color: beige;\n"
                                   "    font: 63 italic 13pt \"URW Bookman\";\n"
                                   "    padding: 6px;\n"
                                   "}\n"
                                   "QPushButton#sel_all:pressed {\n"
                                   "    background-color: rgb(200, 200, 200);\n"
                                   "    border-style: inset;\n"
                                   "}")
        self.sel_all.setObjectName("sel_all")
        self.sel_all.setText("All")

        self.sel_good = QtWidgets.QPushButton(self.widget)
        self.sel_good.setGeometry(QtCore.QRect(110, 10, 61, 31))
        self.sel_good.setStyleSheet("QPushButton#sel_good {\n"
                                    "    background-color: rgb(238, 238, 236);\n"
                                    "    border-style: outset;\n"
                                    "    border-width: 1px;\n"
                                    "    border-color: beige;\n"
                                    "    font: 63 italic 13pt \"URW Bookman\";\n"
                                    "    padding: 6px;\n"
                                    "}\n"
                                    "QPushButton#sel_good:pressed {\n"
                                    "    background-color: rgb(200, 200, 200);\n"
                                    "    border-style: inset;\n"
                                    "}")
        self.sel_good.setObjectName("sel_good")
        self.sel_good.setText("Good")

        self.sel_bad = QtWidgets.QPushButton(self.widget)
        self.sel_bad.setGeometry(QtCore.QRect(180, 10, 61, 31))
        self.sel_bad.setStyleSheet("QPushButton#sel_bad {\n"
                                   "    background-color: rgb(238, 238, 236);\n"
                                   "    border-style: outset;\n"
                                   "    border-width: 1px;\n"
                                   "    border-color: beige;\n"
                                   "    font: 63 italic 13pt \"URW Bookman\";\n"
                                   "    padding: 6px;\n"
                                   "}\n"
                                   "QPushButton#sel_bad:pressed {\n"
                                   "    background-color: rgb(200, 200, 200);\n"
                                   "    border-style: inset;\n"
                                   "}")
        self.sel_bad.setObjectName("sel_bad")
        self.sel_bad.setText("Bad")

        self.left_button = QtWidgets.QToolButton(self.widget)
        self.left_button.setArrowType(QtCore.Qt.LeftArrow)
        self.left_button.setGeometry(QtCore.QRect(540, 10, 51, 31))
        self.left_button.setObjectName("left_button")

        self.right_button = QtWidgets.QToolButton(self.widget)
        self.right_button.setArrowType(QtCore.Qt.RightArrow)
        self.right_button.setGeometry(QtCore.QRect(600, 10, 51, 31))
        self.right_button.setObjectName("right_button")

        self.logout_button = QtWidgets.QPushButton(self.widget)
        self.logout_button.setGeometry(QtCore.QRect(1090, 10, 89, 41))
        self.logout_button.setStyleSheet("border-color: rgb(238, 238, 236);\n"
                                         "font: 13pt \"Ubuntu\";\n"
                                         "color: rgb(43, 44, 229);\n"
                                         "border-radius:20px;\n"
                                         "")
        self.logout_button.setObjectName("logout_button")
        self.logout_button.setText("log out")

        self.widget1 = QtWidgets.QWidget(self.widget)
        self.widget1.setGeometry(QtCore.QRect(10, 40, 1190, 650))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(20, 20, 30, 20)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        self.label20 = QtWidgets.QLabel(self.widget1)
        # self.label22.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label20.setText("")
        self.label20.setAlignment(QtCore.Qt.AlignCenter)
        self.label20.setObjectName("label20")
        self.gridLayout.addWidget(self.label20, 2, 5, 1, 1)

        self.label22 = QtWidgets.QLabel(self.widget1)
        # self.label22.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label22.setText("")
        self.label22.setAlignment(QtCore.Qt.AlignCenter)
        self.label22.setObjectName("label22")
        self.gridLayout.addWidget(self.label22, 3, 0, 1, 1)

        self.label9 = QtWidgets.QLabel(self.widget1)
        # self.label9.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label9.setText("")
        self.label9.setAlignment(QtCore.Qt.AlignCenter)
        self.label9.setObjectName("label9")
        self.gridLayout.addWidget(self.label9, 1, 1, 1, 1)

        self.label12 = QtWidgets.QLabel(self.widget1)
        # self.label12.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label12.setText("")
        self.label12.setAlignment(QtCore.Qt.AlignCenter)
        self.label12.setObjectName("label12")
        self.gridLayout.addWidget(self.label12, 1, 4, 1, 1)

        self.label4 = QtWidgets.QLabel(self.widget1)
        # self.label4.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label4.setText("")
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setObjectName("label4")
        self.gridLayout.addWidget(self.label4, 0, 3, 1, 1)

        self.label17 = QtWidgets.QLabel(self.widget1)
        # self.label17.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label17.setText("")
        self.label17.setAlignment(QtCore.Qt.AlignCenter)
        self.label17.setObjectName("label17")
        self.gridLayout.addWidget(self.label17, 2, 2, 1, 1)

        self.label8 = QtWidgets.QLabel(self.widget1)
        # self.label8.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label8.setText("")
        self.label8.setAlignment(QtCore.Qt.AlignCenter)
        self.label8.setObjectName("label8")
        self.gridLayout.addWidget(self.label8, 1, 0, 1, 1)

        self.label11 = QtWidgets.QLabel(self.widget1)
        # self.label11.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label11.setText("")
        self.label11.setAlignment(QtCore.Qt.AlignCenter)
        self.label11.setObjectName("label11")
        self.gridLayout.addWidget(self.label11, 1, 3, 1, 1)

        self.label26 = QtWidgets.QLabel(self.widget1)
        # self.label26.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label26.setText("")
        self.label26.setAlignment(QtCore.Qt.AlignCenter)
        self.label26.setObjectName("label26")
        self.gridLayout.addWidget(self.label26, 3, 4, 1, 1)

        self.label21 = QtWidgets.QLabel(self.widget1)
        # self.label21.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label21.setText("")
        self.label21.setAlignment(QtCore.Qt.AlignCenter)
        self.label21.setObjectName("label21")
        self.gridLayout.addWidget(self.label21, 2, 6, 1, 1)

        self.label28 = QtWidgets.QLabel(self.widget1)
        # self.label28.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label28.setText("")
        self.label28.setAlignment(QtCore.Qt.AlignCenter)
        self.label28.setObjectName("label28")
        self.gridLayout.addWidget(self.label28, 3, 6, 1, 1)

        self.label13 = QtWidgets.QLabel(self.widget1)
        # self.label13.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label13.setText("")
        self.label13.setAlignment(QtCore.Qt.AlignCenter)
        self.label13.setObjectName("label13")
        self.gridLayout.addWidget(self.label13, 1, 5, 1, 1)

        self.label19 = QtWidgets.QLabel(self.widget1)
        # self.label19.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label19.setText("")
        self.label19.setAlignment(QtCore.Qt.AlignCenter)
        self.label19.setObjectName("label19")
        self.gridLayout.addWidget(self.label19, 2, 4, 1, 1)

        self.label23 = QtWidgets.QLabel(self.widget1)
        # self.label23.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label23.setText("")
        self.label23.setAlignment(QtCore.Qt.AlignCenter)
        self.label23.setObjectName("label23")
        self.gridLayout.addWidget(self.label23, 3, 1, 1, 1)

        self.label7 = QtWidgets.QLabel(self.widget1)
        # self.label7.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label7.setText("")
        self.label7.setAlignment(QtCore.Qt.AlignCenter)
        self.label7.setObjectName("label7")
        self.gridLayout.addWidget(self.label7, 0, 6, 1, 1)

        self.label5 = QtWidgets.QLabel(self.widget1)
        # self.label5.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label5.setText("")
        self.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.label5.setObjectName("label5")
        self.gridLayout.addWidget(self.label5, 0, 4, 1, 1)

        self.label10 = QtWidgets.QLabel(self.widget1)
        # self.label10.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label10.setText("")
        self.label10.setAlignment(QtCore.Qt.AlignCenter)
        self.label10.setObjectName("label10")
        self.gridLayout.addWidget(self.label10, 1, 2, 1, 1)

        self.label2 = QtWidgets.QLabel(self.widget1)
        # self.label2.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label2.setText("")
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setObjectName("label2")
        self.gridLayout.addWidget(self.label2, 0, 1, 1, 1)

        self.label3 = QtWidgets.QLabel(self.widget1)
        # self.label3.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label3.setText("")
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setObjectName("label3")
        self.gridLayout.addWidget(self.label3, 0, 2, 1, 1)

        self.label25 = QtWidgets.QLabel(self.widget1)
        # self.label25.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label25.setText("")
        self.label25.setAlignment(QtCore.Qt.AlignCenter)
        self.label25.setObjectName("label25")
        self.gridLayout.addWidget(self.label25, 3, 3, 1, 1)

        self.label16 = QtWidgets.QLabel(self.widget1)
        # self.label16.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label16.setText("")
        self.label16.setAlignment(QtCore.Qt.AlignCenter)
        self.label16.setObjectName("label16")
        self.gridLayout.addWidget(self.label16, 2, 1, 1, 1)

        self.label18 = QtWidgets.QLabel(self.widget1)
        # self.label18.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label18.setText("")
        self.label18.setAlignment(QtCore.Qt.AlignCenter)
        self.label18.setObjectName("label18")
        self.gridLayout.addWidget(self.label18, 2, 3, 1, 1)
        self.label15 = QtWidgets.QLabel(self.widget1)
        # self.label15.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label15.setText("")
        self.label15.setAlignment(QtCore.Qt.AlignCenter)
        self.label15.setObjectName("label15")
        self.gridLayout.addWidget(self.label15, 2, 0, 1, 1)

        self.label6 = QtWidgets.QLabel(self.widget1)
        # self.label6.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label6.setText("")
        self.label6.setAlignment(QtCore.Qt.AlignCenter)
        self.label6.setObjectName("label6")
        self.gridLayout.addWidget(self.label6, 0, 5, 1, 1)

        self.label24 = QtWidgets.QLabel(self.widget1)
        # self.label24.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label24.setText("")
        self.label24.setAlignment(QtCore.Qt.AlignCenter)
        self.label24.setObjectName("label24")
        self.gridLayout.addWidget(self.label24, 3, 2, 1, 1)

        self.label1 = QtWidgets.QLabel(self.widget1)
        # self.label1.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label1.setText("")
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)

        self.label14 = QtWidgets.QLabel(self.widget1)
        # self.label14.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label14.setText("")
        self.label14.setAlignment(QtCore.Qt.AlignCenter)
        self.label14.setObjectName("label14")
        self.gridLayout.addWidget(self.label14, 1, 6, 1, 1)

        self.label27 = QtWidgets.QLabel(self.widget1)
        # self.label27.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.label27.setText("")
        self.label27.setAlignment(QtCore.Qt.AlignCenter)
        self.label27.setObjectName("label27")
        self.gridLayout.addWidget(self.label27, 3, 5, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sel_all.setText(_translate("Dialog", "All"))
        self.sel_good.setText(_translate("Dialog", "Good"))
        self.sel_bad.setText(_translate("Dialog", "Bad"))
        self.left_button.setText(_translate("Dialog", "prev"))
        self.right_button.setText(_translate("Dialog", "next"))
        self.logout_button.setText(_translate("Dialog", "log out"))

    def fill_img(self, units, size=QtCore.QSize(140, 130)):  # 140, 110
        label_list = [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6, self.label7,
                      self.label8, self.label9, self.label10, self.label11, self.label12, self.label13, self.label14,
                      self.label15, self.label16, self.label17, self.label18, self.label19, self.label20, self.label21,
                      self.label22, self.label23, self.label24, self.label25, self.label26, self.label27, self.label28]
        for i in range(len(units)):
            img_path = f"{thumbnail_path}/{units[i][0]}.png"
            if os.path.isfile(img_path):
                status = units[i][1]
                pixmap = QPixmap(img_path)
                pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
                label_list[i].setPixmap(pixmap)
                if status == "Bad":
                    label_list[i].setStyleSheet("background-color: rgb(239, 41, 41);")
                else:
                    label_list[i].setStyleSheet("")
            else:
                label_list[i].setStyleSheet("")
                label_list[i].clear()
        if len(units) < 28:
            for i in range(len(units), 28):
                label_list[i].setStyleSheet("")
                label_list[i].clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(700)
    widget.setFixedWidth(1200)
    widget.show()
    try:
        os.system("python3 outlier_detector.py")
        sys.exit(app.exec())
    except:
        print("Exiting")
