#!/bin/bash

# Check if the user provided an XML file name as an argument
if [ -z "$1" ]; then
    echo "Usage: ./xml_split.sh <filename.xml>"
    exit 1
fi

# Set the input file and output file names
INPUT_FILE="$1"
OUTPUT_FILE1="${INPUT_FILE%.xml}_part1.xml"
OUTPUT_FILE2="${INPUT_FILE%.xml}_part2.xml"

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found."
    exit 1
fi

# Get the total line count of the input XML file
TOTAL_LINES=$(wc -l < "$INPUT_FILE")

# Calculate the approximate halfway point
HALFWAY_POINT=$(( TOTAL_LINES / 2 ))

# Split the file at the halfway point, preserving XML structure
# Part 1: Up to halfway point
head -n "$HALFWAY_POINT" "$INPUT_FILE" > "$OUTPUT_FILE1"

# Part 2: From halfway point to end
tail -n +$((HALFWAY_POINT + 1)) "$INPUT_FILE" > "$OUTPUT_FILE2"

# Notify the user of the output files
echo "The XML file has been split into:"
echo "1. $OUTPUT_FILE1"
echo "2. $OUTPUT_FILE2"
