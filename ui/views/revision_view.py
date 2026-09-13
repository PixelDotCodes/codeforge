"""
Revision View

Displays the revision queue, scheduling controls, and revision history.
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


class RevisionView(ttk.Frame):
    """Placeholder view for the Revision management screen."""

    view_name = "Revision"

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
            text="Revision Tracker",
            style="HeaderTitle.TLabel",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Organize and track spaced practice revisions.",
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

        self.btn_add_revision = tk.Button(
            filter_card,
            text="+ Log Revision",
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
        self.btn_add_revision.pack(side="left", padx=(0, 16))

        lbl_type = tk.Label(
            filter_card,
            text="Revision Type:",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        lbl_type.pack(side="left", padx=(0, 6))

        self.type_cb = ttk.Combobox(
            filter_card,
            values=["All Types", "Quick Review", "Deep Review", "Redo from Scratch"],
            state="readonly",
            width=18,
        )
        self.type_cb.set("All Types")
        self.type_cb.pack(side="left", padx=(0, 16))

        # 3. Revision Queue / History Table
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

        columns = ("rev_id", "prob_id", "date", "type")
        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("rev_id", text="Revision ID")
        self.tree.heading("prob_id", text="Problem ID")
        self.tree.heading("date", text="Revision Date")
        self.tree.heading("type", text="Revision Type")

        self.tree.column("rev_id", width=90, anchor="center")
        self.tree.column("prob_id", width=90, anchor="center")
        self.tree.column("date", width=140, anchor="center")
        self.tree.column("type", width=180, anchor="w")

        v_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")

        # Empty state note
        self.placeholder_note = tk.Label(
            table_card,
            text="No revisions logged yet.\nRevision tracking will connect to RevisionService in Step 8.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        self.placeholder_note.place(relx=0.5, rely=0.5, anchor="center")

        # 4. Spaced repetition info footer
        info_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_SMALL + 4,
        )
        info_card.grid(row=3, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, PAD_OUTER_Y))

        info_text = (
            "📌 Spaced repetition strategy: Review new problems at 1 day, 3 days, and 7 days. "
            "Track quick passes vs complete re-implementations."
        )
        info_label = tk.Label(
            info_card,
            text=info_text,
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
        )
        info_label.pack(anchor="w")
