from pysnow import Client, QueryBuilder
from pprint import pprint

client = Client("instance_name", user="username", password="password") # instance_name without
# service-now.com
incident = client.resource(api_path='/table/incident')

qb = (QueryBuilder().field('priority').less_than_or_equal(3).AND().field('state').equals("3"))

response = incident.get(
    query=qb,
)

ticket_numbers = []
for record in response.all():
    #ticket_numbers.append((record['number'], record['impact'], record['urgency'], record['comments_and_work_notes']))
    number, impact, urgency, comments_work_notes = record['number'], int(record['impact']), int(record['urgency']), record['comments_and_work_notes']

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

    updated_record = incident.update(query={'number': number}, payload=update)
    print(updated_record['priority'], updated_record['comments_and_work_notes'], updated_record['number'])
    break


#print(ticket_numbers)
# Impact	Urgency	Priority
# 1 - High	1 - High	1 - Critical
# 1 - High	2 - Medium	2 - High
# 1 - High	3 - Low	3 - Moderate
# 2 - Medium	1 - High	2 - High
# 2 - Medium	2 - Medium	3 - Moderate
# 3 - Low	1 - High	3 - Moderate

# 2 - Medium	3 - Low	4 - Low
# 3 - Low	2 - Medium	4 - Low
# 3 - Low	3 - Low	5 - Planning
# for ticket_number, priority_val, comment in ticket_numbers:
#     print(ticket_number, priority_val)
#     update = {
#         'priority': str(priority_val+1),
#         # change impact and urgency
#         'description': comment + "Reduced priority by 1"
#     }
#     updated_record = incident.update(query={'number': ticket_number}, payload=update)
#     pprint(updated_record)
#     print(updated_record['priority'], updated_record['description'], updated_record['number'])
#     break

# [('INC0000007', 1), ('INC0000017', 1), ('INC0000002', 1), ('INC0000054', 1), ('INC0000040', 3)]
# [('INC0000040', 3, ''), ('INC0000007', 1, ''), ('INC0000017', 1, ''), ('INC0000002', 1, ''), ('INC0000054', 1, '')]
# INC0000040 3
# <Response [200 - PUT]>
# 3 Reduced priority by 1 INC0000040
