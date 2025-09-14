import csv
import json
import re
from datetime import datetime

def update_data():
    index_file_path = 'C:\\Users\\Mr. Abhishek Lohiya\\Desktop\\Badminton Account\\BaddyAutomation\\badminton\\index.html'
    csv_file_path = 'C:\\Users\\Mr. Abhishek Lohiya\\Desktop\\Badminton Account\\BaddyAutomation\\badminton\\PlayersData.csv'

    # Read new player data from CSV
    csv_data = {}
    csv_players = set()
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            player_name = row[0]
            csv_players.add(player_name)
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

    # Read existing player data from index.html
    with open(index_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    match = re.search(r'const playerData = (.*?);', content, re.DOTALL)
    if match:
        html_data_str = match.group(1)
        # Be more robust in parsing the JS object
        # 1. Add quotes around keys
        html_data_str = re.sub(r'([\w\s]+):', r'"\1":', html_data_str)
        # 2. Replace single quotes with double quotes
        html_data_str = html_data_str.replace("'", '"')
        # 3. Remove trailing commas
        html_data_str = re.sub(r',(\s*[}\]])', r'\1', html_data_str)
        try:
            html_data = json.loads(html_data_str)
            html_players = set(html_data.keys())

            new_players = csv_players - html_players
            removed_players = html_players - csv_players

            # If there are new or removed players, update the initialPasswords object
            if new_players or removed_players:
                password_match = re.search(r'const initialPasswords = {([^}]*)};', content)
                if password_match:
                    passwords_str = password_match.group(1)
                    # Simple conversion from JS object to a dictionary-like string for regex
                    passwords_dict_str = f"{{{passwords_str}}}"
                    passwords_dict_str = passwords_dict_str.replace("'", '"')
                    
                    # Use regex to extract key-value pairs
                    pairs = re.findall(r'\s*"([^"]+)"\s*:\s*"([^"]+)"\s*,?', passwords_dict_str)
                    
                    passwords = dict(pairs)

                    for player in new_players:
                        passwords[player] = f'{player.lower()}123'
                    
                    for player in removed_players:
                        if player in passwords:
                            del passwords[player]

                    # Convert back to JS object string format
                    new_passwords_str = ', '.join([f"'{k}': '{v}'" for k, v in passwords.items()])
                    
                    # Replace the old passwords object with the new one
                    content = re.sub(r'const initialPasswords = {([^}]*)};', f'const initialPasswords = {{{new_passwords_str}}};', content)

        except json.JSONDecodeError as e:
            print(f"Could not parse existing player data in index.html: {e}")


    # Convert python dict to a string that looks like a JS object
    js_object_str = json.dumps(csv_data, indent=12).replace('"', "'")

    # Update player data
    content = re.sub(r'const playerData = .*?;', f'const playerData = {js_object_str};', content, flags=re.DOTALL)

    # Update the last updated date
    current_date = datetime.now().strftime('%B %d, %Y')
    content = re.sub(r'<p class="last-updated">Last Updated: .*?</p>', f'<p class="last-updated">Last Updated: {current_date}</p>', content)

    with open(index_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print("Successfully updated player data and date in index.html")

if __name__ == '__main__':
    update_data()
