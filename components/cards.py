import customtkinter as ctk
from config import CARD, TEXT, MUTED, BORDER


def make_card(parent, corner=18):
    return ctk.CTkFrame(
        parent, fg_color=CARD, corner_radius=corner,
        border_width=1, border_color=BORDER
    )


def make_label(parent, text, size=14, color=TEXT, weight="normal"):
    return ctk.CTkLabel(
        parent, text=text, font=("Segoe UI", size, weight), text_color=color
    )


def metric_card(parent, column, title, value, symbol, green):
    panel = make_card(parent, 15)
    panel.grid(row=0, column=column, sticky="ew", padx=4, pady=3)
    make_label(panel, f"{symbol}  {title}", 11, MUTED, "bold").pack(
        anchor="w", padx=13, pady=(13, 7)
    )
    value_label = make_label(panel, value, 22, TEXT, "bold")
    value_label.pack(anchor="w", padx=13, pady=(0, 14))
    return value_label
