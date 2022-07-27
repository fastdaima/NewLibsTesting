import asyncio
import aiosnow
from aiosnow.models.table.declared import IncidentModel as Incident


async def main():
    client = aiosnow.Client("dev108399.service-now.com", basic_auth=("Resolve", "Resolve@123"))

    async with Incident(client, table_name="incident") as inc:
        query = aiosnow.select(
            Incident.priority.less_or_equals(3) & Incident.state.equals(3)
        ).order_asc(Incident.priority)

        ticket_numbers = []
        output = []

        for response in await inc.get(query, limit=10):
            ticket_numbers.append((response['number'], response['priority'].key))
        print(ticket_numbers)

        # priority_map = {
        #     1: '1 - Critical',
        #     2: '2 - High',
        #     3: '3 - Moderate',
        #     4: '4 - Low'
        # }
        #
        # for ticket_number, priority_value in ticket_numbers:
        #     print(priority_map[priority_value + 1])
        #     response = await inc.update(Incident.number == ticket_number,
        #                                 dict(priority=(2, "High"),
        #                                      description="checking aiosnow update234")
        #                                 )
        #     output.append(f"Updated: {response['number']}, new priority: {response['priority'].key}, response: {response['description']}")

        print(output)

asyncio.run(main())