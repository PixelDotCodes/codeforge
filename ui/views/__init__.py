"""
Views package for CodeForge UI.
"""

from ui.views.analytics_view import AnalyticsView
from ui.views.dashboard_view import DashboardView
from ui.views.import_view import ImportView
from ui.views.problems_view import ProblemsView
from ui.views.revision_view import RevisionView

__all__ = [
    "DashboardView",
    "ProblemsView",
    "RevisionView",
    "AnalyticsView",
    "ImportView",
]
