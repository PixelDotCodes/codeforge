"""
Import View

Provides controls for bulk importing problem lists from CSV or JSON files.
Connects Tkinter UI -> ProblemService -> ProblemRepository -> PostgreSQL.
"""

import csv
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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
    """View for problem and activity import functionality."""

    view_name = "Import"

    def __init__(self, parent, app=None, problem_service=None, activity_service=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._problem_service = problem_service
        self._activity_service = activity_service
        self._build_ui()

    @property
    def problem_service(self):
        if self._problem_service is not None:
            return self._problem_service
        if self.app is not None and hasattr(self.app, "problem_service"):
            return self.app.problem_service
        return None

    @property
    def activity_service(self):
        if self._activity_service is not None:
            return self._activity_service
        if self.app is not None and hasattr(self.app, "activity_service"):
            return self.app.activity_service
        return None

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

        self.btn_browse = ttk.Button(file_frame, text="Browse...", command=self._browse_file)
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
            state="normal",
            command=self._start_import,
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
            "Required fields for CSV / JSON import:\n\n"
            "• platform: e.g. 'LeetCode', 'Codeforces'\n"
            "• question_number: Positive integer (e.g. 1, 42)\n"
            "• title: Problem title string\n"
            "• difficulty: 'Easy', 'Medium', or 'Hard'\n"
            "• problem_url: Valid problem link URL\n\n"
            "All rows are validated via ProblemService before persisting."
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

        # Import Log / Console Area
        self.log_card = tk.Frame(
            bottom_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_CARD_BORDER,
            highlightthickness=1,
            padx=PAD_INNER,
            pady=PAD_INNER,
        )
        self.log_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        log_title = tk.Label(
            self.log_card,
            text="Import Output & Logs",
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_CARD_TITLE,
        )
        log_title.pack(anchor="w", pady=(0, 8))

        self.log_container = tk.Frame(self.log_card, bg=COLOR_BG)
        self.log_container.pack(fill="both", expand=True)

        # Retain placeholder label attribute for test compatibility
        self.log_placeholder = tk.Label(
            self.log_container,
            text="No active import.\nValidation and import logs will appear here during execution.",
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED,
            font=FONT_BODY,
            justify="center",
        )
        self.log_placeholder.pack(fill="both", expand=True)

        # Text widget for live logging
        self.log_text = tk.Text(
            self.log_container,
            bg=COLOR_BG,
            fg="#e2e8f0",
            font=FONT_CAPTION,
            relief="flat",
            wrap="word",
            padx=8,
            pady=8,
        )

    def _browse_file(self):
        """Open file dialog and populate file_entry."""
        filetypes = [
            ("All Supported (*.csv, *.json)", "*.csv;*.json"),
            ("CSV Files (*.csv)", "*.csv"),
            ("JSON Files (*.json)", "*.json"),
        ]
        chosen = filedialog.askopenfilename(parent=self, filetypes=filetypes)
        if chosen:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, chosen)
            if chosen.lower().endswith(".json"):
                self.format_var.set("JSON")
            elif chosen.lower().endswith(".csv"):
                self.format_var.set("CSV")

    def _append_log(self, text):
        """Append text to the log console."""
        self.log_placeholder.pack_forget()
        self.log_text.pack(fill="both", expand=True)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def _start_import(self):
        """Parse source file, validate with ProblemService, and record items."""
        filepath = self.file_entry.get().strip()
        if not filepath:
            messagebox.showwarning("Missing File", "Please select a file to import.", parent=self)
            return

        if not os.path.exists(filepath):
            messagebox.showerror("File Error", f"File not found:\n{filepath}", parent=self)
            return

        if not self.problem_service:
            messagebox.showerror("Error", "ProblemService is not available.", parent=self)
            return

        # Clear previous logs
        self.log_text.delete("1.0", tk.END)
        self._append_log(f"--- Starting import from: {os.path.basename(filepath)} ---")

        records = []
        fmt = self.format_var.get().upper()

        try:
            if fmt == "JSON" or filepath.lower().endswith(".json"):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        records = data
                    elif isinstance(data, dict):
                        records = data.get("problems", [data])
            else:
                with open(filepath, "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    records = list(reader)
        except Exception as read_err:
            self._append_log(f"[ERROR] Failed to read file: {read_err}")
            messagebox.showerror("File Error", f"Failed to read file:\n{read_err}", parent=self)
            return

        self._append_log(f"Found {len(records)} entries. Processing...")

        success_count = 0
        fail_count = 0

        for idx, item in enumerate(records, start=1):
            if not isinstance(item, dict):
                self._append_log(f"[SKIP] Row {idx}: Invalid data type.")
                fail_count += 1
                continue

            platform = item.get("platform", "").strip()
            raw_qno = item.get("question_number") or item.get("platform_question_no")
            title = item.get("title", "").strip()
            difficulty = item.get("difficulty", "").strip()
            url = item.get("problem_url", "").strip()

            try:
                qno = int(raw_qno)
            except (ValueError, TypeError):
                self._append_log(f"[FAILED] Row {idx}: Invalid question number '{raw_qno}'.")
                fail_count += 1
                continue

            try:
                new_p = self.problem_service.add_problem(
                    platform=platform,
                    question_number=qno,
                    title=title,
                    difficulty=difficulty,
                    problem_url=url,
                )

                # Single-user desktop activity recording (user_id = 1)
                if self.activity_service and new_p:
                    try:
                        self.activity_service.record_problem_activity(
                            user_id=1,
                            problem_id=new_p["problem_id"],
                        )
                    except Exception:
                        pass

                success_count += 1
                self._append_log(f"[SUCCESS] Row {idx}: Added #{qno} {title} ({difficulty})")
            except ValueError as ve:
                self._append_log(f"[VALIDATION ERROR] Row {idx}: {ve}")
                fail_count += 1
            except Exception as dbe:
                self._append_log(f"[DATABASE ERROR] Row {idx}: {dbe}")
                fail_count += 1

        self._append_log(f"\n--- Import finished: {success_count} succeeded, {fail_count} failed ---")
        messagebox.showinfo(
            "Import Complete",
            f"Import finished!\n\nSuccessfully added: {success_count}\nFailed / Skipped: {fail_count}",
            parent=self,
        )
