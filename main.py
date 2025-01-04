import pandas as pd
import getGroups as gg
import makeGroups as mg


def main():

    numberOfGroups = input("How many ELs are taking part in this event? ")
    # Path to input file
    input_file = "CSV Files/FormSubmissions (2).csv"

    # Read the input CSV, note that NUSync imported forms start column titles on row 3
    df = pd.read_csv(input_file, header=1)
    # Extract the distinct group names as a list
    groupNames = gg.getGroups(df)

    # Extract the members of each group
    groups = []
    for groupName in groupNames:
        members = [[groupName]]
        for row in df.itertuples():
            if row._30 == groupName:
                members.append(row._22) # Note full name is stored in column _22
        groups.append(members)

    # Group participants by skill level
    groupingsdf = mg.makeGroups(df, groups, numberOfGroups)

    # Save the output CSV
    output_file = "CSV Files/Output.csv"
    df.to_csv(output_file, index=False)
    print(f"Processed file saved to {output_file}")


if __name__ == "__main__":
    main()
