"""Module for Genomic Silent Mutation Translation."""
from variant.translators.translator import Translator
from variant.schemas.classification_response_schema import ClassificationType
from variant.schemas.token_response_schema import GenomicSilentMutationToken


class GenomicSilentMutation(Translator):
    """The Genomic Silent Mutation Translator class."""

    def can_translate(self, type: ClassificationType) -> bool:
        """Return if classification type is Genomic Silent Mutation."""
        return type == ClassificationType.GENOMIC_SILENT_MUTATION

    def is_token_instance(self, token):
        """Return if the token is an Genomic Silent Mutation token
        instance.
        """
        return isinstance(token, GenomicSilentMutationToken)
