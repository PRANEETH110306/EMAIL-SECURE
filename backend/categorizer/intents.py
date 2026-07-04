from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Intent:

    name: str

    keywords: List[str]


INTENTS = [

    # ---------------- SECURITY ----------------

    Intent(
        "Password Change",
        [
            "password changed",
            "password reset",
            "reset password",
            "forgot password",
            "change password"
        ]
    ),

    Intent(
        "Security Alert",
        [
            "security alert",
            "suspicious login",
            "unauthorized access",
            "account locked",
            "new login",
            "login detected",
            "verify login"
        ]
    ),

    Intent(
        "OTP",
        [
            "otp",
            "verification code",
            "login code",
            "authentication code",
            "one time password",
            "2fa",
            "mfa"
        ]
    ),

    Intent(
        "Email Verification",
        [
            "verify email",
            "confirm your email",
            "verify your account"
        ]
    ),

    # ---------------- GOOGLE ----------------

    Intent(
        "Terms Update",
        [
            "terms of service",
            "privacy policy",
            "terms update",
            "updated terms",
            "updated privacy"
        ]
    ),

    Intent(
        "Storage Alert",
        [
            "storage full",
            "google one",
            "drive storage",
            "icloud storage"
        ]
    ),

    # ---------------- BANKING ----------------

    Intent(
        "Statement",
        [
            "account statement",
            "monthly statement",
            "statement available"
        ]
    ),

    Intent(
        "Transaction Alert",
        [
            "credited",
            "debited",
            "transaction",
            "upi",
            "neft",
            "imps",
            "rtgs"
        ]
    ),

    Intent(
        "Payment Receipt",
        [
            "payment successful",
            "receipt",
            "payment received"
        ]
    ),

    # ---------------- SHOPPING ----------------

    Intent(
        "Order Confirmation",
        [
            "order confirmed",
            "order placed",
            "thank you for your order"
        ]
    ),

    Intent(
        "Delivery Update",
        [
            "out for delivery",
            "tracking",
            "shipment",
            "delivered",
            "shipped"
        ]
    ),

    Intent(
        "Refund",
        [
            "refund",
            "refund processed",
            "refund initiated"
        ]
    ),

    # ---------------- LINKEDIN ----------------

    Intent(
        "Job Alert",
        [
            "jobs for you",
            "recommended jobs",
            "job matches",
            "new opportunities",
            "hiring"
        ]
    ),

    Intent(
        "Connection Request",
        [
            "wants to connect",
            "connection request",
            "invited you to connect"
        ]
    ),

    Intent(
        "Profile View",
        [
            "viewed your profile",
            "profile views"
        ]
    ),

    Intent(
        "Message",
        [
            "sent you a message",
            "new message"
        ]
    ),

    # ---------------- GITHUB ----------------

    Intent(
        "Pull Request",
        [
            "pull request",
            "merged",
            "review requested"
        ]
    ),

    Intent(
        "Issue",
        [
            "opened issue",
            "closed issue",
            "issue assigned"
        ]
    ),

    Intent(
        "Workflow",
        [
            "workflow",
            "build failed",
            "build succeeded",
            "deployment"
        ]
    ),

    # ---------------- CALENDAR ----------------

    Intent(
        "Meeting",
        [
            "meeting",
            "calendar invite",
            "google meet",
            "teams meeting",
            "zoom"
        ]
    ),

    # ---------------- TRAVEL ----------------

    Intent(
        "Booking Confirmation",
        [
            "booking confirmed",
            "booking confirmation",
            "pnr"
        ]
    ),

    Intent(
        "Boarding Pass",
        [
            "boarding pass",
            "check in",
            "web check in"
        ]
    ),

    # ---------------- EDUCATION ----------------

    Intent(
        "Assignment",
        [
            "assignment",
            "due date",
            "submit"
        ]
    ),

    Intent(
        "Certificate",
        [
            "certificate",
            "course completed"
        ]
    ),

    # ---------------- DEFAULT ----------------

    Intent(
        "General",
        []
    )
]

import re

STOP_WORDS = {
    "the", "a", "an", "to", "for", "of", "and",
    "your", "you", "is", "are", "on", "in",
    "with", "from", "this", "that", "our",
    "please", "re", "fw", "fwd"
}

def summarize_subject(subject: str) -> str:

    if not subject:
        return "Notification"

    words = re.findall(
        r"[A-Za-z0-9]+",
        subject
    )

    cleaned = []

    for word in words:

        word = word.strip()

        if len(word) < 3:
            continue

        if word.lower() in STOP_WORDS:
            continue

        cleaned.append(word)

    if not cleaned:
        return "Notification"

    #
    # First meaningful word
    #

    if len(cleaned) == 1:

        return cleaned[0].title()

    #
    # First two meaningful words
    #

    return (
        cleaned[0].title()
        + " "
        + cleaned[1].title()
    )


def detect_intent(
    subject: str,
    body: str
) -> str:

    text = (
        subject +
        " " +
        body
    ).lower()

    best_match = None

    best_score = 0

    for intent in INTENTS:

        score = 0

        for keyword in intent.keywords:

            if keyword in text:
                score += 1

        if score > best_score:

            best_score = score

            best_match = intent.name

    #
    # Known intent
    #

    if best_match:

        return best_match

    #
    # Unknown
    #

    return summarize_subject(
        subject
    )