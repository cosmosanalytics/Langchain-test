"""Demo data: past claim cases (to build the world model) and new cases (to score)."""

PAST_CASES = {
    "C1": "Ana filed a claim online with all documents attached, so it moved to review. "
          "The adjuster reviewed the claim and approved it because the policy was active and the documents were complete. "
          "The approved claim was paid 3 days later.",
    "C2": "Ben's claim was under review when the adjuster found the medical report was missing, so the claim was put on hold. "
          "After Ben uploaded the medical report, the claim went back to review and was approved.",
    "C3": "Carla's claim was reviewed and denied because the policy had lapsed before the incident date.",
    "C4": "Dev's claim for $80,000 was above the $50,000 limit for standard review, so the adjuster escalated it to a senior reviewer. "
          "The senior reviewer approved the claim.",
    "C5": "During review of Elena's claim, the invoice dates did not match the incident date, so the claim was sent to fraud check. "
          "The fraud check found the claim was valid and it was sent back to review.",
    "C6": "Farid's claim was approved and payment was sent within 5 days.",
}

# ground_truth=None means no labeled outcome exists: the case is scored on the world model alone.
NEW_CASES = [
    {"id": "N1", "current_state": "under_review", "ground_truth": "approved",
     "text": "Grace filed a $4,200 water damage claim. The policy is active, and the photos and repair invoice are attached."},
    {"id": "N2", "current_state": "under_review", "ground_truth": "on_hold",
     "text": "Hiro's claim is under review. His policy is active, but the police report has not been provided yet."},
    {"id": "N3", "current_state": "under_review", "ground_truth": None,
     "text": "Ivy's claim for $72,000 is under review. All documents are present and the policy is active."},
    {"id": "N4", "current_state": "under_review", "ground_truth": None,
     "text": "Jon's claim is under review. His policy expired two months before the accident."},
    {"id": "N5", "current_state": "under_review", "ground_truth": "fraud_check",
     "text": "Kim's claim is under review. The receipt shows a purchase date after the reported theft date."},
    {"id": "N6", "current_state": "approved", "ground_truth": None,
     "text": "Leo's claim was approved yesterday after review of complete documents."},
]
