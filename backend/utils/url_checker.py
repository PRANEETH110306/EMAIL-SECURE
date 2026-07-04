import asyncio
import os
import re

from dataclasses import dataclass
from typing import List

import httpx


SUSPICIOUS_TLDS = [
    ".xyz",
    ".tk",
    ".cf",
    ".ml",
    ".ga",
    ".top",
    ".click",
    ".loan",
    ".pw",
    ".cc",
]


URL_SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
]


BRAND_NAMES = [
    "paypal",
    "amazon",
    "google",
    "microsoft",
    "apple",
    "facebook",
    "netflix",
    "instagram",
    "bank",
    "sbi",
    "hdfc",
    "icici",
    "uidai",
    "irctc",
]


SAFE_BROWSING_URL = (
    "https://safebrowsing.googleapis.com/v4/"
    "threatMatches:find"
)


@dataclass
class URLCheckResult:

    url: str

    is_safe: bool

    threat_type: str

    confidence: float

    reasons: List[str]


def extract_urls(
    text: str
) -> List[str]:

    if not text:
        return []

    return re.findall(
        r'https?://[^\s<>"]+',
        text
    )


def extract_domain(
    url: str
) -> str:

    match = re.search(
        r"https?://([^/:?#]+)",
        url,
        re.IGNORECASE,
    )

    if not match:
        return ""

    return match.group(1).lower()


async def google_safe_browsing_check(
    url: str
):

    api_key = os.getenv(
        "GOOGLE_SAFE_BROWSING_API_KEY"
    )

    if not api_key:
        return None

    body = {

        "client": {

            "clientId":
                "email-secure",

            "clientVersion":
                "1.0",

        },

        "threatInfo": {

            "threatTypes": [

                "MALWARE",

                "SOCIAL_ENGINEERING",

                "UNWANTED_SOFTWARE",

            ],

            "platformTypes": [

                "ANY_PLATFORM"

            ],

            "threatEntryTypes": [

                "URL"

            ],

            "threatEntries": [

                {

                    "url": url

                }

            ],

        },

    }

    try:

        async with httpx.AsyncClient(
            timeout=8
        ) as client:

            response = await client.post(

                SAFE_BROWSING_URL,

                params={
                    "key": api_key
                },

                json=body,

            )

            return response.json()

    except Exception:

        return None


async def check_url(
    url: str
) -> URLCheckResult:

    reasons = []

    is_safe = True

    threat_type = "none"

    confidence = 0.90

    domain = extract_domain(
        url
    )

    #
    # Google Safe Browsing
    #

    result = await google_safe_browsing_check(
        url
    )

    if result:

        matches = result.get(
            "matches",
            []
        )

        if matches:

            is_safe = False

            confidence = 1.0

            threat_type = matches[0].get(
                "threatType",
                "UNKNOWN"
            )

            reasons.append(
                "🔴 Google Safe Browsing flagged this URL"
            )

    #
    # Heuristic A
    # Raw IP
    #

    if re.match(

        r"https?://\d+\.\d+\.\d+\.\d+",

        url,

        re.IGNORECASE,

    ):

        is_safe = False

        reasons.append(

            "⚠️ URL uses raw IP address instead of domain"

        )

    #
    # Heuristic B
    # Suspicious TLD
    #

    for tld in SUSPICIOUS_TLDS:

        if domain.endswith(tld):

            is_safe = False

            reasons.append(

                f"⚠️ Suspicious top-level domain: {tld}"

            )

            break

    #
    # Heuristic C
    # URL Shortener
    #

    if domain in URL_SHORTENERS:

        confidence = min(
            confidence,
            0.50
        )

        reasons.append(

            "ℹ️ URL is shortened — destination unknown"

        )

    #
    # Heuristic D
    # Brand Impersonation
    #

    for brand in BRAND_NAMES:

        if brand in domain:

            valid = (

                domain == f"{brand}.com"

                or

                domain == f"www.{brand}.com"

                or

                domain == f"{brand}.in"

                or

                domain == f"www.{brand}.in"

            )

            if not valid:

                is_safe = False

                reasons.append(

                    f"🔴 Domain impersonates known brand: {brand}"

                )

                break

    #
    # Heuristic E
    # Too many subdomains
    #

    if domain.count(".") > 3:

        confidence -= 0.20

        reasons.append(

            "⚠️ Unusual number of subdomains"

        )

    #
    # Heuristic F
    # HTTP
    #

    if url.lower().startswith(
        "http://"
    ):

        confidence -= 0.15

        reasons.append(

            "ℹ️ URL uses unencrypted HTTP"

        )

    confidence = max(
        confidence,
        0.10
    )

    if not reasons:

        reasons.append(

            "✅ No threats detected"

        )

    return URLCheckResult(

        url=url,

        is_safe=is_safe,

        threat_type=threat_type,

        confidence=round(
            confidence,
            2
        ),

        reasons=reasons,

    )