import pandas as pd
import json

# Read the JSON file
with open('new_assg\course_details.json', 'r') as f:
    data = json.load(f)

# Convert to a pandas DataFrame
df = pd.DataFrame(data)

# Write to an Excel file
df.to_excel('outputf.xlsx', index=False)

print("Conversion completed. Excel file 'output.xlsx' has been created.")