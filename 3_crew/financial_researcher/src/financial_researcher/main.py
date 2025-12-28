#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from datetime import datetime
from financial_researcher.crew import ResearchCrew

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)


def run():
    """
    Run the research crew.
    """
    # Get current date information
    now = datetime.now()
    current_year = now.year
    current_month = now.strftime("%B")
    previous_year = current_year - 1
    next_year = current_year + 1

    inputs = {
        "company": "Apple",
        "current_date": now.strftime("%B %Y"),
        "current_year": str(current_year),
        "previous_year": str(previous_year),
        "next_year": str(next_year),
        "current_month": current_month,
    }

    # Create and run the crew
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")


if __name__ == "__main__":
    run()
