from requests import post

from firmitas.conf import logrdata, standard
from firmitas.unit import issubody, issuhead


def makenote(
    retcount,
    servname,
    strtdate,
    stopdate,
    daystobt,
    daystodd,
    certfile,
    issuauth,
    serialno,
    assignee,
):
    try:
        logrdata.logrobjc.debug(
            f"[{servname}] Notification request attempt count - {retcount+1} of {standard.maxretry}"
        )
        rqstobjc = post(
            url=f"https://pagure.io/api/0/{standard.reponame}/new_issue",
            headers={"Authorization": f"token {standard.password}"},
            data={
                "title": issuhead.format(servname=servname, daysqant=standard.daysqant),
                "issue_content": issubody.format(
                    servname=servname,
                    daysqant=standard.daysqant,
                    strtdate=strtdate,
                    stopdate=stopdate,
                    daystobt=abs(daystobt),
                    daystodd=abs(daystodd),
                    certfile=certfile,
                    issuauth=issuauth,
                    serialno=serialno,
                ),
                "tag": ",".join(standard.tagslist),
                "assignee": assignee,
            },
        )
        logrdata.logrobjc.debug(
            f"[{servname}] The notification request was met with response code "
            + f"{rqstobjc.status_code}"
        )
        if rqstobjc.status_code == 200:
            logrdata.logrobjc.debug(
                f"[{servname}] The created notification ticket was created with ID "
                + f"#{rqstobjc.json()['issue']['id']} ({rqstobjc.json()['issue']['full_url']})."
            )
            return (
                True,
                rqstobjc.json()["issue"]["full_url"],
                rqstobjc.json()["issue"]["date_created"],
            )
        else:
            return False, "", ""
    except Exception as expt:
        logrdata.logrobjc.error(
            f"[{servname}] The notification ticket could not be created - {expt}"
        )
        return False, "", ""
