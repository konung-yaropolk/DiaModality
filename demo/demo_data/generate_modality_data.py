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
    signal_treshold = 1.5
    for _ in range(num_rows):

        # generate data columns:
        col1 = random.uniform(0, 2.7)
        col2 = random.uniform(0, 3.3)
        col3 = random.uniform(0, 7.3)

        # generate binarization columns:
        col4 = 1 if col1 > signal_treshold else ''
        col5 = 1 if col2 > signal_treshold else ''
        col6 = 1 if col3 > signal_treshold else ''

        writer.writerow([col1, col2, col3, col4, col5, col6])
