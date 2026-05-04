# TrioSage-AI

**A Multi-Agent Decision Support System for Conflict Resolution & High-Stakes Decisions**

![Application Overview](https://github.com/user-attachments/assets/45a8feda-3888-4cb7-8178-942a92ef5509)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://triosage.streamlit.app)

---

## Introduction

TrioSage-AI is an advanced, web-based multi-agent decision support system. Users describe a real-life problem, conflict, or high-stakes decision they are facing. The system passes the scenario through a sequential pipeline of three distinct, highly specialized AI "Sages"—each inspired by foundational literature in psychology, behavioral economics, and leadership. Finally, a Synthesizer agent aggregates their diverse perspectives into one coherent, actionable plan.

By avoiding the "single-agent anchor bias," TrioSage-AI provides deeper, more empathetic, and mathematically grounded advice.

---

## Features

- **Multi-Agent Sequential Pipeline**: Advice is processed independently through three specialized frameworks to ensure diverse reasoning styles.
- **High-Fidelity UI/UX**: An elegant, editorial-style Streamlit interface designed for readability, focus, and modern aesthetics.
- **Secure API Management**: Bring-your-own-key (BYOK) architecture. API keys are strictly session-bound and securely injected from the clipboard.
- **Rate-Limit Resilience**: Built-in orchestration to handle Gemini API quotas gracefully (15 RPM limits) with proper sleep intervals between agent executions.

---

## The Three Sages

TrioSage-AI is powered by three distinct agents, executed in a specific sequence before being aggregated:

1. **The Empathetic Mediator (NVC)**: Grounded in Marshall Rosenberg's *Nonviolent Communication*. It focuses on translating judgments into core human needs, ensuring emotional safety, and prioritizing empathy.
2. **The Behavioral Analyst (Kahneman)**: Inspired by Daniel Kahneman's *Thinking, Fast and Slow*. This agent acts as a cognitive safety net, identifying biases (anchoring, loss aversion, status quo bias) and evaluating the objective realities of the situation.
3. **The Strategic Planner (Covey)**: Based on Stephen Covey's *The 7 Habits of Highly Effective People*. It takes the emotional foundation (NVC) and objective analysis (Kahneman) to build a proactive, long-term, and principle-centered action plan ("Begin with the End in Mind").
4. **The Synthesizer**: The final agent that reviews the raw outputs of the three Sages and generates a single, cohesive master plan.

---

## Architecture & Models

TrioSage-AI is built on a clear, logical foundation to ensure advice is generated systematically and free from single-agent bias. Below are the core models that define how the system operates.

### How Users Interact with the System
The interaction flow is designed to be as frictionless and secure as possible. The user securely injects their session-bound API key and provides a scenario. The system abstracts away the complex multi-agent orchestration, presenting a simple, unified interface for receiving synthesized advice while handling all API communication securely in the background.

![Use Case Model](https://github.com/user-attachments/assets/0706478e-1a57-4d48-95a0-1b3a757bf784)

### The Orchestration Pipeline
When a user submits a scenario, it doesn't just go to a single LLM. Instead, it triggers a highly controlled pipeline. As shown in the process model below, the input is handled with robust state management—ensuring the UI is locked during processing, error handling for API limits is engaged, and the output is safely delivered to the final interface state.

![Process Model Success](https://github.com/user-attachments/assets/e6b298d2-dcfe-429e-a1f1-2e40f43fd0f9)

### The Technical Backbone
Under the hood, TrioSage-AI leverages a lightweight but resilient architecture. Streamlit handles the frontend state and secure UI, while the custom Python orchestrator manages the strict sequential logic, rate limiting (with built-in API sleep intervals), and connection to the Google GenAI SDK. This separation of concerns ensures the application remains responsive and scalable.

![Solution Architecture Model](https://github.com/user-attachments/assets/df1526f5-69eb-4aad-bd69-2122f05fb8ee)

---

## Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [Google Gemini (`gemini-flash-latest`)](https://ai.google.dev/) via the modern `google-genai` SDK
- **Styling**: Custom CSS (Flexbox, Inter typography, Glassmorphism) & Streamlit HTML Components

---

## Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone <YOUR_REPO_LINK_HERE>
   cd TrioSage-AI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

5. **Provide an API Key:** 
   Once the app opens in your browser at `http://localhost:8501`, paste your Google Gemini API key into the secure input box to begin.

---

## Deployment

TrioSage-AI is designed to be deployed instantly on **Streamlit Community Cloud**. 
- No environment variables or `.env` files are required on the server, as the architecture uses a session-state API key provided by the user.
- Ensure your `requirements.txt` is up-to-date before pushing to the main branch.

---

## Contributors

<div>
    <table align="center">
        <tr>
            <td align="center">
                <a href="https://github.com/YassienTawfikk" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/126521373?v=4" width="150px;"
                         alt="Yassien Tawfik"/>
                    <br/>
                    <sub><b>Yassien Tawfik</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Mazenmarwan023" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/127551364?v=4" width="150px;" alt="Mazen Marwan"/>
                    <br/>
                    <sub><b>Mazen Marwan</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/mohamedddyasserr" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/126451832?v=4" width="150px;"
                         alt="Mohamed Yasser"/>
                    <br/>
                    <sub><b>Mohamed Yasser</b></sub>
                </a>
            </td>
              </td>
        </tr>
    </table>
</div>