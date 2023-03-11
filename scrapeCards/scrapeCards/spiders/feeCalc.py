def feeCalc(input):
    if input < 0.03:
        return 0
    elif input >= 0.03 and input < 0.22:
        return input - 0.02
    elif input >= 0.22 and input < 0.33:
        return input - 0.03
    elif input >= 0.33 and input < 0.44:
        return input - 0.04
    elif input == 0.44:
        return input - 0.05
    elif input >= 0.45 and input < 0.56:
        return input - 0.06
    elif input >= 0.56 and input < 0.67:
        return input - 0.07
    elif input == 0.67:
        return input - 0.08
    elif input >= 0.68 and input < 0.79:
        return input - 0.09
    elif input >= 0.79 and input < 0.9:
        return input - 0.1
    elif input == 0.9:
        return input - 0.11
    elif input >= 0.91 and input < 1.02:
        return input - 0.12
    else:
        return -1