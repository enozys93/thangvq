import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget
from PyQt5.uic import loadUi
import sqlite3
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class WelcomeScreen(QDialog):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver  = webdriver.Chrome(options=options)
    url = 'https://fms.vnpt.vn/'
    driver.get(url)
    
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("loginscreen.ui",self)
        
        self.btn_Login.clicked.connect(self.otpsr)
        self.txt_Password.returnPressed.connect(self.otpsr)
        self.setStyleSheet("QLabel#lbl_ThongBao{background-color: rgba( 255, 255, 255, 0% )}")
        self.lbl_ThongBao.setText("")
    def otpsr(self):
        username = self.txt_Username.text()
        password = self.txt_Password.text()
        if (len(username) == 0 or len(password) == 0):
            self.setStyleSheet("QLabel#lbl_ThongBao{background-color:rgb(221, 75, 57)}")
            self.lbl_ThongBao.setText("Đăng nhập không thành công, kiểm tra tên đăng nhập/mật khẩu.Truy cập mail.vnpt.vn để kiểm tra tài khoản !")
        else:
            '''options = webdriver.ChromeOptions()
            options.headless = True
            driver  = webdriver.Chrome(options=options)
            driver.implicitly_wait(0.8)'''          
            
            # Key in username
            email_field = self.driver.find_element(By.ID,'username').clear()
            email_field = self.driver.find_element(By.ID,'username')
            email_field.send_keys(username)
        
            # Key in password
            password_filed =self.driver.find_element(By.NAME,'password').clear()
            password_filed =self.driver.find_element(By.NAME,'password')
            password_filed.send_keys(password)
            
            # Click login button 
            login_filed = self.driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[2]/div/form/section/button')
            login_filed.click()
            print('- Logging in progress...')
            time.sleep(4) 
        
        # Check username and password
        
        page_source = BeautifulSoup(self.driver.page_source)
        errors =  page_source.find_all('div', id='msg')
        print(errors)
        if errors == []:
            login = OtpScreen() 
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)              
        else:
            self.setStyleSheet("QLabel#lbl_ThongBao{background-color:rgb(221, 75, 57)}")
            self.lbl_ThongBao.setText("Đăng nhập không thành công, kiểm tra tên đăng nhập/mật khẩu.Truy cập mail.vnpt.vn để kiểm tra tài khoản !")
        
class OtpScreen(QDialog):
    def __init__(self):
        super(OtpScreen, self).__init__()
        loadUi("otpscreen.ui",self)
        self.btn_Login.clicked.connect(self.otp_clicked)
        self.txt_OTP.returnPressed.connect(self.otp_clicked)
        self.setStyleSheet("QLabel#lbl_ThongBao{background-color: rgba( 255, 255, 255, 0% )}")
        self.lbl_ThongBao.setText("")
        
        
    def otp_clicked(self):
            
            try:
                otp = self.txt_OTP.text()  
                print("OPT LA",otp)
                search_field = WelcomeScreen.driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[2]/div[1]/div/form/div[1]/div/input').clear()
                search_field = WelcomeScreen.driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[2]/div[1]/div/form/div[1]/div/input')
                search_field.send_keys(otp)
                search_field.send_keys(Keys.RETURN)
                page_source = BeautifulSoup(WelcomeScreen.driver.page_source)
                title_content =  page_source.find_all('meta', content='Hệ thống quản lý lỗi mạng - Fault management system')
                for content in title_content:
                    contents = content.get('content')
                print(contents)
                if contents == 'Hệ thống quản lý lỗi mạng - Fault management system':
                    print("Go to Main UI")
                    #main = MainUI() 
                    #widget.addWidget(main)
                    #widget.setCurrentIndex(widget.currentIndex() + 1)   
            except: 
                print("Sai mật khẩu")
                self.setStyleSheet("QLabel#lbl_ThongBao{background-color:rgb(221, 75, 57)}")
                self.lbl_ThongBao.setText("Mật khẩu OTP không chính xác!")
            
            
                
           
                
        
                
            
            
        
        
        
    
#main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(700)
widget.setFixedWidth(1300)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
