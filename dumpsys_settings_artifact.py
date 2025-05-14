# MVT module for settings on bugreports
# by K+Lab 2025

from mvt.android.artifacts.settings import Settings as SettingsArtifact

class DumpsysSettingsArtifact(SettingsArtifact):
    def check_indicators(self) -> None:
        super().check_indicators()

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
                        self.results[namespace][key] = value
                        cur_setting = line
                    else:
                        cur_setting += "\n" + line
            if cur_setting != "":
                setting_dict = self._parse_setting(cur_setting)
                key = setting_dict["name"]
                value = setting_dict["value"]
                self.results[namespace][key] = value


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

