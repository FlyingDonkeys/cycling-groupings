
# Note, df is the dataframe object while groups is a 2d array, consisting of groups of names in the same group
# Note: For groups, 1st elem is an 1 elem array with the group name
def makeGroups(df, groups, eventGroupSize, numberOfELs):

    # Check if any large groups exist:
    for i in range(len(groups)):
        if (len(groups[i]) - 1 > eventGroupSize):
            print(f'{groups[i][0]} is too large, please note this.')

    # Want to sort individuals by cycling ability first
    # Note that cycling ability questions are in index 36 to 38
    individualScores = [] # Should contain an array with 2 elements, [name, abilityScore]
    groupScores = [] # Should contain an array with 3 elements [[group code], abilityScore, number of people]
    for row in df.itertuples():
        # Check if participant is an individual
        if (row._30.lower().strip() == "individual"):
            abilityScore = 0
            abilityScore += int(row._36[0])
            abilityScore += (4 - int(row._37[0])) # For question 37, the higher, the less competent, to change for next event
            abilityScore += (int(row._38[0]))
            individualScores.append([row._22, abilityScore])
    print(individualScores)

    for group in groups:
        totalAbilityScore = 0

        # Aggregate the ability scores for each member in the group
        for member in group:
            for row in df.itertuples():
                if (row._22 == member):
                    totalAbilityScore += int(row._36[0])
                    totalAbilityScore += (4 - int(row._37[0]))
                    totalAbilityScore += (int(row._38[0]))
                    break

        # Compute average score and add
        groupScores.append([group[0], round(totalAbilityScore / (len(group) - 1), ), len(group) - 1])

    finalGroupings = []
    individualScores = sorted(individualScores, key=lambda x: x[1], reverse=False)
    groupScores = sorted(groupScores, key=lambda x: x[1], reverse=True)
    print(groupScores)

    if (len(groupScores) <= numberOfELs):
        # If we have fewer or equal predetermined groups than EL count, then 1 final group should have 1
        # or fewer predetermined groups. After inserting predetermined groups, fill vacancies with individuals
        for group in groupScores:
            currentSize = group[2]
            currentGroup = [group[0]]
            while (currentSize < eventGroupSize):
                currentGroup.append(individualScores.pop()[0])
                currentSize += 1
            finalGroupings.append(currentGroup)
    else:
        # If we have more predetermined groups than EL count, then 1 final group can have more than 1
        # predetermined group, provided that we dont exceed eventGroupSize
        while groupScores:
            currentSize = 0
            currentGroup = []

            # Logic to form an event group using 1 or more predetermined groups
            pos = len(groupScores) - 1
            while pos >= 0:
                if (currentSize + groupScores[pos][2] <= eventGroupSize):
                    currentSize += groupScores[pos][2]
                    currentGroup.append(groupScores.pop(pos)[0])
                pos -= 1

            # Logic to make each event group have the correct number of people
            while (currentSize < eventGroupSize):
                currentGroup.append(individualScores.pop()[0])
                currentSize += 1
            finalGroupings.append(currentGroup)

    # Account for leftover individuals
    while individualScores:
        currentSize = 0
        currentGroup = []
        while (currentSize < eventGroupSize and individualScores):
            currentGroup.append(individualScores.pop()[0])
            currentSize += 1
        finalGroupings.append(currentGroup)
    print(finalGroupings)


    for group in finalGroupings:
        while (not isinstance(group[0], str)):
            # Then this group consists of 1 predetermined group (i.e: 1 group with same group codes)
            group_code = group[0][0]
            for row in df.itertuples():
                if (row._30 == group_code):
                    group.append(row._22)
            group.pop(0)

    return finalGroupings


