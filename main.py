import os
import csv
import json


# ═══════════════════════════════════════════════════════════════
# CLASS FileManager
# Practice 6 Task 1 | Covers: Practice 4 Task B1, Practice 5 Task B1
# Responsibility: check if CSV exists, create output folder
# ═══════════════════════════════════════════════════════════════
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        """Check if the data file exists. Returns True/False."""
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found. Please download the file from LMS.")
            return False

    def create_output_folder(self, folder='output'):
        """Create output folder if it does not exist."""
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


# ═══════════════════════════════════════════════════════════════
# CLASS DataLoader
# Practice 6 Task 2 | Covers: Practice 4 Task B2, Practice 5 Tasks B1 + B4
# Responsibility: load CSV data, preview rows, exception handling
# ═══════════════════════════════════════════════════════════════
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        """
        Load CSV file into self.students using csv.DictReader.
        Practice 5 Task B4: wrapped in try/except FileNotFoundError.
        """
        print("Loading data...")
        try:
            with open(self.filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.students = list(reader)
            print(f"Data loaded successfully: {len(self.students)} students")
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the filename.")
        except Exception as e:
            print(f"Error: {e}")
        return self.students

    def preview(self, n=5):
        """
        Print first n rows: student_id, age, gender, country, GPA.
        Practice 5 Task B1: n has default value 5.
        """
        print(f"First {n} rows:")
        print("-" * 30)
        for student in self.students[:n]:
            print(
                f"{student['student_id']} | "
                f"{student['age']} | "
                f"{student['gender']} | "
                f"{student['country']} | "
                f"GPA: {student['GPA']}"
            )
        print("-" * 30)


# ═══════════════════════════════════════════════════════════════
# CLASS ResultSaver
# Practice 6 Task 4 | Covers: Practice 4 Task B4
# Responsibility: save result dictionary to JSON file
# ═══════════════════════════════════════════════════════════════
class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        """Save self.result to JSON with indent=4. Handles write errors."""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"Result saved to {self.output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")


# ═══════════════════════════════════════════════════════════════
# CLASS DataAnalyser — Base Class
# Practice 7 Task 1
# Defines shared structure: analyse() placeholder, print_results(), __str__
# ═══════════════════════════════════════════════════════════════
class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        """Placeholder — must be overridden in every child class."""
        print("Not implemented — use a child class")

    def print_results(self):
        """Base version: prints each key: value from self.result."""
        for key, value in self.result.items():
            print(f"{key}: {value}")

    def __str__(self):
        return f"DataAnalyser: base class, {len(self.students)} students"


# ═══════════════════════════════════════════════════════════════
# CLASS CountryAnalyser — Child Class (Variant B)
# Practice 7 Tasks 2 & 3
# Inherits DataAnalyser. Overrides analyse(), print_results(), __str__.
# Contains lambda/map/filter (Practice 5 Task B3).
# ═══════════════════════════════════════════════════════════════
class CountryAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)   # calls DataAnalyser.__init__

    def analyse(self):
        """
        Practice 4 Task B3 / Practice 5 Task B2 — analyse_countries logic.
        Counts students per country, finds top 3 using sorted() + lambda.
        Practice 5 Task B4: try/except ValueError per row, skips with continue.
        """
        country_counts = {}
        for student in self.students:
            try:
                country = student['country']
                if country in country_counts:
                    country_counts[country] += 1
                else:
                    country_counts[country] = 1
            except ValueError:
                print(
                    f"Warning: could not convert value for student "
                    f"{student.get('student_id', '?')} — skipping row."
                )
                continue

        top_3 = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(country_counts),
            "top_3_countries": [{"country": c, "count": n} for c, n in top_3],
            "all_countries": country_counts
        }
        return self.result

    def print_results(self):
        """
        Practice 7 Task 3 — Overrides base print_results().
        Adds formatted COUNTRY ANALYSIS REPORT header/footer.
        Calls super().print_results() to reuse base class key: value loop.
        """
        print("=" * 30)
        print("COUNTRY ANALYSIS REPORT")
        print("=" * 30)
        super().print_results()
        print("=" * 30)

    def lambda_map_filter(self):
        """
        Practice 5 Task B3 — Lambda / Map / Filter.
        filter() GPA > 3.5, map() all GPA values, filter() attendance > 90%.
        """
        high_gpa = list(filter(lambda s: float(s['GPA']) > 3.5, self.students))
        gpa_values = list(map(lambda s: float(s['GPA']), self.students))
        good_attendance = list(
            filter(lambda s: float(s['class_attendance_percent']) > 90, self.students)
        )

        print("-" * 30)
        print("Lambda / Map / Filter")
        print("-" * 30)
        print(f"Students with GPA > 3.5      : {len(high_gpa)}")
        print(f"GPA values (first 5)         : {gpa_values[:5]}")
        print(f"Students attendance > 90%    : {len(good_attendance)}")
        print("-" * 30)

    def __str__(self):
        return f"CountryAnalyser: Country Analysis, {len(self.students)} students"


