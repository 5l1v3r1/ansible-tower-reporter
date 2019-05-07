# Tower API Reference https://tower-cli.readthedocs.io/en/latest/api_ref/index.html

from tower_cli import get_resource
from tower_cli.exceptions import Found
from tower_cli.conf import settings
import json
import datetime

# Set column spacing and formatting
columnFormat = '{:<10} {:<60} {:<15} {:<80} {:<50} {:<50} {:<50}'

# Get list of all items
res = get_resource('job_template')

# Get list of all items
with settings.runtime_values():
  try:
      res = get_resource('job_template')
      list_results = res.list(all_pages=True)
  except NotFound:
      print('No job templates exist. Exiting.')
      exit()

# Verify we received a dictionary
assert isinstance(list_results, dict)

#print json.dumps(list_results['results'][1], sort_keys=True, indent=4)

# Print totals
print "Ansible Tower Report"
print '-' * 100
print "Host = " + settings.host
print "Username = " + settings.username
print "Generated on = " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print "Total Job Templates  = " + str(list_results['count'])
print ""
print ""

# Print header information
print columnFormat.format("ID", "NAME", "LAST RUN", "PLAYBOOK", "PROJECT NAME", "INVENTORY NAME", "CREDENTIALS")
print '-' * 300

# Get resources
#res_project = get_resource('project')
#res_inventory = get_resource('inventory')
#res_credentials = get_resource('credential')

# Loop over each item
for item in list_results['results']:
  try:
    # Ansible Tower uses iso8601 datetime format
    ts = item['summary_fields']['last_job']['finished']
    dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    last_job = '{:%Y-%m-%d}'.format(dt)
  except KeyError:
    last_job = "_NONE_"

  if (item['ask_inventory_on_launch'] == 'true'):
    inv_name = "_PROMPT_ON_LAUNCH_"
  else:
    try:
      inv_name = item['summary_fields']['inventory']['name']
    except KeyError:
      inv_name = "_NONE_"

  #try:
  #  cred_name = item['summary_fields']['credential']['name']
  #except KeyError:
  cred_name = "_NONE_"
  for cred in item['summary_fields']['credentials']:
    if cred_name == "_NONE_":
      cred_name = cred['name']
    else:
      cred_name = cred_name + ', ' + cred['name']

  print columnFormat.format(item['id'], item['name'], last_job, item['playbook'], item['summary_fields']['project']['name'], inv_name , cred_name)

print ""
print ""
