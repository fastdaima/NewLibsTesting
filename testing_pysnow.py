from pysnow import Client, QueryBuilder
import argparse

ap = argparse.ArgumentParser()

ap.add_argument('-i', '--instance_name', required=True, help='Instance name of service now')
ap.add_argument('-u', '--username', required=True, help='username of the service now instance')
ap.add_argument('-p', '--password', required=True, help='password of the service now instance')


def update_priority(instance_name, username, password):
    client = Client(instance_name, user=username, password=password)  # instance_name without
    # service-now.com
    incident = client.resource(api_path='/table/incident')

    qb = (QueryBuilder().field('priority').less_than_or_equal(3).AND().field('state').equals("3"))

    response = incident.get(
        query=qb,
    )

    output = []
    for record in response.all():
        number = record['number']
        impact = int(record['impact'])
        urgency = int(record['urgency'])
        comments_work_notes = record['comments_and_work_notes']

        if impact == urgency:
            impact += 1
        elif impact < urgency:
            impact += 1
        elif urgency < impact:
            urgency += 1

        update = {
            'impact': str(impact),
            'urgency': str(urgency),
            'comments_and_work_notes': comments_work_notes + "Priority reduced by 1"
        }

        response = incident.update(query={'number': number}, payload=update)
        output.append(
            f"Updated: {response['number']}, new priority: {response['priority']}, response: {response['comments_and_work_notes']}")

    print(output)


if __name__ == '__main__':
    args = vars(ap.parse_args())
    update_priority(args['instance_name'], args['username'], args['password'])
