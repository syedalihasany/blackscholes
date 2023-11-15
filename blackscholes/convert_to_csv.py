import csv

# Specify the input and output file paths
input_file = "input_features.txt"  # Replace with your input file path
output_file = "input_features.csv"  # Replace with your desired output file path

# Open the input text file for reading
with open(input_file, "r", newline="") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")

    # Open the output CSV file for writing
    with open(output_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        # Loop through the TSV file and write its content to the CSV file
        for row in tsvreader:
            csvwriter.writerow(row)

print(f"Conversion from {input_file} to {output_file} complete.")
