#!/bin/bash

# Ensure nmap is installed
'''if ! command -v nmap &> /opt/homebrew/bin/; then
    echo "nmap not found. Please install it first."
    exit 1
fi'''

# Define target
TARGET="roundrock.actionjackson.ai"

# Run nmap scan
echo "Starting nmap scan against $TARGET for known vulnerabilities on well-known ports..."

nmap -sV -Pn --script vuln --top-ports 1000 -oN nmap_scan_results.txt "$TARGET"

echo "Scan completed. Results saved to nmap_scan_results.txt"