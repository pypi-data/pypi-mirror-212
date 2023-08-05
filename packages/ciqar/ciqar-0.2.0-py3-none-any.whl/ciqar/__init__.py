"""
Ciqar is a tool for creating reports from different code quality analyzers output.
"""

__version__ = "0.2.0"

def main() -> None:
    from ciqar.application import CiqarApplication
    application = CiqarApplication()
    application.run()
