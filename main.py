"""
CodeForge - Coding Practice and Contest Tracker
Main Application Entry Point
"""

from ui.app import CodeForgeApp


def main():
    """Launch the CodeForge desktop application."""
    app = CodeForgeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
