import requests

# Your API endpoint
url = 'https://pupqcfis-com.onrender.com/api/all/Faculty_Profile'

# Replace 'your_api_key_here' with your actual API key
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiIzM2Y0ZWI4NWNjNDQ0MTQzOWFkMzMwYWUzMzJiNmYwYyJ9.5pjwXdaIIZf6Jm9zb26YueCPQhj6Tc18bbZ0vnX4S9M'

# Set up headers with the API key in the 'API Key' authorization header
headers = {
    'Authorization': 'API Key',
    'token': api_key,  # 'token' key with the API key value
    'Content-Type': 'application/json'  # Adjust content type as needed
}

# Make a GET request to the API with the API key in the headers
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Process the API response data
    api_data = response.json()
    print("Success Fetch api data:" + str(response.status_code))
    
    # RETURNING SPECIFIC DATA FROM ALL FACULTIES
    
    # Extracting faculty_account_ids into a list
    faculty_account_ids = list(api_data['Faculties'].keys())

    # Fetching Specific data for each faculty
    for faculty_id in faculty_account_ids:
        faculty_info = api_data['Faculties'][faculty_id]
        faculty_rank = faculty_info['rank']
        faculty_name = faculty_info['name']
        faculty_email = faculty_info['email']

        print("\nFaculty ID:", faculty_id)
        print("Rank:", faculty_rank)
        print("Name:", faculty_name)
        print("Email:", faculty_email)

    
    # RETURNING API DATA FROM EACH ATTRIBUTES

    print("\n\nEXAMPLE FETCH\n")
    print("FACULTY DATA")
    print(api_data['Faculties']['000-000-A-029'])
    print("\n\nFACULTY SPECIFIC DATA")
    print(api_data['Faculties']['000-000-A-029']['name'])
    print(api_data['Faculties']['000-000-A-029']['email'])
    print(api_data['Faculties']['000-000-A-029']['rank'])
    
else:
    print("Failed to fetch data. Status code:", response.status_code)
    

