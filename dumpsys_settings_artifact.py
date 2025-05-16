# MVT module for settings on bugreports
# by K+Lab 2025

from mvt.android.artifacts.artifact import AndroidArtifact
from mvt.android.artifacts.settings import ANDROID_DANGEROUS_SETTINGS


ANDROID_DANGEROUS_APPS = ['com.android.shell']

class DumpsysSettingsArtifact(AndroidArtifact):
    def check_indicators(self) -> None:
        for namespace, settings in self.results.items():
            for key, values in settings.items():
                for danger in ANDROID_DANGEROUS_SETTINGS:
                    # Check if one of the dangerous settings is using an unsafe
                    # value (different than the one specified).
                    if danger["key"] == key and danger["safe_value"] != values["value"]:
                        self.log.warning(
                            'Found suspicious "%s" setting "%s = %s" (%s)',
                            namespace,
                            key,
                            values["value"],
                            danger["description"],
                        )
                    if values['pkg'] in ANDROID_DANGEROUS_APPS:
                        self.log.warning(
                            'Found suspicious "%s" setting "%s = %s" (was modified by %s)',
                            namespace,
                            key,
                            values['value'],
                            values['pkg'],
                        )
                        break

    def parse(self, content: str) -> None:
        self.results = {}
        sections = content.split("\n\n")

        for section in sections:
            namespace = ""
            cur_setting = ""
            for line in section.splitlines():
                if namespace == "":
                    if line.strip().startswith("CONFIG SETTINGS"):
                        namespace = "config"
                    elif line.strip().startswith("GLOBAL SETTINGS"):
                        namespace = "global"
                    elif line.strip().startswith("SECURE SETTINGS"):
                        namespace = "secure"
                    elif line.strip().startswith("SYSTEM SETTINGS"):
                        namespace = "system"
                    else:
                        continue
                    self.results[namespace] = {}
                else:
                    # discard the version line
                    if line.strip().lower().startswith("version"):
                        continue

                    if line.strip().startswith("_id:"):
                        if cur_setting == "":
                            cur_setting = line
                            continue
                        setting_dict = self._parse_setting(cur_setting)
                        key = setting_dict["name"]
                        value = setting_dict["value"]
                        pkg = setting_dict["pkg"]
                        self.results[namespace][key] = {
                            "value": value,
                            "pkg": pkg
                            }
                        cur_setting = line
                    else:
                        cur_setting += "\n" + line
            if cur_setting != "":
                setting_dict = self._parse_setting(cur_setting)
                key = setting_dict["name"]
                value = setting_dict["value"]
                self.results[namespace][key] = {
                            "value": value,
                            "pkg": pkg
                            }


    def _parse_setting(self, setting):
        setting_dict = {}

        key_strings = [ # minus _id because begins at offset 0
            " name:",
            " pkg:",
            " value:",
            " default:",
            " defaultSystemSet:",
            "end"
            ]
        offset = 0
        for key_str in key_strings:
            if key_str != "end":
                end_offset = setting.find(key_str)
            else:
                end_offset = len(setting)
            if end_offset > 0:
                substr = setting[offset:end_offset].strip()
                key, value =  substr.split(":", 1)
                setting_dict[key] = value
                offset = end_offset

        return setting_dict

