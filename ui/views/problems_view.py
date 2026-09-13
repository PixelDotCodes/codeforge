"""
Problems View

Displays the problem repository table, search and filtering controls,
and action buttons for problem management.
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
    FONT_BODY_BOLD,
    FONT_CAPTION,
    PAD_INNER,
    PAD_OUTER_X,
    PAD_OUTER_Y,
    PAD_SMALL,
)


class ProblemsView(ttk.Frame):
    """Placeholder view for the Problems list and management screen."""

    view_name = "Problems"

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

        # Add Problem button placeholder
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
            state="disabled",
        )
        self.btn_add.pack(side="left", padx=(0, 16))

        # Search box placeholder
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

        # Platform filter placeholder
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

        # Difficulty filter placeholder
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
            text="No problems loaded yet.\nProblem CRUD operations will connect to ProblemService in Step 8.",
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
