"""Module for Token Schema."""
from pydantic import BaseModel
from typing import List, Union, Dict, Any, Type
from enum import IntEnum


class TokenMatchType(IntEnum):
    """Gene Token match types."""

    ID = 1
    SYMBOL = 2
    ALIAS = 3
    PREVIOUS = 4
    UNSPECIFIED = 5


class Token(BaseModel):
    """A string from a given query."""

    token: str
    token_type: str
    match_type: TokenMatchType
    input_string: str
    object_type = 'Token'

    class Config:
        """Configure model."""

        orm_mode = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type['Token']) -> None:
            """Configure OpenAPI schema."""
            if 'title' in schema.keys():
                schema.pop('title', None)
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
            schema['example'] = {
                "token": "",
                "token_type": "Unknown",
                "match_type": 5,
                "input_string": "foo",
                "object_type": "Token"
            }


class GeneMatchToken(Token):
    """Define model for gene symbol token."""

    matched_value: str
    token_type = 'GeneSymbol'

    class Config:
        """Configure model."""

        orm_mode = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type['GeneMatchToken']) -> None:
            """Configure OpenAPI schema."""
            if 'title' in schema.keys():
                schema.pop('title', None)
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
            schema['example'] = {
                "token": "BRAF",
                "token_type": "GeneSymbol",
                "match_type": 2,
                "input_string": "BRAF",
                "object_type": "Token",
                "matched_value": "BRAF"
            }


class GenePairMatchToken(Token):
    """Define model for gene pair token."""

    left_gene_token: GeneMatchToken
    right_gene_token: GeneMatchToken
    token_type = 'GenePair'

    class Config:
        """Configure model."""

        orm_mode = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type['GenePairMatchToken']) -> None:
            """Configure OpenAPI schema."""
            if 'title' in schema.keys():
                schema.pop('title', None)
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
            schema['example'] = {
                "token": "BRAF-ABL1",
                "token_type": "GenePair",
                "match_type": 5,
                "input_string": "braf-abl1",
                "object_type": "Token",
                "left_gene_token": {
                    "token": "BRAF",
                    "token_type": "GeneSymbol",
                    "match_type": 2,
                    "input_string": "BRAF",
                    "object_type": "Token",
                    "matched_value": "BRAF"
                },
                "right_gene_token": {
                    "token": "ABL1",
                    "token_type": "GeneSymbol",
                    "match_type": 2,
                    "input_string": "ABL1",
                    "object_type": "Token",
                    "matched_value": "ABL1"
                }
            }


class ProteinSubstitutionToken(Token):
    """Define model for Protein Substitution token."""

    # TODO: These might be optional in future
    ref_protein: str
    alt_protein: str
    position: int
    token_type = 'ProteinSubstitution'

    class Config:
        """Configure model."""

        orm_mode = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type['ProteinSubstitutionToken']) -> None:
            """Configure OpenAPI schema."""
            if 'title' in schema.keys():
                schema.pop('title', None)
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
            schema['example'] = {
                "token": "V600E",
                "token_type": "ProteinSubstitution",
                "match_type": 5,
                "input_string": "V600E",
                "object_type": "Token",
                "ref_protein": "V",
                "alt_protein": "E",
                "position": 600
            }


class TokenResponseSchema(BaseModel):
    """Define model for token response."""

    search_term: str
    tokens: List[Union[GeneMatchToken, GenePairMatchToken,
                       ProteinSubstitutionToken, Token]]

    class Config:
        """Configure model."""

        orm_mode = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type['TokenResponseSchema']) -> None:
            """Configure OpenAPI schema."""
            if 'title' in schema.keys():
                schema.pop('title', None)
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
            schema['example'] = {
                "search_term": "BRAF V600E",
                "tokens": [
                    {
                        "token": "BRAF",
                        "token_type": "GeneSymbol",
                        "match_type": 2,
                        "input_string": "BRAF",
                        "object_type": "Token",
                        "matched_value": "BRAF"
                    },
                    {
                        "token": "V600E",
                        "token_type": "ProteinSubstitution",
                        "match_type": 5,
                        "input_string": "V600E",
                        "object_type": "Token",
                        "ref_protein": "V",
                        "alt_protein": "E",
                        "position": 600
                    }
                ]
            }