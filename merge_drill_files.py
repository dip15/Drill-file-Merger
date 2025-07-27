# merge_drill_files.py
# This script combines and sorts Excellon drill files by hole size.
# One tool per unique hole size. Output is in mm.
# All drill files are automatically detected and processed from a selected ZIP file.

import os
import re
import zipfile
from collections import defaultdict
from tkinter import Tk, filedialog, messagebox

# === STEP 1: SELECT ZIP FILE ===
root = Tk()
root.withdraw()
INPUT_ZIP = filedialog.askopenfilename(title="Select Gerber ZIP File", filetypes=[("ZIP files", "*.zip")])
if not INPUT_ZIP:
    raise ValueError("❌ No file selected. Exiting.")

# Set extract folder to same directory as input zip
base_folder = os.path.dirname(INPUT_ZIP)
EXTRACT_FOLDER = os.path.join(base_folder, os.path.splitext(os.path.basename(INPUT_ZIP))[0] + "_extracted")
OUTPUT_FILE = os.path.join(EXTRACT_FOLDER, "Merge_drill_file "+ ".drl")

# === STEP 2: EXTRACT ZIP ===
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
try:
    with zipfile.ZipFile(INPUT_ZIP, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)
except zipfile.BadZipFile:
    messagebox.showerror("Error", "❌ Selected file is not a valid ZIP archive.")
    raise SystemExit

# === STEP 3: FIND ALL .DRL FILES ===
drl_files = []
for root_dir, _, files in os.walk(EXTRACT_FOLDER):
    for file in files:
        if file.lower().endswith(".drl"):
            drl_files.append(os.path.join(root_dir, file))

if not drl_files:
    messagebox.showerror("Error", "❌ No .drl files found in the ZIP archive.")
    raise SystemExit

# === STEP 4: PARSE EACH DRILL FILE ===
size_to_coords = defaultdict(list)  # 1.0 -> [X001000Y002000, ...]
tool_def_pattern = re.compile(r"T(\d+)C([\d\.]+)", re.IGNORECASE)
coord_pattern_simple = re.compile(r"^X[-+]?\d+\.?\d*Y[-+]?\d+\.?\d*$")
coord_pattern_g85 = re.compile(r"^(X[-+]?\d+\.?\d*Y[-+]?\d+\.?\d*)G85")

valid_data_found = False

for drl_file in drl_files:
    with open(drl_file, 'r') as f:
        lines = f.readlines()
        tool_sizes = {}
        current_tool = None

        for line in lines:
            line = line.strip()

            # Tool definition
            match = tool_def_pattern.match(line)
            if match:
                tool_id, size = match.groups()
                tool_sizes[f"T{tool_id.zfill(2)}"] = float(size)
                continue

            # Tool change
            if re.match(r"^T\d+$", line):
                current_tool = f"T{line[1:].zfill(2)}"
                continue

            # Match normal coordinate
            if coord_pattern_simple.match(line) and current_tool in tool_sizes:
                hole_size = tool_sizes[current_tool]
                size_to_coords[hole_size].append(line)
                valid_data_found = True
                continue

            # Match G85-style coordinate
            if "G85" in line and current_tool in tool_sizes:
             hole_size = tool_sizes[current_tool]
             size_to_coords[hole_size].append(line)  # Keep full G85 line
             valid_data_found = True
             continue



if not valid_data_found:
    messagebox.showerror("Error", "❌ No valid drill coordinates found in .drl files.")
    raise SystemExit

# === STEP 5: WRITE FINAL MERGED FILE ===
with open(OUTPUT_FILE, 'w') as out:
    out.write("M48\n")
    out.write("; This is an auto-generated drill file\n")
    out.write("; All drill files are combined and sorted by hole size\n")
    out.write("; Created using Python GUI script\n")
    out.write("; This script is under testing, Made by Dip Ghodmare Version 2.1\n")
    out.write("; FORMAT=2:4\n")
    out.write("METRIC,TZ\n")
    out.write("%\n")

    # Write tool definitions sorted by hole size
    size_list = sorted(size_to_coords.keys())
    size_to_tool = {}
    for i, size in enumerate(size_list, 1):
        tool_id = f"T{str(i).zfill(2)}"
        size_to_tool[size] = tool_id
        out.write(f"{tool_id}C{size:.3f}\n")

    out.write("%\n")

    # Write coordinates grouped under tool
    for size in size_list:
        out.write(f"{size_to_tool[size]}\n")
        for coord in size_to_coords[size]:
            out.write(f"{coord}\n")

    out.write("M30\n")

# === STEP 6: NOTIFY USER ===
messagebox.showinfo("Merge Complete", f"✅ Drill files merged successfully!\nSaved as:\n{OUTPUT_FILE}")
