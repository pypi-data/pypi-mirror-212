import re
import pandas as pd

# Regular expression patterns
ICD9_REGEX = "|".join([
    r"\d{3}\.?\d{0,2}",
    r"E\d{3}\.?\d?",
    r"V\d{2}\.?\d{0,2}"
])
ICD10_REGEX = r"[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}"

def validate_icd9(code):
    if re.match(ICD9_REGEX, code):
        return f"{code} is a valid ICD-9 code"
    else:
        return f"{code} is not a valid ICD-9 code"

def validate_icd10(code):
    if re.match(ICD10_REGEX, code):
        return f"{code} is a valid ICD-10 code"
    else:
        return f"{code} is not a valid ICD-10 code"

def validate_codes_from_csv(input_file, column_name, icd_version=9):
    if icd_version == 9:
        validator = validate_icd9
    elif icd_version == 10:
        validator = validate_icd10
    else:
        raise ValueError("Invalid ICD version, must be 9 or 10")

    df = pd.read_csv(input_file)
    df['Validation'] = df[column_name].apply(validator)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df)
