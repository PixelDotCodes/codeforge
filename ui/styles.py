"""
UI Styling and Theme Definitions for CodeForge.

Provides color palette constants, font definitions, dimensions,
and TTK style configuration for dark theme desktop appearance.
"""

import tkinter.font as tkfont
from tkinter import ttk

# --- Dark Theme Color Palette ---
COLOR_BG = "#0f172a"              # Main window content background (slate-900)
COLOR_SIDEBAR_BG = "#090d16"      # Sidebar deep dark background (slate-950)
COLOR_SIDEBAR_TEXT = "#cbd5e1"    # Sidebar text (slate-300)
COLOR_SIDEBAR_MUTED = "#64748b"   # Sidebar subtitles (slate-500)
COLOR_SIDEBAR_SEP = "#1e293b"     # Sidebar divider line (slate-800)

COLOR_NAV_ACTIVE_BG = "#1e293b"   # Active navigation item background (slate-800)
COLOR_NAV_ACTIVE_TEXT = "#38bdf8" # Active navigation item text (sky-400 accent)
COLOR_NAV_HOVER_BG = "#151e2e"    # Navigation item hover background

COLOR_CARD_BG = "#1e293b"         # Card background (slate-800)
COLOR_CARD_BORDER = "#334155"     # Card border / divider (slate-700)
COLOR_TEXT_PRIMARY = "#f8fafc"    # Primary text (slate-50 - crisp white)
COLOR_TEXT_SECONDARY = "#94a3b8"  # Secondary text (slate-400)
COLOR_TEXT_MUTED = "#64748b"      # Placeholder / disabled text (slate-500)

COLOR_PRIMARY = "#2563eb"         # Primary blue (blue-600)
COLOR_PRIMARY_HOVER = "#1d4ed8"   # Primary blue hover (blue-700)
COLOR_PRIMARY_TEXT = "#ffffff"

COLOR_ACCENT = "#38bdf8"          # Sky blue accent
COLOR_SUCCESS = "#22c55e"         # Green
COLOR_WARNING = "#f59e0b"         # Amber
COLOR_DANGER = "#ef4444"          # Red

# --- Window Dimensions ---
WINDOW_TITLE = "CodeForge - Practice & Contest Tracker"
WINDOW_DEFAULT_SIZE = "1020x680"
WINDOW_MIN_WIDTH = 850
WINDOW_MIN_HEIGHT = 550
SIDEBAR_WIDTH = 210

# --- Standard Spacing ---
PAD_OUTER_X = 24
PAD_OUTER_Y = 18
PAD_INNER = 16
PAD_SMALL = 8

# --- Fonts ---
FONT_FAMILY = "Segoe UI"

FONT_TITLE = (FONT_FAMILY, 16, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 10)
FONT_SECTION = (FONT_FAMILY, 12, "bold")
FONT_CARD_TITLE = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 10)
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_CAPTION = (FONT_FAMILY, 9)
FONT_NAV = (FONT_FAMILY, 10, "bold")
FONT_METRIC_VALUE = (FONT_FAMILY, 22, "bold")
FONT_METRIC_LABEL = (FONT_FAMILY, 9)


def configure_styles(root=None):
    """
    Configure ttk styles used across the application.
    Applies consistent dark theme to frames, labels, buttons, entries, and tables.
    """
    style = ttk.Style(root)

    # Use clam theme when available to allow cross-platform color customization
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")

    # Content background frames
    style.configure(
        "TFrame",
        background=COLOR_BG,
    )
    style.configure(
        "Content.TFrame",
        background=COLOR_BG,
    )
    style.configure(
        "Card.TFrame",
        background=COLOR_CARD_BG,
        relief="solid",
        borderwidth=1,
    )

    # Labels
    style.configure(
        "TLabel",
        background=COLOR_BG,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_BODY,
    )
    style.configure(
        "HeaderTitle.TLabel",
        background=COLOR_BG,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_TITLE,
    )
    style.configure(
        "HeaderSubtitle.TLabel",
        background=COLOR_BG,
        foreground=COLOR_TEXT_SECONDARY,
        font=FONT_SUBTITLE,
    )
    style.configure(
        "CardTitle.TLabel",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_CARD_TITLE,
    )
    style.configure(
        "CardBody.TLabel",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_SECONDARY,
        font=FONT_BODY,
    )
    style.configure(
        "CardCaption.TLabel",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_MUTED,
        font=FONT_CAPTION,
    )
    style.configure(
        "MetricValue.TLabel",
        background=COLOR_CARD_BG,
        foreground=COLOR_ACCENT,
        font=FONT_METRIC_VALUE,
    )
    style.configure(
        "MetricLabel.TLabel",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_SECONDARY,
        font=FONT_METRIC_LABEL,
    )

    # Buttons
    style.configure(
        "Primary.TButton",
        font=FONT_BODY_BOLD,
        background=COLOR_PRIMARY,
        foreground=COLOR_PRIMARY_TEXT,
        padding=(12, 6),
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLOR_PRIMARY_HOVER), ("disabled", COLOR_CARD_BORDER)],
        foreground=[("disabled", COLOR_TEXT_MUTED)],
    )

    style.configure(
        "Secondary.TButton",
        font=FONT_BODY,
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_PRIMARY,
        padding=(10, 6),
        borderwidth=1,
    )

    # Entry fields
    style.configure(
        "TEntry",
        fieldbackground=COLOR_CARD_BG,
        foreground=COLOR_TEXT_PRIMARY,
        insertcolor=COLOR_TEXT_PRIMARY,
        bordercolor=COLOR_CARD_BORDER,
        lightcolor=COLOR_CARD_BORDER,
        darkcolor=COLOR_CARD_BORDER,
    )

    # Combobox
    style.configure(
        "TCombobox",
        fieldbackground=COLOR_CARD_BG,
        background=COLOR_CARD_BORDER,
        foreground=COLOR_TEXT_PRIMARY,
        arrowcolor=COLOR_TEXT_PRIMARY,
        bordercolor=COLOR_CARD_BORDER,
        lightcolor=COLOR_CARD_BORDER,
        darkcolor=COLOR_CARD_BORDER,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLOR_CARD_BG)],
        selectbackground=[("readonly", COLOR_CARD_BG)],
        selectforeground=[("readonly", COLOR_TEXT_PRIMARY)],
    )

    # Radiobuttons
    style.configure(
        "TRadiobutton",
        background=COLOR_CARD_BG,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_BODY,
    )
    style.map(
        "TRadiobutton",
        background=[("active", COLOR_CARD_BG)],
        foreground=[("active", COLOR_TEXT_PRIMARY)],
    )

    # Scrollbars
    style.configure(
        "TScrollbar",
        background=COLOR_CARD_BORDER,
        troughcolor=COLOR_BG,
        bordercolor=COLOR_BG,
        arrowcolor=COLOR_TEXT_SECONDARY,
    )

    # Treeview / Tables (Dark Theme)
    style.configure(
        "Treeview",
        background=COLOR_CARD_BG,
        fieldbackground=COLOR_CARD_BG,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_BODY,
        rowheight=26,
        bordercolor=COLOR_CARD_BORDER,
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_PRIMARY)],
        foreground=[("selected", "#ffffff")],
    )

    style.configure(
        "Treeview.Heading",
        font=FONT_BODY_BOLD,
        background=COLOR_CARD_BORDER,
        foreground=COLOR_TEXT_PRIMARY,
        padding=(6, 6),
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#475569")],
        foreground=[("active", COLOR_TEXT_PRIMARY)],
    )

    return style
