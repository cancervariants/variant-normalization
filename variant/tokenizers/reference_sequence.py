"""A module for Reference Sequence Tokenization."""
from typing import Optional
from .tokenizer import Tokenizer
from variant.schemas.token_response_schema import Token, TokenMatchType

REFSEQ_PREFIXES = ["NC_", "NT_", "NW_", "NG_", "NM_", "NR_", "NP_", "LRG_",
                   "ENSP", "ENST"]


class ReferenceSequence(Tokenizer):
    """Class for Reference Sequence."""

    def match(self, input_string: str) -> Optional[Token]:
        """Return a Reference Sequence match if it exists.

        :param str input_string: The input string to match
        """
        if input_string[:3].upper() in REFSEQ_PREFIXES:
            return Token(
                token=input_string,
                token_type='ReferenceSequence',
                input_string=input_string,
                match_type=TokenMatchType.UNSPECIFIED
            )
        return None
