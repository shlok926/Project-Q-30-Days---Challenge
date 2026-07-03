# Project Q: 30 Days Challenge - Zero to Quantum Hero ⚛️

A 30-day intensive journey into Quantum Computing and Qiskit. This repository contains my daily workbooks, learning notes, and practical implementations, including a **Quantum-Secured Password Generator** built as a mini-project.

## 📁 Repository Structure

The repository is organized day-by-day. Each folder contains the daily workbook/materials provided in the challenge, along with a `Solutions_and_Notes` folder for personal notes and solved exercises.

* **Day_01 to Day_10**: Core quantum concepts (Qubits, Superposition, Entanglement, Measurement) and Qiskit basics.
* **Mini_Project_1**: The Quantum Randomness Laboratory.

## 🛡️ Mini-Project: Quantum-Secured Password Generator

As part of the Day 1 to 10 milestone, I built a **Quantum-Secured Password Generator**. 

Unlike classical password generators that rely on pseudo-random mathematical algorithms, this project uses **Quantum Superposition** to generate numbers. By simulating a 6-qubit quantum circuit and measuring the collapsed states, the resulting password is intrinsically probabilistic and physically impossible to predict.

### How to Run the Mini-Project
1. Navigate to the Mini Project directory:
   ```bash
   cd "Mini_Project_1/Quantum-Randomness-Lab"
   ```
2. Install the required quantum libraries:
   ```bash
   pip install qiskit qiskit-aer matplotlib numpy scipy
   ```
3. Run the Quantum Password Generator:
   ```bash
   python quantum_password.py
   ```

## 🛠️ Technologies Used
* **Python 3**
* **Qiskit & Qiskit Aer** (IBM's Quantum Computing SDK)
* **Matplotlib & NumPy** (For data visualization and statistics)

---
*This repository is maintained as part of the Project-Q 30-Day Quantum Challenge.*
