def convertGradeToPercentage(grade):
    if 1.0 <= grade <= 1.05:
        return 100
    elif 1.05 < grade <= 1.11:
        return 99
    elif 1.11 < grade <= 1.17:
        return 98
    elif 1.17 < grade <= 1.24:
        return 97
    elif 1.24 < grade <= 1.32:
        return 96
    elif 1.32 < grade <= 1.4:
        return 95
    elif 1.40 < grade <= 1.5:
        return 94
    elif 1.5 < grade <= 1.57:
        return 93
    elif 1.57 < grade <= 1.65:
        return 92
    elif 1.65 < grade <= 1.74:
        return 91
    elif 1.74 < grade <= 1.82:
        return 90
    elif 1.82 < grade <= 1.9:
        return 89
    elif 1.90 < grade <= 1.99:
        return 88
    elif 1.99 < grade <= 2.07:
        return 87
    elif 2.07 < grade <= 2.15:
        return 86
    elif 2.15 < grade <= 2.24:
        return 85
    elif 2.24 < grade <= 2.32:
        return 84
    elif 2.32 < grade <= 2.4:
        return 83
    elif 2.4 < grade <= 2.49:
        return 82
    elif 2.49 < grade <= 2.57:
        return 81
    elif 2.57 < grade <= 2.65:
        return 80
    elif 2.65 < grade <= 2.74:
        return 79
    elif 2.74 < grade <= 2.82:
        return 78
    elif 2.82 < grade <= 2.9:
        return 77
    elif 2.9 < grade <= 3.99:
        return 76
    elif 3.99 < grade <= 3.1:
        return 75
    else:
        return 0  # Indicates an invalid grade


def checkStatus(grade):
    if grade <= 3.00 and grade >= 1.00:
        return "P"
    elif grade <= 4.00:
        return "Inc."
    else:
        return "D"