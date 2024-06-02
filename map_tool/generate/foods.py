import xlrd
import json

def update_restaurants_from_excel(json_file, xls_file):
    """
    Update restaurants data in a JSON file with data from an Excel file.

    Args:
    - json_file: Path to the JSON file containing restaurants data.
    - xls_file: Path to the Excel file containing data to be updated.

    Returns:
    - Updated restaurants data as a list of dictionaries.
    """
    # Load restaurants data from JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    restaurants = data["restaurants"]

    # Open Excel file
    workbook = xlrd.open_workbook(xls_file)
    sheet = workbook.sheet_by_index(0)
    j=0
    # Iterate over rows in Excel file
    for i in range(200, sheet.nrows):  # Start from 1 to skip header row
        name = sheet.cell_value(i, 3)  # Get name from Excel file
        cat = sheet.cell_value(i, 11)  
        cat=cat[3:] # Get cat from Excel file
        
        recommendation = sheet.cell_value(i, 18)   # Get recommendation from Excel file
        # Find corresponding restaurant in JSON data and update its fields
        restaurant=restaurants[j]
        restaurant["name"] = name
        restaurant["type"] = cat
        foods_list = [food.strip() for food in recommendation.split(";")[:8]]
        restaurant["foods"] = foods_list
        j+=1
        if(j>=30):
            break

    # Save updated restaurants data to JSON file
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Restaurants data updated successfully!")

# Specify paths to JSON and Excel files
json_file = "map_tool/json/restaurants.json"
xls_file = "map_tool/xls/restaurants.xls"

# Update restaurants data from Excel file
update_restaurants_from_excel(json_file, xls_file)
