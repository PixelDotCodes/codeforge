"""
Dashboard View

Provides an overview of problem-solving statistics, streaks, upcoming revisions,
and user activity heatmap.
Connects Tkinter UI -> AnalyticsService / RevisionService / ActivityService.
"""

from datetime import date, timedelta
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
    """View for the CodeForge Dashboard."""

    view_name = "Dashboard"

    def __init__(self, parent, app=None, analytics_service=None, revision_service=None, activity_service=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._analytics_service = analytics_service
        self._revision_service = revision_service
        self._activity_service = activity_service
        self._build_ui()

    @property
    def analytics_service(self):
        if self._analytics_service is not None:
            return self._analytics_service
        if self.app is not None and hasattr(self.app, "analytics_service"):
            return self.app.analytics_service
        return None

    @property
    def revision_service(self):
        if self._revision_service is not None:
            return self._revision_service
        if self.app is not None and hasattr(self.app, "revision_service"):
            return self.app.revision_service
        return None

    @property
    def activity_service(self):
        if self._activity_service is not None:
            return self._activity_service
        if self.app is not None and hasattr(self.app, "activity_service"):
            return self.app.activity_service
        return None

    def on_show(self):
        """Lifecycle hook invoked when Dashboard view becomes visible."""
        self.refresh_dashboard()

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

        # 3. Activity Heatmap Section
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
            text="▦  Activity Heatmap (52-Week Grid)\nDaily practice frequency and streak heatmap will be rendered here.",
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

        # Left Card: Recent Activity
        self.recent_card = tk.Frame(
            middle_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER - 2,
        )
        self.recent_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        recent_title = tk.Label(
            self.recent_card,
            text="Recent Problem Activity",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        recent_title.pack(anchor="w", pady=(0, 8))

        self.recent_container = tk.Frame(self.recent_card, bg=COLOR_CARD_BG)
        self.recent_container.pack(fill="both", expand=True)

        self.recent_placeholder = tk.Label(
            self.recent_container,
            text="No activity recorded yet.\nSolved problems and daily submissions will appear here once connected.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
            pady=20,
        )
        self.recent_placeholder.pack(fill="both", expand=True)

        # Right Card: Revision Schedule
        self.revision_card = tk.Frame(
            middle_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER - 2,
        )
        self.revision_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        revision_title = tk.Label(
            self.revision_card,
            text="Revisions Due Today",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        revision_title.pack(anchor="w", pady=(0, 8))

        self.revision_container = tk.Frame(self.revision_card, bg=COLOR_CARD_BG)
        self.revision_container.pack(fill="both", expand=True)

        self.revision_placeholder = tk.Label(
            self.revision_container,
            text="No revisions due today.\nSchedule problem reviews to build long-term retention.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
            pady=20,
        )
        self.revision_placeholder.pack(fill="both", expand=True)

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
            text="💡 Tip: Solve problems consistently and log revisions. Spaced repetition builds long-term retention.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        tip_label.pack(anchor="w")

    def refresh_dashboard(self):
        """Fetch latest statistics from backend services and update UI."""
        # 1. Total Solved from AnalyticsService
        total_solved = 0
        if self.analytics_service:
            try:
                total_solved = self.analytics_service.get_total_solved_count()
            except Exception:
                total_solved = 0
        if "Total Solved" in self.metric_cards:
            self.metric_cards["Total Solved"].configure(text=str(total_solved))

        # 2. Due Revisions from RevisionService
        due_count = 0
        revisions_due = []
        today_date = date.today()
        if self.revision_service:
            try:
                all_revs = self.revision_service.get_all_revisions() or []
                for r in all_revs:
                    r_date = r.get("revision_date")
                    if isinstance(r_date, str):
                        try:
                            r_date = date.fromisoformat(r_date.strip())
                        except ValueError:
                            continue
                    if r_date and r_date <= today_date:
                        due_count += 1
                        if r_date == today_date:
                            revisions_due.append(r)
            except Exception:
                due_count = 0
        if "Due Revision" in self.metric_cards:
            self.metric_cards["Due Revision"].configure(text=str(due_count))

        # 3. Heatmap Data & Streak from AnalyticsService
        heatmap_data = {}
        if self.analytics_service:
            try:
                heatmap_data = self.analytics_service.get_activity_heatmap_data() or {}
            except Exception:
                heatmap_data = {}

        active_days = len(heatmap_data)
        streak = self._calculate_streak(heatmap_data)
        if "Current Streak" in self.metric_cards:
            self.metric_cards["Current Streak"].configure(text=str(streak))
        if "Active Days" in self.metric_cards:
            self.metric_cards["Active Days"].configure(text=str(active_days))

        # Update Heatmap Label summary
        if heatmap_data:
            total_act = sum(heatmap_data.values())
            self.heatmap_label.configure(
                text=f"Total Practice Sessions: {total_act} across {active_days} active days.\n"
                     f"Current Streak: {streak} consecutive days."
            )
        else:
            self.heatmap_label.configure(
                text="▦  Activity Heatmap (52-Week Grid)\nNo activity logged yet. Solve problems or log revisions to see your activity."
            )

        # 4. Recent Activity from ActivityService
        self._update_recent_activity()

        # 5. Revisions Due Today
        self._update_revisions_due(revisions_due)

    def _calculate_streak(self, heatmap_data):
        """Calculate consecutive active days ending today or yesterday."""
        if not heatmap_data:
            return 0

        active_dates = set(heatmap_data.keys())
        today_d = date.today()
        current = today_d
        if current not in active_dates:
            current = today_d - timedelta(days=1)
            if current not in active_dates:
                return 0

        streak = 0
        while current in active_dates:
            streak += 1
            current -= timedelta(days=1)
        return streak

    def _update_recent_activity(self):
        """Display recent activity items in recent_container."""
        for widget in self.recent_container.winfo_children():
            widget.destroy()

        activities = []
        if self.activity_service:
            try:
                activities = self.activity_service.get_all_activities() or []
            except Exception:
                activities = []

        if not activities:
            lbl = tk.Label(
                self.recent_container,
                text="No activity recorded yet.\nSolved problems and revisions will appear here.",
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                font=FONT_BODY,
                justify="center",
                pady=20,
            )
            lbl.pack(fill="both", expand=True)
            return

        # Show latest 5 activities
        for act in reversed(activities[-5:]):
            prob_id = act.get("problem_id", "")
            act_type = act.get("activity_type", "Practice")
            act_date = act.get("activity_date", "")
            row = tk.Frame(self.recent_container, bg=COLOR_CARD_BG, pady=3)
            row.pack(fill="x")

            txt = f"• Problem #{prob_id} — {act_type}"
            tk.Label(row, text=txt, bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY).pack(side="left")
            tk.Label(row, text=str(act_date), bg=COLOR_CARD_BG, fg=COLOR_TEXT_MUTED, font=FONT_CAPTION).pack(side="right")

    def _update_revisions_due(self, revisions_due):
        """Display due revisions in revision_container."""
        for widget in self.revision_container.winfo_children():
            widget.destroy()

        if not revisions_due:
            lbl = tk.Label(
                self.revision_container,
                text="No revisions due today.\nSchedule problem reviews to build long-term retention.",
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                font=FONT_BODY,
                justify="center",
                pady=20,
            )
            lbl.pack(fill="both", expand=True)
            return

        for rev in revisions_due[:5]:
            prob_id = rev.get("problem_id", "")
            rev_type = rev.get("revision_type", "Review")
            row = tk.Frame(self.revision_container, bg=COLOR_CARD_BG, pady=3)
            row.pack(fill="x")

            txt = f"• Problem #{prob_id} — {rev_type}"
            tk.Label(row, text=txt, bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY).pack(side="left")
            tk.Label(row, text="Due today", bg=COLOR_CARD_BG, fg="#38bdf8", font=FONT_CAPTION).pack(side="right")
