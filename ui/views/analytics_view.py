"""
Analytics View

Provides visualization for problem difficulty breakdown,
topic distributions, and activity trends.
Connects Tkinter UI -> AnalyticsService -> Repositories.
"""

import tkinter as tk
from tkinter import ttk

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

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
    """View for Analytics and charts screen."""

    view_name = "Analytics"

    def __init__(self, parent, app=None, analytics_service=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._analytics_service = analytics_service
        self.chart1_canvas = None
        self.chart2_canvas = None
        self._build_ui()

    @property
    def analytics_service(self):
        if self._analytics_service is not None:
            return self._analytics_service
        if self.app is not None and hasattr(self.app, "analytics_service"):
            return self.app.analytics_service
        return None

    def on_show(self):
        """Lifecycle hook invoked when Analytics view becomes visible."""
        self.refresh_analytics()

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

        self.kpi_labels = {}
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

            self.kpi_labels[kpi_title] = lbl_val

        # 3. Chart Placeholder Frames (2 side-by-side)
        charts_frame = ttk.Frame(self, style="Content.TFrame")
        charts_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_OUTER_X, pady=(0, 16))
        charts_frame.columnconfigure(0, weight=1, uniform="charts")
        charts_frame.columnconfigure(1, weight=1, uniform="charts")
        charts_frame.rowconfigure(0, weight=1)

        # Chart 1: Difficulty Breakdown
        self.chart1_card = tk.Frame(
            charts_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        self.chart1_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        chart1_title = tk.Label(
            self.chart1_card,
            text="Difficulty Distribution",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        chart1_title.pack(anchor="w", pady=(0, 4))

        self.chart1_container = tk.Frame(self.chart1_card, bg=COLOR_CARD_BG)
        self.chart1_container.pack(fill="both", expand=True)

        self.chart1_placeholder = tk.Label(
            self.chart1_container,
            text="📊 No problem difficulty data to display.\nAdd problems to view the difficulty breakdown.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        self.chart1_placeholder.pack(fill="both", expand=True)

        # Chart 2: Topic Breakdown
        self.chart2_card = tk.Frame(
            charts_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        self.chart2_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        chart2_title = tk.Label(
            self.chart2_card,
            text="Topic Coverage",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        chart2_title.pack(anchor="w", pady=(0, 4))

        self.chart2_container = tk.Frame(self.chart2_card, bg=COLOR_CARD_BG)
        self.chart2_container.pack(fill="both", expand=True)

        self.chart2_placeholder = tk.Label(
            self.chart2_container,
            text="📈 No topic practice data to display.\nTopic coverage will appear as problems are solved.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        self.chart2_placeholder.pack(fill="both", expand=True)

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
            text="Analytics calculations are powered by AnalyticsService.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        footer_label.pack(anchor="w")

    def refresh_analytics(self):
        """Query AnalyticsService and refresh KPIs and embedded charts."""
        if not self.analytics_service:
            return

        diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        top_topic = "None"
        consistency_text = "0%"
        topic_counts = {}

        try:
            diff_counts = self.analytics_service.get_difficulty_counts()
        except Exception:
            diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}

        try:
            top_topics = self.analytics_service.get_most_practiced_topics(limit=1)
            if top_topics:
                top_topic = list(top_topics.keys())[0]
        except Exception:
            top_topic = "None"

        try:
            heatmap = self.analytics_service.get_activity_heatmap_data() or {}
            active_days = len(heatmap)
            consistency_text = f"{min(100, int(active_days / 30 * 100))}%"
        except Exception:
            consistency_text = "0%"

        try:
            topic_counts = self.analytics_service.get_topic_problem_counts() or {}
        except Exception:
            topic_counts = {}

        # Update KPI labels
        if "Difficulty Ratio (E / M / H)" in self.kpi_labels:
            self.kpi_labels["Difficulty Ratio (E / M / H)"].configure(
                text=f"{diff_counts.get('Easy', 0)} / {diff_counts.get('Medium', 0)} / {diff_counts.get('Hard', 0)}"
            )

        if "Top Practiced Topic" in self.kpi_labels:
            self.kpi_labels["Top Practiced Topic"].configure(text=str(top_topic))

        if "Practice Consistency" in self.kpi_labels:
            self.kpi_labels["Practice Consistency"].configure(text=consistency_text)

        # Update Chart 1: Difficulty Distribution
        self._render_difficulty_chart(diff_counts)

        # Update Chart 2: Topic Coverage
        self._render_topic_chart(topic_counts)

    def _render_difficulty_chart(self, diff_counts):
        """Render bar chart of difficulty distribution via Matplotlib or fallback."""
        total = sum(diff_counts.values())

        # Clean existing canvas
        if self.chart1_canvas:
            self.chart1_canvas.get_tk_widget().destroy()
            self.chart1_canvas = None

        if total == 0 or not MATPLOTLIB_AVAILABLE:
            self.chart1_placeholder.pack(fill="both", expand=True)
            return

        self.chart1_placeholder.pack_forget()

        categories = ["Easy", "Medium", "Hard"]
        values = [diff_counts.get("Easy", 0), diff_counts.get("Medium", 0), diff_counts.get("Hard", 0)]
        colors = ["#22c55e", "#f59e0b", "#ef4444"]

        fig = Figure(figsize=(4, 2.8), dpi=80, facecolor="#1e293b")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1e293b")

        bars = ax.bar(categories, values, color=colors, width=0.5)
        ax.tick_params(colors="#94a3b8", labelsize=10)
        ax.spines["bottom"].set_color("#334155")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#334155")

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{int(height)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                color="#e2e8f0",
                fontsize=9,
            )

        fig.tight_layout()

        self.chart1_canvas = FigureCanvasTkAgg(fig, master=self.chart1_container)
        self.chart1_canvas.draw()
        self.chart1_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _render_topic_chart(self, topic_counts):
        """Render horizontal bar chart of topic coverage via Matplotlib or fallback."""
        if self.chart2_canvas:
            self.chart2_canvas.get_tk_widget().destroy()
            self.chart2_canvas = None

        if not topic_counts or not MATPLOTLIB_AVAILABLE:
            self.chart2_placeholder.pack(fill="both", expand=True)
            return

        self.chart2_placeholder.pack_forget()

        # Display top 5 topics
        items = list(topic_counts.items())[:5]
        topics = [k for k, _ in reversed(items)]
        counts = [v for _, v in reversed(items)]

        fig = Figure(figsize=(4, 2.8), dpi=80, facecolor="#1e293b")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1e293b")

        bars = ax.barh(topics, counts, color="#3b82f6", height=0.55)
        ax.tick_params(colors="#94a3b8", labelsize=9)
        ax.spines["bottom"].set_color("#334155")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#334155")

        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f"{int(width)}",
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(4, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                color="#e2e8f0",
                fontsize=9,
            )

        fig.tight_layout()

        self.chart2_canvas = FigureCanvasTkAgg(fig, master=self.chart2_container)
        self.chart2_canvas.draw()
        self.chart2_canvas.get_tk_widget().pack(fill="both", expand=True)
