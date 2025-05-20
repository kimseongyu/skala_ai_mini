#! python3
from workflow import run_workflow
import os
from dotenv import load_dotenv


def main():
    # Load environment variables
    load_dotenv()

    # Example keywords
    keywords = ["AI", "LLM", "LLVM"]

    # Run the workflow
    final_state = run_workflow(keywords)

    # Print the report path
    print("end")


if __name__ == "__main__":
    main()
