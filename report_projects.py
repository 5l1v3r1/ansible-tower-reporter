from tower_cli import get_resource
from tower_cli.exceptions import Found
from tower_cli.conf import settings
import json

columnFormat = '{:<10} {:<50} {:<10}'
# Get all projects
with settings.runtime_values():
    try:
        res = get_resource('project')
        projects = res.list(all_pages=True)
    except Found:
        print('This organization already exists.')

assert isinstance(projects, dict)

#print json.dumps(projects, sort_keys=True, indent=4)

print "Total projects = " + str(projects['count'])

print columnFormat.format("PROJECT ID", "PROJECT NAME", "JOB TEMPLATE COUNT")

for item in projects['results']:
  #print item['name']
  res = get_resource('job_template')
  jts = res.list(all_pages=True, project=item['id'])
  print columnFormat.format(item['id'], item['name'], jts['count'])
  #print jts['count']
