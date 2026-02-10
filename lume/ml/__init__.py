"""
Lume ML Module - Natural Language Normalization

This module provides SAFE, OFFLINE machine learning capabilities
for normalizing natural language input.

SECURITY GUARANTEES:
- ML NEVER generates shell commands
- ML NEVER executes anything
- ML only normalizes natural language
- Rule engine remains the sole authority
- Fully offline operation (no API calls)
- Graceful fallback to rule-based parsing

Version: 0.3.0
"""

from lume.ml.normalizer import MLNormalizer

__all__ = ['MLNormalizer']
