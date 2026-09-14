"""
CodeForge Main Application Window

Manages the top-level Tkinter window, persistent navigation sidebar,
and dynamic view switching between Dashboard, Problems, Revision,
Analytics, and Import screens.
"""

import tkinter as tk
from tkinter import ttk

from repositories import (
    ActivityRepository,
    ProblemRepository,
    RevisionRepository,
    TopicRepository,
)
from services.activity_service import ActivityService
from services.analytics_service import AnalyticsService
from services.problem_service import ProblemService
from services.revision_service import RevisionService
from ui.styles import (
    COLOR_BG,
    COLOR_NAV_ACTIVE_BG,
    COLOR_NAV_ACTIVE_TEXT,
    COLOR_NAV_HOVER_BG,
    COLOR_SIDEBAR_BG,
    COLOR_SIDEBAR_MUTED,
    COLOR_SIDEBAR_SEP,
    COLOR_SIDEBAR_TEXT,
    FONT_BODY,
    FONT_CAPTION,
    FONT_NAV,
    FONT_SECTION,
    SIDEBAR_WIDTH,
    WINDOW_DEFAULT_SIZE,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_TITLE,
    configure_styles,
)
from ui.views import (
    AnalyticsView,
    DashboardView,
    ImportView,
    ProblemsView,
    RevisionView,
)


