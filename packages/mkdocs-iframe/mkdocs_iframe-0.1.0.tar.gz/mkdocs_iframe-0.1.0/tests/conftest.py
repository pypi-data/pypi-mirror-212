"""Configuration for the pytest test suite."""
from pytest_html.html_report import HTMLReport


def pytest_html_report_title(report: HTMLReport) -> None:
    """Set the pytest report title."""
    report.title = "Test Report"
