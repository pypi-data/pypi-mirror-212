issuhead = "[FMTS] TLS certificate for {servname} service is about to expire in {daysqant} days"

issubody = """
This is to inform that the TLS certificate for **{servname}** service will expire in about **{daysqant} day(s)** from now on **{stopdate} UTC**. The following are information relevant to the associated TLS certificate.

- **Service name** - **{servname}** (Certificate stored as **{certfile}**)
- **Issuing authority** - {issuauth} (**#{serialno}**)
- **Validity starting** - **{strtdate} UTC** (**{daystobt} day(s)** passed since beginning)
- **Validity ending** - **{stopdate} UTC** (**{daystodd} day(s)** left before expiring)

The point of contact for the service have been tagged into this ticket and notified about the same. It is strongly recommended to promptly renew the TLS certificate for the service before the existing one expires.

_This issue ticket was automatically created by the [**Firmitas notification service**](https://gitlab.com/t0xic0der/firmitas). Please contact [**Fedora Infrastructure**](https://pagure.io/fedora-infrastructure/issues) team if you believe that this notification is mistaken._
"""  # noqa
