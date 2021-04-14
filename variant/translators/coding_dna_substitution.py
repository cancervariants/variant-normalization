"""Module for DNA Coding Substitution Translation."""
from .dna_sequence_variant_base import DNASequenceVariantBase
from variant.schemas.classification_response_schema import ClassificationType
from variant.schemas.token_response_schema import CodingDNASubstitutionToken


class CodingDNASubstitution(DNASequenceVariantBase):
    """The Coding DNA Substitution Translator class."""

    def can_translate(self, type: ClassificationType) -> bool:
        """Return if classification type is Amino Acid Substitution."""
        return type == ClassificationType.DNA_CODING_SUBSTITUTION

    def is_token_instance(self, token):
        """Return if the token is an Coding DNA Substitution token instance."""
        return isinstance(token, CodingDNASubstitutionToken)