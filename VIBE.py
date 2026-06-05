#!/usr/bin/env python3
# Candace Williams
# CIS261
# VIBE Coding

"""VIBE launcher: entrypoint for the student records manager.

This file delegates to the student_records CLI so you can run:
	python3 VIBE.py --help
"""

from student_records import main


if __name__ == "__main__":
		main()