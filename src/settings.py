import toml
import os

config = {
    "info": {
        "name": "NXP",
        "version": "v1.1.0",
        "codev": "252627"
    },
    "repos": {
        "def-repo": "https://raw.githubusercontent.com/hithja/nxp-repo/main"
    },
    "path": {
        "bin": "~/.bin",
        "cache": ".cache",
        "conf-folder": "~/.config/nxp",
        "nxpi": ".nxpi",
        "conf-file": ".nxprc",
    }
}

USER=os.getlogin()