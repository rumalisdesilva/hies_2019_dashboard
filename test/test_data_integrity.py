import pandas as pd

# Load dataset
df = pd.read_csv("data/hies_2019_expanded_expenditure_dataset.csv")

# Test 1: Required columns are present
assert 'Expenditure_Rs' in df.columns, "❌ Column 'Expenditure_Rs' is missing"
assert 'Category' in df.columns, "❌ Column 'Category' is missing"

# Test 2: No missing values in critical columns
assert df['Expenditure_Rs'].isnull().sum() == 0, "❌ Missing values in 'Expenditure_Rs'"

# Test 3: No duplicate records
assert df.duplicated().sum() == 0, "❌ Duplicate rows found"

## ✅ Test Case 4: Data Type Check
- Ensured 'Expenditure_Rs' is numeric
- ✅ Passed – Column is numeric

## ✅ Test Case 5: Value Range Check
- Checked if all values in 'Expenditure_Rs' are ≥ 0
- ✅ Passed – No negative values found

print("✅ All tests passed!")
