import unittest
import pandas as pd
import io
import os
import json
from app import app, UPLOAD_FOLDER

class TestFlexibleMapping(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        # Ensure upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
    def test_full_flow(self):
        # 1. Create Dummy Excel
        df = pd.DataFrame({
            'Nome Completo': ['João Silva', 'Maria Souza'],
            'Tel Casa': ['11999999999', '21888888888'],
            'Whatsapp': ['11977777777', None]
        })
        
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        
        # 2. Test /analyze
        response = self.client.post('/analyze', data={
            'file': (excel_buffer, 'test.xlsx')
        }, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('filename', data)
        self.assertIn('Nome Completo', data['headers'])
        
        filename = data['filename']
        
        # 3. Test /process
        payload = {
            'filename': filename,
            'mapping': {
                'Nome': 'Nome Completo',
                'Telefones': ['Tel Casa', 'Whatsapp']
            }
        }
        
        response = self.client.post('/process', 
                                  data=json.dumps(payload),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Load result from response
        result_buffer = io.BytesIO(response.data)
        result_df = pd.read_excel(result_buffer)
        
        # Validation
        # João: 2 rows
        joao = result_df[result_df['Nome'] == 'João Silva']
        self.assertEqual(len(joao), 2)
        
        # Maria: 1 row
        maria = result_df[result_df['Nome'] == 'Maria Souza']
        self.assertEqual(len(maria), 1)
        
        # Columns
        expected_cols = ['Numero', 'Nome', 'Email']
        for col in expected_cols:
            self.assertIn(col, result_df.columns)
            
        print("\n✅ Verification Passed!")

if __name__ == '__main__':
    unittest.main()
