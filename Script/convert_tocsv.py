import json
import pandas as pd

# Đọc file JSON
input_file = "../Data/cleaned_data.json"
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Chuyển thành DataFrame
df = pd.DataFrame(data)

# Lưu thành CSV
output_file = "../Data/Data_tcd.csv"
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"Saved to {output_file}")