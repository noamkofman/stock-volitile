import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import numpy as np
import math

# Path to your ZIP file
zip_file_path = 'New folder/archive (1).zip'
sqrt_31 = math.sqrt(31)
# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as archive:
    # List the contents of the ZIP file to ensure 'stocks/UHAL.csv' exists
    #print(archive.namelist())  # This lists all files in the zip
    
    # Extract and read the 'stocks/UHAL.csv' file into a DataFrame
    with archive.open('stocks/UHAL.csv') as uhal_file: # uhaul_file is the name we give the uhaul stock so we can call it 
        pr = pd.read_csv(uhal_file)
        print(pr.columns)
        month_1 = pr['Date'].tolist()
        march_low = []
        # splitting datset into only the month of march, (3)
        for index, row in pr.iterrows():
            date = row['Date']
            month = date.split('-')[1]
            if month == '03':
                # gives lows of march
                march_low.append(row['High'])

        if march_low:
            # 
            std_dev = pd.Series(march_low).std()
            mean_high = pd.Series(march_low).mean()
            volatility = std_dev / mean_high
            print("volatility ratio is: ", volatility )
        # if standrid div is higher than 10% of the mean it is volitile if less than 5% then not volitile
            vol_high = mean_high * .10
            vol_low = mean_high * .05

            if std_dev > vol_high:
                print("stock is volitle")
            elif std_dev < vol_low:
                print("stock is NOT volitle")
            else:
                print("stock has medium volatility")
        

   