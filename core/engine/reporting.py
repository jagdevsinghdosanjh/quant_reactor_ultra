#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#core/engine/reporting.py

from pathlib import Path
from typing import Union
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd


def generate_pdf_report(
    symbol: str,
    df: pd.DataFrame,
    metrics: dict,
    output_dir: Union[str, Path] = "assets"
) -> str:

    # Convert to Path
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Report_{symbol}_{timestamp}.pdf"
    out_path = output_dir / filename

    # Ensure Date column is datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    with PdfPages(out_path) as pdf:

        # PAGE 1 — Title + Metrics
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis("off")

        text = f"Quant Reactor Ultra Report\n\nSymbol: {symbol}\n\nMetrics:\n"
        for k, v in metrics.items():
            try:
                text += f"- {k}: {float(v):.4f}\n"
            except Exception:
                text += f"- {k}: {v}\n"

        ax.text(0.05, 0.95, text, va="top", fontsize=10)
        pdf.savefig(fig)
        plt.close(fig)

        # PAGE 2 — Equity Curve
        if "Returns" in df.columns and "Date" in df.columns:
            plot_df = df.dropna(subset=["Date"])
            equity = (1 + plot_df["Returns"].fillna(0)).cumprod()

            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.plot(plot_df["Date"], equity)
            ax.set_title(f"{symbol} – Equity Curve")
            ax.set_xlabel("Date")
            ax.set_ylabel("Equity")
            pdf.savefig(fig)
            plt.close(fig)

    return str(out_path)


# from pathlib import Path
# from datetime import datetime
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# import pandas as pd


# def generate_pdf_report(
#     symbol: str,
#     df: pd.DataFrame,
#     metrics: dict,
#     output_dir: str = "assets"
# ) -> str:

#     # Ensure output directory exists
#     output_dir = Path(output_dir)
#     output_dir.mkdir(parents=True, exist_ok=True)

#     # Build output path
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"Report_{symbol}_{timestamp}.pdf"
#     out_path = output_dir / filename

#     # Ensure Date column is datetime
#     if "Date" in df.columns:
#         df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

#     with PdfPages(out_path) as pdf:

#         # -------------------------
#         # PAGE 1 — Title + Metrics
#         # -------------------------
#         fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 portrait
#         ax.axis("off")

#         text = f"Quant Reactor Ultra Report\n\nSymbol: {symbol}\n\nMetrics:\n"

#         for k, v in metrics.items():
#             try:
#                 text += f"- {k}: {float(v):.4f}\n"
#             except Exception:
#                 text += f"- {k}: {v}\n"

#         ax.text(0.05, 0.95, text, va="top", fontsize=10)
#         pdf.savefig(fig)
#         plt.close(fig)

#         # -------------------------
#         # PAGE 2 — Equity Curve
#         # -------------------------
#         if "Returns" in df.columns and "Date" in df.columns:
#             plot_df = df.dropna(subset=["Date"])
#             equity = (1 + plot_df["Returns"].fillna(0)).cumprod()

#             fig, ax = plt.subplots(figsize=(8.27, 11.69))
#             ax.plot(plot_df["Date"], equity)
#             ax.set_title(f"{symbol} – Equity Curve")
#             ax.set_xlabel("Date")
#             ax.set_ylabel("Equity")
#             pdf.savefig(fig)
#             plt.close(fig)

#     return str(out_path)
