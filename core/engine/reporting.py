import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from pathlib import Path
from datetime import datetime

def generate_pdf_report(
    symbol: str,
    df: pd.DataFrame,
    metrics: dict,
    output_dir: str = "assets"
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Report_{symbol}_{timestamp}.pdf"
    out_path = str(Path(output_dir) / filename)

    with PdfPages(out_path) as pdf:
        # Page 1: Title & metrics
        fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 portrait
        ax.axis("off")
        text = f"Quant Reactor Ultra Report\n\nSymbol: {symbol}\n\nMetrics:\n"
        for k, v in metrics.items():
            text += f"- {k}: {v:.4f}\n"
        ax.text(0.05, 0.95, text, va="top", fontsize=10)
        pdf.savefig(fig)
        plt.close(fig)

        # Page 2: Equity curve
        if "Returns" in df.columns:
            equity = (1 + df["Returns"].fillna(0)).cumprod()
            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.plot(df["Date"], equity)
            ax.set_title(f"{symbol} – Equity Curve")
            ax.set_xlabel("Date")
            ax.set_ylabel("Equity")
            pdf.savefig(fig)
            plt.close(fig)

    return out_path
