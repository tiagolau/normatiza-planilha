import pandas as pd
import re

def normalize_phone(value):
    """
    Normalizes phone number to DDD + 9 digits (11 digits total).
    Handles:
    - Stripping non-numeric chars
    - Removing country code (55) if present and length > 11
    - Ensuring 9 digits for mobile (adding 9 if missing, though risky without knowing if it's 8 or 9 digits originally, assuming standard mobile) - *Wait, simple 11 digits enforcement is safer first.*
    
    Correction based on user request: "DDD+celular 9 dígitos"
    """
    if pd.isna(value):
        return ''
    
    # Strip non-digits
    digits = re.sub(r'\D', '', str(value))
    
    # Handle Country Code 55 (Brazil)
    # If starts with 55 and length is 12 or 13 (55 + 10 or 55 + 11), strip 55
    if digits.startswith('55') and len(digits) > 11:
        digits = digits[2:]
        
    # Validation/Formatting logic
    # Rule for missing 9th digit:
    # If length is 10 digits (DDD + 8 digits), we treat it as a mobile missing the 9.
    # We insert '9' after the DDD (first 2 digits).
    if len(digits) == 10:
        digits = digits[:2] + '9' + digits[2:]
    
    return digits

def process_dataframe(df):
    """
    Normalizes the input dataframe to match RhinoCRM_gabarito format.
    1. Rename columns: ALUNO -> Nome, EMAIL -> Email, CELULAR -> Numero
    2. Normalize Numero to digits only
    3. Return only required columns
    """
    # Mapping dictionary
    column_mapping = {
        'ALUNO': 'Nome',
        'EMAIL': 'Email',
        'CELULAR': 'Numero'
    }
    
    # Check if required columns exist (case insensitive search could be better, but sticking to exact match from analysis)
    # The user analysis showed exact headers: ALUNO, EMAIL, CELULAR
    
    # Rename columns
    # We use a copy to avoid SettingWithCopy warnings if it's a slice
    processed_df = df.rename(columns=column_mapping).copy()
    
    # Ensure all target columns exist, create them if missing (though they should exist based on mapping)
    target_columns = ['Numero', 'Nome', 'Email']
    
    for col in target_columns:
        if col not in processed_df.columns:
            # If a separate input format is used, this might fail or we could add empty info
            processed_df[col] = ''
            
    # Normalize phone numbers
    processed_df['Numero'] = processed_df['Numero'].apply(normalize_phone)
    
    # Select and reorder columns
    processed_df = processed_df[target_columns]
    
    return processed_df
