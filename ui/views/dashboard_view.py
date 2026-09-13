"""
Dashboard View

Provides an overview of problem-solving statistics, streaks, upcoming revisions,
and user activity heatmap.
In Step 7.1, this provides a clean placeholder layout adhering to CodeForge dark theme design rules.
"""

import tkinter as tk
from tkinter import ttk

from ui.styles import (
    COLOR_BG,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_BODY,
    FONT_CAPTION,
    FONT_CARD_TITLE,
    FONT_METRIC_LABEL,
    FONT_METRIC_VALUE,
    PAD_INNER,
    PAD_OUTER_X,
    PAD_OUTER_Y,
    PAD_SMALL,
)


class DashboardView(ttk.Frame):
    """Placeholder view for the CodeForge Dashboard."""

    view_name = "Dashboard"

    def __init__(self, parent, app=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # 1. Header
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(PAD_OUTER_Y, 10))

        title_label = ttk.Label(
            header_frame,
            text="Dashboard",
            style="HeaderTitle.TLabel",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Overview of your coding practice, activity streak, and upcoming revisions.",
            style="HeaderSubtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # 2. Key Metrics Summary Grid (4 cards)
        metrics_frame = ttk.Frame(self, style="Content.TFrame")
        metrics_frame.grid(row=1, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, 12))

        for col_idx in range(4):
            metrics_frame.columnconfigure(col_idx, weight=1, uniform="metrics")

        self.metric_cards = {}
        metrics_spec = [
            ("Total Solved", "0", "problems"),
            ("Due Revision", "0", "scheduled"),
            ("Current Streak", "0", "days"),
            ("Active Days", "0", "total"),
        ]

        for idx, (title, default_val, subtext) in enumerate(metrics_spec):
            card = tk.Frame(
                metrics_frame,
                bg=COLOR_CARD_BG,
                highlightbackground=COLOR_CARD_BORDER,
                highlightthickness=1,
                padx=PAD_INNER,
                pady=PAD_INNER - 4,
            )
            card.grid(row=0, column=idx, padx=(0 if idx == 0 else 8, 0), sticky="nsew")

            lbl_title = tk.Label(
                card,
                text=title.upper(),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_SECONDARY,
                font=FONT_METRIC_LABEL,
            )
            lbl_title.pack(anchor="w")

            lbl_value = tk.Label(
                card,
                text=default_val,
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_PRIMARY,
                font=FONT_METRIC_VALUE,
            )
            lbl_value.pack(anchor="w", pady=(2, 1))

            lbl_sub = tk.Label(
                card,
                text=subtext,
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                font=FONT_METRIC_LABEL,
            )
            lbl_sub.pack(anchor="w")

            self.metric_cards[title] = lbl_value

        # 3. Activity Heatmap Section (Placeholder for 52-week activity grid)
        self.heatmap_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER - 2,
        )
        self.heatmap_card.grid(row=2, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, 12))

        heatmap_header = tk.Frame(self.heatmap_card, bg=COLOR_CARD_BG)
        heatmap_header.pack(fill="x", pady=(0, 8))

        heatmap_title = tk.Label(
            heatmap_header,
            text="Activity Heatmap",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        heatmap_title.pack(side="left")

        heatmap_legend = tk.Label(
            heatmap_header,
            text="Less  ■ ■ ■ ■  More",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION,
        )
        heatmap_legend.pack(side="right")

        # Visual placeholder container reserving area for the heatmap canvas/grid
        self.heatmap_container = tk.Frame(
            self.heatmap_card,
            bg=COLOR_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=16,
        )
        self.heatmap_container.pack(fill="x")

        self.heatmap_label = tk.Label(
            self.heatmap_container,
            text="▦  Activity Heatmap (52-Week Grid)\nDaily practice frequency and streak heatmap will be rendered here.\nWill connect to AnalyticsService.get_activity_heatmap_data() in Step 8.",
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        self.heatmap_label.pack(expand=True)

        # 4. Two-column Activity & Schedule section
        middle_frame = ttk.Frame(self, style="Content.TFrame")
        middle_frame.grid(row=3, column=0, sticky="nsew", padx=PAD_OUTER_X, pady=(0, 12))
        middle_frame.columnconfigure(0, weight=3, uniform="middle")
        middle_frame.columnconfigure(1, weight=2, uniform="middle")
        middle_frame.rowconfigure(0, weight=1)

        # Left Card: Recent Activity Placeholder
        recent_card = tk.Frame(
            middle_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER - 2,
        )
        recent_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        recent_title = tk.Label(
            recent_card,
            text="Recent Problem Activity",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        recent_title.pack(anchor="w", pady=(0, 8))

        recent_placeholder = tk.Label(
            recent_card,
            text="No activity recorded yet.\nSolved problems and daily submissions will appear here once connected.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
            pady=20,
        )
        recent_placeholder.pack(fill="both", expand=True)

        # Right Card: Revision Schedule Placeholder
        revision_card = tk.Frame(
            middle_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER - 2,
        )
        revision_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        revision_title = tk.Label(
            revision_card,
            text="Revisions Due Today",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        revision_title.pack(anchor="w", pady=(0, 8))

        revision_placeholder = tk.Label(
            revision_card,
            text="No revisions due today.\nSchedule problem reviews to build long-term retention.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
            pady=20,
        )
        revision_placeholder.pack(fill="both", expand=True)

        # 5. Footer Note
        footer_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_SMALL + 2,
        )
        footer_card.grid(row=4, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, PAD_OUTER_Y))

        tip_label = tk.Label(
            footer_card,
            text="💡 Tip: Solve problems consistently and log revisions. Data will be connected to services in Step 8.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        tip_label.pack(anchor="w")
