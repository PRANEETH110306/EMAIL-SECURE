from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Priority(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Category:
    id: str
    name: str
    color: str
    text_color: str
    priority: Priority
    keywords: List[str] = field(default_factory=list)
    sender_patterns: List[str] = field(default_factory=list)
    subject_patterns: List[str] = field(default_factory=list)


CATEGORIES = [

    Category(
        id="critical_security",
        name="Critical Security Alert",
        color="#8B0000",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL,
        keywords=[
            "account compromised",
            "unauthorized access",
            "suspicious login",
            "unusual activity"
        ],
        subject_patterns=[
            "security alert",
            "account locked",
            "unauthorized",
            "verify now"
        ]
    ),

    Category(
        id="scam_phishing",
        name="Scam/Phishing",
        color="#CC0000",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL,
        keywords=[
            "click here to verify",
            "you have won",
            "lottery",
            "wire transfer",
            "bitcoin",
            "claim your prize"
        ],
        subject_patterns=[
            "urgent",
            "verify account",
            "winner",
            "claim"
        ]
    ),

    Category(
        id="malware_attachment",
        name="Malware/Attachment Threat",
        color="#4A0018",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL,
        keywords=[
            "enable macros",
            "open attachment"
        ],
        subject_patterns=[
            "invoice",
            "shared file"
        ]
    ),

    Category(
        id="financial_fraud",
        name="Financial Fraud",
        color="#DC143C",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL,
        keywords=[
            "fake invoice",
            "wire transfer required",
            "overdue payment",
            "final notice"
        ],
        subject_patterns=[
            "payment failed",
            "overdue",
            "final notice"
        ]
    ),

    Category(
        id="domain_impersonation",
        name="Domain Impersonation",
        color="#8B0000",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL,
        sender_patterns=[
            "microsoft-support",
            "paypal-secure",
            "amazon-verify",
            "-support.xyz",
            "-secure.net"
        ]
    ),

    Category(
        id="data_leak",
        name="Data Leak Alert",
        color="#880000",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL,
        keywords=[
            "data breach",
            "your data was exposed",
            "breach notification"
        ],
        subject_patterns=[
            "data breach",
            "security incident"
        ]
    ),

    Category(
        id="blacklisted",
        name="Blacklisted Sender",
        color="#111111",
        text_color="#FFFFFF",
        priority=Priority.CRITICAL
    ),

    Category(
        id="suspicious_sender",
        name="Suspicious Sender",
        color="#FF4500",
        text_color="#FFFFFF",
        priority=Priority.WARNING,
        sender_patterns=[
            "suspicious",
            "mailer-daemon"
        ]
    ),

    Category(
        id="unknown_sender",
        name="Unknown Sender",
        color="#444444",
        text_color="#FFFFFF",
        priority=Priority.WARNING
    ),

    Category(
        id="otp_verification",
        name="OTP/Verification",
        color="#00BCD4",
        text_color="#000000",
        priority=Priority.VERY_HIGH,
        keywords=[
            "otp",
            "one time password",
            "verification code",
            "login code",
            "2fa",
            "mfa",
            "your code is"
        ],
        subject_patterns=[
            "otp",
            "verification code",
            "login code"
        ]
    ),

    Category(
        id="password_reset",
        name="Password Reset",
        color="#87CEEB",
        text_color="#000000",
        priority=Priority.VERY_HIGH,
        keywords=[
            "reset your password",
            "forgot password",
            "account recovery",
            "reset link"
        ],
        subject_patterns=[
            "password reset",
            "forgot password"
        ]
    ),

    Category(
        id="government",
        name="Government",
        color="#4CAF50",
        text_color="#000000",
        priority=Priority.HIGH,
        keywords=[
            "aadhaar",
            "uidai",
            "income tax",
            "itr",
            "passport",
            "election commission",
            "pan card",
            "epfo"
        ],
        sender_patterns=[
            "gov.in",
            "uidai.gov",
            "incometax.gov"
        ]
    ),

    Category(
        id="banking",
        name="Banking",
        color="#2E7D32",
        text_color="#FFFFFF",
        priority=Priority.HIGH,
        keywords=[
            "account statement",
            "transaction alert",
            "credited",
            "debited",
            "netbanking",
            "upi",
            "neft"
        ],
        sender_patterns=[
            "sbi.co.in",
            "hdfcbank.com",
            "icicibank.com",
            "axisbank.com",
            "paypal.com"
        ]
    ),

    Category(
        id="tax_legal",
        name="Tax & Legal",
        color="#50C878",
        text_color="#000000",
        priority=Priority.HIGH,
        keywords=[
            "gst",
            "tax notice",
            "court order",
            "legal notice",
            "compliance",
            "penalty"
        ],
        subject_patterns=[
            "tax notice",
            "legal notice",
            "penalty"
        ]
    ),

    Category(
        id="healthcare",
        name="Healthcare",
        color="#008080",
        text_color="#FFFFFF",
        priority=Priority.HIGH,
        keywords=[
            "medical report",
            "test results",
            "appointment",
            "prescription",
            "insurance claim",
            "lab report"
        ],
        sender_patterns=[
            "apollo",
            "fortis",
            "manipal"
        ]
    ),

    Category(
        id="interview",
        name="Interview Invitation",
        color="#FFD700",
        text_color="#000000",
        priority=Priority.HIGH,
        keywords=[
            "interview scheduled",
            "interview invitation",
            "assessment round",
            "hr round",
            "interview link"
        ],
        subject_patterns=[
            "interview",
            "assessment",
            "hr round"
        ]
    ),

        Category(
        id="offer_letter",
        name="Offer Letter",
        color="#FFC200",
        text_color="#000000",
        priority=Priority.HIGH,
        keywords=[
            "offer letter",
            "job offer",
            "pleased to offer",
            "joining date",
            "stipend",
            "ctc"
        ],
        subject_patterns=[
            "offer letter",
            "job offer"
        ]
    ),

    Category(
        id="personal_direct",
        name="Direct Personal Mail",
        color="#FFD700",
        text_color="#000000",
        priority=Priority.HIGH
    ),

    Category(
        id="family_friends",
        name="Family & Friends",
        color="#DAA520",
        text_color="#000000",
        priority=Priority.HIGH
    ),

    Category(
        id="client_communication",
        name="Client Communication",
        color="#4169E1",
        text_color="#FFFFFF",
        priority=Priority.HIGH,
        keywords=[
            "project update",
            "deliverable",
            "milestone",
            "contract",
            "proposal",
            "quotation"
        ],
        subject_patterns=[
            "project",
            "proposal",
            "contract"
        ]
    ),

    Category(
        id="job_application",
        name="Job Application",
        color="#FFA500",
        text_color="#000000",
        priority=Priority.MEDIUM,
        keywords=[
            "application received",
            "thank you for applying",
            "your application",
            "application submitted"
        ],
        subject_patterns=[
            "application received",
            "your application"
        ]
    ),

    Category(
        id="educational",
        name="Educational",
        color="#ADD8E6",
        text_color="#000000",
        priority=Priority.MEDIUM,
        keywords=[
            "course enrollment",
            "certificate",
            "assignment due",
            "coursera",
            "udemy",
            "edx",
            "semester"
        ],
        sender_patterns=[
            "coursera.org",
            "udemy.com",
            "edx.org",
            "ibm.com"
        ]
    ),

    Category(
        id="company_comms",
        name="Company Communication",
        color="#1E90FF",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "product update",
            "new feature",
            "terms of service",
            "privacy policy",
            "service update"
        ],
        sender_patterns=[
            "google.com",
            "microsoft.com",
            "linkedin.com",
            "github.com",
            "apple.com"
        ]
    ),

    Category(
        id="work_email",
        name="Work Email",
        color="#000080",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "standup",
            "sprint",
            "pull request",
            "code review",
            "meeting notes",
            "action items",
            "deadline"
        ],
        subject_patterns=[
            "standup",
            "sprint",
            "meeting",
            "deadline"
        ]
    ),

    Category(
        id="social_media",
        name="Social Media",
        color="#800080",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "liked your post",
            "new follower",
            "friend request",
            "tagged you",
            "mentioned you"
        ],
        sender_patterns=[
            "facebookmail.com",
            "instagram.com",
            "twitter.com",
            "reddit.com",
            "linkedin.com"
        ]
    ),

    Category(
        id="shopping",
        name="Shopping",
        color="#A0522D",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "your order",
            "wish list",
            "cart",
            "deal of the day",
            "back in stock"
        ],
        sender_patterns=[
            "amazon.in",
            "flipkart.com",
            "myntra.com",
            "meesho.com"
        ]
    ),

    Category(
        id="order_confirmation",
        name="Order Confirmation",
        color="#A0522D",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "order confirmed",
            "order placed",
            "thank you for your order",
            "order id"
        ],
        subject_patterns=[
            "order confirmed",
            "order placed",
            "your order"
        ]
    ),

    Category(
        id="shipping_delivery",
        name="Shipping & Delivery",
        color="#7B3F00",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "shipped",
            "out for delivery",
            "delivered",
            "tracking",
            "estimated delivery",
            "courier"
        ],
        subject_patterns=[
            "shipped",
            "out for delivery",
            "tracking",
            "delivered"
        ]
    ),

        Category(
        id="event_invitation",
        name="Event Invitation",
        color="#FF69B4",
        text_color="#000000",
        priority=Priority.MEDIUM,
        keywords=[
            "you are invited",
            "webinar",
            "conference",
            "workshop",
            "seminar",
            "register now",
            "rsvp"
        ],
        subject_patterns=[
            "invitation",
            "invite",
            "webinar",
            "workshop",
            "rsvp"
        ]
    ),

    Category(
        id="calendar_event",
        name="Calendar Event",
        color="#FF00FF",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "meeting invite",
            "calendar invite",
            "scheduled",
            "google meet",
            "zoom meeting",
            "teams meeting"
        ],
        subject_patterns=[
            "meeting",
            "calendar invite",
            "appointment"
        ]
    ),

    Category(
        id="travel",
        name="Travel",
        color="#40E0D0",
        text_color="#000000",
        priority=Priority.MEDIUM,
        keywords=[
            "booking confirmation",
            "flight",
            "train",
            "hotel",
            "check-in",
            "pnr",
            "itinerary",
            "ticket"
        ],
        sender_patterns=[
            "makemytrip.com",
            "goibibo.com",
            "irctc.co.in",
            "indigo.in",
            "airbnb.com",
            "booking.com"
        ]
    ),

    Category(
        id="utility_bills",
        name="Utility Bills",
        color="#808000",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "bill generated",
            "bill due",
            "pay now",
            "electricity bill",
            "water bill",
            "broadband bill"
        ],
        subject_patterns=[
            "bill",
            "due",
            "payment due",
            "electricity"
        ]
    ),

    Category(
        id="payment_receipt",
        name="Payment Receipt",
        color="#98FF98",
        text_color="#000000",
        priority=Priority.MEDIUM,
        keywords=[
            "payment successful",
            "amount debited",
            "amount credited",
            "upi payment",
            "transaction successful"
        ],
        subject_patterns=[
            "payment successful",
            "payment receipt",
            "transaction"
        ]
    ),

    Category(
        id="invoice",
        name="Invoice",
        color="#008B8B",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "invoice",
            "bill to",
            "amount due",
            "tax invoice",
            "billing statement"
        ],
        subject_patterns=[
            "invoice",
            "bill",
            "amount due"
        ]
    ),

    Category(
        id="finance_reports",
        name="Finance Reports",
        color="#228B22",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "account statement",
            "portfolio update",
            "mutual fund",
            "demat",
            "trading",
            "nse",
            "bse"
        ],
        sender_patterns=[
            "zerodha.com",
            "groww.in",
            "motilaloswal.com"
        ]
    ),

    Category(
        id="security_newsletter",
        name="Security Newsletter",
        color="#4682B4",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "cve",
            "vulnerability",
            "patch",
            "security advisory",
            "threat intelligence",
            "cert"
        ],
        sender_patterns=[
            "cert-in.org.in",
            "cisa.gov",
            "us-cert.gov"
        ]
    ),

    Category(
        id="github_notifications",
        name="GitHub Notifications",
        color="#4B0082",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "pull request",
            "merged",
            "opened issue",
            "closed issue",
            "review requested",
            "workflow run"
        ],
        sender_patterns=[
            "github.com",
            "notifications@github.com"
        ]
    ),

    Category(
        id="dev_tools",
        name="Development Tools",
        color="#310062",
        text_color="#FFFFFF",
        priority=Priority.MEDIUM,
        keywords=[
            "build failed",
            "build succeeded",
            "pipeline",
            "deployment",
            "jira issue",
            "sprint completed",
            "docker image"
        ],
        sender_patterns=[
            "atlassian.com",
            "jenkins.io",
            "hub.docker.com",
            "circleci.com",
            "gitlab.com"
        ]
    ),

    Category(
        id="subscription",
        name="Subscription",
        color="#EE82EE",
        text_color="#000000",
        priority=Priority.LOW,
        keywords=[
            "unsubscribe",
            "newsletter",
            "digest",
            "weekly roundup",
            "manage subscription"
        ],
        subject_patterns=[
            "newsletter",
            "digest",
            "weekly",
            "unsubscribe"
        ]
    ),

    Category(
        id="product_updates",
        name="Product Updates",
        color="#8F00FF",
        text_color="#FFFFFF",
        priority=Priority.LOW,
        keywords=[
            "new feature",
            "product update",
            "changelog",
            "release notes",
            "what's new"
        ],
        subject_patterns=[
            "what's new",
            "product update",
            "changelog",
            "release"
        ]
    ),

    Category(
        id="marketing",
        name="Marketing",
        color="#FF8C00",
        text_color="#FFFFFF",
        priority=Priority.LOW,
        keywords=[
            "exclusive offer",
            "limited time",
            "sale",
            "discount",
            "flash sale"
        ],
        subject_patterns=[
            "sale",
            "offer",
            "discount",
            "exclusive",
            "limited time"
        ]
    ),

    Category(
        id="advertisements",
        name="Advertisements",
        color="#FF6600",
        text_color="#FFFFFF",
        priority=Priority.LOW,
        keywords=[
            "sponsored",
            "promo code",
            "coupon",
            "deal"
        ],
        subject_patterns=[
            "sponsored",
            "promo code",
            "coupon"
        ]
    ),

    Category(
        id="academic_research",
        name="Academic Research",
        color="#96DED1",
        text_color="#000000",
        priority=Priority.LOW,
        keywords=[
            "research paper",
            "journal",
            "publication",
            "peer review",
            "arxiv",
            "doi"
        ],
        sender_patterns=[
            "arxiv.org",
            "researchgate.net",
            "ieee.org",
            "acm.org"
        ]
    ),

    Category(
        id="community_forums",
        name="Community Forums",
        color="#B57BEC",
        text_color="#000000",
        priority=Priority.LOW,
        keywords=[
            "answered your question",
            "reply to your post",
            "mentioned in",
            "new post in"
        ],
        sender_patterns=[
            "stackoverflow.com",
            "discord.com",
            "reddit.com",
            "quora.com"
        ]
    ),

    Category(
        id="surveys",
        name="Surveys",
        color="#FFDAB9",
        text_color="#000000",
        priority=Priority.LOW,
        keywords=[
            "take our survey",
            "feedback",
            "rate your experience",
            "questionnaire"
        ],
        subject_patterns=[
            "survey",
            "feedback",
            "questionnaire",
            "your opinion"
        ]
    ),

    Category(
        id="promotions",
        name="Promotions",
        color="#FF4500",
        text_color="#FFFFFF",
        priority=Priority.LOW,
        keywords=[
            "coupon",
            "cashback",
            "redeem",
            "voucher",
            "promo"
        ],
        subject_patterns=[
            "cashback",
            "coupon",
            "voucher",
            "redeem"
        ]
    ),

    Category(
        id="bulk_mail",
        name="Bulk Mail",
        color="#D3D3D3",
        text_color="#000000",
        priority=Priority.LOW,
        keywords=[
            "bulk mail",
            "list-unsubscribe"
        ]
    ),

    Category(
        id="auto_generated",
        name="Auto Generated",
        color="#888888",
        text_color="#FFFFFF",
        priority=Priority.LOW,
        keywords=[
            "do not reply",
            "this is an automated message"
        ],
        sender_patterns=[
            "noreply@",
            "no-reply@",
            "donotreply@",
            "notifications@"
        ]
    ),

    Category(
        id="read_later",
        name="Read Later",
        color="#C0C0C0",
        text_color="#000000",
        priority=Priority.LOW,
        keywords=[
            "weekly digest",
            "monthly report",
            "annual report"
        ],
        subject_patterns=[
            "digest",
            "monthly report",
            "weekly wrap"
        ]
    )

]

CATEGORY_MAP = {
    category.id: category
    for category in CATEGORIES
}