import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from processor import process_dataframe
import pandas as pd
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}.xlsx"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Read only headers
            df = pd.read_excel(filepath, nrows=0)
            headers = df.columns.tolist()
            
            return jsonify({
                'filename': filename,
                'headers': headers
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_file():
    data = request.get_json()
    if not data or 'filename' not in data or 'mapping' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    filename = data['filename']
    mapping = data['mapping']
    
    # Security check: filename must be in uploads folder and strict UUID format to avoid path traversal
    # For now, just relying on basename
    filename = os.path.basename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
        
    try:
        # Read the identified file
        df = pd.read_excel(filepath)
        
        # Process with mapping
        processed_df = process_dataframe(df, mapping=mapping)
        
        # Save to memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            processed_df.to_excel(writer, index=False)
        output.seek(0)
        
        # Cleanup: Delete the uploaded file
        try:
           os.remove(filepath)
        except OSError as e:
           print(f"Error deleting temp file: {e}")
        
        return send_file(
            output,
            as_attachment=True,
            download_name='RhinoCRM_importacao.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        print(f"ERROR in /process: {str(e)}") # Log for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    # Legacy upload, to be deprecated or updated later if needed
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
