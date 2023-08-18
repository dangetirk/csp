from google.cloud import bigquery
from simple_salesforce import Salesforce

# Set up BigQuery client
client = bigquery.Client()
try:
    datasets = list(client.list_datasets())
    print("BigQuery connection successful!")
except Exception as e:
    print("BigQuery connection failed:", e)

# Salesforce credentials
sf_username = "ratna-kumar.dangeti@lloydsbanking.com.devpoc"
sf_password = "Sony@4075"
sf_consumer_key = "3MVG9od6vNol.eBijuSl01nDrsc_Ngz.DmtOGEn0Ja4DdL75sh_rzjhKqKo0C1DVygt2QyQ1xeGkrwtkfRE1L"
sf_consumer_secret = "FB008DFDC0E87E35543FBD64DB3F5EA2B7AD7789E423138986F0B4F4203C8B03"

# Set up Salesforce connection
sf = Salesforce(
    username=sf_username,
    password=sf_password,
    consumer_key=sf_consumer_key,
    consumer_secret=sf_consumer_secret
)

try:
    user_info = sf.query("SELECT Id, Name FROM User LIMIT 1")
    print("Salesforce connection successful!")
except Exception as e:
    print("Salesforce connection failed:", e)
