# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eip.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from support import movies_from_category, trivial
import traceback
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(584, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Label for Wanted Comment Number
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(320, 20, 111, 16))
        self.label.setObjectName("label")

        # Text field for Wanted Comment Number
        self.WantedCommentNumber = QtWidgets.QLineEdit(self.centralwidget)
        self.WantedCommentNumber.setGeometry(QtCore.QRect(320, 50, 160, 22))
        self.WantedCommentNumber.setObjectName("WantedCommentNumber")

        # Label for Wanted Interest Percent
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 90, 111, 16))
        self.label_2.setObjectName("label_2")

        # Text field for Wanted Interest Percent
        self.WantedInterestPercent = QtWidgets.QLineEdit(self.centralwidget)
        self.WantedInterestPercent.setGeometry(QtCore.QRect(320, 130, 160, 22))
        self.WantedInterestPercent.setObjectName("WantedInterestPercent")

        # Label for Interest 1 Value
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(320, 170, 171, 16))
        self.label_3.setObjectName("label_3")

        # Text field for Interest 1 Value
        self.interest_1_v = QtWidgets.QLineEdit(self.centralwidget)
        self.interest_1_v.setGeometry(QtCore.QRect(320, 200, 160, 22))
        self.interest_1_v.setObjectName("interest_1_v")

        # Text field for Wanted Movie Number
        self.WantedMovieNumber = QtWidgets.QLineEdit(self.centralwidget)
        self.WantedMovieNumber.setGeometry(QtCore.QRect(130, 70, 160, 22))
        self.WantedMovieNumber.setObjectName("WantedMovieNumber")

        # Text field for Wanted Stars
        self.WantedStars = QtWidgets.QLineEdit(self.centralwidget)
        self.WantedStars.setGeometry(QtCore.QRect(130, 130, 160, 22))
        self.WantedStars.setObjectName("WantedStars")

        self.Categories = QtWidgets.QTextEdit(self.centralwidget)
        self.Categories.setGeometry(QtCore.QRect(10, 40, 111, 251))
        self.Categories.setObjectName("Categories")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 271, 30))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 50, 161, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(130, 100, 201, 16))
        self.label_6.setObjectName("label_6")

        # Start Button
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(200, 290, 161, 81))
        self.StartButton.setObjectName("StartButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 584, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.StartButton.clicked.connect(self.run_trivial)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EIP"))
        self.label.setText(_translate("MainWindow", "Yorum Sayısı:"))
        self.label_2.setText(_translate("MainWindow", "İstediğiniz Oran:"))
        self.label_3.setText(_translate("MainWindow", "Toplam Yorum Sayısı:"))
        self.label_4.setText(_translate("MainWindow", "Kategoriler(alt alta yazınız):"))
        self.label_5.setText(_translate("MainWindow", "İstenilen Film Sayısı:"))
        self.label_6.setText(_translate("MainWindow", "Film yıldız Sayısı"))
        self.StartButton.setText(_translate("MainWindow", "Başlat"))

    def run_trivial(self):
        import datetime,random
        try:
            # Get the category string from the textEdit
            categories = self.Categories.toPlainText().split('\n')
            complete_result = []

            # Loop over the categories and run the function with the given parameters
            for category in categories:
                wanted_movie_number = int(self.WantedMovieNumber.text())
                wanted_stars = float(self.WantedStars.text())
                movie_list = movies_from_category(category, wanted_movie_number, wanted_stars)  # default parameters for number of movies and wanted stars

                wanted_comment_number = int(self.WantedCommentNumber.text())
                interest_percent = float(self.WantedInterestPercent.text())
                interest_1_v = float(self.interest_1_v.text())

                result = trivial(movie_list, wanted_comment_number, interest_percent, interest_1_v)
                complete_result.extend(result)

            # Generate the HTML table for the results
            table_html = "<html><head><style>table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 8px;} th {background-color: #f2f2f2;}</style></head><body>"
            table_html += "<h2>Results</h2>"
            table_html += "<table>"
            table_html += "<tr><th>Category</th><th>Movie</th><th>Comment</th><th>Interest Percentage</th></tr>"

        
            for item in complete_result:
                name = item.split("|||")[0]
                comment = item.split("|||")[1]
                interest_percent = item.split("|||")[2]
                category = item.split("|||")[3]
                table_html += f"<tr><td>{category}</td><td>{name}</td><td>{comment}</td><td>{interest_percent}</td></tr>\n"
            table_html += "</table></body></html>"

            file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".html"
            with open(f"results{random.randint(0,99999)}.html", "w") as file:
                file.write(table_html)

        except Exception:
            pass
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
