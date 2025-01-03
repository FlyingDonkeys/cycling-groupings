import pandas as pd
import getGroups as gg

def main():

    # Path to input file
    input_file = "CSV Files/FormSubmissions.csv"

    # Read the input CSV, note that NUSync imported forms start column titles on row 3
    df = pd.read_csv(input_file, header=1)

    # Extract the distinct group names as a list
    groupNames = gg.getGroups(df)

    # Extract the members of each group
    groups = []
    for groupName in groupNames:
        members = []
        for row in df.itertuples():
            if row._29 == groupName:
                members.append(row._21)
        groups.append(members)

    # Save the output CSV
    output_file = "CSV Files/New.csv"
    df.to_csv(output_file, index=False)
    print(f"Processed file saved to {output_file}")


if __name__ == "__main__":
    main()
