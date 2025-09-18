import pandas as pd

# Define the file path
file_path = 'apps/prototype/data/incoming/RBSI Onboarding Sprint 2 Testing Flow v3.csv'

# Read the CSV file
df = pd.read_csv(file_path)

# Find the row with Keyname 'Description-new-application' and clear its 'Helper' column
df.loc[df['Keyname'] == 'Description-new-application', 'Helper'] = ''

# Save the updated DataFrame back to the CSV
df.to_csv(file_path, index=False)

print("CSV file has been updated successfully.")
