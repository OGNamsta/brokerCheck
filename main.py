import httpx
import asyncio
from time import perf_counter
from aiolimiter import AsyncLimiter
import openpyxl
import json


async def log_request(request):
    print(f"Request: {request.url!r} {request.method!r}")


async def log_response(response):
    print(f"Response: {response.url!r} {response.status_code!r}")


async def get_broker_id():
    headers = {
        'authority': 'api.brokercheck.finra.org',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,en-GB;q=0.8,de;q=0.7,es;q=0.6',
        'dnt': '1',
        'origin': 'https://brokercheck.finra.org',
        'referer': 'https://brokercheck.finra.org/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    firm_source_ids = []
    for page in range(123):
        url: str = f'https://api.brokercheck.finra.org/search/firm?state=NY&filter=broker=true,brokeria=true,active=true&hl=true&nrows=12&start={page * 12}&r=25&sort=score%2Bdesc&wt=json'

        async with httpx.AsyncClient(event_hooks={'request': [log_request], 'response': [log_response]},
                                     headers=headers, timeout=60.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                if content_type := response.headers.get('Content-Type', '').lower():
                    if 'application/json' in content_type:
                        data = response.json()
                        # Extract the firm_source_id. This is the ID we will use to get the broker data
                        firm_source_ids.extend([firm['_source']['firm_source_id'] for firm in data.get('hits', {}).get('hits', [])])

                        # Cache the JSON output to a file
                        with open(f'broker_data_{page + 1}.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            print(f"Data cached to broker_data_{page + 1}.json")

                    else:
                        print(f"Received error response: {response.status_code}")
                else:
                    print("No Content-Type header received")
            else:
                print(f"Received error response: {response.status_code}")

    # Save the firm_source_ids to a file
    with open('firm_source_ids.txt', 'w') as f:
        for firm_source_id in firm_source_ids:
            f.write(f'{firm_source_id}\n')

    # prints the length of the list
    print(len(firm_source_ids))
    return firm_source_ids


# async def get_broker_data():
# async with httpx.AsyncClient() as client:
# pass


async def main():
    start_time = perf_counter()
    # Fetch IDs
    broker_ids = await get_broker_id()
    print("Fetched broker IDs:", broker_ids)

    # Fetch Broker Data
    # broker_data = await get_broker_data()
    # print(broker_data.json())

    end_time = perf_counter()
    print('Time taken:', end_time - start_time, 'seconds')


if __name__ == '__main__':
    asyncio.run(main())
