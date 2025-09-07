
import csv
import json
import re

def update_data():
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

    # Convert python dict to a string that looks like a JS object
    js_object_str = json.dumps(csv_data, indent=12).replace('"', "'")

    # Use regex to replace the old playerData object with the new one
    new_content = re.sub(r'const playerData = .*?;', f'const playerData = {js_object_str};', content, flags=re.DOTALL)

    with open(index_file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print("Successfully updated player data in index.html")

if __name__ == '__main__':
    update_data()
