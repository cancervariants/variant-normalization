"""Module for testing Protein Substitution Classifier."""
import unittest
from varlexapp.classifiers import ProteinSubstitutionClassifier
from .classifier_base import ClassifierBase


class TestProteinSubstitutionTokenizer(ClassifierBase, unittest.TestCase):
    """A class to test the Protein Substitution Classifier."""

    def classifier_instance(self):
        """Return ProteinSubstitutionClassifier instance."""
        return ProteinSubstitutionClassifier()

    def fixture_name(self):
        """Return ProteinSubstitutionClassifier fixture name."""
        return 'protein_substitution'