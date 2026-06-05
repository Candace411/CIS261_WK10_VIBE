# CIS261_WK10_VIBE

## Student Records Manager

Run the student records CLI via `VIBE.py` for local use:

Example:

```
./VIBE.py add --id 1 --name "Alice" --scores 90 85 92
./VIBE.py list
./VIBE.py grade --id 1
```

To make `VIBE.py` executable locally:

```
chmod +x VIBE.py
```

To run tests:

```
python3 -m unittest test_student_records.py -v
```
