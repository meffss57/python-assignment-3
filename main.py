from analytics import FileManager, DataLoader, ResultSaver, Report
from analytics.analyser import DataAnalyser, CountryAnalyser, GpaAnalyser

fm = FileManager('students.csv')
if not fm.check_file():
    print('Stopping program.')
    exit()
fm.create_output_folder()

dl = DataLoader('students.csv')
dl.load()
dl.preview()

print("\n--- Base class demonstration ---")
base = DataAnalyser(dl.students)
print(base)
base.analyse()

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

analysers[0].lambda_map_filter()

print("\n--- Generating Report ---")
saver = ResultSaver(analysers[0].result, 'output/result.json')
report = Report(analysers[0], saver)
report.generate()

print("\n--- Testing exception handling ---")
test_loader = DataLoader("wrong_file.csv")
test_loader.load()