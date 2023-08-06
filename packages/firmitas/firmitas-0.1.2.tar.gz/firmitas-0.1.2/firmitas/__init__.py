import os.path
import sys
from importlib import metadata
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path

import yaml

from firmitas.conf import logrdata, standard

__vers__ = metadata.version("firmitas")


def readconf(confobjc):
    standard.gitforge = confobjc.get("gitforge", standard.gitforge)
    standard.repoloca = confobjc.get("repoloca", standard.repoloca)
    standard.reponame = confobjc.get("reponame", standard.reponame)
    standard.username = confobjc.get("username", standard.username)
    standard.password = confobjc.get("password", standard.password)
    standard.daysqant = confobjc.get("daysqant", standard.daysqant)
    standard.maxretry = confobjc.get("maxretry", standard.maxretry)
    standard.certloca = confobjc.get("certloca", standard.certloca)
    standard.hostloca = confobjc.get("hostloca", standard.hostloca)

    dictConfig(standard.logrconf)
    logrdata.logrobjc = getLogger(__name__)

    if standard.gitforge not in ["pagure", "github", "gitlab"]:
        logrdata.logrobjc.error("The specified ticketing repository forge is not yet supported")
        sys.exit(1)

    if not isinstance(standard.daysqant, int):
        logrdata.logrobjc.error(
            "The variable 'daysqant' must have a value of the integer data type only"
        )
        sys.exit(1)
    else:
        if standard.daysqant <= 0:
            logrdata.logrobjc.error(
                "The variable 'daysqant' must have a non-zero positive integer value"
            )
            sys.exit(1)

    if not os.path.exists(standard.certloca):
        logrdata.logrobjc.error(
            "Please set the directory containing X.509 standard TLS certificates properly"
        )
        sys.exit(1)

    if not os.path.exists(standard.hostloca):
        logrdata.logrobjc.error(
            "Please set the directory containing the service hostname map properly"
        )
        sys.exit(1)
    else:
        standard.certdict = yaml.safe_load(Path(standard.hostloca).read_text())
