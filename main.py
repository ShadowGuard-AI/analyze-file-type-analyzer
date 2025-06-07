import argparse
import logging
import os
import sys
import magic
import pandas as pd
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the command-line argument parser.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Analyze the file type of a given file based on its magic bytes and entropy.")
    parser.add_argument("file_path", help="Path to the file to analyze.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    parser.add_argument("-o", "--output", help="Output file for report (CSV format).", default="file_analysis_report.csv")
    return parser

def calculate_entropy(file_path):
    """
    Calculates the entropy of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        float: The calculated entropy value.  Returns -1 on error.
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        if not data:
            return 0.0

        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x])))/len(data)
            if p_x > 0:
                entropy += - p_x*math.log2(p_x)
        return entropy
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return -1
    except Exception as e:
        logging.error(f"Error calculating entropy for {file_path}: {e}")
        return -1

def analyze_file(file_path):
    """
    Analyzes the file using libmagic and calculates entropy.

    Args:
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing the analysis results.  Returns None on error.
    """
    try:
        if not os.path.isfile(file_path):
            logging.error(f"Invalid file path: {file_path}")
            return None

        file_size = os.path.getsize(file_path)

        #Detect file type using libmagic
        try:
            file_type = magic.from_file(file_path)
        except Exception as e:
            logging.error(f"Error using libmagic on {file_path}: {e}")
            file_type = "Unknown (Error during magic analysis)"

        entropy = calculate_entropy(file_path)
        if entropy == -1:
            return None #Indicates an error occurred within calculate_entropy

        return {
            "file_path": file_path,
            "file_size": file_size,
            "file_type": file_type,
            "entropy": entropy
        }

    except Exception as e:
        logging.error(f"An unexpected error occurred during analysis of {file_path}: {e}")
        return None

def generate_report(analysis_results, output_file):
    """
    Generates a report in CSV format from the analysis results.

    Args:
        analysis_results (list): A list of dictionaries containing the analysis results.
        output_file (str): The path to the output CSV file.
    """
    try:
        df = pd.DataFrame(analysis_results)
        df.to_csv(output_file, index=False)
        logging.info(f"Report generated successfully: {output_file}")
    except Exception as e:
        logging.error(f"Error generating report: {e}")

def main():
    """
    Main function to execute the file type analyzer.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")

    file_path = args.file_path

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

    analysis_result = analyze_file(file_path)
    if analysis_result:
      generate_report([analysis_result], args.output)
    else:
      logging.error(f"Analysis failed for {file_path}")
      sys.exit(1)


if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()


"""
Usage Examples:

1. Analyze a file and generate a report:
   python main.py suspicious_file.exe

2. Analyze a file and specify a custom output file:
   python main.py suspicious_file.exe -o my_report.csv

3. Analyze a file with verbose logging:
   python main.py suspicious_file.exe -v

Offensive Tool Considerations:

- This tool can be used to identify file masquerading techniques.  For example, a file with a .txt extension might actually be a PE executable.
- The entropy calculation can help identify packed or obfuscated files, which are often used by malware. A high entropy value is a red flag.
- The tool can be integrated into a larger malware analysis pipeline.
- The results can be used to create signatures for malware detection.
- Ensure the tool is run in a sandboxed environment to avoid accidental execution of malicious files.
- Be cautious when handling untrusted files, as they may contain vulnerabilities or exploits.

Security Best Practices:
- Sanitize file paths to prevent path traversal vulnerabilities.
- Implement input validation to prevent malicious input from crashing the tool or causing unexpected behavior.
- Use secure file handling practices to prevent information leakage or unauthorized access.
- Keep the tool and its dependencies up to date to patch security vulnerabilities.

"""