import boto3
import botocore
import click

session = boto3.Session(profile_name='snapshotTool')
ec2 = session.resource('ec2')


@click.group()
def cli():
    """"snapshotTool manages shapshots of AWS EC2 instances"""


@cli.group('instances')
def instances():
    """Commands for instances"""


@instances.command('list')
@click.option('--project', default=None,
              help="Only instances for project ( Project:<name>)")
def list_instances(project):
    """List EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('project', '<no project>'))))
    return


@instances.command('stop')
@click.option('--project', default=None,
              help='Only instances for project')
def stop_instances(project):
    """Stop EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...", format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop instance {0} ".format(i.id) + str(e))
            continue
    return


@instances.command('start')
@click.option('--project', default=None,
              help='Only instances for project')
def stop_instances(project):
    """Start EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...", format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start instance {0} ".format(i.id) + str(e))
            continue
    return


def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


@cli.group('volumes')
def volumes():
    """Commands for volumes"""


@volumes.command('list')
@click.option('--project', default=None,
              help="Only volumes for project ( Project:<name>)")
def list_volumes(project):
    """List volumes of the EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                i.id,
                v.id,
                str(v.size) + 'GiB',
                v.state,
                v.encrypted and 'Encrypted' or 'Not Encrypted')))
    return


@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""


@instances.command('snapshot',
                   help='Create snapshots of all volumes')
@click.option('--project', default=None,
              help="Only of volumes within project ( Project:<name>)")
def create_snapshots(project):
    """"Create snapshots for EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print('Creating snapshot of {0}'.format(v.id))
            v.create_snapshot(Description='Created by snapshotTool')

        print('Starting {0}'.format(i.id))

        i.start()
        i.wait_until_running()

    print('Finished creating snapshots')

    return


@snapshots.command('list')
@click.option('--project', default=None,
              help="Only snapshots for project ( Project:<name>)")
def list_snapshots(project):
    """"List snapshots of volumes in EC2 instances"""

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    i.id,
                    v.id,
                    s.id,
                    s.description,
                    str(s.volume_size) + 'GiB',
                    s.start_time.strftime('%c'),
                    s.encrypted and 'Encrypted' or 'Not Encrypted')))
    return


if __name__ == '__main__':
    cli()

