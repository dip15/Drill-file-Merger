# Drill-file-Merger
Its an script primarily made for Copper-Cam software which only accept only one drill file, It combine 2 or more drill file.

📘 Drill File Merger – User Guide
Overview
The Drill File Merger is a Python utility that automates the process of consolidating multiple Excellon drill files (.drl) into a single, sorted file. It is primarily designed for PCB fabrication workflows where drill data is distributed across several files within a Gerber archive.
This tool:
●	Automatically extracts .drl files from a selected ZIP archive

●	Parses and categorizes drill holes based on size

●	Groups and organizes coordinate data by tool

●	Produces a clean, manufacturer-ready .drl file

________________________________________
Features
✅ ZIP-Based Input
 → Accepts a compressed ZIP archive containing your PCB project files.
🔍 Automated Parsing
 → Detects and reads all .drl files, including those nested within folders.
📏 Hole Size Deduplication
 → Merges tools with the same drill size to eliminate redundancy.
🧠 Coordinate Format Support
 → Compatible with both:
●	Standard Excellon: X...Y...

●	Extended format (e.g., plated slots): X...Y...G85X...Y...

🖥 User-Friendly Interface
 → Simple file selection dialog via GUI – no command-line input required.
📂 Organized Output
 → Output file is saved in the same directory as the original ZIP file with the same base name (e.g., MyPCB.zip → MyPCB.drl).
🛠 Testing-Ready Format
 → Output includes proper M48 header and M30 footer, uses METRIC,TZ format.
🧯 Error Handling
 → Alerts the user for common issues:
●	Invalid ZIP file

●	Missing .drl files

●	No valid drill coordinates

________________________________________
How to Use
1.	Run the script: merge_drill_files.py

2.	Select a Gerber ZIP archive when prompted.

3.	The tool will:

○	Extract the ZIP to a folder named extracted_gerber_final

○	Locate and process all .drl files

○	Create a merged .drl file with hole data sorted by size

4.	Check the output:

○	File saved in the same location as the input ZIP

○	Example: Design_v1.zip → Design_v1.drl

________________________________________
Output Format Example
excellon
CopyEdit
M48
; Auto-generated drill file
; FORMAT=2:4
METRIC,TZ
%
T01C0.600
T02C0.800
%
T01
X138.430Y-41.275
X180.594Y-20.447
T02
X211.836Y-43.180
X169.545Y-53.340
M30

________________________________________
System Requirements
●	Python 3.x

●	Required Modules: tkinter, zipfile, os, re, collections

No additional installation required – pure Python standard libraries are used.
________________________________________
Notes
●	Unit Format: Metric (mm), Trailing Zeros omitted.

●	Tool Mapping: One tool assigned per unique drill size.

●	Safety: Original files are not modified or deleted.

________________________________________

