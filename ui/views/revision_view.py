"""
Revision View

Displays the revision queue, scheduling controls, and revision history.
Connects Tkinter UI -> RevisionService -> RevisionRepository -> PostgreSQL.
"""

from datetime import date
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


class RevisionView(ttk.Frame):
    """View for the Revision management screen."""

    view_name = "Revision"

    def __init__(self, parent, app=None, revision_service=None):
        super().__init__(parent, style="Content.TFrame")
        self.app = app
        self._revision_service = revision_service
        self.all_revisions = []
        self._build_ui()

    @property
    def revision_service(self):
        if self._revision_service is not None:
            return self._revision_service
        if self.app is not None and hasattr(self.app, "revision_service"):
            return self.app.revision_service
        return None

    def on_show(self):
        """Lifecycle hook invoked when this view becomes visible."""
        self.load_revisions()

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
            state="normal",
            command=self._open_add_revision_dialog,
        )
        self.btn_add_revision.pack(side="left", padx=(0, 8))

        # Delete Revision button
        self.btn_delete_revision = tk.Button(
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
            command=self._delete_selected_revision,
        )
        self.btn_delete_revision.pack(side="left", padx=(0, 16))

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
        self.type_cb.bind("<<ComboboxSelected>>", lambda _e: self._apply_type_filter())

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
            text="No revisions logged yet.\nClick '+ Log Revision' to record a revision.",
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

    def load_revisions(self):
        """Fetch all revisions from RevisionService and refresh table."""
        if not self.revision_service:
            return

        try:
            self.all_revisions = self.revision_service.get_all_revisions() or []
            self._apply_type_filter()
        except Exception:
            self.all_revisions = []
            self._render_table([])

    def _apply_type_filter(self):
        """Filter revision list by selected revision type."""
        selected_type = self.type_cb.get()
        if selected_type == "All Types":
            filtered = list(self.all_revisions)
        else:
            filtered = [
                r for r in self.all_revisions
                if isinstance(r, dict) and r.get("revision_type") == selected_type
            ]
        self._render_table(filtered)

    def _render_table(self, revisions):
        """Populate the Treeview widget with revision records."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in revisions:
            rid = r.get("revision_id", "")
            pid = r.get("problem_id", "")
            rdate = r.get("revision_date", "")
            rtype = r.get("revision_type", "")
            self.tree.insert("", "end", iid=str(rid), values=(rid, pid, rdate, rtype))

        if revisions:
            self.placeholder_note.place_forget()
        else:
            self.placeholder_note.configure(
                text="No revisions match the current filter.\nClick '+ Log Revision' to add one."
            )
            self.placeholder_note.place(relx=0.5, rely=0.5, anchor="center")

    def _delete_selected_revision(self):
        """Delete the currently selected revision record."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Revision", "Please select a revision to delete.", parent=self)
            return

        revision_id = int(selected[0])
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete revision #{revision_id}?",
            parent=self,
        )
        if not confirm:
            return

        if not self.revision_service:
            return

        try:
            self.revision_service.delete_revision(revision_id)
            self.load_revisions()
        except Exception as err:
            messagebox.showerror("Error", f"Failed to delete revision: {err}", parent=self)

    def _open_add_revision_dialog(self):
        """Open a modal dialog to collect new revision data and submit via RevisionService."""
        dialog = tk.Toplevel(self)
        dialog.title("Log Revision")
        dialog.geometry("400x260")
        dialog.minsize(360, 220)
        dialog.configure(bg=COLOR_CARD_BG)
        dialog.transient(self)
        dialog.grab_set()

        form_frame = tk.Frame(dialog, bg=COLOR_CARD_BG, padx=20, pady=16)
        form_frame.pack(fill="both", expand=True)

        # Problem ID
        lbl_pid = tk.Label(form_frame, text="Problem ID:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_pid.grid(row=0, column=0, sticky="w", pady=6)
        entry_pid = ttk.Entry(form_frame)
        entry_pid.grid(row=0, column=1, sticky="ew", pady=6)

        # Revision Date
        lbl_date = tk.Label(form_frame, text="Revision Date:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_date.grid(row=1, column=0, sticky="w", pady=6)
        entry_date = ttk.Entry(form_frame)
        entry_date.insert(0, date.today().strftime("%Y-%m-%d"))
        entry_date.grid(row=1, column=1, sticky="ew", pady=6)

        # Revision Type
        lbl_type = tk.Label(form_frame, text="Revision Type:", bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY, font=FONT_BODY)
        lbl_type.grid(row=2, column=0, sticky="w", pady=6)
        cb_type = ttk.Combobox(
            form_frame,
            values=["Quick Review", "Deep Review", "Redo from Scratch"],
            state="readonly",
        )
        cb_type.set("Quick Review")
        cb_type.grid(row=2, column=1, sticky="ew", pady=6)

        form_frame.columnconfigure(1, weight=1)

        btn_box = tk.Frame(form_frame, bg=COLOR_CARD_BG)
        btn_box.grid(row=3, column=0, columnspan=2, pady=(18, 0), sticky="e")

        def _on_cancel():
            dialog.destroy()

        def _on_save():
            raw_pid = entry_pid.get().strip()
            raw_date = entry_date.get().strip()
            raw_type = cb_type.get().strip()

            try:
                parsed_pid = int(raw_pid)
            except (ValueError, TypeError):
                messagebox.showwarning("Validation Error", "Problem ID must be a positive integer.", parent=dialog)
                return

            if not self.revision_service:
                messagebox.showerror("Error", "RevisionService is not available.", parent=dialog)
                return

            try:
                new_rev = self.revision_service.add_revision(
                    problem_id=parsed_pid,
                    revision_date=raw_date,
                    revision_type=raw_type,
                )

                # Single-user desktop activity recording (user_id = 1)
                if self.app and hasattr(self.app, "activity_service") and self.app.activity_service and new_rev:
                    try:
                        self.app.activity_service.record_problem_activity(
                            user_id=1,
                            problem_id=parsed_pid,
                        )
                    except Exception:
                        pass

                dialog.destroy()
                self.load_revisions()
            except ValueError as val_err:
                messagebox.showwarning("Validation Error", str(val_err), parent=dialog)
            except Exception as db_err:
                messagebox.showerror("Database Error", f"Failed to save revision: {db_err}", parent=dialog)

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
            text="Save Revision",
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            relief="flat",
            font=FONT_BODY_BOLD,
            padx=14,
            pady=4,
            command=_on_save,
        )
        btn_save.pack(side="left")
