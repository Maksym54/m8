from decouple import config

EMAIL_USERNAME = config('EMAIL_USERNAME')
EMAIL_PASSWORD = config('EMAIL_PASSWORD')
SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')