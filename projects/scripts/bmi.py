bmi_value = 27


# wraph the code in a function
def classify_bmi(bmi):
    
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    print(category)

    classify_bmi(bmi_value)

