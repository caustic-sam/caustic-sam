# Retry saving the file with pip value formula included and provide download link

# Ensure data is properly structured for Excel export
data_with_pip_formula_retry = {
    'Currency Pair': user_trades['Market'],
    'Position Size': position_size_cleaned,
    'Entry Price': user_trades['Opening Price'],
    'Stop Loss': user_trades['Stop Loss'],
    'Take Profit': user_trades['Take Profit'],
    'Current Price': user_trades['Current Price'],
    'Pip Value': ['=IF(FIND("JPY", A2), (B2 * 0.01), (B2 * 0.0001))'] + [''] * (len(user_trades) - 1)
}

# Create a DataFrame with the specified structure
df_with_pip_formula_retry = pd.DataFrame(data_with_pip_formula_retry)

# Save the DataFrame to Excel
file_path_retry = "/mnt/data/Forex_Risk_Reward_with_Pip_Value_Template_Retry.xlsx"
df_with_pip_formula_retry.to_excel(file_path_retry, index=False)

# Provide the corrected download link
file_path_retry
