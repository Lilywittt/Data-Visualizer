import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import dask.dataframe as dd
import plotly.graph_objects as go
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plotly Charts')
        self.setGeometry(5, 30, 1355, 730)

        df = dd.read_csv('data_7_5.csv', dtype={'Ai0': 'float64', 'Ai1': 'float64', 'Ai2': 'float64', 'Ai3': 'float64'})

        x_data = df['timestamp']
        y_data0 = df['Ai0']
        y_data1 = df['Ai1']
        y_data2 = df['Ai2']
        y_data3 = df['Ai3']

        x_data = x_data.compute()
        y_data0 = y_data0.compute()
        y_data1 = y_data1.compute()
        y_data2 = y_data2.compute()
        y_data3 = y_data3.compute()

        power_data = 2250 * y_data3 * (y_data0 + y_data1 + y_data2)

        y_data0 = y_data0 * 25
        y_data1 = y_data1 * 25
        y_data2 = y_data2 * 25
        y_data3 = y_data3 * 90

        fig0 = go.Figure(data=go.Scatter(x=x_data, y=y_data0, mode='lines'), layout_title_text='Ai0')
        fig1 = go.Figure(data=go.Scatter(x=x_data, y=y_data1, mode='lines'), layout_title_text='Ai1')
        fig2 = go.Figure(data=go.Scatter(x=x_data, y=y_data2, mode='lines'), layout_title_text='Ai2')
        fig3 = go.Figure(data=go.Scatter(x=x_data, y=y_data3, mode='lines'), layout_title_text='Ai3')

        fig_power = go.Figure(data=go.Scatter(x=x_data, y=power_data, mode='lines'), layout_title_text='Power')

        # Specify the output folder in the project directory
        output_folder = "output"

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        fig0_file = os.path.join(output_folder, 'fig0.html')
        fig1_file = os.path.join(output_folder, 'fig1.html')
        fig2_file = os.path.join(output_folder, 'fig2.html')
        fig3_file = os.path.join(output_folder, 'fig3.html')
        fig_power_file = os.path.join(output_folder, 'fig_power.html')

        # Save figures as HTML files
        fig0.write_html(fig0_file)
        fig1.write_html(fig1_file)
        fig2.write_html(fig2_file)
        fig3.write_html(fig3_file)
        fig_power.write_html(fig_power_file)

        # Create QWebEngineView widgets
        self.browser0 = QWebEngineView()
        self.browser1 = QWebEngineView()
        self.browser2 = QWebEngineView()
        self.browser3 = QWebEngineView()

        # Load the HTML files from the output folder
        self.browser0.load(QUrl.fromLocalFile(os.path.abspath(fig0_file)))
        self.browser1.load(QUrl.fromLocalFile(os.path.abspath(fig1_file)))
        self.browser2.load(QUrl.fromLocalFile(os.path.abspath(fig2_file)))
        self.browser3.load(QUrl.fromLocalFile(os.path.abspath(fig3_file)))

        # Create layout and add the web engine views
        layout = QGridLayout()
        layout.addWidget(self.browser0, 0, 0)
        layout.addWidget(self.browser1, 0, 1)
        layout.addWidget(self.browser2, 1, 0)
        layout.addWidget(self.browser3, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()