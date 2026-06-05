import unittest
import tempfile
from pathlib import Path

import student_records as sr


class TestStudentRecords(unittest.TestCase):
    def test_add_update_grade_delete(self):
        with tempfile.TemporaryDirectory() as td:
            dbpath = Path(td) / "test_students.json"
            # start with empty db
            db = sr.load_db(dbpath)
            self.assertEqual(db, {})

            # add a student
            sr.add_student(db, "1", "Alice", [90, 80, 70])
            sr.save_db(db, dbpath)

            # reload and check
            db2 = sr.load_db(dbpath)
            self.assertIn("1", db2)
            rec = db2["1"]
            self.assertEqual(rec.name, "Alice")
            self.assertAlmostEqual(rec.average(), 80.0)
            self.assertEqual(rec.letter_grade(), "B")

            # update scores
            sr.update_scores(db2, "1", [100, 95])
            sr.save_db(db2, dbpath)
            db3 = sr.load_db(dbpath)
            self.assertAlmostEqual(db3["1"].average(), 97.5)
            self.assertEqual(db3["1"].letter_grade(), "A")

            # delete
            sr.delete_student(db3, "1")
            sr.save_db(db3, dbpath)
            db4 = sr.load_db(dbpath)
            self.assertNotIn("1", db4)


if __name__ == "__main__":
    unittest.main()
