init python:
    test = 0

label night_start:
    "Night starts!"
    jump night_end

label night_end:
    "Night Ends!"
    jump morning_start