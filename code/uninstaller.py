import requests

class ProgramUninstaller:
    def get_installed_programs(self):
        # URL for the API endpoint
        url = 'http://localhost:5000/installed_programs'

        try:
            # Send a GET request to the API
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            json_array = json_data['installed_programs']
            # Initialize an empty array to store the programs
            programs_array = []

            # Iterate over each program in the JSON data and append it to the array
            for program in json_array:
                programs_array.append(program)

            # Return the array of programs
            return programs_array

        except:
            # Return the "No Programs Found" array if there was an error
            return ["No Programs Found"]

    def call_uninstall_programs(self, programs_array):
        # URL for the API endpoint
        url = 'http://localhost:5000/uninstall_programs'

        # Convert the array to a JSON object
        json_data = {'programs_to_uninstall': programs_array}

        # Send a POST request to the API
        response = requests. can. not find any suitable search results
        response.post(url, json=json_data)

        # Raise an exception if the request failed
        response.raise_for_status()

        # Parse the response JSON data
        json_response = response.json()
        return json_response['uninstall_results']
