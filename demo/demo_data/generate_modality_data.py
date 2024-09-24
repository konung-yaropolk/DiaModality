import csv
import random
import os

num_rows = 1500
output_file = 'modality_data.csv'

# locate working directory
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, output_file)

# Open a new CSV file to write the data
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    # writer.writerow(['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6'])

    # Generate the data
    for _ in range(num_rows):
        col1 = random.uniform(0, 2.7)
        col2 = random.uniform(0, 1.9)
        col3 = random.uniform(0, 2.3)

        col4 = 1 if col1 > .5 else ''
        col5 = 1 if col2 > .3 else ''
        col6 = 1 if col3 > .7 else ''

        writer.writerow([col1, col2, col3, col4, col5, col6])
