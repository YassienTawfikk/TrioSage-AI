"""
Orchestrator — Sequential multi-agent pipeline with failure handling.
Runs NVC → Kahneman → Covey → Synthesizer, each building on previous outputs.
"""

from agents import NVC_PROMPT, KAHNEMAN_PROMPT, COVEY_PROMPT, SYNTHESIZER_PROMPT
from gemini_client import call_gemini


class AllAgentsFailedError(Exception):
    """Raised when all three agents fail — no outputs available for synthesis."""
    pass


# Agent definitions in execution order
AGENTS = [
    {"name": "nvc", "label": "NVC (Rosenberg)", "prompt": NVC_PROMPT},
    {"name": "kahneman", "label": "Kahneman", "prompt": KAHNEMAN_PROMPT},
    {"name": "covey", "label": "Covey", "prompt": COVEY_PROMPT},
]


def validate_inputs(scenario: str, api_key: str) -> tuple[bool, str]:
    """
    Validate that the user has provided both a scenario and an API key.

    Returns:
        (True, "") if valid.
        (False, error_message) if invalid.
    """
    if not api_key or not api_key.strip():
        return False, "Please enter your Gemini API key to continue."

    if not scenario or not scenario.strip():
        return False, "Please describe your scenario before analyzing."

    return True, ""


def _build_message(scenario: str, previous_outputs: dict[str, str]) -> str:
    """
    Build the message to send to an agent, including the scenario
    and all previous successful agent outputs for context.
    """
    parts = [f"## Scenario\n{scenario}"]

    if previous_outputs:
        parts.append("\n## Previous Advisor Analyses")
        for agent_name, output in previous_outputs.items():
            parts.append(f"\n### {agent_name} Advisor Response:\n{output}")

    return "\n".join(parts)


def _build_synthesis_message(scenario: str, outputs: dict[str, str], failed: list[str]) -> str:
    """
    Build the message for the synthesizer, including labeled outputs
    from all agents that succeeded and notes about any that failed.
    """
    parts = [f"## Original Scenario\n{scenario}\n"]
    parts.append("## Advisor Analyses\n")

    label_map = {
        "nvc": "NVC (Nonviolent Communication) Advisor",
        "kahneman": "Kahneman (Thinking, Fast and Slow) Advisor",
        "covey": "Covey (7 Habits) Advisor",
    }

    for agent_name, output in outputs.items():
        label = label_map.get(agent_name, agent_name)
        parts.append(f"### {label}:\n{output}\n")

    if failed:
        failed_labels = [label_map.get(f, f) for f in failed]
        parts.append(
            f"\n**Note:** The following advisors were unavailable: "
            f"{', '.join(failed_labels)}. Synthesize from the available analyses only."
        )

    return "\n".join(parts)


def run_pipeline(scenario: str, api_key: str, progress_callback=None) -> dict:
    """
    Run the full multi-agent pipeline sequentially.

    Args:
        scenario: The user's problem description.
        api_key: The user's Gemini API key.
        progress_callback: Optional callable(agent_name: str, status: str)
                           where status is 'running', 'done', or 'failed'.

    Returns:
        dict with keys: nvc, kahneman, covey, synthesis, failed_agents.
        Each agent key is either a string (response) or None (if failed).

    Raises:
        AllAgentsFailedError: If all three agents fail.
    """
    results = {"nvc": None, "kahneman": None, "covey": None, "synthesis": None, "failed_agents": []}
    successful_outputs = {}  # Ordered dict of agent_name -> output

    # Run each agent sequentially
    for agent in AGENTS:
        name = agent["name"]
        label = agent["label"]

        if progress_callback:
            progress_callback(name, "running")

        try:
            message = _build_message(scenario, successful_outputs)
            response = call_gemini(agent["prompt"], message, api_key)
            results[name] = response
            successful_outputs[name] = response

            if progress_callback:
                progress_callback(name, "done")

        except Exception:
            results[name] = None
            results["failed_agents"].append(name)

            if progress_callback:
                progress_callback(name, "failed")

    # Check if all agents failed
    if len(results["failed_agents"]) == len(AGENTS):
        if progress_callback:
            progress_callback("synthesizer", "failed")
        raise AllAgentsFailedError(
            "All agents failed — please check your API key and try again."
        )

    # Run synthesizer on available outputs
    if progress_callback:
        progress_callback("synthesizer", "running")

    try:
        synthesis_message = _build_synthesis_message(
            scenario, successful_outputs, results["failed_agents"]
        )
        results["synthesis"] = call_gemini(SYNTHESIZER_PROMPT, synthesis_message, api_key)

        if progress_callback:
            progress_callback("synthesizer", "done")

    except Exception:
        results["synthesis"] = None

        if progress_callback:
            progress_callback("synthesizer", "failed")

    return results
