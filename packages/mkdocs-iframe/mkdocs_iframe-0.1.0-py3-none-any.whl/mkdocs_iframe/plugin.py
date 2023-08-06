"""This module contains the `mkdocs_iframe` plugin."""

from __future__ import annotations

import re
import shutil
import textwrap
from pathlib import Path
from tempfile import mkdtemp
from typing import TYPE_CHECKING, Any, Sequence

from mkdocs.config.config_options import Type as MkType
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files

from mkdocs_iframe.loggers import get_logger

if TYPE_CHECKING:
    from mkdocs.config import Config

log = get_logger(__name__)


class Report:
    """HTML Report."""

    def __init__(
        self,
        *,
        name: str,
        path: str | None = None,
        root: str = "index.html",
        page: str | None = None,
        use_directory_urls: bool = False,
    ):
        """Initialize Report."""
        self.name = name
        self.path = path or f"html{name}"
        self.root = root
        self.page = page or f"{name}.md"
        self.id = f"{name}iframe"
        self.use_directory_urls = use_directory_urls

    def root_file(self) -> str:
        """Return the root page of the report."""
        report_index = self.root
        if report_index == "index.html":
            report_index = f"{self.name}index.html"

        if self.use_directory_urls:
            return report_index
        return f"{self.name}/{report_index}"

    def nav_page(self) -> str:
        """Generate the NAV page source."""
        root = self.root_file()

        style = textwrap.dedent(
            """
            <style>
            article h1, article > a, .md-sidebar--secondary {
                display: none !important;
            }
            </style>
            """,
        )

        iframe = textwrap.dedent(
            f"""
            <iframe
                id="{self.id}"
                src="{root}"
                frameborder="0"
                scrolling="no"
                onload="resizeIframe();"
                width="100%">
            </iframe>
            """,
        )

        script = textwrap.dedent(
            f"""
            <script>
            var {self.id} = document.getElementById("{self.id}");

            function resizeIframe() {{
                {self.id}.style.height = {self.id}.contentWindow.document.documentElement.offsetHeight + 'px';
            }}

            testiframe.contentWindow.document.body.onclick = function() {{
                {self.id}.contentWindow.location.reload();
            }}
            </script>

            """,
        )
        return style + iframe + script


class MkDocsIframePlugin(BasePlugin):
    """The MkDocs plugin to integrate the HTML reports in the site."""

    config_scheme: Sequence[tuple[str, MkType]] = (("reports", MkType(list, default=[])),)

    def reports(self, *, use_directory_urls: bool = False) -> list[Report]:
        """Convert config data to Reports."""
        res = []
        for report in self.config["reports"]:
            if isinstance(report, str):
                res.append(Report(use_directory_urls=use_directory_urls, name=report))
            else:
                res.append(Report(use_directory_urls=use_directory_urls, **report))
        return res

    def on_files(self, files: Files, config: Config, **kwargs: Any) -> Files:  # noqa: ARG002
        """Add the html report to the navigation.

        Hook for the [`on_files` event](https://www.mkdocs.org/user-guide/plugins/#on_files).

        Arguments:
            files: The files collection.
            config: The MkDocs config object.
            **kwargs: Additional arguments passed by MkDocs.

        Returns:
            The modified files collection.

        """
        site_dir = Path(config["site_dir"])
        use_directory_urls = config["use_directory_urls"]
        for report in self.reports(use_directory_urls=use_directory_urls):
            page_contents = report.nav_page()
            tmp_dir = mkdtemp()
            tmp_file = Path(tmp_dir) / report.page
            with tmp_file.open("w") as fp:
                fp.write(page_contents)

            files.append(
                File(
                    report.page,
                    str(tmp_file.parent),
                    str(site_dir),
                    use_directory_urls,
                ),
            )

        return files

    def on_post_build(self, config: Config, **kwargs: Any) -> None:  # noqa: ARG002
        """Copy the HTML reports into the site directory.

        Hook for the [`on_post_build` event](https://www.mkdocs.org/user-guide/plugins/#on_post_build).

        Arguments:
            config: The MkDocs config object.
            **kwargs: Additional arguments passed by MkDocs.

        """
        site_dir = Path(config["site_dir"])
        use_directory_urls = config["use_directory_urls"]

        for report in self.reports(use_directory_urls=use_directory_urls):
            report_dir = site_dir / report.name
            tmp_index = site_dir / f".{report.name}-tmp.html"

            if report.root == "index.html":
                if config["use_directory_urls"]:
                    shutil.move(str(report_dir / "index.html"), tmp_index)
                else:
                    shutil.move(str(report_dir.with_suffix(".html")), tmp_index)

            shutil.rmtree(str(report_dir), ignore_errors=True)
            try:
                shutil.copytree(report.path, str(report_dir))
            except FileNotFoundError:
                log.warning(f"No such HTML report directory: {report.path}")
                return

            if report.root == "index.html":
                report_root = report.root_file()

                shutil.move(str(report_dir / "index.html"), report_dir / report_root)
                if use_directory_urls:
                    shutil.move(str(tmp_index), report_dir / "index.html")
                else:
                    shutil.move(str(tmp_index), report_dir.with_suffix(".html"))

                for html_file in report_dir.iterdir():
                    if html_file.suffix == ".html" and html_file.name != "index.html":
                        html_file.write_text(
                            re.sub(r'href="index\.html"', f'href="{report_root}"', html_file.read_text()),
                        )
