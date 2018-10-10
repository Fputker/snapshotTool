import boto3
import click

session = boto3.Session(profile_name='snapshotTool')
ec2 = session.resource('ec2')


@click.group()
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
         i.stop()

    return


def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


if __name__ == '__main__':
    instances()

