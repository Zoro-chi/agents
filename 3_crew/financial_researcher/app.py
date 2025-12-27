#!/usr/bin/env python
"""
Gradio interface for Financial Researcher
"""
import os
import sys
import gradio as gr
from pathlib import Path

print("Starting Financial Researcher Gradio App...")
print(f"Current directory: {os.getcwd()}")
print(f"App file location: {__file__}")

# Add src to path so we can import the crew
src_path = str(Path(__file__).parent / "src")
sys.path.insert(0, src_path)
print(f"Added to path: {src_path}")

try:
    from financial_researcher.crew import ResearchCrew

    print("Successfully imported ResearchCrew")
except Exception as e:
    print(f"Error importing ResearchCrew: {e}")
    raise

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
print("Output directory created/verified")


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
        # Stage 1: Initialization
        progress(0, desc="🚀 Starting research...")
        yield f"# Researching {company_name}...\n\n⏳ Initializing AI research agents..."

        inputs = {"company": company_name.strip()}

        # Stage 2: Setting up agents
        progress(0.15, desc="🤖 Setting up AI research agents...")
        yield f"# Researching {company_name}...\n\n✅ Agents initialized\n\n⏳ Gathering financial data from the web..."

        # Stage 3: Research phase
        progress(0.3, desc="🔍 Researching company information...")
        yield f"# Researching {company_name}...\n\n✅ Agents initialized\n✅ Web search in progress\n\n⏳ This may take 1-2 minutes as we analyze multiple sources..."

        # Create and run the crew
        result = ResearchCrew().crew().kickoff(inputs=inputs)

        # Stage 4: Analysis
        progress(0.8, desc="📊 Analyzing data and generating report...")
        yield f"# Researching {company_name}...\n\n✅ Research complete\n✅ Data collected\n\n⏳ Generating comprehensive analysis..."

        # Get the raw report
        report = result.raw

        # Stage 5: Finalizing
        progress(0.95, desc="✨ Finalizing report...")
        yield f"# Researching {company_name}...\n\n✅ Research complete\n✅ Analysis complete\n\n⏳ Formatting final report..."

        progress(1.0, desc="✅ Complete!")

        # Yield final report (not return!)
        yield f"# Financial Research Report: {company_name}\n\n{report}"

    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "api_key" in error_msg.lower():
            yield f"❌ **API Key Error**\n\nIt looks like your API keys are not configured correctly.\n\nPlease make sure you have set:\n- `OPENAI_API_KEY` environment variable\n- `SERPER_API_KEY` environment variable\n\n**Error details:** {error_msg}"
        else:
            yield f"❌ **Error during research**\n\n{error_msg}\n\nPlease try again or contact support if the issue persists."


# Create the Gradio interface
with gr.Blocks(title="Financial Researcher", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🔍 Financial Researcher
        
        Get comprehensive financial research and analysis on any publicly traded company.
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
                value="💡 **Ready to research!**\n\nEnter a company name and click 'Start Research' to get a comprehensive financial analysis.",
            )

    # Connect the button to the function
    submit_btn.click(fn=research_company, inputs=[company_input], outputs=[output])

    # Also allow Enter key to submit
    company_input.submit(fn=research_company, inputs=[company_input], outputs=[output])

if __name__ == "__main__":
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get("PORT", 7860))

    print(f"Starting Gradio server on 0.0.0.0:{port}")

    demo.launch(server_name="0.0.0.0", server_port=port, share=False, show_error=True)
