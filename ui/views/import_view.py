"""
Import View

Provides controls for bulk importing problem lists from CSV or JSON files.
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
    FONT_CARD_TITLE,
    PAD_INNER,
    PAD_OUTER_X,
    PAD_OUTER_Y,
    PAD_SMALL,
)


class ImportView(ttk.Frame):
    """Placeholder view for problem and activity import functionality."""

    view_name = "Import"

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
            text="Import Problems & Data",
            style="HeaderTitle.TLabel",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Bulk import problem lists and activity records from external files.",
            style="HeaderSubtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # 2. File Selection Card
        input_card = tk.Frame(
            self,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        input_card.grid(row=1, column=0, sticky="ew", padx=PAD_OUTER_X, pady=(0, 16))

        card_title = tk.Label(
            input_card,
            text="Select Import Source",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        card_title.pack(anchor="w", pady=(0, 12))

        # Format selector
        format_frame = tk.Frame(input_card, bg=COLOR_CARD_BG)
        format_frame.pack(fill="x", pady=(0, 10))

        lbl_format = tk.Label(
            format_frame,
            text="Format:",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
            width=10,
            anchor="w",
        )
        lbl_format.pack(side="left")

        self.format_var = tk.StringVar(value="CSV")
        rb_csv = ttk.Radiobutton(format_frame, text="CSV File (.csv)", variable=self.format_var, value="CSV")
        rb_csv.pack(side="left", padx=(0, 16))
        rb_json = ttk.Radiobutton(format_frame, text="JSON File (.json)", variable=self.format_var, value="JSON")
        rb_json.pack(side="left")

        # File path row
        file_frame = tk.Frame(input_card, bg=COLOR_CARD_BG)
        file_frame.pack(fill="x", pady=(0, 14))

        lbl_file = tk.Label(
            file_frame,
            text="File Path:",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
            width=10,
            anchor="w",
        )
        lbl_file.pack(side="left")

        self.file_entry = ttk.Entry(file_frame)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_browse = ttk.Button(file_frame, text="Browse...", state="disabled")
        self.btn_browse.pack(side="left")

        # Action button
        self.btn_import = tk.Button(
            input_card,
            text="Start Import",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief="flat",
            font=FONT_BODY_BOLD,
            padx=16,
            pady=6,
            cursor="hand2",
            state="disabled",
        )
        self.btn_import.pack(anchor="w")

        # 3. Import Log & Instructions Area (2 side-by-side)
        bottom_frame = ttk.Frame(self, style="Content.TFrame")
        bottom_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_OUTER_X, pady=(0, PAD_OUTER_Y))
        bottom_frame.columnconfigure(0, weight=1, uniform="import_bottom")
        bottom_frame.columnconfigure(1, weight=1, uniform="import_bottom")
        bottom_frame.rowconfigure(0, weight=1)

        # Expected Schema Guidelines
        guide_card = tk.Frame(
            bottom_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        guide_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        guide_title = tk.Label(
            guide_card,
            text="Expected File Structure",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        guide_title.pack(anchor="w", pady=(0, 8))

        guide_content = (
            "Required columns for CSV import:\n\n"
            "• platform: e.g. 'LeetCode', 'Codeforces'\n"
            "• question_number: Positive integer (e.g. 1, 42)\n"
            "• title: Problem title string\n"
            "• difficulty: 'Easy', 'Medium', or 'Hard'\n"
            "• problem_url: Valid problem link URL\n\n"
            "Validation rules will be applied via ProblemService before persisting."
        )
        guide_label = tk.Label(
            guide_card,
            text=guide_content,
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY,
            justify="left",
            anchor="nw",
        )
        guide_label.pack(fill="both", expand=True)

        # Import Log / Console Placeholder
        log_card = tk.Frame(
            bottom_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        log_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        log_title = tk.Label(
            log_card,
            text="Import Output & Logs",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        log_title.pack(anchor="w", pady=(0, 8))

        log_placeholder = tk.Label(
            log_card,
            text="No active import.\nValidation and import logs will appear here during execution.",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        log_placeholder.pack(fill="both", expand=True)
