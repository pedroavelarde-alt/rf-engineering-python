"""Plot receiver sensitivity margins and their pass/fail threshold."""
import matplotlib.pyplot as plt
from receiver_sensitivity import evaluate_receivers


def main():
    minimum_required_margin_db = 3.0
    results = evaluate_receivers(minimum_required_margin_db=minimum_required_margin_db)
    names = [r["name"].replace(" Receiver", "") for r in results]
    margins = [r["margin_db"] for r in results]
    colors = ["green" if r["result"] == "PASS" else "red" for r in results]
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(names, margins, color=colors)
    ax.axhline(minimum_required_margin_db, color="black", linestyle="--", label="Minimum Required Margin")
    ax.set_ylabel("Sensitivity Margin (dB)")
    ax.set_title("Receiver Sensitivity Margin Comparison")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend()
    for bar, margin in zip(bars, margins):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{margin:.2f} dB", ha="center")
    fig.tight_layout()
    fig.savefig("receiver_comparison_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
