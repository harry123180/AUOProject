from datetime import datetime
currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%Y_%m_%d %H:%M:%S")

print("The current date and time is",currentTime)