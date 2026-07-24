# QST Test & Subsystem Coverage Matrix

This matrix documents the verification coverage of each subsystem in the Quantum Security Toolkit (QST) framework across unit tests, integration tests, end-to-end tests, and property-based validation.

| Subsystem Name | Package / Path | Unit Testing | Integration Testing | End-to-End Testing | Property Testing |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Domain Models** | `src/qst/models/` | ✅ | ✅ | ✅ | ✅ |
| **BB84 Protocol Engine** | `src/qst/core/bb84/` | ✅ | | ✅ | ✅ |
| **Eve Simulation** | `src/qst/core/bb84/eavesdropper.py` | ✅ | | ✅ | ✅ |
| **Basis Reconciliation** | `src/qst/core/bb84/reconciliation.py` | ✅ | | ✅ | ✅ |
| **Key Sifting** | `src/qst/core/bb84/sifting.py` | ✅ | | ✅ | ✅ |
| **QBER Calculation** | `src/qst/core/bb84/qber.py` | ✅ | | ✅ | ✅ |
| **Security Metrics** | `src/qst/core/bb84/metrics.py` | ✅ | ✅ | | ✅ |
| **Simulation Orchestrator**| `src/qst/orchestration/` | ✅ | ✅ | ✅ | ✅ |
| **Statistics Engine** | `src/qst/orchestration/statistics.py` | ✅ | ✅ | ✅ | |
| **Parameter Sweeps** | `src/qst/orchestration/sweep_generator.py`| ✅ | ✅ | ✅ | |
| **Analysis Layer** | `src/qst/analysis/` | ✅ | ✅ | | |
| **Reporting / Export Layer**| `src/qst/reporting/` | ✅ | ✅ | ✅ | |
| **Visualization Engine** | `src/qst/visualization/` | ✅ | ✅ | ✅ | |
| **Command Line Interface** | `src/qst/cli/` | ✅ | | ✅ | |
