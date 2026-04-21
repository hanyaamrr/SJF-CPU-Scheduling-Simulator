import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget
                              , QLineEdit, QPushButton, QHBoxLayout
                            , QVBoxLayout,QMessageBox)
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SJF Non-Preemptive Simulator")
        self.setGeometry(500, 100, 1000, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.row = QHBoxLayout()

        self.p_label = QLabel("Enter number of processes: ", self)
        self.process_box = QLineEdit(self)
        self.submit = QPushButton("submit", self)

        self.enter = None

        self.pro = []  # array for processes widget, arrival and burst
        self.p_int = None   # number of processes int
        self.pid = None


        self.initUI()

    def initUI(self):   # method for UI

        self.p_label.setFixedSize(160,50)
        self.process_box.setFixedSize(170,30)
        self.submit.setFixedSize(70,30)

        self.process_box.setPlaceholderText("no of processes")
        self.process_box.setValidator(QIntValidator(1, 100))  # 100 = number of 3 digits

        self.submit.clicked.connect(self.create_in_fields)

        self.row.addWidget(self.p_label)
        self.row.addWidget(self.process_box)
        self.row.addWidget(self.submit)

        self.layout.addLayout(self.row)
        self.layout.setAlignment(Qt.AlignTop)

        self.setStyleSheet("""
            QWidget {
               background-color: #C5B5A6
            }
            QLabel {
                color: #794022;
                font-family:arial;
                font-weight:bold
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #794022;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px;
                
            }
            QPushButton:disabled {
                background-color:#a9745a;
            }
            QMessageBox{
            background-color:white;
            }
            
        """)

    def validate_input(self, field, flag=False):
        text = field.text()

        if not text.isdigit():
            field.setStyleSheet("border: 1px solid #8b0000;")
            return False
        if int(text) == 0 and not flag: # flag allows zero
            field.setStyleSheet("border: 1px solid #8b0000;")
            return False
        else:
            field.setStyleSheet("")
            return True


    def create_in_fields(self):    # method to create input fields for each process

        self.submit.setText("submitted")
        self.submit.setDisabled(True)

        if not self.validate_input(self.process_box):
            QMessageBox.warning(self, "Invalid Input", "Please enter a positive integer.")
            return

        p_text = self.process_box.text()

        self.p_int = int(p_text)

        for i in range(self.p_int):
            row2 = QHBoxLayout()

            self.pid = QLabel(f"P{i + 1}")

            arrival = QLineEdit(self)
            arrival.setPlaceholderText("Arrival")
            arrival.setValidator(QIntValidator(0, 100))

            arrival.setFixedSize(170,30)

            burst = QLineEdit(self)
            burst.setPlaceholderText("Burst")
            burst.setValidator(QIntValidator(1, 100))

            burst.setFixedSize(170, 30)

            row2.addWidget(self.pid)
            row2.addWidget(arrival)
            row2.addWidget(burst)

            row_widget = QWidget()
            row_widget.setLayout(row2)
            self.layout.addWidget(row_widget)
            self.pro.append((row_widget, arrival, burst, f"p{i+1}"))

        self.enter = QPushButton("Run Simulation", self)

        self.enter.setFixedSize(150,30)

        self.layout.addWidget(self.enter)
        self.enter.clicked.connect(self.run)




    def run(self):    # run the simulation

        for _, arrival_field, burst_field, name in self.pro:

            if not self.validate_input(arrival_field,True) :  # arrival can be 0
                QMessageBox.warning(self, "Invalid Input",
                                        f"All fields for {name} must be filled with valid integers.")
                return
            if not self.validate_input(burst_field):
                QMessageBox.warning(self, "Invalid Input", f"Burst time for {name} must be greater than 0.")
                return

        for i in reversed(range(self.layout.count())):
            if i > 0:
                widget = self.layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

        data, gantt = self.sjf_simulator()

        self.draw_gantt(gantt)

        sum_w = 0
        sum_t = 0
        sum_r = 0

        for f in data:
            pid = QLabel(f"{f['pid']}   Waiting Time= {f['waiting']}   ,Turn-around Time= {f['turnaround']}   "
                        f",Response Time= {f['response']}",self)

            label0 = QLabel("                           ", self)

            pid.setStyleSheet("font-size:11px; font-family:arial")
            self.layout.addWidget(label0)
            self.layout.addWidget(pid)

            sum_w += f['waiting']
            sum_t += f['turnaround']
            sum_r += f['response']

        n = len(data)
        avg_w = sum_w / n
        avg_t = sum_t / n
        avg_r = sum_r / n

        label0 = QLabel("                           ",self)
        label_w = QLabel(f"Average Waiting Time: {avg_w}", self)
        label_t = QLabel(f"Average Turn-around Time: {avg_t}", self)
        label_r = QLabel(f"Average Response Time: {avg_r}", self)


        self.layout.addWidget(label0)
        self.layout.addWidget(label_w)
        self.layout.addWidget(label_t)
        self.layout.addWidget(label_r)

    def sjf_simulator(self):  # cpu scheduling
        process_data = []
        for _, a, b, i in self.pro:
            arr = int(a.text())
            bur = int(b.text())

            process_data.append({
                'pid': i, 'arrival': arr, 'burst': bur,
                'start': 0, 'completion': 0, 'turnaround': 0,
                'waiting': 0, 'response': 0, 'done': False
            })
        time = 0
        completed = 0
        gantt_chart = []

        while completed < self.p_int:
            ready = [i for i in process_data if i['arrival'] <= time and not i['done']]
            if ready:
                shortest = ready[0]
                for s in ready:
                    if s['burst'] < shortest['burst']:
                        shortest = s

                shortest['start'] = time
                shortest['completion'] = shortest['start'] + shortest['burst']
                shortest['turnaround'] = shortest['completion'] - shortest['arrival']
                shortest['waiting'] = shortest['turnaround'] - shortest['burst']
                shortest['response'] = shortest['start'] - shortest['arrival']
                shortest['done'] = True

                gantt_chart.append({'pid': shortest['pid'],
                                   'start': shortest['start'],
                                   'completion': shortest['completion']
                                   })
                time = shortest['completion']
                completed += 1
            else:
                time += 1

        return process_data, gantt_chart


    def draw_gantt(self, gantt):
        gantt_widget = QWidget()
        gantt_widget.setMinimumHeight(90)
        gantt_widget.setMinimumWidth(600)

        def paint(event):
            painter = QPainter(gantt_widget)

            y = 30
            height = 30
            scale = 30
            painter.setFont(QFont("Arial"))

            for p in gantt:
                start = p['start']
                end = p['completion']
                duration = end - start
                x = start * scale
                width = duration * scale

                painter.setBrush(QColor("#D96D3A"))
                painter.setPen(QPen(Qt.black, 1))
                painter.drawRect(x, y, width, height)

                painter.setPen(Qt.white)
                painter.drawText(x, y, width, height, Qt.AlignCenter, p['pid'])

                painter.setPen(Qt.black)  # numbers
                painter.drawText(x, y + height + 15, str(start))

            if gantt:
                end_x = gantt[-1]['completion'] * scale
                painter.drawText(end_x, y + height + 15, str(gantt[-1]['completion']))

        gantt_widget.paintEvent = paint
        self.layout.addWidget(QLabel("Gantt Chart:"))
        self.layout.addWidget(gantt_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())