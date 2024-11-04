# DiaModality - The Modality Diagram

Simple tool to plot vector modality diagram

### To install package run the command:
```bash
pip install diamodality
```


### How to use:
See the /demo directory on Git repo or  
create and run the following two files:

---
``generate_sample_data.py``:
```python
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

    # Generate the data
    for _ in range(num_rows):
        col1 = random.uniform(0, 2.7)
        col2 = random.uniform(0, 3.3)
        col3 = random.uniform(0, 7.3)

        col4 = 1 if col1 > 1.5 else ''
        col5 = 1 if col2 > 1.5 else ''
        col6 = 1 if col3 > 1.5 else ''

        writer.writerow([col1, col2, col3, col4, col5, col6])

```


---
``plot_sample_data.py``:
```python
import DiaModality.CsvParser as csv
import DiaModality.ModalityPlot as plt
import os

# input file:
files = 'modality_data.csv'

# Get full path of input files
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, file)

# Parse data from csv file
new_csv = csv.LoadCsv(file_path)
data, binarization = new_csv.ParseCsv(3, 3)

# Make figure:
plot = plt.ModalityPlot(data,
                        binarization,
                        modalities=[
                            'Set 1', 'Set 2', 'Set 3'],
                        angles=[210, 90, 330],
                        labels=False,
                        scalecircle=0.5,           # Scale circle radius
                        scalecircle_linestyle=':',
                        scalecircle_linewidth=0.75,
                        marker='',                 # vector endpoints marker
                        linestyle='-',
                        linewidth=0.5,
                        alpha=0.5,
                        same_scale=False,          # Draw all the subplots in the same scale
                        full_center=True,          # Draw all vectors in the central subplot, else draw trimodal vectors only
                        whole_sum=True,            # Calculate all three modality vectors despite binarization
                        figsize=(10, 10),
                        title='Modality Diagram Example',
                        colors=(
                            'tab:green',   # Set 1 color
                            'navy',        # Set 2 color
                            'tab:red',     # Set 3 color
                            '#1E88E5',     # Sets 1 & 2 intersection color
                            '#FF9933',     # Sets 1 & 3 intersection color
                            '#9900FF',     # Sets 2 & 3 intersection color
                            'black',       # All sets   intersection color
                        ),      
        )

plot.save(file_path, type='png', transparent=False)
plot.show()
```

Source page: 
https://github.com/konung-yaropolk/DiaModality


![modality_data csv](https://github.com/user-attachments/assets/eb77b4d7-281f-45b0-a5ce-4c2442fc9a75)
