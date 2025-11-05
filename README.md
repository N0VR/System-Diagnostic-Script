# System Diagnostic Utility

## Overview

A modular Windows system diagnostic tool written in Python. This utility collects real-time system information including CPU usage, memory usage, disk space, and Windows service status. The goal of the project is to create a maintainable and extensible tool that can later be expanded with cleanup tasks, reporting features, and network diagnostics.

## Features

- Real-time CPU and RAM monitoring
- Drive scanning to show total, used, and free space
- Windows service status inspection (with readable "Running"/"Stopped" output)
- Organized using object-oriented design for easier maintenance and expansion

## How to Run

- Windows OS
- Python 3.9 or later
- Psutil (Install)

**Run the script:**
```bash
python System-Diagnostic-Utility.py
```

## What I Learned

- How to run and parse PowerShell command output through Python using subprocess
- How to structure a script using Object-Oriented Programming for better modularity
- How to implement real-time system monitoring using psutil and timing loops

## Planned Improvements

- Add a menu-driven interface for switching between monitoring modes
- Add a temporary file cleanup feature with user confirmation
- Implement a network connectivity test module
- Generate formatted system reports (text / JSON / HTML)

## Project Status

- Core monitoring features implemented
- Currently improving structure and planning additional functionality
- This project is actively evolving as I continue to learn and build