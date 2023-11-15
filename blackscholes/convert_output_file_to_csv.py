import csv

# Specify the input and output file paths
input_file = "output_features.txt"    # Replace with your input file path
output_file = "output_features.csv"  

# Read the values from the input text file
with open(input_file, "r") as text_file:
    lines = text_file.readlines()

# Open the output CSV file for writing
with open(output_file, "w", newline="") as csv_file:
    csvwriter = csv.writer(csv_file)

    # Write each value to a separate row in the CSV file
    for line in lines:
        csvwriter.writerow([line.strip()])

print(f"Conversion from {input_file} to {output_file} complete.")
