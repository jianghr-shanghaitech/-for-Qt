# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Code/UI/ui/product.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
import os
sys.path.append('..')
from Code.Class.seller_buyer_product import Product, User
from Code.SQL import sql
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from Chat import Chat_Temp
from Class import trade

current_path = os.path.dirname(os.path.realpath(__file__))

class ProductUIForm(object):

    def setupUi(self, Form, product_id):
        self.bought = False
        self.is_liked = False
        self.product = Product()
        self.product_info = self.product.find_product(product_id)
        self.product_id = product_id
        Form.setObjectName("Form")
        Form.resize(715, 571)
        self.name_label = QtWidgets.QLineEdit(Form)
        self.name_label.setGeometry(QtCore.QRect(60, 350, 311, 20))
        self.name_label.setObjectName("name_label")
        self.renminbi_label = QLabel(Form)
        self.renminbi_label.setGeometry(QtCore.QRect(395, 350, 40, 20))
        self.price_label = QtWidgets.QLineEdit(Form)
        self.price_label.setGeometry(QtCore.QRect(410, 350, 60, 20))
        self.price_label.setObjectName("price_label")
        self.tag_label = QtWidgets.QComboBox(Form)
        self.tag_label.setGeometry(QtCore.QRect(530, 30, 80, 25))
        self.tag_label.setObjectName("tag_label")
        self.sub_botton = QPushButton(Form)
        self.sub_botton.setGeometry(QtCore.QRect(530, 65, 20, 23))
        self.sub_botton.setText("-")
        self.add_botton = QPushButton(Form)
        self.add_botton.setGeometry(QtCore.QRect(590, 65, 20, 23))
        self.add_botton.setText("+")
        self.amount_edit = QLineEdit(Form)
        self.amount_edit.setGeometry(QtCore.QRect(550, 65, 40, 23))
        self.amount_edit.setText(self.product_info['amount'])
        self.add_botton.clicked.connect(lambda: self.amount_edit.setText(str(eval(self.amount_edit.text()) + 1)))
        self.sub_botton.clicked.connect(self.sub)
        self.describe_label = QtWidgets.QLineEdit(Form)
        self.describe_label.setGeometry(QtCore.QRect(60, 400, 411, 131))
        self.describe_label.setObjectName("describe_label")
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(520, 150, 113, 32))
        self.save_button.setObjectName("save_button")
        self.save_button.setText("save")
        self.ban_button = QtWidgets.QPushButton(Form)
        self.ban_button.setGeometry(QtCore.QRect(520, 110, 113, 32))
        self.ban_button.setObjectName("ban_button")
        self.retranslateUi(Form)
        if sys.platform == 'win32' or sys.platform == 'win64':
            png = QtGui.QPixmap(current_path + '\\..\\pictures\\' + self.product.get_picture(product_id))
        else:
            png = QtGui.QPixmap(current_path + '/../pictures/' + self.product.get_picture(product_id))
        self.pic_label = QtWidgets.QLabel(Form)
        self.pic_label.setGeometry(QtCore.QRect(60, 30, 411, 291))
        self.pic_label.setPixmap(png)
        self.pic_label.setScaledContents(True)
        self.ban_pic_widget = QtWidgets.QWidget(Form)
        self.ban_pic_widget.setGeometry(QtCore.QRect(60, 30, 411, 291))
        self.ban_pic_widget.setObjectName("ban_pic_widget")
        ban_png = QtGui.QPixmap(os.path.join(current_path, 'banned.png'))
        self.ban_pic_label = QtWidgets.QLabel(self.ban_pic_widget)
        self.ban_pic_label.setPixmap(ban_png)
        self.ban_pic_label.setScaledContents(True)
        self.ban_pic_label.setGeometry(QtCore.QRect(0, 0, 411, 291))
        self.ban_pic_widget.hide()
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.ban_button.clicked.connect(self.Ban)
        self.save_button.clicked.connect(self.save)
        if not self.product_info['if_banned'] == 'FALSE':
            self.ban_button.hide()
            self.ban_pic_widget.show()

    def sub(self):
        if eval(self.amount_edit.text()) > 0:
            self.amount_edit.setText(str(eval(self.amount_edit.text()) - 1))

    def retranslateUi(self, Form):

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.renminbi_label.setText("￥")
        self.name_label.setText(_translate("Form", self.product_info['product_name']))
        self.price_label.setText(_translate("Form", self.product_info['price']))
        self.describe_label.setText(_translate("Form", self.product_info['description']))
        if self.product_info['if_banned'] == 'FALSE':
            self.ban_button.setText(_translate("Form", "Ban"))
        self.tag_label.addItems(self.product.get_all_tags())
        self.tag_label.setCurrentIndex(self.product.get_all_tags().index(self.product_info['tag']))

    def Ban(self):
        self.ban_button.hide()
        self.ban_pic_widget.show()
        self.product.ban_product(self.product_id)

    def save(self):
        product_name = self.name_label.text()
        price = self.price_label.text()
        tag = self.tag_label.currentText()
        description = self.describe_label.text()
        amount = self.amount_edit.text()
        if amount.isdigit() == False:
            res = QMessageBox.warning(self, "Warning",
                                      "Your input seems invalid, please retry.",
                                      QMessageBox.Ok)
            return
        if eval(amount) < 0:
            QMessageBox.warning(self, "Warning", "Amount of product can not be negative", QMessageBox.Ok)
            self.amount_edit.setText('0')
            return
        modify_dict = {}
        if not product_name == self.product_info['product_name']:
            modify_dict['product_name'] = product_name
        if price.isdigit() == False:
            res = QMessageBox.warning(self, "Warning",
                                      "Your input seems invalid, please retry.",
                                      QMessageBox.Ok)
            return
        if not price == self.product_info['price'] and int(price) > 0:
            modify_dict['price'] = price
        if not price == self.product_info['price'] and int(price) <= 0:
            inform = QMessageBox.warning(self, "Warning",
                                         "Product price can not be less than 0",
                                         QMessageBox.Ok)
            return
        if not tag == self.product_info['tag']:
            modify_dict['tag'] = tag
        if not description == self.product_info['description']:
            modify_dict['description'] = description
        if not amount == self.product_info['amount']:
            modify_dict['amount'] = amount
        if len(modify_dict.keys()) > 0:
            self.product.modify_product(self.product_id, modify_dict)
            self.product_info = self.product.find_product(self.product_id)


class ProductUIMain(QtWidgets.QWidget, ProductUIForm):
    def __init__(self, product_id):
        self.username = ""
        self.password = ""
        self.email = ""
        super(ProductUIMain, self).__init__()
        self.setupUi(self, product_id)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_main = ProductUIMain()
    ui_main.show()
    sys.exit(app.exec_())

