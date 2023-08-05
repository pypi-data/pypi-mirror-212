import requests
import json



class PigeonsDB:

    __connection = None
    __index_p = None

    @staticmethod
    def search(query_text, k, metadata_filters=None, keywords=None):
        if PigeonsDB.__connection is None:
            print("Error: Connection not initialized.")
            return

        url = "http://test-search-1248249294.us-east-2.elb.amazonaws.com:8080/search"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "query_text": query_text,
            "k": k,
            "metadata_filters": metadata_filters,
            "keywords": keywords
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print the response
        res = response.text
        return res

    @staticmethod
    def init(API, DB_Name):
        index_p, connect = PigeonsDB.get_db_info(API, DB_Name)
        if connect:
            PigeonsDB.__connection = connect
            PigeonsDB.__index_p = index_p
        else:
            print("API key or DB name not found")

    @staticmethod
    def get_db_info(api_key, db_name):
        url = "http://ec2-52-14-162-65.us-east-2.compute.amazonaws.com/api/v1/sdk/get-db-info"
        headers = {"Content-Type": "application/json"}
        data = {"api_key": api_key, "dbname": db_name}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Extract data from the response
        db_info = response.json().get('DB info', {})
        print(db_info)
        index_p = db_info.get('s3_identifier')

        # Create db object with specific keys
        keys = ['dbname', 'user', 'password', 'host']
        connect = {key: db_info.get(key) for key in keys}
        print(connect)
        return index_p, connect


    @staticmethod
    def add(documents, metadata_list):
        if PigeonsDB.__connection is None:
            print("Error: Connection not initialized.")
            return

        url = "http://add-dev-177401989.us-east-2.elb.amazonaws.com:8080/add_documents"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "documents": documents,
            "metadata_list": metadata_list
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print the response
        print(response.text)


PigeonsDB.get_db_info("psk-5debdb081c6649708218d7b2987b475b", "dbtest1")
