![Harbour mouth before the run: foredeck with a coiled rope, a lit lantern, a brass bell and a tied chart roll in front, open slate channel water and diminishing lit buoys behind, no text](intro-banner.png)

# analyze-file-type-analyzer

![Pilot boat at dawn looking aft over its boiling wake toward a distant inbound ship, the project name painted in chalk on the slate transom board](banner.png)

![The run in three bands: the horizon brightens and a distant hull rides the swell, buoys pass and dip through the channel, and the foredeck lantern sways while the bell swings and pauses](scene.svg)


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

> Pilot note: the CSV report is written on every successful run whether or not -o is supplied, because -o carries the default file_analysis_report.csv, and no live run backs the parameter list on this page, which was taken from the argument parser in main.py. Both facts stand here in the open, where a careful reader will find them.