class CodeForgeApp(tk.Tk):
    """Main application shell for CodeForge desktop GUI."""

    NAV_ITEMS = [
        ("Dashboard", "📊  Dashboard"),
        ("Problems", "📝  Problems"),
        ("Revision", "🔄  Revision"),
        ("Analytics", "📈  Analytics"),
        ("Import", "📥  Import"),
    ]

    VIEW_CLASSES = {
        "Dashboard": DashboardView,
        "Problems": ProblemsView,
        "Revision": RevisionView,
        "Analytics": AnalyticsView,
        "Import": ImportView,
    }

    def __init__(
        self,
        problem_repository=None,
        activity_repository=None,
        revision_repository=None,
        topic_repository=None,
        problem_service=None,
        revision_service=None,
        activity_service=None,
        analytics_service=None,
    ):
        super().__init__()

        # 1. Window setup
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_DEFAULT_SIZE)
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.configure(bg=COLOR_BG)

        # 2. Configure ttk styles
        self.style = configure_styles(self)

        # 3. Initialize Repositories & Services
        self.problem_repository = problem_repository or ProblemRepository()
        self.activity_repository = activity_repository or ActivityRepository()
        self.revision_repository = revision_repository or RevisionRepository()
        self.topic_repository = topic_repository or TopicRepository()

        self.problem_service = problem_service or ProblemService(self.problem_repository)
        self.revision_service = revision_service or RevisionService(self.revision_repository)
        self.activity_service = activity_service or ActivityService(self.activity_repository)
        self.analytics_service = analytics_service or AnalyticsService(
            problem_repository=self.problem_repository,
            activity_repository=self.activity_repository,
            topic_repository=self.topic_repository,
        )

        # 4. Application State
        self.current_view_name = None
        self.views = {}
        self.nav_buttons = {}

        # 5. Build application layout
        self._build_shell()

        # 6. Show initial view
        self.show_view("Dashboard")

    def _build_shell(self):
        """Construct the sidebar and content frame containers."""
        # Main horizontal container
        self.shell_container = tk.Frame(self, bg=COLOR_BG)
        self.shell_container.pack(fill="both", expand=True)

        # --- Left Sidebar ---
        self.sidebar_frame = tk.Frame(
            self.shell_container,
            bg=COLOR_SIDEBAR_BG,
            width=SIDEBAR_WIDTH,
        )
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Top App Branding
        brand_frame = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR_BG, padx=16, pady=20)
        brand_frame.pack(fill="x")

        brand_title = tk.Label(
            brand_frame,
            text="CodeForge",
            bg=COLOR_SIDEBAR_BG,
            fg="#ffffff",
            font=FONT_SECTION,
            anchor="w",
        )
        brand_title.pack(fill="x")

        brand_subtitle = tk.Label(
            brand_frame,
            text="Practice Tracker",
            bg=COLOR_SIDEBAR_BG,
            fg=COLOR_SIDEBAR_MUTED,
            font=FONT_CAPTION,
            anchor="w",
        )
        brand_subtitle.pack(fill="x", pady=(2, 0))

        # Brand separator line
        sep = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR_SEP, height=1)
        sep.pack(fill="x", padx=16, pady=(0, 16))

        # Navigation Buttons List
        nav_container = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR_BG)
        nav_container.pack(fill="x", padx=8)

        for view_key, label_text in self.NAV_ITEMS:
            btn = tk.Button(
                nav_container,
                text=label_text,
                bg=COLOR_SIDEBAR_BG,
                fg=COLOR_SIDEBAR_TEXT,
                activebackground=COLOR_NAV_ACTIVE_BG,
                activeforeground=COLOR_NAV_ACTIVE_TEXT,
                relief="flat",
                bd=0,
                anchor="w",
                font=FONT_NAV,
                padx=14,
                pady=10,
                cursor="hand2",
                command=lambda name=view_key: self.show_view(name),
            )
            btn.pack(fill="x", pady=2)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, k=view_key: self._on_nav_hover(b, k, True))
            btn.bind("<Leave>", lambda e, b=btn, k=view_key: self._on_nav_hover(b, k, False))

            self.nav_buttons[view_key] = btn

        # Sidebar Footer
        footer_frame = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR_BG, padx=16, pady=16)
        footer_frame.pack(side="bottom", fill="x")

        version_label = tk.Label(
            footer_frame,
            text="v0.1.0",
            bg=COLOR_SIDEBAR_BG,
            fg=COLOR_SIDEBAR_MUTED,
            font=FONT_CAPTION,
            anchor="w",
        )
        version_label.pack(fill="x")

        # --- Right Content Area ---
        self.content_container = ttk.Frame(self.shell_container, style="Content.TFrame")
        self.content_container.pack(side="right", fill="both", expand=True)
        self.content_container.columnconfigure(0, weight=1)
        self.content_container.rowconfigure(0, weight=1)

        # Pre-instantiate all views
        for view_key, ViewClass in self.VIEW_CLASSES.items():
            view = ViewClass(self.content_container, app=self)
            self.views[view_key] = view
            view.grid(row=0, column=0, sticky="nsew")

    def _on_nav_hover(self, button, view_key, is_hovering):
        """Provide subtle hover feedback for inactive navigation buttons."""
        if self.current_view_name == view_key:
            return

        if is_hovering:
            button.configure(bg=COLOR_NAV_HOVER_BG, fg="#ffffff")
        else:
            button.configure(bg=COLOR_SIDEBAR_BG, fg=COLOR_SIDEBAR_TEXT)

    def show_view(self, view_name):
        """
        Switch visible content area to the requested view.
        Updates navigation highlighting and brings target view to front.
        """
        if view_name not in self.views:
            raise KeyError(f"View '{view_name}' is not registered.")

        # Raise target view frame
        target_view = self.views[view_name]
        target_view.tkraise()
        self.current_view_name = view_name

        # Update sidebar button states
        for key, btn in self.nav_buttons.items():
            if key == view_name:
                btn.configure(
                    bg=COLOR_NAV_ACTIVE_BG,
                    fg=COLOR_NAV_ACTIVE_TEXT,
                )
            else:
                btn.configure(
                    bg=COLOR_SIDEBAR_BG,
                    fg=COLOR_SIDEBAR_TEXT,
                )

        # Optional on_show hook for view refresh in future steps
        if hasattr(target_view, "on_show"):
            target_view.on_show()
