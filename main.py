import argparse
import logging
import os
import sys
import magic
import pandas as pd
import math
from collections import Counter

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
        # The whole file is read into memory here. That is the simple
        # version, and it is the reason a multi gigabyte file is a bad
        # input for this tool even though the tally itself is cheap.
        with open(file_path, "rb") as f:
            data = f.read()
        if not data:
            return 0.0

        # One tally pass. Counting byte by byte with data.count() instead
        # rescans the whole buffer once per possible value, 256 passes over
        # the same bytes to get these same probabilities.
        entropy = 0
        for count in Counter(data).values():
            p_x = count / len(data)
            entropy += - p_x * math.log2(p_x)
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
        # A libmagic failure degrades to an Unknown string and the run
        # continues to entropy, while an entropy failure below aborts
        # the whole analysis. That split is deliberate: a report with a
        # missing type still carries a usable entropy number, but a
        # report with the sentinel in the entropy column would look
        # like data.
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
        # This failure is only logged, and main has already moved on,
        # so the run exits 0 with no report written. Also note the
        # report is not optional: the output argument has a default
        # file name, so every successful run writes a CSV whether the
        # caller asked for one or not, and nothing is printed instead.
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
