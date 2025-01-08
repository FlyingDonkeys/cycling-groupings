import math

import pandas as pd
import getGroups as gg
import makeGroups as mg


def main():

    # Extract number of ELs
    numberOfELs = int(input("Enter the number of ELs for this event: "))
    # Path to input file
    input_file = "CSV Files/FormSubmissions (2).csv"

    # Read the input CSV, note that NUSync imported forms start column titles on row 3
    df = pd.read_csv(input_file, header=1)
    # Extract the distinct group names as a list
    groupNames = gg.getGroups(df)
    # Calculate maximum group size for this event
    maxGroupSize = math.ceil(len(df) / numberOfELs)

    # Extract the members of each group
    # Groups is an array with elements in the form [[groupName], member1, member2, ...]
    groups = []
    for groupName in groupNames:
        members = [[groupName]]
        for row in df.itertuples():
            if row._30 == groupName:
                members.append(row._22) # Note full name is stored in column _22
        groups.append(members)

    # Group participants by skill level
    # Note: groupingsArray is a 2d array containing groups of participant names
    groupingsArray = mg.makeGroups(df, groups, maxGroupSize, numberOfELs)
    print(groupingsArray)

    # Step 1: Normalize the groups to have the same length by padding with None
    max_group_size = max(len(group) for group in groupingsArray)
    normalized_groups = [
        group + [None] * (max_group_size - len(group))  # Pad with None
        for group in groupingsArray
    ]

    # Step 2: Create a DataFrame where each column is a group
    group_columns = {f"Group {i + 1}": normalized_groups[i] for i in range(len(groupingsArray))}
    groupings_df = pd.DataFrame(group_columns)
    header = "Note: Group 1 is the strongest group, followed by Group 2, Group 3, etc."
    note_row = [header] + [None] * (len(group_columns) - 1)  # Place the note in the first column
    groupings_df.loc[len(groupings_df)] = note_row  # Append the row to the bottom

    # Step 3: Save the DataFrame to a CSV file
    output_file = "CSV Files/Output.csv"
    groupings_df.to_csv(output_file, index=False)
    print(f"Grouped participants saved to {output_file}")


if __name__ == "__main__":
    main()
