# MVT module for settings on bugreports
# by K+Lab 2025

import sys

from mvt.android.cmd_check_bugreport import CmdAndroidCheckBugreport
from mvt.common.utils import init_logging, set_verbose_logging

from bugreport_settings import Settings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python3 {sys.argv[0]} [path to bugreport (dir or zip)]")
        sys.exit()

    bugreport_path = sys.argv[1]


    set_verbose_logging(False)

    cmd = CmdAndroidCheckBugreport(
        target_path=bugreport_path,
        hashes=True,
    )

    cmd.modules.append(Settings)
    cmd.run()

