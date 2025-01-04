
# Note, df is the dataframe object while groups is a 2d array, consisting of groups of names in the same group
def makeGroups(df, groups):

    # Want to sort individuals by cycling ability first
    # Note that cycling ability questions are in index 36 to 38
    individualScores = [] # Should contain a array with 2 elements, [name, abilityScore]
    for row in df.itertuples():
        # Check if participant is an individual
        if (row._30.lower().strip() == "individual"):
            abilityScore = 0
            abilityScore += int(row._36[0])
            abilityScore += (4 - int(row._37[0])) # For question 37, the higher the less competent, to change for next event
            abilityScore += (int(row._38[0]))
            individualScores.append([row._22, abilityScore])
    print(individualScores)
    return


