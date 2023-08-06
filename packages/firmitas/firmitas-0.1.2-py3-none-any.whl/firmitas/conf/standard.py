"""
Variables related to notifications
"""

# The source code forge on which the issue tickets need to be created
gitforge = "pagure"

# The location of the ticketing repository
repoloca = ""

# The name of the ticketing repository with namespace
reponame = ""

# The username to masquerade as in order to create notification tickets
username = ""

# The API key for the source code forge pertaining to the user
password = ""

# Number of days from validity expiry to make the notification for
daysqant = 30

# List of labels to tag the notification tickets with
tagslist = ["firmitas", "automate", "notifier"]

# Maximum number of retries to opening the notification ticket
maxretry = 5

"""
Variables related to probing
"""

# The location of the X.509 standard TLS certificates
certloca = "/var/tmp/firmitas/certhere"

# The location of the service hostnames and maintainers map
hostloca = "/var/tmp/firmitas/certlist.yml"

"""
Variables related to logging
"""

# The default configuration for service logging
logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[FMTS] %(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

"""
Variables used for computing
"""

certdict = {}
