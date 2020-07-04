import csv

ALPHA = 0.75
BETA = 1.1

class Program:
    def __init__(self, name, sanctioned, original):
        self.name = name
        self.sanctioned = int(sanctioned)
        self.original = int(original)
        self.current = self.original
        self.min = round(self.sanctioned * ALPHA)
        self.max = round(self.sanctioned * BETA)
        self.blocked = False
        self.bcpi = 0.00
        self.cutoff = 11.00


class Student:
    def __init__(self, name, roll, cpi, branch, category, preferences):
        self.name = name
        self.roll = roll
        self.cpi = float(cpi)
        self.category = category
        self.original_branch = branch
        self.alloted_branch = branch
        self.preferences = list(preferences)
        self.eligible = True
        if (category == 'GE' and self.cpi < 8.00):
            self.eligible = False
        if (category != 'GE' and self.cpi < 7.00):
            self.eligible = False


programs = []
with open('branchChange/input_programmes.csv', 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    for row in rows:
        programs.append(Program(row[0], row[1], row[2]))

students = []
with open('branchChange/input_options.csv', 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    for row in rows:
        pref, i = [], 5
        while (i < 20 and row[i] != ''):
            pref.append(row[i])
            i += 1
        students.append(Student(row[1], row[0], row[3], row[2], row[4], pref))

students.sort(key=lambda student: student.cpi, reverse=True)


def find_program(name, programs):
    return [x for x in programs if x.name == name][0]


update = True
while update:
    update = False
    for student in students:
        if student.eligible:
            moved = False
            for pref in student.preferences:
                if pref == student.alloted_branch:
                    break
                if moved:
                    break

                dprog = find_program(pref, programs)
                if (not dprog.blocked) or (dprog.blocked and student.cpi > dprog.bcpi):
                    if student.cpi >= dprog.cutoff:
                        print (f"{student.name}({student.cpi}) moves from {student.alloted_branch} to {dprog.name}")
                        curr = find_program(student.alloted_branch, programs)
                        curr.current -= 1
                        dprog.current += 1
                        student.alloted_branch = dprog.name
                        moved = True
                        update = True
                        dprog.cutoff = min(dprog.cutoff, student.cpi)
                    elif (student.cpi >= 9) or (student.cpi < 9 and dprog.current >= dprog.min):
                        if dprog.current < dprog.max:
                            print (f"{student.name}({student.cpi}) moves from {student.alloted_branch} to {dprog.name}")
                            curr = find_program(student.alloted_branch, programs)
                            curr.current -= 1
                            dprog.current += 1
                            student.alloted_branch = dprog.name
                            moved = True
                            update = True
                            dprog.cutoff = min(dprog.cutoff, student.cpi)
        for pref in student.preferences:
            if pref != student.alloted_branch:
                dprog = find_program(pref, programs)
                dprog.blocked = True
                dprog.bcpi = max(dprog.bcpi, student.cpi)
            else:
                break

    for prog in programs:
        prog.blocked = False
        prog.bcpi = 0.00

output_stats = []
for prog in programs:
    nrow = {
        'Program': prog.name,
        'Cutoff': prog.cutoff,
        'Santioned Strength': prog.sanctioned,
        'Original Strength': prog.original,
        'Final Strength': prog.current
    }
    if nrow['Cutoff'] == 11:
        nrow['Cutoff'] = 'NA'
    output_stats.append(nrow)

writer = csv.DictWriter(open('myoutputstats.csv', 'w'),
                        delimiter=',',
                        fieldnames=[
                            'Program', 'Cutoff', 'Santioned Strength',
                            'Original Strength', 'Final Strength'
                        ])
writer.writerows(output_stats)

allotment = []
for student in students:
    nrow = {
        'Roll': student.roll,
        'Name': student.name,
        'Original': student.original_branch,
        'Alloted': student.alloted_branch
    }
    if nrow['Original'] == nrow['Alloted']:
        nrow['Alloted'] = "Branch Unchanged"
    if not student.eligible:
        nrow['Alloted'] = "Ineligible"
    allotment.append(nrow)

writer = csv.DictWriter(open('myallotment.csv', 'w'),
                        delimiter=',',
                        fieldnames=['Roll', 'Name', 'Original', 'Alloted'])
writer.writerows(allotment)
