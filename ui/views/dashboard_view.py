"""
Dashboard View

Provides an overview of problem-solving statistics, streaks,
LeetCode-style contribution heatmap, suggested questions for review,
and recent user activity.
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
        self._cell_map = {}
        self._last_heatmap_summary = ""
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
            text="Overview of your coding practice, activity streak, and review recommendations.",
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
            ("Due Revision", "0", "review suggestions"),
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

        # 3. LeetCode-style Activity Heatmap Section
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
        heatmap_header.pack(fill="x", pady=(0, 6))

        heatmap_title = tk.Label(
            heatmap_header,
            text="Activity Heatmap",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        heatmap_title.pack(side="left")

        # Intensity Legend
        legend_frame = tk.Frame(heatmap_header, bg=COLOR_CARD_BG)
        legend_frame.pack(side="right")

        tk.Label(
            legend_frame,
            text="Less",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION,
        ).pack(side="left", padx=(0, 4))

        for color_hex in ["#252d3d", "#0e4429", "#007335", "#00b84c", "#39d353"]:
            sq = tk.Frame(
                legend_frame,
                bg=color_hex,
                width=10,
                height=10,
                highlightthickness=1,
                highlightbackground="#334155",
            )
            sq.pack(side="left", padx=1)
            sq.pack_propagate(False)

        tk.Label(
            legend_frame,
            text="More",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION,
        ).pack(side="left", padx=(4, 0))

        self.heatmap_container = tk.Frame(
            self.heatmap_card,
            bg=COLOR_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=8,
            pady=8,
        )
        self.heatmap_container.pack(fill="x")

        # Canvas for LeetCode-style grid
        self.heatmap_canvas = tk.Canvas(
            self.heatmap_container,
            bg=COLOR_BG,
            height=125,
            highlightthickness=0,
        )
        self.heatmap_canvas.pack(fill="x", expand=True)
        self.heatmap_canvas.bind("<Motion>", self._on_heatmap_motion)
        self.heatmap_canvas.bind("<Leave>", self._on_heatmap_leave)

        self.heatmap_label = tk.Label(
            self.heatmap_container,
            text="Loading activity heatmap...",
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION,
            justify="center",
            pady=4,
        )
        self.heatmap_label.pack(fill="x")

        # 4. Two-column Activity & Schedule section
        middle_frame = ttk.Frame(self, style="Content.TFrame")
        middle_frame.grid(row=3, column=0, sticky="nsew", padx=PAD_OUTER_X, pady=(0, 12))
        middle_frame.columnconfigure(0, weight=3, uniform="middle")
        middle_frame.columnconfigure(1, weight=3, uniform="middle")
        middle_frame.rowconfigure(0, weight=1)

        # Left Card: Recent Problem Activity (Preserved)
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

        # Right Card: Suggested Questions to Review (Replaces "Revisions Due Today")
        self.revision_card = tk.Frame(
            middle_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER - 2,
        )
        self.revision_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.suggested_title = tk.Label(
            self.revision_card,
            text="Suggested Questions to Review",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        self.suggested_title.pack(anchor="w", pady=(0, 8))

        self.revision_container = tk.Frame(self.revision_card, bg=COLOR_CARD_BG)
        self.revision_container.pack(fill="both", expand=True)
        self.suggested_container = self.revision_container

        self.revision_placeholder = tk.Label(
            self.revision_container,
            text="No questions eligible for review.\nSolve more problems or log practices to build your review queue.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
            pady=20,
        )
        self.revision_placeholder.pack(fill="both", expand=True)

        # 5. Footer Note with Top Practiced Problem Badge
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
            text="💡 Spaced repetition strategy: Review new problems at 1 day, 3 days, and 7 days.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        tip_label.pack(side="left")

        self.top_problem_label = tk.Label(
            footer_card,
            text="",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION,
        )
        self.top_problem_label.pack(side="right")

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

        # 2. Suggested Questions to Review from AnalyticsService
        suggested = []
        if self.analytics_service and hasattr(self.analytics_service, "get_suggested_questions_for_review"):
            try:
                suggested = self.analytics_service.get_suggested_questions_for_review(limit=5) or []
            except Exception:
                suggested = []

        if "Due Revision" in self.metric_cards:
            self.metric_cards["Due Revision"].configure(text=str(len(suggested)))

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

        # Render real LeetCode-style contribution heatmap
        self._render_heatmap(heatmap_data)

        # Update Heatmap Label summary
        if heatmap_data:
            total_act = sum(heatmap_data.values())
            summary_text = (
                f"Total Practice Sessions: {total_act} across {active_days} active days • "
                f"Current Streak: {streak} consecutive days"
            )
        else:
            summary_text = "No activity logged yet. Solve problems or log revisions to see your activity."

        self._last_heatmap_summary = summary_text
        self.heatmap_label.configure(text=summary_text)

        # 4. Top Practiced Problem
        if self.analytics_service and hasattr(self.analytics_service, "get_top_practiced_problem"):
            try:
                top_prob = self.analytics_service.get_top_practiced_problem()
                if top_prob:
                    title = top_prob.get("title", "")
                    plat = top_prob.get("platform", "")
                    qno = top_prob.get("platform_question_no", "")
                    cnt = top_prob.get("practice_count", 0)
                    t_str = "practice" if cnt == 1 else "practices"
                    ref = f"{plat} #{qno}" if plat and qno else f"#{top_prob.get('problem_id')}"
                    self.top_problem_label.configure(
                        text=f"⭐ Top Practiced: {title} ({ref} • {cnt} {t_str})"
                    )
                else:
                    self.top_problem_label.configure(text="")
            except Exception:
                self.top_problem_label.configure(text="")

        # 5. Recent Activity from ActivityService
        self._update_recent_activity()

        # 6. Suggested Questions to Review (max 5)
        self._update_suggested_reviews(suggested)

    def _render_heatmap(self, heatmap_data):
        """Draw LeetCode-style calendar contribution heatmap on Tkinter Canvas."""
        self.heatmap_canvas.delete("all")
        self._cell_map.clear()

        today = date.today()
        # LeetCode grid: 7 rows (Sunday to Saturday) across 52 weeks
        days_since_sunday = (today.weekday() + 1) % 7
        this_sunday = today - timedelta(days=days_since_sunday)
        start_sunday = this_sunday - timedelta(weeks=51)

        cell_size = 10
        gap = 3
        step = cell_size + gap
        margin_left = 32
        margin_top = 20

        # Day of week labels on left
        day_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
        for r_idx, d_name in day_labels.items():
            y_pos = margin_top + r_idx * step + cell_size // 2
            self.heatmap_canvas.create_text(
                margin_left - 6,
                y_pos,
                text=d_name,
                fill="#64748b",
                font=("Segoe UI", 7),
                anchor="e",
            )

        last_month = None

        for col in range(52):
            for row in range(7):
                day_offset = col * 7 + row
                curr_d = start_sunday + timedelta(days=day_offset)
                x1 = margin_left + col * step
                y1 = margin_top + row * step
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Month label along the top
                if row == 0:
                    curr_month = curr_d.strftime("%b")
                    if curr_month != last_month and col < 51:
                        self.heatmap_canvas.create_text(
                            x1,
                            8,
                            text=curr_month,
                            fill="#64748b",
                            font=("Segoe UI", 8),
                            anchor="w",
                        )
                        last_month = curr_month

                if curr_d > today:
                    continue

                cnt = heatmap_data.get(curr_d, 0)
                if cnt == 0:
                    fill_col = "#252d3d"
                    outline_col = "#334155"
                elif cnt <= 2:
                    fill_col = "#0e4429"
                    outline_col = "#166534"
                elif cnt <= 4:
                    fill_col = "#007335"
                    outline_col = "#22c55e"
                elif cnt <= 6:
                    fill_col = "#00b84c"
                    outline_col = "#4ade80"
                else:
                    fill_col = "#39d353"
                    outline_col = "#86efac"

                rect_id = self.heatmap_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_col,
                    outline=outline_col,
                    tags=("cell",),
                )
                self._cell_map[rect_id] = (curr_d, cnt)

    def _on_heatmap_motion(self, event):
        """Display tooltip/details for hovered heatmap cell."""
        item = self.heatmap_canvas.find_withtag("current")
        if item and item[0] in self._cell_map:
            curr_d, cnt = self._cell_map[item[0]]
            s_word = "submission" if cnt == 1 else "submissions"
            date_str = curr_d.strftime("%B %d, %Y")
            self.heatmap_label.configure(
                text=f"{cnt} {s_word} on {date_str}"
            )
        else:
            self._restore_heatmap_summary()

    def _on_heatmap_leave(self, event):
        self._restore_heatmap_summary()

    def _restore_heatmap_summary(self):
        if self._last_heatmap_summary:
            self.heatmap_label.configure(text=self._last_heatmap_summary)

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
        """Display recent activity items in recent_container (Preserved)."""
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

    def _update_suggested_reviews(self, suggestions):
        """Display up to 5 suggested questions to review based on practice history."""
        for widget in self.revision_container.winfo_children():
            widget.destroy()

        if not suggestions:
            lbl = tk.Label(
                self.revision_container,
                text="No questions eligible for review.\nSolve more problems or log practices to build your review queue.",
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                font=FONT_BODY,
                justify="center",
                pady=20,
            )
            lbl.pack(fill="both", expand=True)
            return

        for item in suggestions[:5]:
            title = item.get("title", "")
            plat = item.get("platform", "")
            qno = item.get("platform_question_no", "")
            diff = item.get("difficulty", "Medium")
            cnt = item.get("practice_count", 0)

            row = tk.Frame(self.revision_container, bg=COLOR_CARD_BG, pady=4)
            row.pack(fill="x")

            left_box = tk.Frame(row, bg=COLOR_CARD_BG)
            left_box.pack(side="left", fill="x", expand=True)

            ref = f"{plat} #{qno}" if plat and qno else f"#{item.get('problem_id')}"
            tk.Label(
                left_box,
                text=ref,
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                font=FONT_CAPTION,
            ).pack(side="left", padx=(0, 6))

            disp_title = (title[:26] + "…") if len(title) > 28 else title
            tk.Label(
                left_box,
                text=disp_title,
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_PRIMARY,
                font=FONT_BODY,
            ).pack(side="left")

            right_box = tk.Frame(row, bg=COLOR_CARD_BG)
            right_box.pack(side="right")

            diff_color = "#22c55e" if diff == "Easy" else ("#ef4444" if diff == "Hard" else "#f59e0b")
            tk.Label(
                right_box,
                text=diff,
                bg=COLOR_CARD_BG,
                fg=diff_color,
                font=FONT_CAPTION,
            ).pack(side="left", padx=(0, 8))

            c_text = "0 practices" if cnt == 0 else (f"{cnt} practice" if cnt == 1 else f"{cnt} practices")
            tk.Label(
                right_box,
                text=c_text,
                bg=COLOR_CARD_BG,
                fg="#38bdf8",
                font=FONT_CAPTION,
            ).pack(side="left")

    def _update_revisions_due(self, revisions_due):
        """Backward-compatibility alias for test suites."""
        if hasattr(self, "analytics_service") and self.analytics_service and hasattr(self.analytics_service, "get_suggested_questions_for_review"):
            try:
                suggestions = self.analytics_service.get_suggested_questions_for_review(limit=5) or []
                self._update_suggested_reviews(suggestions)
                return
            except Exception:
                pass
        self._update_suggested_reviews(revisions_due)
