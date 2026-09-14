"""
Problems View

Displays the problem repository table, search and filtering controls,
and action buttons for problem management.
Connects Tkinter UI -> ProblemService -> ProblemRepository -> PostgreSQL.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from ui.styles import (
    COLOR_BG,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_CAPTION,
    PAD_INNER,
    PAD_OUTER_X,
    PAD_OUTER_Y,
    PAD_SMALL,
)


class ProblemsView(ttk.Frame):
    """View for the Problems list and management screen."""

    view_name = "Problems"

    def __init__(self, parent, app=None, problem_service=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._problem_service = problem_service
        self.all_problems = []
        self._build_ui()

    @property
    def problem_service(self):
        if self._problem_service is not None:
            return self._problem_service
        if self.app is not None and hasattr(self.app, "problem_service"):
            return self.app.problem_service
        return None

    def on_show(self):
        """Lifecycle hook invoked when this view becomes visible."""
        self.load_problems()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # 1. Header
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(PAD_OUTER_Y, 12))

        title_label = ttk.Label(
            header_frame,
            text="Problem Tracker",
            style="HeaderTitle.TLabel",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Manage and filter coding problems across platforms.",
            style="HeaderSubtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # 2. Action & Filter Bar Card
        filter_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_SMALL + 2,
        )
        filter_card.grid(row=1, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, 12))

        # Add Problem button
        self.btn_add = tk.Button(
            filter_card,
            text="+ Add Problem",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief="flat",
            font=FONT_BODY_BOLD,
            padx=12,
            pady=4,
            cursor="hand2",
            state="normal",
            command=self._open_add_dialog,
        )
        self.btn_add.pack(side="left", padx=(0, 8))

        # Delete Problem button
        self.btn_delete = tk.Button(
            filter_card,
            text="Delete",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            activebackground="#b91c1c",
            activeforeground="#ffffff",
            relief="flat",
            font=FONT_BODY,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._delete_selected_problem,
        )
        self.btn_delete.pack(side="left", padx=(0, 16))

        # Search box
        lbl_search = tk.Label(
            filter_card,
            text="Search:",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        lbl_search.pack(side="left", padx=(0, 6))

        self.search_entry = ttk.Entry(filter_card, width=24)
        self.search_entry.pack(side="left", padx=(0, 16))
        self.search_entry.bind("<KeyRelease>", lambda _e: self._apply_filters())

        # Platform filter
        lbl_platform = tk.Label(
            filter_card,
            text="Platform:",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        lbl_platform.pack(side="left", padx=(0, 6))

        self.platform_cb = ttk.Combobox(
            filter_card,
            values=["All Platforms", "LeetCode", "Codeforces", "HackerRank"],
            state="readonly",
            width=14,
        )
        self.platform_cb.set("All Platforms")
        self.platform_cb.pack(side="left", padx=(0, 16))
        self.platform_cb.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        # Difficulty filter
        lbl_diff = tk.Label(
            filter_card,
            text="Difficulty:",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        lbl_diff.pack(side="left", padx=(0, 6))

        self.diff_cb = ttk.Combobox(
            filter_card,
            values=["All", "Easy", "Medium", "Hard"],
            state="readonly",
            width=10,
        )
        self.diff_cb.set("All")
        self.diff_cb.pack(side="left")
        self.diff_cb.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        # 3. Problems Table Card
        table_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        table_card.grid(row=2, column=0, sticky="nsew", padx=PAD_OUTER_X, pady=(0, 12))
        table_card.columnconfigure(0, weight=1)
        table_card.rowconfigure(0, weight=1)

        columns = ("id", "platform", "number", "title", "difficulty", "url")
        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("platform", text="Platform")
        self.tree.heading("number", text="#")
        self.tree.heading("title", text="Title")
        self.tree.heading("difficulty", text="Difficulty")
        self.tree.heading("url", text="Problem URL")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("platform", width=110, anchor="w")
        self.tree.column("number", width=70, anchor="center")
        self.tree.column("title", width=260, anchor="w")
        self.tree.column("difficulty", width=90, anchor="center")
        self.tree.column("url", width=220, anchor="w")

        v_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_card, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        # Empty state note
        self.placeholder_note = tk.Label(
            table_card,
            text="No problems loaded yet.\nClick '+ Add Problem' to add your first problem.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        self.placeholder_note.place(relx=0.5, rely=0.5, anchor="center")

        # 4. Status Bar
        status_frame = ttk.Frame(self, style="Content.TFrame")
        status_frame.grid(row=3, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, PAD_OUTER_Y))

        self.status_label = ttk.Label(
            status_frame,
            text="Showing 0 problems",
            style="HeaderSubtitle.TLabel",
        )
        self.status_label.pack(side="left")

    def load_problems(self):
        """Fetch all problems from ProblemService and refresh display."""
        if not self.problem_service:
            return

        try:
            self.all_problems = self.problem_service.get_all_problems() or []
            self._apply_filters()
        except Exception as err:
            self.all_problems = []
            self._render_table([])
            self.status_label.configure(text=f"Database unavailable ({err})")

    def _apply_filters(self):
        """Filter local problem list by search query, platform, and difficulty."""
        search_txt = self.search_entry.get().strip().lower()
        platform_filter = self.platform_cb.get()
        diff_filter = self.diff_cb.get()

        filtered = []
        for p in self.all_problems:
            if not isinstance(p, dict):
                continue

            if platform_filter != "All Platforms" and p.get("platform") != platform_filter:
                continue

            if diff_filter != "All" and p.get("difficulty") != diff_filter:
                continue

            if search_txt:
                title = str(p.get("title", "")).lower()
                qno = str(p.get("platform_question_no") or p.get("question_number") or "").lower()
                plat = str(p.get("platform", "")).lower()
                if search_txt not in title and search_txt not in qno and search_txt not in plat:
                    continue

            filtered.append(p)

        self._render_table(filtered)

    def _render_table(self, problems):
        """Populate the Treeview widget with problem items."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in problems:
            pid = p.get("problem_id", "")
            plat = p.get("platform", "")
            qno = p.get("platform_question_no") or p.get("question_number", "")
            title = p.get("title", "")
            diff = p.get("difficulty", "")
            url = p.get("problem_url", "")
            self.tree.insert("", "end", iid=str(pid), values=(pid, plat, qno, title, diff, url))

        if problems:
            self.placeholder_note.place_forget()
        else:
            self.placeholder_note.configure(
                text="No problems match the current filter.\nClick '+ Add Problem' to create one."
            )
            self.placeholder_note.place(relx=0.5, rely=0.5, anchor="center")

        total = len(self.all_problems)
        showing = len(problems)
        self.status_label.configure(text=f"Showing {showing} of {total} problems")

    def _delete_selected_problem(self):
        """Delete the currently selected problem from the database."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Problem", "Please select a problem to delete.", parent=self)
            return

        problem_id = int(selected[0])
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete problem #{problem_id}?",
            parent=self,
        )
        if not confirm:
            return

        if not self.problem_service:
            return

        try:
            self.problem_service.delete_problem(problem_id)
            self.load_problems()
        except Exception as err:
            messagebox.showerror("Error", f"Failed to delete problem: {err}", parent=self)

    def _open_add_dialog(self):
        """Open a modal dialog to collect new problem input and submit via ProblemService."""
        dialog = tk.Toplevel(self)
        dialog.title("Add New Problem")
        dialog.geometry("460x360")
        dialog.minsize(400, 320)
        dialog.configure(bg=COLOR_CARD_BG)
        dialog.transient(self)
        dialog.grab_set()

        form_frame = tk.Frame(dialog, bg=COLOR_CARD_BG, padx=20, pady=16)
        form_frame.pack(fill="both", expand=True)

        # Platform
        lbl_plat = tk.Label(form_frame, text="Platform:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_plat.grid(row=0, column=0, sticky="w", pady=6)
        cb_plat = ttk.Combobox(form_frame, values=["LeetCode", "Codeforces", "HackerRank"], state="readonly")
        cb_plat.set("LeetCode")
        cb_plat.grid(row=0, column=1, sticky="ew", pady=6)

        # Question Number
        lbl_num = tk.Label(form_frame, text="Question #:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_num.grid(row=1, column=0, sticky="w", pady=6)
        entry_num = ttk.Entry(form_frame)
        entry_num.grid(row=1, column=1, sticky="ew", pady=6)

        # Title
        lbl_title = tk.Label(form_frame, text="Title:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_title.grid(row=2, column=0, sticky="w", pady=6)
        entry_title = ttk.Entry(form_frame)
        entry_title.grid(row=2, column=1, sticky="ew", pady=6)

        # Difficulty
        lbl_diff = tk.Label(form_frame, text="Difficulty:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_diff.grid(row=3, column=0, sticky="w", pady=6)
        cb_diff = ttk.Combobox(form_frame, values=["Easy", "Medium", "Hard"], state="readonly")
        cb_diff.set("Medium")
        cb_diff.grid(row=3, column=1, sticky="ew", pady=6)

        # Problem URL
        lbl_url = tk.Label(form_frame, text="Problem URL:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_url.grid(row=4, column=0, sticky="w", pady=6)
        entry_url = ttk.Entry(form_frame)
        entry_url.grid(row=4, column=1, sticky="ew", pady=6)

        form_frame.columnconfigure(1, weight=1)

        # Buttons
        btn_box = tk.Frame(form_frame, bg=COLOR_CARD_BG)
        btn_box.grid(row=5, column=0, columnspan=2, pady=(18, 0), sticky="e")

        def _on_cancel():
            dialog.destroy()

        def _on_save():
            raw_plat = cb_plat.get()
            raw_num = entry_num.get().strip()
            raw_title = entry_title.get().strip()
            raw_diff = cb_diff.get()
            raw_url = entry_url.get().strip()

            try:
                parsed_num = int(raw_num)
            except (ValueError, TypeError):
                messagebox.showwarning("Validation Error", "Question number must be a positive integer.", parent=dialog)
                return

            if not self.problem_service:
                messagebox.showerror("Error", "ProblemService is not available.", parent=dialog)
                return

            try:
                new_problem = self.problem_service.add_problem(
                    platform=raw_plat,
                    question_number=parsed_num,
                    title=raw_title,
                    difficulty=raw_diff,
                    problem_url=raw_url,
                )

                # Single-user desktop activity recording (user_id = 1)
                if self.app and hasattr(self.app, "activity_service") and self.app.activity_service and new_problem:
                    try:
                        self.app.activity_service.record_problem_activity(
                            user_id=1,
                            problem_id=new_problem["problem_id"],
                        )
                    except Exception:
                        pass

                dialog.destroy()
                self.load_problems()
            except ValueError as val_err:
                messagebox.showwarning("Validation Error", str(val_err), parent=dialog)
            except Exception as db_err:
                messagebox.showerror("Database Error", f"Failed to save problem: {db_err}", parent=dialog)

        btn_cancel = tk.Button(
            btn_box,
            text="Cancel",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            relief="flat",
            padx=12,
            pady=4,
            command=_on_cancel,
        )
        btn_cancel.pack(side="left", padx=(0, 8))

        btn_save = tk.Button(
            btn_box,
            text="Save Problem",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            relief="flat",
            font=FONT_BODY_BOLD,
            padx=14,
            pady=4,
            command=_on_save,
        )
        btn_save.pack(side="left")
