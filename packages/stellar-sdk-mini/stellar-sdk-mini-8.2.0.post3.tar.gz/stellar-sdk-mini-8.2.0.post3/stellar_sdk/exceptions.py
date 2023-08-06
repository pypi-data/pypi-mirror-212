__all__ = [
    "SdkError",
    "ValueError",
    "TypeError",
    "AttributeError",
    "BadSignatureError",
    "Ed25519PublicKeyInvalidError",
    "Ed25519SecretSeedInvalidError",
    "MissingEd25519SecretSeedError",
    "MuxedEd25519AccountInvalidError",
    "MemoInvalidException",
    "AssetCodeInvalidError",
    "AssetIssuerInvalidError",
    "NoApproximationError",
    "SignatureExistError",
    "FeatureNotEnabledError",
]


# The following is kept for compatibility
ValueError = ValueError
TypeError = TypeError
AttributeError = AttributeError


class SdkError(Exception):
    """Base exception for all stellar sdk related errors"""


class BadSignatureError(SdkError, ValueError):
    """Raised when the signature was forged or otherwise corrupt."""


class Ed25519PublicKeyInvalidError(SdkError, ValueError):
    """Ed25519 public key is incorrect."""


class Ed25519SecretSeedInvalidError(SdkError, ValueError):
    """Ed25519 secret seed is incorrect."""


class MissingEd25519SecretSeedError(SdkError, ValueError):
    """Missing Ed25519 secret seed in the keypair"""


class MuxedEd25519AccountInvalidError(SdkError, ValueError):
    """Muxed Ed25519 public key is incorrect."""


class MemoInvalidException(SdkError, ValueError):
    """Memo is incorrect."""


class AssetCodeInvalidError(SdkError, ValueError):
    """Asset Code is incorrect."""


class AssetIssuerInvalidError(SdkError, ValueError):
    """Asset issuer is incorrect."""


class NoApproximationError(SdkError):
    """Approximation cannot be found"""


class SignatureExistError(SdkError, ValueError):
    """A keypair can only sign a transaction once."""

class FeatureNotEnabledError(SdkError):
    """The feature is not enabled."""
