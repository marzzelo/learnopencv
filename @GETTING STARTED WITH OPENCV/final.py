# Import necessary libraries
import argparse
from datetime import datetime, timedelta
from colorama import Fore

# Updated setup for the argument parser
parser = argparse.ArgumentParser(description="Modify the current datetime or a specified datetime with a given hours delta.")
parser.add_argument("hours_delta", type=int, help="Number of hours to add to the datetime.")
parser.add_argument("-d", "--date", type=str, help="Date in the format dd/mm/yy to set the initial datetime.")
parser.add_argument("-t", "--time", type=str, help="Time in the format hh/mm to set the initial datetime.")

# Parse the arguments
args = parser.parse_args()

# Get the current datetime
now = datetime.now()

# Function to parse date and time strings and update the datetime object accordingly
def parse_and_update_datetime(datetime_obj, date_str=None, time_str=None):

    if date_str:
        date_parts = date_str.split('/')
        day = int(date_parts[0])
        month = datetime_obj.month
        year = datetime_obj.year

        if len(date_parts) > 1:
            month = int(date_parts[1])

        if len(date_parts) > 2:
            year = int(date_parts[2])
            # Adjust year to full format (e.g., '21' -> 2021)
            year += 2000 if year < 100 else 0

        datetime_obj = datetime_obj.replace(day=day, month=month, year=year)
        

    if time_str:
        hour, minute = map(int, time_str.split(':'))
        datetime_obj = datetime_obj.replace(hour=hour, minute=minute)

    return datetime_obj

# Update the datetime if date or time parameters are provided
start_datetime = parse_and_update_datetime(now, args.date, args.time)

# Add hours_delta to the datetime
result_datetime = start_datetime + timedelta(hours=args.hours_delta)

# Output the result
formatted_result = result_datetime.strftime("%d/%m/%Y %H:%M (%a)")
formatted_start = start_datetime.strftime("%d/%m/%Y %H:%M (%a)")

print(f'{Fore.BLUE}\n\n======================  ======================{Fore.RESET}')
print(f'{Fore.MAGENTA}Fecha de Inicio:        {formatted_start}{Fore.RESET}')
print(f'{Fore.YELLOW}Fecha de Finalización:  {formatted_result}{Fore.RESET}')
print(f'{Fore.BLUE}======================  ======================{Fore.RESET}\n\n')
