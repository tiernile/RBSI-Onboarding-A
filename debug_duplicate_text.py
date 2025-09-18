import pandas as pd

# Load the CSV file
file_path = 'apps/prototype/data/incoming/RBSI Onboarding Sprint 2 Testing Flow v3.csv'
df = pd.read_csv(file_path)

# Find rows containing the specific text
search_text = "Applying for an account with us"
matching_rows = df[df['Question'].str.contains(search_text, na=False)]

# Print the matching rows
print(matching_rows[['Section', 'Keyname', 'Question']].to_string())
