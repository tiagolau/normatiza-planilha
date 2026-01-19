import unittest
import pandas as pd
from processor import process_dataframe

class TestProcessor(unittest.TestCase):
    def test_process_dataframe(self):
        # Create sample data
        data = {
            'ALUNO': ['João Silva', 'Maria Souza'],
            'EMAIL': ['joao@test.com', 'maria@test.com'],
            'CELULAR': ['(11) 99999-9999', '21988887777'],
            'CPF': ['111.111.111-11', '222.222.222-22'],  # Irrelevant column
            'Outro': [1, 2] # Irrelevant column
        }
        df = pd.DataFrame(data)
        
        # Process
        result = process_dataframe(df)
        
        # Assertions
        expected_columns = ['Numero', 'Nome', 'Email']
        self.assertEqual(list(result.columns), expected_columns)
        
        # Check normalization
        self.assertEqual(result.iloc[0]['Numero'], '11999999999') # Stripped () -
        self.assertEqual(result.iloc[1]['Numero'], '21988887777') # Already cleanish
        
        # Check renaming
        self.assertEqual(result.iloc[0]['Nome'], 'João Silva')
        self.assertEqual(result.iloc[0]['Email'], 'joao@test.com')

if __name__ == '__main__':
    unittest.main()
