"""
Agent definitions — re-exports all system prompts for clean imports.

Usage:
    from agents import NVC_PROMPT, KAHNEMAN_PROMPT, COVEY_PROMPT, SYNTHESIZER_PROMPT
"""

from agents.nvc import SYSTEM_PROMPT as NVC_PROMPT
from agents.kahneman import SYSTEM_PROMPT as KAHNEMAN_PROMPT
from agents.covey import SYSTEM_PROMPT as COVEY_PROMPT
from agents.synthesizer import SYSTEM_PROMPT as SYNTHESIZER_PROMPT

__all__ = ["NVC_PROMPT", "KAHNEMAN_PROMPT", "COVEY_PROMPT", "SYNTHESIZER_PROMPT"]
