![Banner](banner.png)

# analyze-file-type-analyzer
Determines the file type of a given file from its magic bytes and reports its entropy, to help detect files whose extension does not match their contents.

## Install
```
git clone https://github.com/ShadowGuard-AI/analyze-file-type-analyzer
cd analyze-file-type-analyzer
pip install -r requirements.txt
```

## Usage
```
python3 main.py FILE_PATH [-v] [-o OUTPUT]
```

## Parameters
- `FILE_PATH`: path to the file to analyze.
- `-h`: show help message and exit.
- `-v`, `--verbose`: enable verbose logging.
- `-o`, `--output`: output file for the report in CSV format. Default: `file_analysis_report.csv`.

## Verified behavior
- A missing input file exits 1.
- The report CSV carries the file path, file size, detected file type, and entropy.
- The output file is not optional in practice: because `-o` has a default, every successful run writes a CSV in the working directory unless `-o` names another file, and nothing is printed instead.
- Live run not possible in this environment: the `magic` package is not installed here and installs are not permitted in this wave. The parameter list above is taken from the argument parser in `main.py`, and the file compiles cleanly.

## License
MIT License, see LICENSE.
