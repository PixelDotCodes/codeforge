"""
Analytics View

Provides visualization placeholders for problem difficulty breakdown,
topic distributions, and activity trends.
In Step 7.1, this provides a clean placeholder layout adhering to CodeForge design rules.
"""

import tkinter as tk
from tkinter import ttk

from ui.styles import (
    COLOR_BG,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_BODY,
    FONT_CARD_TITLE,
    FONT_METRIC_LABEL,
    FONT_METRIC_VALUE,
    PAD_INNER,
    PAD_OUTER_X,
    PAD_OUTER_Y,
    PAD_SMALL,
)


class AnalyticsView(ttk.Frame):
    """Placeholder view for the Analytics and charts screen."""

    view_name = "Analytics"

    def __init__(self, parent, app=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # 1. Header
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(PAD_OUTER_Y, 12))

        title_label = ttk.Label(
            header_frame,
            text="Analytics & Insights",
            style="HeaderTitle.TLabel",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Visualize problem difficulty distribution, topic coverage, and practice trends.",
            style="HeaderSubtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # 2. Analytics KPI cards (3 cards)
        kpi_frame = ttk.Frame(self, style="Content.TFrame")
        kpi_frame.grid(row=1, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, 16))

        for col_idx in range(3):
            kpi_frame.columnconfigure(col_idx, weight=1, uniform="kpi")

        kpis = [
            ("Difficulty Ratio (E / M / H)", "0 / 0 / 0", "problem distribution"),
            ("Top Practiced Topic", "None", "based on solved problems"),
            ("Practice Consistency", "0%", "active days ratio"),
        ]

        for idx, (kpi_title, kpi_val, kpi_sub) in enumerate(kpis):
            card = tk.Frame(
                kpi_frame,
                bg=COLOR_CARD_BG,
                highlightbackground=COLOR_CARD_BORDER,
                highlightthickness=1,
                padx=PAD_INNER,
                pady=PAD_INNER,
            )
            card.grid(row=0, column=idx, padx=(0 if idx == 0 else 10, 0), sticky="nsew")

            lbl_title = tk.Label(
                card,
                text=kpi_title.upper(),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_SECONDARY,
                font=FONT_METRIC_LABEL,
            )
            lbl_title.pack(anchor="w")

            lbl_val = tk.Label(
                card,
                text=kpi_val,
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_PRIMARY,
                font=FONT_METRIC_VALUE,
            )
            lbl_val.pack(anchor="w", pady=(4, 2))

            lbl_sub = tk.Label(
                card,
                text=kpi_sub,
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                font=FONT_METRIC_LABEL,
            )
            lbl_sub.pack(anchor="w")

        # 3. Chart Placeholder Frames (2 side-by-side)
        charts_frame = ttk.Frame(self, style="Content.TFrame")
        charts_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_OUTER_X, pady=(0, 16))
        charts_frame.columnconfigure(0, weight=1, uniform="charts")
        charts_frame.columnconfigure(1, weight=1, uniform="charts")
        charts_frame.rowconfigure(0, weight=1)

        # Chart 1: Difficulty Breakdown
        chart1_card = tk.Frame(
            charts_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        chart1_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        chart1_title = tk.Label(
            chart1_card,
            text="Difficulty Distribution",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        chart1_title.pack(anchor="w")

        chart1_placeholder = tk.Label(
            chart1_card,
            text="📊 [Chart Placeholder]\nMatplotlib pie / bar chart will be embedded here in Step 7.4 / Step 8.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        chart1_placeholder.pack(fill="both", expand=True)

        # Chart 2: Topic Breakdown
        chart2_card = tk.Frame(
            charts_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        chart2_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        chart2_title = tk.Label(
            chart2_card,
            text="Topic Coverage",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        chart2_title.pack(anchor="w")

        chart2_placeholder = tk.Label(
            chart2_card,
            text="📈 [Chart Placeholder]\nTopic distribution and practice frequency will appear here.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        chart2_placeholder.pack(fill="both", expand=True)

        # 4. Footer Note
        footer_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_SMALL + 4,
        )
        footer_card.grid(row=3, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, PAD_OUTER_Y))

        footer_label = tk.Label(
            footer_card,
            text="Analytics calculations are powered by AnalyticsService. GUI rendering will be attached in Step 8.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        footer_label.pack(anchor="w")
