#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#app/Report_Generator.py
# app/PDF_Report_Generator.py
import streamlit as st
import pandas as pd
from pathlib import Path

from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.metrics import compute_basic_metrics
from core.engine.reporting import generate_pdf_report


def main():
    st.title("📄 PDF Report Generator")

    data_dir = "core/data"
    files = list_csv_files(data_dir)

    if not files:
        st.warning("No CSV files found in core/data")
        st.stop()

    selected = st.selectbox("Select Symbol", files)
    if not selected:
        st.warning("No symbol selected")
        st.stop()

    symbol = Path(selected).stem

    # Load data
    df = load_single_csv(selected)
    df = add_simple_returns(df)

    # Compute metrics
    metrics = compute_basic_metrics(df["Returns"].fillna(0))

    st.subheader("Preview Metrics")
    st.json(metrics)

    # Generate PDF
    if st.button("Generate PDF Report"):
        try:
            out_path = generate_pdf_report(symbol, df, metrics)
            st.success(f"Report generated successfully: {out_path}")

            # Optional download button
            with open(out_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=Path(out_path).name,
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"Failed to generate report: {e}")

# import streamlit as st
# from core.utils.helpers import list_csv_files
# from core.engine.loader import load_single_csv
# from core.engine.indicators import add_simple_returns
# from core.engine.metrics import compute_basic_metrics
# from core.engine.reporting import generate_pdf_report

# st.title("📄 PDF Report Generator")

# data_dir = "core/data"
# files = list_csv_files(data_dir)

# if not files:
#     st.warning("No CSV files found in core/data")
#     st.stop()

# selected = st.selectbox("Select Symbol", files)
# if selected is None:
#     st.warning("No file selected")
#     st.stop()
# symbol = selected.split("/")[-1].replace(".csv", "")

# df = load_single_csv(selected)
# df = add_simple_returns(df)
# metrics = compute_basic_metrics(df["Returns"])

# st.subheader("Preview Metrics")
# st.json(metrics)

# if st.button("Generate PDF Report"):
#     path = generate_pdf_report(symbol, df, metrics, output_dir="assets")
#     st.success(f"Report generated: {path}")
#     with open(path, "rb") as f:
#         st.download_button(
#             label="Download PDF",
#             data=f,
#             file_name=path.split("/")[-1],
#             mime="application/pdf",
#         )
