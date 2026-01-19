import os
from flask import Flask, render_template, request, send_file
from processor import process_dataframe
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        try:
            # Read the uploaded file
            df = pd.read_excel(file)
            
            # Process the dataframe
            processed_df = process_dataframe(df)
            
            # Save to memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                processed_df.to_excel(writer, index=False)
            output.seek(0)
            
            return send_file(
                output,
                as_attachment=True,
                download_name='RhinoCRM_importacao.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
