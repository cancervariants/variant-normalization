"""Module for Variant Normalization."""
from variant.schemas.token_response_schema import PolypeptideSequenceVariant
from variant.schemas.ga4gh_vod import Gene, VariationDescriptor, GeneDescriptor
from gene.query import Normalizer as GeneNormalizer


class Normalize:
    """The Normalize class used to normalize a given variant."""

    def __init__(self):
        """Initialize Normalize class."""
        self.gene_normalizer = GeneNormalizer()

    def normalize(self, q, validations, amino_acid_cache):
        """Normalize a given variant.

        :param str q: The variant to normalize
        :param ValidationSummary validations: Invalid and valid results
        :param AminoAcidCache amino_acid_cache: Amino Acid Code and Conversion
        :return: An allele descriptor for a valid result if one exists. Else,
            None.
        """
        if len(validations.valid_results) > 0:
            # For now, only use first valid result
            valid_result = validations.valid_results[0]
            valid_result_tokens = \
                validations.valid_results[0].classification.all_tokens

            polypeptide_sequence_variant_token = \
                ([t for t in valid_result_tokens if isinstance(t, PolypeptideSequenceVariant)] or [None])[0]  # noqa: E501

            if polypeptide_sequence_variant_token:
                molecule_context = 'protein'
                structural_type = 'SO:0001606'
            else:
                molecule_context = None
                structural_type = None
            allele = valid_result.allele
            allele_id = allele['_id']
            del allele['_id']

            gene_token = valid_result.gene_tokens[0]

            # convert 3 letter to 1 letter amino acid code
            if len(polypeptide_sequence_variant_token.ref_protein) == 3:
                for one, three in \
                        amino_acid_cache._amino_acid_code_conversion.items():
                    if three == polypeptide_sequence_variant_token.ref_protein:
                        polypeptide_sequence_variant_token.ref_protein = one

            variation_descriptor = VariationDescriptor(
                id=f"normalize:"
                   f"{q.strip().replace(' ', '_')}",
                value_id=allele_id,
                label=q,
                value=allele,
                molecule_context=molecule_context,
                structural_type=structural_type,
                ref_allele_seq=polypeptide_sequence_variant_token.ref_protein,
                gene_context=self.get_gene_descriptor(gene_token)
            )
        else:
            variation_descriptor = None

        return variation_descriptor

    def get_gene_descriptor(self, gene_token):
        """Return a GA4GH Gene Descriptor using Gene Normalization.

        :param GeneMatchToken gene_token: A gene token
        :return: A gene descriptor for a given gene
        """
        gene_symbol = gene_token.matched_value
        response = self.gene_normalizer.normalize(gene_symbol, incl='hgnc')
        if response['source_matches'][0]['records']:
            record = response['source_matches'][0]['records'][0]
            record_location = record.locations[0] if record.locations else None

            return GeneDescriptor(
                id=f"normalize:{gene_symbol}",
                label=gene_symbol,
                value=Gene(gene_id=record.concept_id),
                xrefs=record.other_identifiers,
                alternate_labels=[record.label] + record.aliases + record.previous_symbols,  # noqa: E501
                extensions=self.get_extensions(record, record_location)
            )

    def get_extensions(self, record, record_location):
        """Return a list of ga4gh extensions.

        :param gene.schemas.Gene record: The record from the normalization
            service
        :param gene.schemas.ChromosomeLocation record_location: The record's
            location
        :return: List of extensions providing additional information
        """
        extensions = list()
        if record.strand:
            self.add_extension(extensions, 'strand', [record.strand])
        if record.symbol_status:
            self.add_extension(extensions, 'symbol_status',
                               [record.symbol_status])
        self.add_extension(extensions, 'associated_with', record.xrefs)
        self.add_extension(extensions, 'chromosome_location',
                           [record_location.dict(by_alias=True)])
        return extensions

    def add_extension(self, extensions, name, value):
        """Add extension to list of extensions.

        :param list extensions: List of ga4gh extensions
        :param str name: name of extension
        :param str value: value of extension
        """
        extensions.append({
            'type': 'Extension',
            'name': name,
            'value': value
        })