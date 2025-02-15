import pandas as pd
import numpy as np


def process_score(value):
    """
    Process the interview score from a string format:
    - Convert to a float after removing any '+' or '-'.
    - If '-' is the first character, subtract 0.33 from the absolute value.
    - If '+' is the last character, add 0.33 to the absolute value.
    """
    if isinstance(value, str):  # Ensure value is a string
        adjust = 0
        if value.startswith("-"):
            adjust -= 0.33
        if value.endswith("+"):
            adjust += 0.33

        # Remove '+' or '-' and convert to float
        num = float(value.strip("+-"))

        # Apply absolute value and adjustments
        return abs(num) + adjust
    elif pd.notna(value):  # If it's already a number, apply abs
        return abs(float(value))
    return np.nan  # Preserve NaN values

# Load the data
data = pd.read_csv("2025interviewscores.csv")

# Apply multiple conditions correctly using the bitwise '&' operator
filtered_data = (data["Ucas Cycle"] == 2025) & \
                (data["FINAL COURSE - Course Group"] == "Computer Science") & \
                (data["UK/International Domicile"] == "UK"or "International") & \
                (data["Offer?"] == "Y")
filtered_data = data[filtered_data].copy()
filtered_data.to_csv("filtered_data.csv", index=False)
# Identify columns that contain interview scores
interview_columns = [col for col in data.columns if "Score" in col]

# Apply the function to each row and compute the adjusted mean
filtered_data.loc[:, "Average Interview Score"] = filtered_data[interview_columns].apply(
    lambda row: np.nanmean([process_score(val) for val in row]), axis=1
)# Sort by Average Interview Score in ascending order

sorted_data = filtered_data.sort_values(by="Average Interview Score", ascending=True)

# Print the sorted DataFrame
print(sorted_data[["Average Interview Score"]])

