from dataclasses import dataclass
from typing import List, Optional

from .brands import resolve_brand
from .intents import detect_intent

from .categories import (
    CATEGORY_MAP,
    CATEGORIES,
    Category,
    Priority,
)

# ============================================================
# Priority Order
# Lower value = Higher priority
# ============================================================

PRIORITY_ORDER = {
    Priority.CRITICAL: 0,
    Priority.WARNING: 1,
    Priority.VERY_HIGH: 2,
    Priority.HIGH: 3,
    Priority.MEDIUM: 4,
    Priority.LOW: 5,
}

# ============================================================
# Match Result
# ============================================================


@dataclass
class CategoryMatch:
    category: Category
    confidence: float
    matched_keywords: List[str]
    matched_sender: bool
    matched_subject: bool


# ============================================================
# Final Classification Result
# ============================================================


@dataclass
class ClassificationResult:

    # Company / Organisation
    brand: str

    # Purpose of email
    intent: str

    # Primary category
    primary: CategoryMatch

    # Top 5 category matches
    all_matches: List[CategoryMatch]

    # SAFE / HIGH / CRITICAL
    risk_label: str

    # Current category matching score (0-100)
    # NOTE:
    # This is NOT the trust score.
    # Trust score will be implemented later using
    # SPF, DKIM, DMARC, reputation, URLs, etc.
    category_score: int


# ============================================================
# Email Classifier
# ============================================================


class EmailClassifier:

    DANGEROUS_ATTACHMENTS = {
        "exe",
        "zip",
        "rar",
        "js",
        "vbs",
        "bat",
        "cmd",
        "msi",
    }

        # ============================================================
    # Pattern Matching
    # ============================================================

    def _contains_pattern(
        self,
        text: str,
        patterns: List[str]
    ) -> bool:

        if not text:
            return False

        text = text.lower()

        for pattern in patterns:

            if pattern.lower() in text:
                return True

        return False

    # ============================================================
    # Keyword Matching
    # ============================================================

    def _match_keywords(
        self,
        content: str,
        keywords: List[str]
    ) -> List[str]:

        matched = []

        if not content:
            return matched

        content = content.lower()

        for keyword in keywords:

            if keyword.lower() in content:
                matched.append(keyword)

        return matched

    # ============================================================
    # Risk Label
    # ============================================================

    def _risk_label(
        self,
        priority: Priority
    ) -> str:

        if priority in (
            Priority.CRITICAL,
            Priority.WARNING,
        ):
            return "CRITICAL"

        if priority == Priority.VERY_HIGH:
            return "HIGH"

        return "SAFE"

    # ============================================================
    # Category Score
    #
    # NOTE:
    # This is NOT Trust Score.
    # It only represents how strongly an email
    # matches a category.
    # ============================================================

    def calculate_category_score(
        self,
        match: CategoryMatch
    ) -> int:

        score = int(
            match.confidence * 100
        )

        # Minimum visible score
        if score < 60:
            score = 60

        # Cap at 99 until Trust Engine is added
        return min(score, 99)

    # ============================================================
    # Classify Email
    # ============================================================

    def classify(
        self,
        sender: str,
        subject: str,
        body: str,
        has_attachment: bool = False,
        attachment_ext: Optional[str] = None,
    ) -> ClassificationResult:
            # =====================================================
            # Normalize Input
            # =====================================================

            original_sender = sender or ""

            sender = original_sender.lower()

            subject = (subject or "").lower()

            body = (body or "").lower()

            searchable_text = f"{subject} {body}"

            # =====================================================
            # Brand Detection
            # =====================================================

            brand = resolve_brand(
                original_sender
            )

            # =====================================================
            # Intent Detection
            # =====================================================

            intent = detect_intent(
                subject,
                body
            )

            # =====================================================
            # Category Matching
            # =====================================================

            matches: List[CategoryMatch] = []

            for category in CATEGORIES:

                score = 0.0

                matched_keywords = []

                matched_sender = self._contains_pattern(
                    sender,
                    category.sender_patterns
                )

                matched_subject = self._contains_pattern(
                    subject,
                    category.subject_patterns
                )

                if matched_sender:
                    score += 0.4

                if matched_subject:
                    score += 0.3

                matched_keywords = self._match_keywords(
                    searchable_text,
                    category.keywords
                )

                keyword_score = min(
                    len(matched_keywords) * 0.1,
                    0.4
                )

                score += keyword_score

                score = min(score, 1.0)

                if score > 0:

                    matches.append(

                        CategoryMatch(

                            category=category,

                            confidence=round(
                                score,
                                2
                            ),

                            matched_keywords=matched_keywords,

                            matched_sender=matched_sender,

                            matched_subject=matched_subject

                        )

                    )

            # =====================================================
            # Dangerous Attachment Detection
            # =====================================================

            if has_attachment and attachment_ext:

                ext = attachment_ext.lower().replace(".", "")

                if ext in self.DANGEROUS_ATTACHMENTS:

                    malware_category = CATEGORY_MAP[
                        "malware_attachment"
                    ]

                    existing = next(

                        (

                            m

                            for m in matches

                            if m.category.id
                            == "malware_attachment"

                        ),

                        None

                    )

                    if existing:

                        existing.confidence = max(
                            existing.confidence,
                            0.85
                        )

                    else:

                        matches.append(

                            CategoryMatch(

                                category=malware_category,

                                confidence=0.85,

                                matched_keywords=[],

                                matched_sender=False,

                                matched_subject=False

                            )

                        )

            # =====================================================
            # No Match Found
            # =====================================================

            if not matches:

                fallback = CategoryMatch(

                    category=CATEGORY_MAP[
                        "unknown_sender"
                    ],

                    confidence=0.30,

                    matched_keywords=[],

                    matched_sender=False,

                    matched_subject=False

                )

                return ClassificationResult(

                    brand=brand,

                    intent=intent,

                    primary=fallback,

                    all_matches=[fallback],

                    risk_label=self._risk_label(
                        fallback.category.priority
                    ),

                    category_score=self.calculate_category_score(
                        fallback
                    )

                )
            
            # =====================================================
            # Sort Matches
            # =====================================================

            matches.sort(

                key=lambda m: (

                    PRIORITY_ORDER[
                        m.category.priority
                    ],

                    -m.confidence

                )

            )

            # =====================================================
            # Primary Match
            # =====================================================

            primary = matches[0]

            # =====================================================
            # Category Score
            #
            # NOTE:
            # This is NOT Trust Score.
            # Trust Score will be introduced later using:
            #   • SPF
            #   • DKIM
            #   • DMARC
            #   • Domain Reputation
            #   • URL Reputation
            #   • Attachment Analysis
            # =====================================================

            category_score = self.calculate_category_score(
                primary
            )

            # =====================================================
            # Final Result
            # =====================================================

            return ClassificationResult(

                brand=brand,

                intent=intent,

                primary=primary,

                all_matches=matches[:5],

                risk_label=self._risk_label(
                    primary.category.priority
                ),

                category_score=category_score

            )
            
    