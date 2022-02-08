# From the pathlib library, import the main class Path.
from pathlib import Path
import csv

# Set path for the csv file and initialize variables.
readdata = csv.reader(open("Resources/budget_data.csv", 'r'))
data = []
data_profit = []
profit = []
total_month_count = 0
total_months = 0
total_difference = 0
average = 0
profit_loss= 0
total = 0

#Export raw data into 'data' list and omit the first line. 
for row in readdata:
    data.append(row)
data.pop(0)

#Calculate total months, total profit and append 'profit' list for further data analysis.
for number in data:
    total_month_count += 1
    number = int(number[1])
    profit_loss += number
    profit_currency = "${:,.2f}".format(profit_loss)
    data_profit.append(number)

#Calculate the change in profit/loss in each line and append the profit list to complete final dataset for analysis.
for i, v in enumerate(data_profit[:-1], start=1):
    total_months = len(data_profit[1:])
    diff = data_profit[i]-data_profit[i-1]
    profit.append(diff)
    total_difference += diff
    average = total_difference / total_months
    average_currency = "${:,.2f}".format(average)

    #Delete sales from 'data' list since the information is not used for final printed analysis. 
for sales in data:
    del sales[1]

    #Define function to calculate maximum change in profits.
def max_change():
    largest_value = -1
    largest_index= 0
    for i, v in enumerate(zip(data[1:], profit)):
        if v[1] > largest_value:
            largest_value = v[1]
            largest_index = v[0]
    max_currency = "${:,.2f}".format(largest_value)
    print(f"Greatest Increase in Profits: {largest_index} {max_currency}")

    #Define function to calculate minimum change in profits.
def min_change():
    smallest_value = -1
    smallest_index= 0
    for i, v in enumerate(zip(data[1:], profit)):
        if v[1] < smallest_value:
            smallest_value = v[1]
            smallest_index = v[0]
    min_currency = "${:,.2f}".format(smallest_value)
    print(f"Greatest Decrease in Profits: {smallest_index} {min_currency}")

    #Print Final Analysis. 
print("Financial Analysis")
print("---------------------------")
print(f"Total Months {total_month_count}")
print(f"Total: {profit_currency}")
print(f"Average Change {average_currency}")

max_change()
min_change()

# Set file paths for menu_data.csv and sales_data.csv
menu_filepath = Path("Resources/menu_data.csv")
sales_filepath = Path("Resources/sales_data.csv")

# Initialize list objects to hold our menu and sales data
menu = []
sales = []

# Read in the menu data into the menu list
with open(menu_filepath) as menu_file:
    reader = csv.reader(menu_file)

    # Skip header of menu data
    next(reader)

    # Iterate over each row after the header
    for row in reader:
        menu.append(row)

# Read in the sales data into the sales list
with open(sales_filepath) as sales_file:
    reader = csv.reader(sales_file)

    # Skip header of sales data
    next(reader)

    # Iterate over each row after the header
    for row in reader:
        sales.append(row)

# Initialize dict object to hold our key-value pairs of items and metrics
report = {}

# Initialize a row counter variable
row_count = 0

# Loop over every row in the sales list object
for row in sales:
    print()
    print(row)

    # Line_Item_ID,Date,Credit_Card_Number,Quantity,Menu_Item
    # Initialize sales data variables
    quantity = int(row[3])
    sales_item = row[4]

    # If the item value not in the report, add it as a new entry with initialized metrics
    # Naming convention allows the keys to be ordered in logical fashion, count, revenue, cost, profit
    if sales_item not in report.keys():
        report[sales_item] = {
            "01-count": 0,
            "02-revenue": 0,
            "03-cogs": 0,
            "04-profit": 0,
        }

    # For every row in our sales data, loop over the menu records to determine a match
    for record in menu:

        # Item,Category,Description,Price,Cost
        # Initialize menu data variables
        item = record[0]
        price = float(record[3])
        cost = float(record[4])

        # Calculate profit of each item in the menu data
        profit = price - cost

        # If the item value in our sales data is equal to the any of the items in the menu, then begin tracking metrics for that item
        if sales_item == item:

            # Print out matching menu data
            print(f"Does {sales_item} equal {item}? - Match!")
            print(f"   Item: {item}")
            print(f"   Price: ${price}")
            print(f"   Cost: ${cost}")
            print(f"   Profit: ${profit}")

            # Cumulatively add up the metrics for each item key
            report[sales_item]["01-count"] += quantity
            report[sales_item]["02-revenue"] += price * quantity
            report[sales_item]["03-cogs"] += cost * quantity
            report[sales_item]["04-profit"] += profit * quantity

        # Else, the sales item does not equal any fo the item in the menu data, therefore no match
        else:
            print("Does", sales_item, "equal", record[0], "- No Match")

    # Increment the row counter by 1
    row_count += 1

# Print total number of records in sales data
print()
print("Total Number of Records:", row_count)
print() # Adds a space between the end of the program and the console input

# Write out report to a text file (won't appear on the command line output)
with open("report.txt", "w") as txt_file:
    for key, value in report.items():

        line = f"{key} {value}\n"
        txt_file.write(line)
