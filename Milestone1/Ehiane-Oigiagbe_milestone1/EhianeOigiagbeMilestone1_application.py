import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
import psycopg2

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Business Browser'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()

        self.state_label = QLabel('Select a State:', self)
        self.layout.addWidget(self.state_label)

        self.state_combo = QComboBox(self)
        self.layout.addWidget(self.state_combo)
        self.state_combo.currentIndexChanged.connect(self.on_state_changed)

        self.city_label = QLabel('Select a City:', self)
        self.layout.addWidget(self.city_label)

        self.city_combo = QComboBox(self)
        self.layout.addWidget(self.city_combo)
        self.city_combo.currentIndexChanged.connect(self.on_city_changed)

        self.business_label = QLabel('Businesses:', self)
        self.layout.addWidget(self.business_label)

        self.business_list = QLabel('', self)
        self.layout.addWidget(self.business_list)

        self.setLayout(self.layout)
        self.load_states()

    def load_states(self):
        conn = psycopg2.connect(
            dbname="milestone1db",
            user="postgres",
            password="12345",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT state_ FROM Business ORDER BY state_;")
        states = cur.fetchall()
        self.state_combo.addItem("")
        for state in states:
            self.state_combo.addItem(state[0])
        cur.close()
        conn.close()

    def on_state_changed(self):
        state = self.state_combo.currentText()
        if state:
            conn = psycopg2.connect(
                dbname="milestone1db",
                user="postgres",
                password="12345",
                host="127.0.0.1",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT city FROM Business WHERE state_=%s ORDER BY city;", (state,))
            cities = cur.fetchall()
            self.city_combo.clear()
            self.city_combo.addItem("")
            for city in cities:
                self.city_combo.addItem(city[0])
            cur.close()
            conn.close()
        else:
            self.city_combo.clear()
            self.business_list.setText('')

    def on_city_changed(self):
        state = self.state_combo.currentText()
        city = self.city_combo.currentText()
        if city:
            conn = psycopg2.connect(
                dbname="milestone1db",
                user="postgres",
                password="12345",
                host="127.0.0.1",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT name_ FROM Business WHERE city=%s AND state_=%s ORDER BY name_;", (city, state))
            businesses = cur.fetchall()
            business_names = '\n'.join([b[0] for b in businesses])
            self.business_list.setText(business_names)
            cur.close()
            conn.close()
        else:
            self.business_list.setText('')

def main():    
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

main();
