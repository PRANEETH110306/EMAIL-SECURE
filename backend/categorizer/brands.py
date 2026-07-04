from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Brand:
    name: str
    domains: List[str]


BRANDS = [

    # ---------- GOOGLE ----------

    Brand(
        "Google",
        [
            "google.com",
            "gmail.com",
            "accounts.google.com",
            "youtube.com",
            "android.com"
        ]
    ),

    # ---------- MICROSOFT ----------

    Brand(
        "Microsoft",
        [
            "microsoft.com",
            "office.com",
            "office365.com",
            "outlook.com",
            "live.com",
            "azure.com"
        ]
    ),

    # ---------- APPLE ----------

    Brand(
        "Apple",
        [
            "apple.com",
            "icloud.com"
        ]
    ),

    # ---------- GITHUB ----------

    Brand(
        "GitHub",
        [
            "github.com"
        ]
    ),

    # ---------- LINKEDIN ----------

    Brand(
        "LinkedIn",
        [
            "linkedin.com"
        ]
    ),

    # ---------- AMAZON ----------

    Brand(
        "Amazon",
        [
            "amazon.in",
            "amazon.com"
        ]
    ),

    Brand(
        "Flipkart",
        [
            "flipkart.com"
        ]
    ),

    Brand(
        "Myntra",
        [
            "myntra.com"
        ]
    ),

    Brand(
        "Meesho",
        [
            "meesho.com"
        ]
    ),

    # ---------- BANKS ----------

    Brand(
        "SBI",
        [
            "sbi.co.in"
        ]
    ),

    Brand(
        "HDFC",
        [
            "hdfcbank.com"
        ]
    ),

    Brand(
        "ICICI",
        [
            "icicibank.com"
        ]
    ),

    Brand(
        "Axis Bank",
        [
            "axisbank.com"
        ]
    ),

    Brand(
        "PayPal",
        [
            "paypal.com"
        ]
    ),

    # ---------- TRAVEL ----------

    Brand(
        "IRCTC",
        [
            "irctc.co.in"
        ]
    ),

    Brand(
        "MakeMyTrip",
        [
            "makemytrip.com"
        ]
    ),

    Brand(
        "Goibibo",
        [
            "goibibo.com"
        ]
    ),

    Brand(
        "IndiGo",
        [
            "goindigo.in"
        ]
    ),

    # ---------- EDUCATION ----------

    Brand(
        "Coursera",
        [
            "coursera.org"
        ]
    ),

    Brand(
        "Udemy",
        [
            "udemy.com"
        ]
    ),

    Brand(
        "edX",
        [
            "edx.org"
        ]
    ),

    # ---------- HEALTH ----------

    Brand(
        "Apollo",
        [
            "apollo247.com",
            "apollohospitals.com"
        ]
    ),

    Brand(
        "Fortis",
        [
            "fortishealthcare.com"
        ]
    )
]

def resolve_brand(sender: str) -> str:

    sender = sender.lower()

    for brand in BRANDS:

        for domain in brand.domains:

            if domain in sender:

                return brand.name

    #
    # Unknown company
    #

    if "@" in sender:

        try:

            domain = sender.split("@")[1]

            company = domain.split(".")[0]

            company = company.replace(
                "-",
                " "
            )

            return company.title()

        except Exception:

            pass

    return "Unknown Organization"