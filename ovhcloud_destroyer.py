#!/usr/bin/env python3
import ovh
from retrying import retry

serviceName = 'd5df6e586e6f4d099ed48d2b17b6b48c'


def main():
    c = OVHClient()
    input('!!!WARNING - THIS WILL DESTROY ALL INSTANCES IN THE PROJECT!!!\nPress Enter to continue...')
    print('Fetching all instances')
    r = c.get('/cloud/project/{}/instance'.format(serviceName))
    for i in r:
        print('Requesting deletion of {}'.format(i['id']))
        c.delete('/cloud/project/{}/instance/{}'.format(serviceName, i['id']))


class OVHClient(ovh.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @retry(stop_max_attempt_number=3)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @retry(stop_max_attempt_number=3)
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


if __name__ == "__main__":
    main()
