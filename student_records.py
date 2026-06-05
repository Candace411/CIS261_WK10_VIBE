#!/usr/bin/env python3
"""Simple student records manager with JSON storage and CLI.

Usage examples:
  python3 student_records.py add --id 1 --name "Alice" --scores 90 85 92
  python3 student_records.py list
  python3 student_records.py grade --id 1
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional

DB_PATH = Path("students.json")


@dataclass
class StudentRecord:
    student_id: str
    name: str
    scores: List[float]

    def average(self) -> Optional[float]:
        if not self.scores:
            return None
        return sum(self.scores) / len(self.scores)

    def letter_grade(self) -> Optional[str]:
        avg = self.average()
        if avg is None:
            return None
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"


def load_db(path: Path = DB_PATH) -> Dict[str, StudentRecord]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    out: Dict[str, StudentRecord] = {}
    for sid, rec in raw.items():
        out[sid] = StudentRecord(student_id=sid, name=rec.get("name", ""), scores=rec.get("scores", []))
    return out


def save_db(db: Dict[str, StudentRecord], path: Path = DB_PATH) -> None:
    serializable = {sid: {"name": r.name, "scores": r.scores} for sid, r in db.items()}
    with path.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


def add_student(db: Dict[str, StudentRecord], student_id: str, name: str, scores: List[float]) -> None:
    if student_id in db:
        raise ValueError(f"Student id {student_id} already exists")
    db[student_id] = StudentRecord(student_id=student_id, name=name, scores=scores)


def update_scores(db: Dict[str, StudentRecord], student_id: str, scores: List[float]) -> None:
    if student_id not in db:
        raise KeyError(f"Student id {student_id} not found")
    db[student_id].scores = scores


def delete_student(db: Dict[str, StudentRecord], student_id: str) -> None:
    if student_id in db:
        del db[student_id]


def list_students(db: Dict[str, StudentRecord]) -> None:
    if not db:
        print("No students in database.")
        return
    for sid, rec in sorted(db.items(), key=lambda x: x[0]):
        avg = rec.average()
        avg_str = f"{avg:.2f}" if avg is not None else "N/A"
        print(f"ID: {sid}  Name: {rec.name}  Avg: {avg_str}  Grade: {rec.letter_grade() or 'N/A'}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Student records manager")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a new student")
    p_add.add_argument("--id", required=True, dest="id")
    p_add.add_argument("--name", required=True, dest="name")
    p_add.add_argument("--scores", type=float, nargs="*", default=[], dest="scores")

    p_list = sub.add_parser("list", help="List all students")

    p_update = sub.add_parser("update", help="Update scores for a student")
    p_update.add_argument("--id", required=True, dest="id")
    p_update.add_argument("--scores", type=float, nargs="*", default=[], dest="scores")

    p_delete = sub.add_parser("delete", help="Delete a student")
    p_delete.add_argument("--id", required=True, dest="id")

    p_grade = sub.add_parser("grade", help="Show a student's average and letter grade")
    p_grade.add_argument("--id", required=True, dest="id")

    args = parser.parse_args(argv)
    db = load_db()

    try:
        if args.cmd == "add":
            add_student(db, args.id, args.name, args.scores)
            save_db(db)
            print(f"Added student {args.name} ({args.id})")
        elif args.cmd == "list":
            list_students(db)
        elif args.cmd == "update":
            update_scores(db, args.id, args.scores)
            save_db(db)
            print(f"Updated scores for {args.id}")
        elif args.cmd == "delete":
            delete_student(db, args.id)
            save_db(db)
            print(f"Deleted student {args.id}")
        elif args.cmd == "grade":
            rec = db.get(args.id)
            if not rec:
                print("Student not found")
                return
            avg = rec.average()
            print(f"Student: {rec.name}  ID: {rec.student_id}")
            print(f"Scores: {rec.scores}")
            if avg is None:
                print("No scores available")
            else:
                print(f"Average: {avg:.2f}")
                print(f"Letter: {rec.letter_grade()}")
        else:
            parser.print_help()
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
