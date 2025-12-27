#!/usr/bin/env python
"""
Gradio interface for Financial Researcher
"""
import os
import sys
import gradio as gr
from pathlib import Path

# Add src to path so we can import the crew
sys.path.insert(0, str(Path(__file__).parent / "src"))

from financial_researcher.crew import ResearchCrew

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)


def research_company(company_name, progress=gr.Progress()):
    """
    Run financial research on a company and return the report.

    Args:
        company_name: Name of the company to research
        progress: Gradio progress tracker

    Returns:
        str: The generated research report
    """
    if not company_name or not company_name.strip():
        return "⚠️ Please enter a company name."

    try:
        progress(0.1, desc="Initializing research crew...")

        inputs = {"company": company_name.strip()}

        progress(0.3, desc="Running research task...")

        # Create and run the crew
        result = ResearchCrew().crew().kickoff(inputs=inputs)

        progress(0.9, desc="Finalizing report...")

        # Get the raw report
        report = result.raw

        progress(1.0, desc="Complete!")

        return f"# Financial Research Report: {company_name}\n\n{report}"

    except Exception as e:
        return f"❌ Error during research: {str(e)}\n\nPlease check your API keys and try again."


# Create the Gradio interface
with gr.Blocks(title="Financial Researcher", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🔍 Financial Researcher
        
        Get comprehensive financial research and analysis on any publicly traded company.
        
        **Note:** This tool requires:
        - OpenAI API key (set as `OPENAI_API_KEY` environment variable)
        - Serper API key (set as `SERPER_API_KEY` environment variable)
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            company_input = gr.Textbox(
                label="Company Name",
                placeholder="e.g., Apple, Microsoft, Tesla",
                lines=1,
            )

            submit_btn = gr.Button("🚀 Start Research", variant="primary", size="lg")

            gr.Markdown(
                """
                ### Examples:
                - Apple
                - Microsoft
                - Tesla
                - NVIDIA
                - Amazon
                """
            )

        with gr.Column(scale=2):
            output = gr.Markdown(
                label="Research Report",
                value="Your research report will appear here...",
            )

    # Connect the button to the function
    submit_btn.click(fn=research_company, inputs=[company_input], outputs=[output])

    # Also allow Enter key to submit
    company_input.submit(fn=research_company, inputs=[company_input], outputs=[output])

if __name__ == "__main__":
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get("PORT", 7860))

    demo.launch(server_name="0.0.0.0", server_port=port, share=False)
