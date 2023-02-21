import csv
import Parser
import pandas as pd


# theme = input("Enter the theme: ")
# pages = int(input("Enter max page: "))
# file_name = input("Enter file name: ") + ".csv"
theme = "python"
pages = 1
file_name = "data1.csv"

# , encoding="utf-8"
with open(file_name, "a", newline='') as file:
    column_name = ["Title", "Specialization", "Salary", "Age", "Employment", "Work schedule",
                   "Experience years", "Experience month", "Citizenship", "Sex", "link to resume"]
    writer = csv.writer(file)
    writer.writerow(column_name)

Parser.go_throw_pages(theme, pages, file_name)


# f = pd.read_csv()
