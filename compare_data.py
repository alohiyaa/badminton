
import csv
import json
import re

def compare_data():
    index_file_path = 'C:\\Users\\Mr. Abhishek Lohiya\\Desktop\\Badminton Account\\BaddyAutomation\\badminton\\index.html'
    csv_file_path = 'C:\\Users\\Mr. Abhishek Lohiya\\Desktop\\Badminton Account\\BaddyAutomation\\badminton\\PlayersData.csv'

    csv_data = {}
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            player_name = row[0]
            csv_data[player_name] = {
                'balance': f'AED {round(float(row[3]))}',
                'totalPaid': f'AED {round(float(row[2]))}',
                'totalExpense': f'AED {round(float(row[1]))}',
                'delayPay': f'AED {round(float(row[4]))}',
                'negativeWeeks': int(round(float(row[5]))),
                'notPlayedSince': '-' if int(row[6]) == 0 else str(int(row[6])),
                'longestStreak': int(row[7]),
                'currentStreak': int(row[8]),
                'daysPlayed': row[12],
                'hoursPlayed': int(round(float(row[13]))),
                'hoursLast30': int(row[14]),
                'caloriesBurned': str(int(round(float(row[16])))),
                'sepDaysPlayed': row[19],
                'sepHoursPlayed': int(row[20]),
                'sepCourtHours': str(round(float(row[21]))),
                'sepCalories': str(int(round(float(row[22]))))
            }

    with open(index_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    match = re.search(r'const playerData = (.*?);', content, re.DOTALL)
    if not match:
        print("Could not find playerData in index.html")
        return

    html_data_str = match.group(1)
    # A more robust way to convert JS object to JSON
    html_data_str = re.sub(r"(\w+):", r'"\1":', html_data_str)
    html_data_str = html_data_str.replace("'", '"')
    
    # Handle trailing commas
    html_data_str = re.sub(r',(\s*[}\]])', r'\1', html_data_str)

    try:
        html_data = json.loads(html_data_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from index.html: {e}")
        # Print the problematic string for debugging
        # print(html_data_str)
        return

    differences = []
    for player, csv_stats in csv_data.items():
        if player in html_data:
            html_stats = html_data[player]
            for key, csv_value in csv_stats.items():
                html_value = html_stats.get(key)

                # Special handling for numeric strings
                if isinstance(csv_value, str) and isinstance(html_value, str):
                    csv_value_numeric = ''.join(filter(str.isdigit, csv_value))
                    html_value_numeric = ''.join(filter(str.isdigit, html_value))
                    if csv_value_numeric == html_value_numeric:
                        continue

                if str(csv_value) != str(html_value):
                    differences.append(f'Mismatch for {player}, {key}: CSV is \'{csv_value}\' and HTML is \'{html_value}\'')
        else:
            differences.append(f'Player {player} not found in HTML data')

    if differences:
        for diff in differences:
            print(diff)
    else:
        print('All data is up to date.')

if __name__ == '__main__':
    compare_data()
