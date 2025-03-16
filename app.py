import os
import pandas as pd
import logging
from flask import Flask, render_template, request, send_file
from fuzzywuzzy import process
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(filename='sku_mapping.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

class SKUMapper:
    def __init__(self, mapping_file):
        self.mapping_file = mapping_file
        self.sku_msku_mapping = self.load_mapping()
        self.generated_msku = {}
        self.counter = 1

    def load_mapping(self):
        try:
            df = pd.read_csv(self.mapping_file, encoding='latin1')
            if 'FNSKU' in df.columns and 'MSKU' in df.columns:
                df.rename(columns={'FNSKU': 'SKU'}, inplace=True)
                df['SKU'] = df['SKU'].astype(str).str.strip().str.upper()
                logging.info("Loaded SKU-MSKU mapping file.")
                return df[['SKU', 'MSKU']].drop_duplicates()
            else:
                logging.error("Mapping file missing required columns.")
                return None
        except Exception as e:
            logging.error(f"Error loading mapping file: {e}")
            return None

    def generate_msku(self, sku):
        if sku in self.generated_msku:
            return self.generated_msku[sku]
        
        msku = f"MSKU_{sku[:3].upper()}_{str(self.counter).zfill(4)}"
        self.generated_msku[sku] = msku
        self.counter += 1
        return msku

    def map_sku_to_msku(self, sku):
        if self.sku_msku_mapping is None:
            logging.error("Mapping data not loaded.")
            return self.generate_msku(sku)

        sku = str(sku).strip().upper()
        match = self.sku_msku_mapping[self.sku_msku_mapping['SKU'] == sku]

        if not match.empty:
            return match['MSKU'].values[0]

        best_match, score = process.extractOne(sku, self.sku_msku_mapping['SKU'].tolist())
        if score > 80:
            logging.info(f"Fuzzy matched {sku} to {best_match} with score {score}")
            return self.sku_msku_mapping[self.sku_msku_mapping['SKU'] == best_match]['MSKU'].values[0]

        logging.warning(f"No match found for SKU: {sku}. Generating new MSKU.")
        return self.generate_msku(sku)

    def process_sku_files(self, files, output_file):
        all_data = []

        for file in files:
            try:
                df = pd.read_csv(file, encoding='latin1')
                if 'SKU' in df.columns:
                    df['Mapped_MSKU'] = df['SKU'].apply(self.map_sku_to_msku)
                    df['Source_File'] = file.filename  # Keep track of original file name
                    all_data.append(df)
                else:
                    logging.error(f"File {file.filename} missing SKU column.")
            except Exception as e:
                logging.error(f"Error processing file {file.filename}: {e}")

        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df.to_csv(output_file, index=False)
            logging.info(f"All SKUs processed and saved to {output_file}")
            return output_file
        else:
            logging.error("No valid data to process.")
            return None

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'files' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('files')

    if not files or all(file.filename == '' for file in files):
        return "No selected files", 400

    mapper = SKUMapper("mapping.csv")  # Load SKU-MSKU mapping
    output_path = os.path.join(app.config['PROCESSED_FOLDER'], "final_sku_mapping.csv")
    result_file = mapper.process_sku_files(files, output_path)

    if result_file:
        return send_file(result_file, as_attachment=True)
    else:
        return "Processing failed", 500

if __name__ == '__main__':
    app.run(debug=True)
