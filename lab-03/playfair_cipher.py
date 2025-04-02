import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow  
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  
        self.ui.setupUi(self)  

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)  
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)  

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        
        plain_text = self.ui.txt_plain_text.toPlainText().strip()
        key = self.ui.txt_key.toPlainText().strip()

        if not plain_text:
            QMessageBox.warning(self, "Error", "Plain text cannot be empty!")
            return
        if not key:
            QMessageBox.warning(self, "Error", "Key cannot be empty!")
            return

        payload = {"plain_text": plain_text, "key": key}

        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                encrypted_message = data.get("encrypted_message", "")

                if encrypted_message:
                    self.ui.txt_cipher_text.setPlainText(encrypted_message)
                    QMessageBox.information(self, "Success", "Encrypted Successfully")
                else:
                    QMessageBox.critical(self, "Error", "Invalid response from API!")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request error: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        
        cipher_text = self.ui.txt_cipher_text.toPlainText().strip()
        key = self.ui.txt_key.toPlainText().strip()

        if not cipher_text:
            QMessageBox.warning(self, "Error", "Cipher text cannot be empty!")
            return
        if not key:
            QMessageBox.warning(self, "Error", "Key cannot be empty!")
            return

        payload = {"cipher_text": cipher_text, "key": key}

        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                decrypted_message = data.get("decrypted_message", "")

                if decrypted_message:
                    self.ui.txt_plain_text.setPlainText(decrypted_message)
                    QMessageBox.information(self, "Success", "Decrypted Successfully")
                else:
                    QMessageBox.critical(self, "Error", "Invalid response from API!")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
