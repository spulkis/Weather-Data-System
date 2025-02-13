import subprocess
import os
from decouple import config
from datetime import datetime

# MySQL credentials
USER = config('MYSQL_USER')
PASSWORD = config('MYSQL_PASSWORD')
HOST = config('MYSQL_HOST')
DATABASE = config('MYSQL_DATABASE')

# Backup directory
BACKUP_DIR = config('BACKUP_DIR')
os.makedirs(BACKUP_DIR, exist_ok=True)

# Date format for backup file
DATE = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Backup file name
BACKUP_FILE = os.path.join(BACKUP_DIR, f"{DATABASE}-{DATE}.sql.gz")

# mysqldump command
command = f"mysqldump -h {HOST} -u {USER} -p{PASSWORD} {DATABASE} | gzip > {BACKUP_FILE}"

# Execute the backup
process = subprocess.run(command, shell=True)

# Print out status messages based on the return code
if process.returncode == 0:
    print("Database backup completed successfully.")
else:
    print(f"Database backup failed with return code {process.returncode}.")

# Optionally, delete old backups older than 7 days
find_command = f"find {BACKUP_DIR} -type f -name '*.gz' -mtime +7 -exec rm {{}} \\;"
subprocess.run(find_command, shell=True)
