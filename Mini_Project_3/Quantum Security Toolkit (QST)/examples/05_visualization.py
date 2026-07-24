"""Example 05: Visualizations.

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Intermediate
Estimated Completion Time: 4 minutes
Concepts Demonstrated:
  - Defining visualization datasets (LineSeries, ScatterSeries, HistogramSeries, HeatmapMatrix)
  - Instantiating the MatplotlibBackend visualization renderer
  - Rendering charts in various styles (LightTheme, DarkTheme, ScientificTheme)
  - Exporting plots to PNG, SVG, and PDF formats using pathlib paths

================================================================================
REQUIREMENTS
================================================================================
  - Python 3.10+
  - matplotlib >= 3.0.0
  - Quantum Security Toolkit (QST) installed or in python path

================================================================================
COMMON TROUBLESHOOTING
================================================================================
  - Missing file format support: Ensure that Matplotlib supports PDF/SVG backends.
  - Overwrite protection triggers: Instantiating `MatplotlibBackend(overwrite_protection=True)` throws validation errors if files already exist.
"""

import sys
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.visualization.styles import LightTheme, DarkTheme, ScientificTheme
from qst.visualization.matplotlib_backend import MatplotlibBackend
from qst.visualization.visualizer import Visualizer
from qst.visualization.datasets import (
    LineSeries,
    ScatterSeries,
    HistogramSeries,
    HeatmapMatrix,
)
from qst.exceptions.base import QSTError


def main() -> None:
    """Generates various visualizations using the MatplotlibBackend and themes."""
    # Define outputs paths using pathlib
    base_dir = Path(__file__).resolve().parent
    figs_dir = base_dir / "outputs" / "figures"
    logs_dir = base_dir / "outputs" / "logs"

    figs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "05_visualization.log"

    print("--- Example 05: Generating QST Visualizations ---")
    print(f"Figures output directory: {figs_dir}\n")

    try:
        # Initialize Matplotlib backend with overwrite protection off for examples
        backend = MatplotlibBackend(overwrite_protection=False)

        # 1. Generate Line Chart (QBER Trend vs Interception) using LightTheme
        # Exports to PNG format
        line_data = LineSeries(
            label="QBER Trend",
            x_values=(0.0, 0.25, 0.50, 0.75, 1.0),
            y_values=(0.0, 0.065, 0.125, 0.185, 0.25),
        )
        line_path = figs_dir / "qber_trend.png"
        visualizer_light = Visualizer(backend, LightTheme())
        visualizer_light.line_chart(line_data, str(line_path))
        print(f"Generated Line Chart: {line_path.name} (PNG)")

        # 2. Generate Scatter Plot (QBER vs Key Rate) using DarkTheme
        # Exports to SVG format
        scatter_data = ScatterSeries(
            label="QBER vs Key Rate",
            x_values=(0.0, 0.05, 0.12, 0.18, 0.25),
            y_values=(0.50, 0.48, 0.45, 0.42, 0.38),
        )
        scatter_path = figs_dir / "qber_vs_keyrate.svg"
        visualizer_dark = Visualizer(backend, DarkTheme())
        visualizer_dark.scatter_chart(scatter_data, str(scatter_path))
        print(f"Generated Scatter Plot: {scatter_path.name} (SVG)")

        # 3. Generate Histogram (Raw QBER Distribution) using ScientificTheme
        # Exports to PDF format
        hist_data = HistogramSeries(
            label="QBER Distribution",
            values=(0.05, 0.12, 0.15, 0.22, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29),
            bin_edges=(0.0, 0.1, 0.2, 0.3, 0.4),
            bin_counts=(1, 2, 6, 1),
        )
        hist_path = figs_dir / "qber_distribution.pdf"
        visualizer_sci = Visualizer(backend, ScientificTheme())
        visualizer_sci.histogram(hist_data, str(hist_path))
        print(f"Generated Histogram:   {hist_path.name} (PDF)")

        # 4. Generate Heatmap Matrix (QBER across Qubits vs Interception) using LightTheme
        # Exports to PNG format
        x_labels = ("Qubits=10", "Qubits=20", "Qubits=30")
        y_labels = ("Prob=0.0", "Prob=0.5", "Prob=1.0")
        matrix = (
            (0.0, 0.0, 0.0),
            (0.12, 0.13, 0.125),
            (0.24, 0.26, 0.25),
        )
        heatmap_data = HeatmapMatrix(
            label="QBER Grid Heatmap",
            x_labels=x_labels,
            y_labels=y_labels,
            matrix=matrix,
        )
        heatmap_path = figs_dir / "qber_heatmap.png"
        visualizer_light.heatmap(heatmap_data, str(heatmap_path))
        print(f"Generated Heatmap:     {heatmap_path.name} (PNG)")

        # Optional: Save a log entry
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write("QST Example 05 Visualization Log\nSuccess\n")

    except QSTError as e:
        print(f"\n[QST Validation Error]: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[System Error]: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# ================================================================================
# EXPECTED OUTPUT
# ================================================================================
# --- Example 05: Generating QST Visualizations ---
# Figures output directory: .../examples/outputs/figures
#
# Generated Line Chart: qber_trend.png (PNG)
# Generated Scatter Plot: qber_vs_keyrate.svg (SVG)
# Generated Histogram:   qber_distribution.pdf (PDF)
# Generated Heatmap:     qber_heatmap.png (PNG)
