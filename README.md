# Broker Data Retrieval
This Python script retrieves broker data from an API endpoint and stores it offline in an unmodified state to ensure data accuracy from the database.

# Requirements
- Python 3.7 or higher
- Required Python libraries: httpx, asyncio, openpyxl, aiolimiter

## Usage
Run the script by executing the following command:
`python broker_data_retrieval.py`
The script will retrieve broker data from the specified API endpoint, cache the JSON output to individual files for each page of data, and save the firm source IDs to a text file named firm_source_ids.txt. The execution time will be displayed upon completion.

## Description
- The script fetches broker data from the FINRA BrokerCheck API asynchronously.
- It logs HTTP requests and responses for monitoring purposes.
- Retrieved JSON data is cached to individual files for each page of data to ensure offline availability and data accuracy.
- Firm source IDs are saved to a text file for future reference.
- Error handling is implemented to handle potential issues during data retrieval and caching.

# Acknowledgment
This script is designed to retrieve broker data and store it offline for further analysis and processing. Future updates may include additional functionality for processing the retrieved data.

# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/OGNamsta/brokerCheck/blob/master/MIT_Licence.txt) file for details.