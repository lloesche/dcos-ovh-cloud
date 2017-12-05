#!/usr/bin/env python3
import ovh
import sys
import time
from retrying import retry
from multiprocessing.pool import ThreadPool


class OVHClient(ovh.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @retry(stop_max_attempt_number=3)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @retry(stop_max_attempt_number=3)
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


def delete_instance(instance_id):
    print('Requesting deletion of {}'.format(instance_id))
    c.delete('/cloud/project/{}/instance/{}'.format(project_id, instance_id))


def detach_volume(volume_id):
    print('Detaching volume {}'.format(volume_id))
    try:
        r = c.get('/cloud/project/{}/volume/{}'.format(project_id, volume_id))
        for instance_id in r['attachedTo']:
            print('Detaching volume {} from instance {}'.format(volume_id, instance_id))
            r = c.post('/cloud/project/{}/volume/{}/detach'.format(project_id, volume_id),
                       serviceName=project_id,
                       instanceId=instance_id)
        return True
    except ovh.exceptions.APIError:
        raise


def cleanup_volume(volume_id):
    print('Cleaning up volume {}'.format(volume_id))
    detach_volume(volume_id)
    wait_for_volume(volume_id, wait_status='available')
    delete_volume(volume_id)


def delete_volume(volume_id):
    print('Removing volume {}'.format(volume_id))
    c.delete('/cloud/project/{}/volume/{}'.format(project_id, volume_id))


def wait_for_volume(volume_id, wait_status='in-use'):
    wait = True
    while wait:
        wait = False
        r = c.get('/cloud/project/{}/volume/{}'.format(project_id, volume_id))
        if r['status'] == wait_status:
            print('Volume {} is {}'.format(volume_id, r['status']))
        elif r['status'] in ['attaching']:
            print('Volume {} is still {}'.format(volume_id, r['status']))
            wait = True
        else:
            print('Volume {} has an unexpected status {}'.format(volume_id, r['status']))
        time.sleep(1)


if len(sys.argv[1:]) == 0:
    print('Usage: {} <projectname>'.format(sys.argv[0]))
    sys.exit(1)

c = OVHClient()
tp = ThreadPool(10)
project = sys.argv[1]
project_id = None

for service_id in c.get('/cloud/project'):
    p = c.get('/cloud/project/{}'.format(service_id))
    print('Found project {} with id {}'.format(p['description'], p['project_id']))
    if p['description'] == project:
        project_id = p['project_id']
        break

if not project_id:
    print("Couldn't find project with name {}".format(project))
    sys.exit(1)

print('Fetching all instances')
ri = c.get('/cloud/project/{}/instance'.format(project_id))

print('Fetching all volumes')
rv = c.get('/cloud/project/{}/volume'.format(project_id))

if len(ri) == 0 and len(rv) == 0:
    print('Project {} has no running instances or volumes'.format(project))
    sys.exit(0)

input('!!!WARNING - THIS WILL DESTROY ALL {} INSTANCES AND {} VOLUMES IN THE PROJECT {}!!!\nPress Enter to continue...'.format(
    len(ri), len(rv), project))

tp.map(cleanup_volume, [v['id'] for v in rv])
tp.map(delete_instance, [i['id'] for i in ri])
