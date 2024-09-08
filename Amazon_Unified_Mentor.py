# %%
"""
Import necessary libraries
"""

# %%
import pandas as pd #For data manipulation and analysis.
import matplotlib.pyplot as plt #For creating static visualizations.
import seaborn as sns #For statistical data visualization built on top of Matplotlib.
import numpy as np #For numerical operations, especially with arrays.
import warnings #To manage warning messages, specifically suppressing them in this case.
warnings.filterwarnings('ignore')
import sqlalchemy as sal #For SQL database integration and manipulation.

# %%
datafile = pd.read_csv("Amazon Sales Data.csv") #Reading "Amazon Sales Data.csv" and creating a dataframe `datafile`

# %%
datafile.describe() #Description of dataframe "datafile"

# %%
datafile.head() #Head returns top 5 rows if not mentioned

# %%
datafile.info() #Information of datafile (dataframe)

# %%
datafile.shape #Knowing the shape of our dataframe (rows,columns)

# %%
order_pri = {"H": "High","L":"Low","M":"Medium","C":"Critical"}
datafile["Order Priority"] = datafile["Order Priority"].replace(order_pri)
#Replacing order_priority values, making values more meaningful

# %%
datafile.columns #Accessing the column names in the dataframe

# %%
datafile.columns = datafile.columns.str.lower()
datafile.columns = datafile.columns.str.replace(" ","_")
#Lowering the column names and adding underscores 

# %%
datafile #Returning the dataframe to check if column names changed

# %%
datafile.isna().sum() #Finding NA(Not Available) values

# %%
datafile.info() #Information of current dataframe with updated column names

# %%
#Changing data type of column named order_date to date-time
datafile['order_date'] = pd.to_datetime(datafile['order_date']) 

# %%
#Changing data type of column named ship_date to date-time (earlier datatype string)
datafile['ship_date'] = pd.to_datetime(datafile['ship_date'])

# %%
#Gives descriptive statistics for all categorical (object-type) columns in the dataframe
datafile.describe(include='object')

# %%
#Iterating over all categorical columns in the dataframe, printing the name of each column, its unique values
for column in datafile.describe(include='object').columns:
    print(column)
    print(datafile[column].unique())
    print("*"*50)

# %%
#Checking NULL values in our dataframe
datafile.isnull().sum()

# %%
#Creating new column profit_margin to find profit margins over items
datafile['profit_margin']= datafile['total_profit']/datafile['total_revenue']*100

# %%
#Creating new column to find gross profit per user
datafile['gross_profit_per_user'] = datafile['unit_price']-datafile['unit_cost']

# %%
datafile.describe(include = 'object')

# %%
#Finding the count of regions sorted descending
datafile['region'].value_counts()

# %%
datafile

# %%
#Evaluating the sales channel using value_counts
sales_medium = datafile['sales_channel'].value_counts(normalize = True)
sales_medium

# %%
#Plotting channels of sales x-axis = Medium y-axis= count/number of frequency
plt.figure(figsize =(5,4))
plt.title("Channels of Sales")
plt.bar(['Online',"Offline"],datafile['sales_channel'].value_counts(),color = 'orange')
plt.show()

# %%
#Finding the most ordered item by its type
item_type_percentage= datafile['item_type'].value_counts(normalize = True)
item_type_percentage

# %%
plt.figure(figsize = (15,4))
ax1 = sns.countplot(x='item_type',hue=datafile["sales_channel"],data=datafile,palette = "Reds")
plt.title("Item types with sales medium",size = 20)
plt.xlabel("Item Category")
plt.ylabel("Payment Medium Count")
plt.show()

# %%
top_regions = datafile['region'].value_counts(normalize = True)*100
top_regions

# %%
sub_prices = ['units_sold',
       'unit_price', 'unit_cost', 'total_revenue', 'total_cost',
       'total_profit', 'profit_margin',
       'gross_profit_per_user']

# %%
sns.scatterplot(x='unit_price',y='units_sold',data=datafile)
plt.title("Unit Price vs Units Sold")
plt.xlabel("Unit Price")
plt.ylabel("Units Sold")
plt.show()

# %%
sns.histplot(datafile['profit_margin'],kde=True)
plt.title("Profit Margin Distribution")
plt.show()

# %%
plt.figure(figsize=(10,8))
correlation_matrix = datafile[sub_prices].corr()
sns.heatmap(correlation_matrix,annot=True,cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# %%
sns.pairplot(datafile)

# %%
grouped_data = datafile.groupby('item_type')[['total_revenue', 'total_cost', 'total_profit']].sum()
grouped_data.plot(kind='bar', stacked=True, figsize=(15, 10))
plt.xlabel('Item Type')
plt.ylabel('Amount')
plt.title('Total Revenue, Cost, and Profit by Item Type')
plt.xticks(rotation=45)
plt.show()


# %%
plt.figure(figsize=(10,8))
sns.stripplot(x='region',y='units_sold',data=datafile,jitter=True,hue='order_priority')
plt.xticks(rotation=25,fontsize=7)
plt.show()

# %%
plt.figure(figsize=(16,9))
sns.stripplot(x='order_priority',y='delivery_time',data=datafile,hue="region",jitter=True,size=5.5)
plt.legend(loc=0,bbox_to_anchor=(1,1),markerscale=2)
plt.xlabel("Order Priority")
plt.ylabel("Delivery Time (in days)")

# %%
plt.figure(figsize=(20,8))
sns.boxplot(x='order_priority',y='delivery_time',data=datafile,hue='region')
plt.legend(loc=0)

# %%
plt.figure(figsize=(15,8))
sns.countplot(x='region',data=datafile,color='orange')
plt.xticks(rotation=34)
plt.show()

# %%
# plt.figure(figsize)
sns.barplot(x='order_priority',y='total_profit',data=datafile,color='red')
plt.xlabel("Ordr Priority")
plt.ylabel("Total Profit")
plt.show()

# %%
sns.distplot(datafile['profit_margin'],kde=True,color ="blue")
plt.xlabel("Profit Margin")
plt.ylabel("Frequency")
plt.show()

# %%
plt.figure(figsize=(15,8))
sns.jointplot(x='profit_margin',y='total_profit',data=datafile,kind='kde',color='blue')
plt.xlabel("Profit Margin")
plt.ylabel("Total Profit")
plt.show()

# %%
engine = sal.create_engine("mysql+mysqlconnector://root:12345678@localhost/Unified_Project_Amazon1")
connection = engine.connect()

# %%
datafile.to_sql("amazon_sales",con= connection,index=False,if_exists="replace")

# %%
