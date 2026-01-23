init python:
    test = 0

label voting_start:
    "Voting starts!"
    jump voting_end

label voting_end:
    "Voting Ends!"
    jump night_start