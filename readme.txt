Link


https://airtable.com/invite/l?inviteId=invqLwryQ4118ENdR&inviteToken=086663eebee14ab2311a122c0948c5ad3e7d0c31d0e553ed3e2752bc68717fdd&utm_medium=email&utm_source=product_team&utm_content=transactional-alerts
Upload processed .csv file in the table columns



# **SKU Mapping Flask Web App**  

A simple Flask web application that allows users to upload multiple CSV files containing SKUs and maps them to MSKUs using an existing mapping file. The processed data from all files is combined into a single CSV file for download.

---

## **📌 Features**  
✅ Upload multiple CSV files at once  
✅ Map SKUs to MSKUs using exact and fuzzy matching  
✅ Automatically generate MSKUs for unmatched SKUs  
✅ Combine all processed data into a single CSV file  
✅ Download the final processed file  

---

## **🚀 Installation & Setup**  

### **1️⃣ Install Dependencies**
Make sure Python (>=3.7) is installed. Then, install the required dependencies:  

```bash
pip install flask requirements.txt
```

---

### **2️⃣ Run the Flask Application**
```bash
python app.py
```
This will start a local web server.  

---

### **3️⃣ Open the Web App**  
Go to:  
👉 **http://127.0.0.1:5000/** in your browser.  

---

### **4️⃣ Upload and Process Files**
1. Select multiple CSV files containing SKUs.  
2. Click **"Upload and Process"**.  
3. The system maps SKUs to MSKUs and merges data into a single CSV file.  
4. Download the processed file.  

---

## **🛠 File Structure**
```
/sku-mapping-flask
│── /uploads            # Temporary uploaded files
│── /processed          # Processed and combined output file
│── /templates          
│   ├── upload.html     # Web interface for file upload
│── app.py              # Main Flask application
│── mapping.csv         # Predefined SKU-MSKU mapping file
│── requirements.txt    # List of dependencies
│── README.md           # Documentation
``