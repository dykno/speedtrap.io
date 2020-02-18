class KeyLookup:

    def __init__(self):
        self.key_to_client_dict = {}
        self.client_to_key_dict = {}

        with open('/run/secrets/api_keys', 'r') as key_file:
            for line in key_file:
                key, client = line.strip(';\r\n').replace('"', '').split(' ')
                self.key_to_client_dict[key] = client
                self.client_to_key_dict[client] = key

    def get_client_by_key(self, api_key):
        return self.key_to_client_dict[api_key]

    def get_key_by_client(self, client):
        return self.client_to_key_dict[client]
        
