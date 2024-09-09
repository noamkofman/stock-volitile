import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import numpy as np
import math

# Path to your ZIP file
zip_file_path = 'New folder/archive (1).zip'
buy = False
make_money = 0
lose_money = 0
def get_next_month(month):
    month = int(month)
    if month == 12:
        return 1 
    else:
        return month + 1
# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as archive:
    # List the contents of the ZIP file to ensure 'stocks/UHAL.csv' exists
    #print(archive.namelist())  # This lists all files in the zip
    
    # Extract and read the 'stocks/UHAL.csv' file into a DataFrame
    with archive.open('stocks/AAPL.csv') as uhal_file: # uhaul_file is the name we give the uhaul stock so we can call it 
        pr = pd.read_csv(uhal_file)
        print(pr.columns)
        month_1 = pr['Date'].tolist()
        march_high = []
        probable_buy = set()
        # splitting datset into only the month of march, (3)
        for index, row in pr.iterrows():
            date = row['Date']

            year = date.split('-')[0]

            month = date.split('-')[1]
          
            if month == '09' and year == '2008':
                # gives highs of march
                march_high.append(row['High'])
                next_month = get_next_month(int(month))
                new_month = f"{next_month:02d}"
                
                


                

                #print(month) 
                # returns the next month with a 0 behind it so the prorgam recognizes it
           

        if march_high:
            # Calculate standard deviation, mean, and volatility ratio
            std_dev = pd.Series(march_high).std()
            mean_high = pd.Series(march_high).mean()
            volatility_percentage = (std_dev / mean_high) * 100
            
            print("mean is: ", mean_high)
            print("standard deviation is: ", std_dev)
            print("volatility ratio is: ", volatility_percentage)

            # Define volatility thresholds (10% and 5%)
            high_volatility_threshold = 10  # 10% of the mean price
            low_volatility_threshold = 5    # 5% of the mean price

            if volatility_percentage > high_volatility_threshold:
                print("The stock is volatile.")
                buy = True
            elif volatility_percentage < low_volatility_threshold:
                print("The stock is not volatile.")
            else:
                print("The stock has medium volatility.")
                
            pr['Year'] = pr['Date'].apply(lambda x: x.split('-')[0])
            pr['Month'] = pr['Date'].apply(lambda x: x.split('-')[1])
            # below we are doing all the stuff for the next month
            next_month_data = pr[(pr['Date'].str.startswith(f'2008-{new_month}'))]
            #print(next_month_data)
            current_closing = pr[(pr['Date'].str.startswith(f'2008-{month}'))]
            print("current months avarege closing price is: ", current_closing)
            
            september_data = pr[pr['Month'] == '09']
            uniqe_years = pr['Year'].unique()
            
            # below we find what months are valubel based on the criteria set on line #87
            for year in pr['Year'].unique():
                for month in range(1, 12):
                    month_str = f"{month:02d}"  # Ensure month is two digits
                    current_month_data = pr[(pr['Year'] == year) & (pr['Month'] == month_str)]
                    
                    if not current_month_data.empty:      
                          current_month_closing = current_month_data['Close'].mean()
                          if current_month_closing < mean_high and buy:
                                probable_buy.add(f'{year}-{month_str}')
                                
            for date in probable_buy:
                year, month_str = date.split('-')
                next_month_data = pr[(pr['Year'] == year) & (pr['Month'] == new_month)]

                if not next_month_data.empty:
                    next_month_close = next_month_data['Close'].mean()
                else:
                    print(f"Missing data for next month: {year}-{new_month}")
                    continue
                # Filter current month's closing price
                current_month_data = pr[(pr['Year'] == year) & (pr['Month'] == month_str)]
                current_month_closing = current_month_data['Close'].mean()

                print(f"Checking {date}: Current Closing = {current_month_closing}, Next Month Closing = {next_month_close}")

                if next_month_close > current_month_closing:
                    make_money += 1
                else:
                    lose_money += 1
                
            print(f"Number of times you'd make money: {make_money}")
            print(f"Number of times you'd lose money: {lose_money}")
                                

