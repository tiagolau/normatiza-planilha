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

def process_dataframe(df, mapping=None):
    """
    Normalizes the input dataframe.
    
    Args:
        df: Input pandas DataFrame
        mapping: Optional dictionary with 'Nome' (str) and 'Telefones' (list of str)
                 If None, uses legacy hardcoded 'ALUNO', 'EMAIL', 'CELULAR'.
    """
    # 1. Handle Legacy Mode (Backwards Compatibility)
    if not mapping:
        column_mapping = {
            'ALUNO': 'Nome',
            'EMAIL': 'Email',
            'CELULAR': 'Numero'
        }
        processed_df = df.rename(columns=column_mapping).copy()
        
        # Add missing columns
        for col in ['Numero', 'Nome', 'Email']:
            if col not in processed_df.columns:
                processed_df[col] = ''
                
        # Normalize
        processed_df['Numero'] = processed_df['Numero'].apply(normalize_phone)
        return processed_df[['Numero', 'Nome', 'Email']]

    # 2. Handle Dynamic Mode
    # mapping = { 'Nome': 'ColName', 'Telefones': ['Tel1', 'Tel2'] }
    
    name_col = mapping.get('Nome')
    phone_cols = mapping.get('Telefones', [])
    
    # Rename Name Column
    processed_df = df.rename(columns={name_col: 'Nome'}).copy()
    
    # Identify other columns to keep (Like Email) - Optional for now as requirements focused on Name/Phone
    # If we want to keep Email, we'd need to ask for it in the mapping or guess it.
    # For now, we'll try to guess 'Email' if it exists in the original headers, otherwise leave blank.
    email_col = None
    for col in df.columns:
        if 'email' in col.lower():
            email_col = col
            break
    
    if email_col:
        processed_df = processed_df.rename(columns={email_col: 'Email'})
    else:
        processed_df['Email'] = ''

    # Explode Rows (Melt) if multiple phones or just one phone
    # We want to transform all phone columns into one 'Numero' column
    
    # Columns to keep fixed (Identifier variables)
    id_vars = ['Nome', 'Email']
    
    # Ensure these cols exist (Name is guaranteed by rename above)
    for col in id_vars:
        if col not in processed_df.columns:
            processed_df[col] = ''
            
    # Melt!
    # If phone_cols is empty (edge case), we just return empty nums? No, validation prevents this.
    try:
        # Only melt if we have phone columns to melt
        if phone_cols:
             processed_df = processed_df.melt(
                id_vars=id_vars,
                value_vars=phone_cols,
                var_name='Tipo_Original',
                value_name='_Numero_Temp'
            )
             processed_df = processed_df.rename(columns={'_Numero_Temp': 'Numero'})
        else:
             processed_df['Numero'] = ''
             
    except KeyError as e:
        # Fallback if a column is missing
        print(f"Error during melt: {e}")
        processed_df['Numero'] = ''

    # Normalize
    processed_df['Numero'] = processed_df['Numero'].apply(normalize_phone)
    
    # Remove empty numbers (artifacts of melt)
    processed_df = processed_df[processed_df['Numero'] != '']
    
    # Sort by Name for better readability
    processed_df = processed_df.sort_values(by='Nome')
    
    return processed_df[['Numero', 'Nome', 'Email']]
