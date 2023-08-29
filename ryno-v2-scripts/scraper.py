import pandas as pd
from utils import storage

# Get all users
all_users = storage.get_all_users()

# Initialize list to store all file data
all_files_data = []

# Get all files for each user
for user_id in all_users:
    user_files_data = storage.get_all_files_for_user(user_id=user_id)
    all_files_data.extend(user_files_data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(all_files_data)

# Write DataFrame to a CSV file
df.to_csv("output.csv", index=False)