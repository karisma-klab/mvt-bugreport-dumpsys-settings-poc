# MVT module for settings on bugreports
# by K+Lab 2025

import logging
from typing import Optional

from dumpsys_settings_artifact import DumpsysSettingsArtifact

from mvt.android.modules.bugreport.base import BugReportModule


mvt_log = logging.getLogger("mvt")

class Settings(DumpsysSettingsArtifact, BugReportModule):
    """This module extracts settings."""

    def __init__(
        self,
        file_path: Optional[str] = None,
        target_path: Optional[str] = None,
        results_path: Optional[str] = None,
        module_options: Optional[dict] = None,
        log: logging.Logger = logging.getLogger(__name__),
        results: Optional[list] = None,
    ) -> None:
        super().__init__(
            file_path=file_path,
            target_path=target_path,
            results_path=results_path,
            module_options=module_options,
            log=mvt_log,
            results=results,
        )

    def run(self) -> None:
        full_dumpsys = self._get_dumpstate_file()
        if not full_dumpsys:
            self.log.error(
                "Unable to find dumpstate file. "
                "Did you provide a valid bug report archive?"
            )
            return

        content = self.extract_dumpsys_section(
            full_dumpsys.decode("utf-8", errors="ignore"),
            "DUMP OF SERVICE settings:",
        )
        self.parse(content)

        for result in self.results:
            self.log.info(
                'Found %d "%s settings"', len(self.results[result]), result
            )


        self.log.info(
            "Identified a total of %d sets of settings", len(self.results)
        )


