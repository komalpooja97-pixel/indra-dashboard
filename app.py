import os
from dotenv import load_dotenv
import google.generativeai as genai
import csv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

with open('settlement_data.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

text = '\n'.join([','.join(row) for row in data])

prompt = f"""
Analyze the following settlement data and detect anomalies using these rules:
- RULE 1: variance_pct > 500% = CRITICAL price spike
- RULE 2: variance_pct > 15% or < -15% = WARNING high variance
- RULE 3: Uplift charge actual > baseline * 1.20 = WARNING uplift spike
- RULE 4: expected_value_usd < 0 and actual = 0 = CRITICAL missing credit
- RULE 5: expected_value_usd > 1000 and actual = 0 = WARNING missing charge

Data:
{text}

Please list any anomalies found, specifying the rule and the row details.
"""

model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content(prompt)
print(response.text)