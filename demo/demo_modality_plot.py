#!/usr/bin/env python
import DiaModality.scsv as csv
import DiaModality.ModalityPlot as plt
import os

if __name__ == '__main__':

    # input files in the demo folder:
    files = [
         'demo_data\modality_data.csv'
    ]

    for file in files:

        # Get full path of input files
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, file)

        # Parse data from csv file
        new_csv = csv.OpenFile(file_path)
        data, binarization = new_csv.GetRows(3, 3)

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
                                dpi=200,
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