# ═══════════════════════════════════════════════════════════════
# CLASS GpaAnalyser — Second Child Class (Variant A logic)
# Practice 7 Task 5 — needed for polymorphism demonstration
# Same interface as CountryAnalyser, different behaviour
# ═══════════════════════════════════════════════════════════════
class GpaAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        """GPA analysis — avg, max, min, count of students with GPA > 3.5."""
        gpas = []
        for student in self.students:
            try:
                gpas.append(float(student['GPA']))
            except ValueError:
                print(
                    f"Warning: could not convert value for student "
                    f"{student.get('student_id', '?')} — skipping row."
                )
                continue

        self.result = {
            "analysis": "GPA Statistics",
            "total_students": len(self.students),
            "average_gpa": round(sum(gpas) / len(gpas), 2),
            "max_gpa": max(gpas),
            "min_gpa": min(gpas),
            "high_performers": sum(1 for g in gpas if g > 3.5)
        }
        return self.result

    def print_results(self):
        """Overrides base — adds GPA ANALYSIS REPORT header/footer."""
        print("=" * 30)
        print("GPA ANALYSIS REPORT")
        print("=" * 30)
        super().print_results()
        print("=" * 30)

    def __str__(self):
        return f"GpaAnalyser: GPA Statistics, {len(self.students)} students"


# ═══════════════════════════════════════════════════════════════
# CLASS Report — Association (USES-A)
# Practice 7 Task 4
# Does NOT inherit — holds references to analyser and saver
# ═══════════════════════════════════════════════════════════════
class Report:
    def __init__(self, analyser, saver):
        self.analyser = analyser    # USES-A DataAnalyser
        self.saver = saver          # USES-A ResultSaver

    def generate(self):
        print("Generating report...")
        self.analyser.analyse()
        self.analyser.print_results()
        self.saver.save_json()
        print("Report complete.")


# ═══════════════════════════════════════════════════════════════
# MAIN — only objects and method calls, no logic here
# ═══════════════════════════════════════════════════════════════

# Step 1 — File and folder check (Practice 4 Task B1)
fm = FileManager('students.csv')
if not fm.check_file():
    print('Stopping program.')
    exit()
fm.create_output_folder()

# Step 2 — Load and preview data (Practice 4 Task B2)
dl = DataLoader('students.csv')
dl.load()
dl.preview()

# Step 3 — Base class demonstration (Practice 7 Task 1)
print("\n--- Base class demonstration ---")
base = DataAnalyser(dl.students)
print(base)
base.analyse()

# Step 4 — Polymorphism (Practice 7 Task 5)
# Same interface (analyse + print_results), different behaviour per class
print("\n" + "-" * 30)
print("Running all analysers:")
print("-" * 30)

analysers = [
    CountryAnalyser(dl.students),
    GpaAnalyser(dl.students)
]

for a in analysers:
    print(a)
    a.analyse()
    a.print_results()

# Step 5 — Lambda / Map / Filter (Practice 5 Task B3)
analysers[0].lambda_map_filter()

# Step 6 — Report via Association (Practice 7 Task 4)
print("\n--- Generating Report ---")
saver = ResultSaver(analysers[0].result, 'output/result.json')
report = Report(analysers[0], saver)
report.generate()

# Step 7 — Exception handling test (Practice 5 Task B4)
print("\n--- Testing exception handling ---")
test_loader = DataLoader("wrong_file.csv")
test_loader.load()