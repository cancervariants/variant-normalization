"""Module for Genomic DelIns Translation."""
from variant.translators.translator import Translator
from variant.schemas.classification_response_schema import ClassificationType
from variant.schemas.token_response_schema import GenomicDelInsToken


class GenomicDelIns(Translator):
    """The Genomic Substitution Translator class."""

    def can_translate(self, type: ClassificationType) -> bool:
        """Return if classification type is Genomic DelIns."""
        return type == ClassificationType.GENOMIC_DELINS

    def is_token_instance(self, token):
        """Return if the token is an Genomic DelIns token instance."""
        return isinstance(token, GenomicDelInsToken)
