"""A module for Protein Substitution Tokenization."""
import re
from typing import Optional
from .caches import AminoAcidCache
from .tokenizer import Tokenizer
from variant.schemas.token_response_schema import ProteinSubstitutionToken,\
    TokenMatchType


class ProteinSubstitution(Tokenizer):
    """Class for tokenizing Protein Substitution."""

    def __init__(self, amino_acid_cache: AminoAcidCache) -> None:
        """Initialize the Protein Substitution Class.

        :param AminoAcidCache amino_acid_cache: Valid amino acid codes.
        """
        self.amino_acid_cache = amino_acid_cache
        self.splitter = re.compile(r'(\d+)')
        self.psub = None

    def match(self, input_string) -> Optional[ProteinSubstitutionToken]:
        """Return a ProteinSubstitutionToken match if one exists.

        :param str input_string: The input string to match
        :return: A ProteinSubstitutionToken if a match exists. Otherwise, None.
        """
        input_string = str(input_string)

        self.psub = {
            'amino_acid': None,
            'position': None,
            'new_amino_acid': None
        }

        if input_string is None:
            return None

        if '.' in input_string:
            if not input_string.startswith('p.'):
                return None
            p_count = input_string.count('p.')
            if p_count == 1:
                psub_parts = self.splitter.split(input_string)
            elif p_count == 2:
                psub_parts = input_string.split()
        else:
            psub_parts = self.splitter.split(input_string)

        self._get_psub(psub_parts)
        ret_psub = False

        if all(self.psub.values()):
            if '^' in self.psub['new_amino_acid']:
                # uncertain
                amino_acids = set(self.psub['new_amino_acid'].split('^'))
            else:
                # missense
                amino_acids = {self.psub['amino_acid'],
                               self.psub['new_amino_acid']}

            # nonsense, silent, unknown
            amino_acids = amino_acids - {'Ter', '=', '?'}

            if not self._is_valid_amino_acid(amino_acids=amino_acids):
                return None

            ret_psub = True
        else:
            # Translation initiation codon: no protein
            if self.psub['amino_acid'] == '' and self.psub['position'] == 0 \
                    and self.psub['new_amino_acid'] == '':
                ret_psub = True
            # splicing
            elif not self.psub['amino_acid'] and not self.psub['position'] \
                    and self.psub['new_amino_acid'] == '?':
                ret_psub = True
        if ret_psub:
            return ProteinSubstitutionToken(
                token=input_string,
                input_string=input_string,
                match_type=TokenMatchType.UNSPECIFIED.value,
                ref_protein=self.psub['amino_acid'],
                alt_protein=self.psub['new_amino_acid'],
                position=self.psub['position']
            )

        return None

    def _get_psub(self, psub_parts):
        """Return Protein Substitution tokens.

        :param list psub_parts: The split input string
        """
        psub_parts_len = len(psub_parts)
        if psub_parts_len == 3:
            if 'p.' in psub_parts[0]:
                psub_parts[0] = psub_parts[0].split('p.')[-1]
            else:
                if not psub_parts[0] and psub_parts[1] and not psub_parts[2]:
                    return

            if '(' in psub_parts[0] and ')' in psub_parts[2]:
                psub_parts[0] = psub_parts[0].split('(')[-1]
                psub_parts[2] = psub_parts[2].split(')')[0]

            self._set_psub(psub_parts[0], psub_parts[1], psub_parts[2])

            if '=/' in self.psub['new_amino_acid']:
                # mosaic
                self.psub['new_amino_acid'] = \
                    self.psub['new_amino_acid'].split('=/')[-1]
        elif psub_parts_len == 2:
            psub_parts[0] = psub_parts[0].split(':')[-1]
            if 'Ter' in psub_parts[0]:
                check_nonsense = f"({psub_parts[0].replace('Ter', '*')})"
                if check_nonsense == psub_parts[1]:
                    psub_parts = \
                        self.splitter.split(psub_parts[0].split('p.')[-1])
                    self._get_psub(psub_parts)
        elif psub_parts_len == 1:
            if 'p.' in psub_parts[0]:
                psub_parts[0] = psub_parts[0].split('p.')[1]
                if psub_parts[0] == '?':
                    self.psub['new_amino_acid'] = psub_parts[0]

    def _set_psub(self, amino_acid, position, new_amino_acid):
        """Initialize protein substitution.

        :param str amino_acid: Reference amino acid
        :param str position: The position of the amino acid substituted
        :param str new_amino_acid: The new amino_acid
        """
        self.psub['amino_acid'] = amino_acid
        self.psub['position'] = int(position)
        self.psub['new_amino_acid'] = new_amino_acid

    def _is_valid_amino_acid(self, **kwargs):
        """Return whether or not amino acids are valid."""
        if 'amino_acids' in kwargs:
            for amino_acid in kwargs['amino_acids']:
                if amino_acid not in self.amino_acid_cache:
                    return False
            return True
        else:
            raise KeyError("amino_acids not found in kwargs.")