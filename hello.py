import praw
import csv


input_file = csv.DictReader(open("nyse-listed_csv.csv"))
for row in input_file:
    writer = csv.DictWriter
    if ("Common Stock" in row['Company Name']):
        print(row)
        
        
    