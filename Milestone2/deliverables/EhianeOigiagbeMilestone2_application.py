"""
Name: Ehiane Oigiagbe
WSU ID: 11732262
Project: Yelp data milestone 2
Date: 7/6/2024
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QComboBox
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

class YelpApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Yelp Data Analysis')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.state_label = QLabel('Select State:')
        self.layout.addWidget(self.state_label)

        self.state_combobox = QComboBox()
        self.layout.addWidget(self.state_combobox)

        self.city_label = QLabel('Select City:')
        self.layout.addWidget(self.city_label)

        self.city_combobox = QComboBox()
        self.layout.addWidget(self.city_combobox)

        self.result_text = QTextEdit()
        self.layout.addWidget(self.result_text)

        self.load_data_button = QPushButton('Load Data')
        self.load_data_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_button)

        self.visualize_button = QPushButton('Visualize Data')
        self.visualize_button.clicked.connect(self.visualize_data)
        self.layout.addWidget(self.visualize_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.db_params = {
            'host': '127.0.0.1',
            'database': 'milestone1db',
            'user': 'postgres',
            'password': '12345'
        }

        self.queries = {
            'Top 10 Businesses by Review Count': """
                SELECT name_, city, state, review_count
                FROM Business
                ORDER BY review_count DESC
                LIMIT 10;
            """,
            'Average Star Rating by City': """
                SELECT city, AVG(stars) as avg_rating
                FROM Business
                GROUP BY city
                ORDER BY avg_rating DESC;
            """,
            'Businesses with the Most Check-ins': """
                SELECT B.name_, B.city, B.state, SUM(C.checkins) as total_checkins
                FROM Business B
                JOIN Checkin C ON B.business_id = C.business_id
                GROUP BY B.name_, B.city, B.state
                ORDER BY total_checkins DESC
                LIMIT 10;
            """,
            'User with the Most Reviews': """
                SELECT user_id, name_, review_count
                FROM Users
                ORDER BY review_count DESC
                LIMIT 1;
            """,
            'Top 10 Most Active Users': """
                SELECT user_id, name_, review_count
                FROM Users
                ORDER BY review_count DESC
                LIMIT 10;
            """,
            'Average Review Rating by User': """
                SELECT U.user_id, U.name_, AVG(R.stars) as avg_rating
                FROM Users U
                JOIN Review R ON U.user_id = R.user_id
                GROUP BY U.user_id, U.name_
                ORDER BY avg_rating DESC
                LIMIT 10;
            """,
            'Reviews per Day': """
                SELECT date, COUNT(*) as reviews_count
                FROM Review
                GROUP BY date
                ORDER BY date;
            """,
            'Top 10 Most Reviewed Businesses': """
                SELECT B.name_, B.city, B.state, COUNT(R.review_id) as review_count
                FROM Business B
                JOIN Review R ON B.business_id = R.business_id
                GROUP BY B.name_, B.city, B.state
                ORDER BY review_count DESC
                LIMIT 10;
            """,
            'Average Rating by Business': """
                SELECT B.name_, B.city, B.state, AVG(R.stars) as avg_rating
                FROM Business B
                JOIN Review R ON B.business_id = R.business_id
                GROUP BY B.name_, B.city, B.state
                ORDER BY avg_rating DESC
                LIMIT 10;
            """
        }

        self.load_states()

    def load_states(self):
        query = "SELECT DISTINCT state FROM Business ORDER BY state;"
        states = self.execute_query(query)
        if states is not None:
            for state in states['state']:
                self.state_combobox.addItem(state)
            self.state_combobox.currentIndexChanged.connect(self.load_cities)

    def load_cities(self):
        state = self.state_combobox.currentText()
        query = f"SELECT DISTINCT city FROM Business WHERE state = '{state}' ORDER BY city;"
        cities = self.execute_query(query)
        self.city_combobox.clear()
        if cities is not None:
            for city in cities['city']:
                self.city_combobox.addItem(city)

    def load_data(self):
        state = self.state_combobox.currentText()
        city = self.city_combobox.currentText()
        query = f"SELECT name_, address, city, state, stars, review_count FROM Business WHERE state = '{state}' AND city = '{city}' ORDER BY name_;"
        data = self.execute_query(query)
        if data is not None:
            self.result_text.setText(data.to_string(index=False))

    def visualize_data(self):
        for title, query in self.queries.items():
            df = self.execute_query(query)
            if df is not None and not df.empty:
                self.result_text.append(f"\n{title}:\n{df}\n")
                if 'avg_rating' in df.columns and 'city' in df.columns:
                    plt.figure(figsize=(10, 6))
                    plt.barh(df['city'], df['avg_rating'], color='skyblue')
                    plt.xlabel('Average Rating')
                    plt.title(title)
                    plt.gca().invert_yaxis()
                    plt.show()
                elif 'review_count' in df.columns and 'name_' in df.columns:
                    plt.figure(figsize=(10, 6))
                    plt.barh(df['name_'], df['review_count'], color='skyblue')
                    plt.xlabel('Review Count')
                    plt.title(title)
                    plt.gca().invert_yaxis()
                    plt.show()
                elif 'total_checkins' in df.columns and 'name_' in df.columns:
                    plt.figure(figsize=(10, 6))
                    plt.barh(df['name_'], df['total_checkins'], color='skyblue')
                    plt.xlabel('Total Check-ins')
                    plt.title(title)
                    plt.gca().invert_yaxis()
                    plt.show()

    def execute_query(self, query):
        conn = None
        df = None
        try:
            conn = psycopg2.connect(**self.db_params)
            df = pd.read_sql_query(query, conn)
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
        finally:
            if conn is not None:
                conn.close()
        return df

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = YelpApp()
    mainWindow.show()
    sys.exit(app.exec_())
