
# Volatility Stop Loss Calculator 

### Description
# - Calculates the best Stop Loss percentage based on Volatility 

### Model Type 
# - Python / Excel 
#15-07-2022

### Version - V1.0

#Insights:
# - This calculator will find the stop loss that will be triggered the least based on the asset volatility. 
# - This doesn't mean you can't be stopped several consecutive days, because it only considers day by day Max and Min prices and not periods. 

### Goals:
# - To find the best stop loss percentage based on volatility 

### Version Updates:
# - Relatory 


### Future Implementations: 
# - Add total Days Count to relatory 
# - Add volatility count by period (W, D, M)
# - Add to any ML model 
# - Considerations about Close price versus Being Stoped - what's the difference? 


### Author - Luiz Gabriel Bongiolo

### Credits & References 
# - Leandro Guerra Outspoken Market - Check him at: www.outspokenmarket.com / instagram @leandrowar / https://www.outspokenmarket.com/blog/stop-de-volatilidade-como-usar-outspoken-market
# - Excel Spreadsheet https://www.outspokenmarket.com/uploads/8/8/2/3/88233040/stop_volatilidade_-_outspoken_market.xlsx


from pandas_datareader import data as pdr 
import yfinance as yf 
yf.pdr_override()
import pandas as pd
import numpy as np
import datetime 




#Import the data

ticker = "^IXIC"                            #You can change this to any ticker from yahoo finance https://finance.yahoo.com/
start = "2014-01-01"                          #Pick the starting date 
end = datetime.datetime.now()                 #Pick end date or leave it as .now() for today's date 

df = pdr.get_data_yahoo(ticker, start, end)


df


#Remove unnecessary columns 

df.pop("Adj Close")
df.pop("Volume")



#Add the Return Column which is: Second Close price / First Close Price and so on


df["Return"] =  (df["Close"].shift(-1)/df["Close"] - 1) * 100

#Shift the return row to be in the right position

df["Return"] = df.Return.shift(1)



#Calculating the Max Distance 

df["Dist_Max"] =  (df["High"]/df["Open"] - 1) * 100


#Calculating the Min Distance 

df["Dist_Min"] =  (df["Open"]/df["Low"] - 1) * 100


#Max Standart Deviation 
dp_max = df['Dist_Max'].std() 
#print("DP Dist_Max - Stop Short = " + str(dp_max.round(decimals=2))+"%")

#Min  Standart Deviation 
dp_min = df['Dist_Min'].std() 
#print("DP Dist_Min - Stop Long  = " + str(dp_min.round(decimals=2))+"%")

#Return  Standart Deviation 
dp_return = df['Return'].std() 
#print("DP Dist_Return -         = " + str(dp_return.round(decimals=2))+"%")


#Double the Standart Deviation as security margin, you can double or trible this value to get less stops 

stop_short = dp_max * 3     #Adjust this number and check how many times you would've been stopped 

stop_long = dp_min * 3 

#print("\n Stop Short " + str(stop_short.round(decimals=2))+"%")
#print(" Stop Long " + str(stop_long.round(decimals=2))+"%")



#Calculating how many times we have been stopped 

df["Stop_Short"] = np.where(df["Dist_Max"]>stop_short, "1", "0")

df["Stop_Long"] = np.where(df["Dist_Min"]>stop_long, "1", "0")





#Count Stops 

stop_short_count = df['Stop_Short'].value_counts()[1]

stop_long_count = df['Stop_Long'].value_counts()[1]

#print(stop_short_count)

#print(stop_long_count)


# % of days stopped 

length = len(df)

per_stop_short = (stop_short_count / length) * 100
per_stop_long = (stop_long_count / length) * 100

#print("Number of Shorts Stopped: "+ str(per_stop_short.round(decimals=2))+"%")
#print("Number of Longs Stopped: "+ str(per_stop_long.round(decimals=2))+"%")


#Print Everything in one 

print("             " + ticker)


print("\n DP Dist_Max - Stop Short = " + str(dp_max.round(decimals=2))+"%")

print(" DP Dist_Min - Stop Long  = " + str(dp_min.round(decimals=2))+"%")

print(" DP Dist_Return -         = " + str(dp_return.round(decimals=2))+"%")


print(" #########################################")
print("\n Stop Short " + str(stop_short.round(decimals=2))+"%")

print(" Stop Long " + str(stop_long.round(decimals=2))+"%")

print("\n #########################################")
print(" \n Number of Shorts Stopped: " + str(stop_short_count))

print(" Number of Longs Stopped: " + str(stop_long_count))


print("\n #########################################")
print(" \n Percentage of Shorts Stopped: "+ str(per_stop_short.round(decimals=2))+"%")
print(" Percentage of Longs Stopped: "+ str(per_stop_long.round(decimals=2))+"%")


