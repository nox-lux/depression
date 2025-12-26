import pickle
import os

filename = "students.dat"
tempfile = "temp.dat"

# ---------- PART 1: CREATE FILE (your original logic is fine) ----------
with open(filename, 'wb') as f:
    while True:
        no = int(input('No: '))
        m = int(input('Marks: '))
        grade = input('Grade: ')
        pickle.dump([no, m, grade], f)
        if input('Break? ') == 'y':
            break

# ---------- PART 2: UPDATE RECORD USING TEMP FILE ----------
r = int(input("Enter roll no to update: "))
found = False

with open(filename, "rb") as fin, open(tempfile, "wb") as fout:
    while True:
        try:
            rec = pickle.load(fin)      # read one record
        except EOFError:
            break                        # end of file – stop loop

        if rec[0] == r:                  # rec[0] = roll no
            new_marks = int(input("Enter new marks: "))
            new_grade = input("Enter new grade: ")
            rec[1] = new_marks           # update marks
            rec[2] = new_grade           # update grade
            found = True

        pickle.dump(rec, fout)

if not found:
    print("Roll number not found.")

# replace old file with temp file
os.remove(filename)
os.rename(tempfile, filename)
