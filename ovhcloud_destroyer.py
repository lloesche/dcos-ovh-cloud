#!/usr/bin/env python3
import ovh
c = ovh.Client()

serviceName = 'd5df6e586e6f4d099ed48d2b17b6b48c'

input('!!!WARNING - THIS WILL DESTROY ALL INSTANCES IN THE PROJECT!!!\nPress Enter to continue...')
print('Fetching all instances')
r = c.get('/cloud/project/{}/instance'.format(serviceName))
for i in r:
    print('Requesting deletion of {}'.format(i['id']))
    c.delete('/cloud/project/{}/instance/{}'.format(serviceName, i['id']))
