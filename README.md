# 🖥️ SJF Scheduling Simulator (Non-Preemptive)

A desktop application that simulates the **Shortest Job First (SJF) Non-Preemptive CPU Scheduling Algorithm**.  
Built using Python and PyQt5, this project helps visualize how operating systems schedule processes based on burst time.

---

## 📌 Features

- Input number of processes dynamically
- Enter arrival time and burst time for each process
- Implements **Non-Preemptive SJF Scheduling**
- Calculates:
  - Waiting Time
  - Turnaround Time
  - Response Time
- Computes average times for all processes
- Generates a **Gantt Chart visualization**
- Input validation for better user experience

---

## ⚙️ How It Works

The algorithm selects the process with the **smallest burst time** among the available processes and executes it completely before moving to the next one.

---

## 🧮 Formulas Used

- **Turnaround Time** = Completion Time − Arrival Time  
- **Waiting Time** = Turnaround Time − Burst Time  
- **Response Time** = Start Time − Arrival Time  

---

## 🛠️ Technologies Used

- Python 🐍  
- PyQt5 (GUI Framework)

---

##👨‍💻 Team Members

Developed as part of an academic project for Operating Systems coursework.

-Hanya Amr
-Farah Samy 
-Mirley Maged

---
## 🚀 How to Run

1. Install dependencies:
```bash
pip install pyqt5
