import re


class VerificationError(Exception):
    pass


class SimpleVerifier:
    def __init__(self, prohibited=None):
        prohibited = prohibited or []
        self.prohibited = [str(p).strip().lower() for p in prohibited if str(p).strip()]

    def allow(self, response_text: str) -> bool:
        text = (response_text or "").lower()
        for w in self.prohibited:
            if re.search(rf"\b{re.escape(w)}\b", text):
                return False
        return True

    def verify_or_raise(self, response_text: str) -> None:
        if not self.allow(response_text):
            raise VerificationError("prohibited content detected")
