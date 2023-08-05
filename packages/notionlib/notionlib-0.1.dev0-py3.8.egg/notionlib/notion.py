import datetime
import json
import os
import pandas as pd
import requests
import urllib.request

#PERSON_PROPERTY = "email"
PERSON_PROPERTY = "id"


class Notion:

    def __init__(self, api_token):
        self.api_token = api_token
        #self.api_version = "2022-06-28" # Breaks everything!
        self.api_version = "2021-08-16"


    @property
    def request_header(self):
        header_dict = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": self.api_version
        }
        return header_dict


    def retrieve_a_page(self, page_id):
        """
        _summary_

        https://developers.notion.com/reference/retrieve-a-page

        Parameters
        ----------
        page_id : _type_
            _description_
        requested_property_type : str, optional
            _description_, by default "title"
        requested_property_name : _type_, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        Exception
            _description_
        """

        url = f"https://api.notion.com/v1/pages/{page_id}"

        resp = requests.get(url, headers=self.request_header)

        if resp.status_code != 200:
            # https://developers.notion.com/reference/retrieve-a-page#errors
            msg = os.linesep.join([
                    resp.reason,
                    "; ".join([f"{k}: {v}" for k, v in resp.json().items()])
                ])
            raise Exception(msg)

        value_dict = {}

        for k, v in resp.json()["properties"].items():
            value_dict[k] = self.parse_database_property_object(v)

        return value_dict


    def query_a_database(self, notion_db_id, return_dataframe=False, ignored_properties=None, ignored_properties_type=None):
        """
        Gets a list of Pages contained in the database.

        https://developers.notion.com/reference/post-database-query

        Parameters
        ----------
        notion_db_id : _type_
            _description_
        return_dataframe : bool, optional
            _description_, by default False
        ignored_properties : _type_, optional
            _description_, by default None
        ignored_properties_type : _type_, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """        
        RESERVED_PROPERTY_NAMES = ("created_by", "created_time", "last_edited_by", "last_edited_time", "page_id")

        notion_page_dict_list = []

        url = f"https://api.notion.com/v1/databases/{notion_db_id}/query"

        requests_data_dict = {
            "page_size": 100
        }

        if ignored_properties_type is None:
            ignored_properties_type = []
        elif isinstance(ignored_properties_type, str):
            ignored_properties_type = [ignored_properties_type]

        if ignored_properties is None:
            ignored_properties = []
        elif isinstance(ignored_properties, str):
            ignored_properties = [ignored_properties]

        has_more = True
        while has_more:
            resp = requests.post(url, headers=self.request_header, data=json.dumps(requests_data_dict))

            if resp.status_code != 200:
                # https://developers.notion.com/reference/post-database-query#errors
                msg = os.linesep.join([
                        resp.reason,
                        "; ".join([f"{k}: {v}" for k, v in resp.json().items()]),
                        json.dumps(requests_data_dict)
                    ])
                raise Exception(msg)

            for page in resp.json()['results']:
                page_dict = {
                    'page_id': page['id'],
                    'created_time': datetime.datetime.strptime(page['created_time'], r"%Y-%m-%dT%H:%M:%S.000Z"),
                    'created_by': page['created_by']['id'],
                    'last_edited_time': datetime.datetime.strptime(page['last_edited_time'], r"%Y-%m-%dT%H:%M:%S.000Z"),
                    'last_edited_by': page['last_edited_by']['id']
                }

                for property, property_dict in page["properties"].items():
                    if (property not in ignored_properties) and (property_dict["type"] not in ignored_properties_type):
                        if property not in RESERVED_PROPERTY_NAMES:
                            page_dict[property] = self.parse_database_property_object(property_dict)
                        else:
                            raise ValueError(f'Property name "{property}" is reserved... Please rename this property in Notion.')    # TODO: it suck... Improve it!

                notion_page_dict_list.append(page_dict)

            has_more = resp.json()['has_more']

            if has_more:
                requests_data_dict = {
                    "page_size": 100,
                    "start_cursor": resp.json()['next_cursor']
                }

        if return_dataframe:
            return pd.DataFrame(notion_page_dict_list)
        else:
            return notion_page_dict_list


    def parse_notion_datetime_str(self, datetime_str):
        if datetime_str is None:
            return None
        elif "T" in datetime_str:
            return datetime.datetime.strptime(datetime_str, r"%Y-%m-%dT%H:%M:%S.000%z")
        else:
            return datetime.date.fromisoformat(datetime_str)


    def parse_notion_datetime_property(self, property_dict):
        value = None

        if property_dict is not None:
            start = self.parse_notion_datetime_str(property_dict["start"])
            end = self.parse_notion_datetime_str(property_dict["end"])       # TODO: utliser plutôt un timerange ?
            timezone = property_dict["time_zone"]                            # TODO: ajouter une timezone ?

            if end is None:
                value = start
            else:
                value = (start, end)                                         # TODO: utliser plutôt un timerange ?

        return value


    def parse_database_property_object(self, property_dict):
        """
        _summary_

        https://developers.notion.com/reference/property-object
        https://developers.notion.com/reference/property-item-object

        Parameters
        ----------
        property_dict : _type_
            _description_

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        NotImplementedError
            _description_
        ValueError
            _description_
        Exception
            _description_
        """        

        if property_dict["type"] == "title":
            # https://developers.notion.com/reference/property-item-object#title-property-values
            value = ""
            for line in property_dict["title"]:
                value += line['plain_text']

        elif property_dict["type"] == "rich_text":
            # https://developers.notion.com/reference/property-item-object#rich-text-property-values
            value = ""
            for line in property_dict["rich_text"]:
                value += line['plain_text']

        elif property_dict["type"] == "number":
            # https://developers.notion.com/reference/property-item-object#number-property-values
            value =  property_dict["number"]

        elif property_dict["type"] == "select":
            # https://developers.notion.com/reference/property-item-object#select-property-values
            value = None
            if property_dict["select"] is not None:
                value = property_dict["select"]["name"]

        elif property_dict["type"] == "status":
            # https://developers.notion.com/reference/property-item-object#multi-select-property-values
            value = None
            if property_dict["status"] is not None:
                value = property_dict["status"]["name"]

        elif property_dict["type"] == "multi_select":
            # https://developers.notion.com/reference/property-item-object#multi-select-property-values
            value = set()
            for ms in property_dict["multi_select"]:
                value.add(ms["name"])
            value = list(value)

        elif property_dict["type"] == "date":
            # https://developers.notion.com/reference/property-item-object#date-property-values
            value = self.parse_notion_datetime_property(property_dict["date"])

        elif property_dict["type"] == "formula":
            # https://developers.notion.com/reference/property-item-object#formula-property-values
            value = None

            if property_dict["formula"]["type"] == "boolean":
                value = property_dict["formula"]["boolean"]
            elif property_dict["formula"]["type"] == "string":
                value = property_dict["formula"]["string"]
            elif property_dict["formula"]["type"] == "number":
                value = property_dict["formula"]["number"]
            elif property_dict["formula"]["type"] == "date":
                value = self.parse_notion_datetime_property(property_dict["formula"]["date"])
            else:
                raise NotImplementedError()

        elif property_dict["type"] == "relation":
            # https://developers.notion.com/reference/property-item-object#relation-property-values
            value = set()
            for ms in property_dict["relation"]:
                page_id = ms["id"]
                value.add(page_id)
                #page_title = self.retrieve_a_page(page_id)
                #value.add(list(page_title.items())[0][1])    # TODO !!!
                
            value = list(value)

        elif property_dict["type"] == "rollup":
            # https://developers.notion.com/reference/property-item-object#rollup-property-values
            value = None

            if property_dict["rollup"]["type"] == "number":
                value = property_dict["rollup"]["number"]

            elif property_dict["rollup"]["type"] == "date":
                value = self.parse_notion_datetime_property(property_dict["rollup"]["date"])

            elif property_dict["rollup"]["type"] == "array":
                value = list()
                for array_item_dict in property_dict["rollup"]["array"]:
                    value.append(self.parse_database_property_object(array_item_dict))
                value = value

            else:
                raise NotImplementedError()

        elif property_dict["type"] == "people":
            # https://developers.notion.com/reference/property-item-object#people-property-values
            value = set()

            for ms in property_dict["people"]:
                if PERSON_PROPERTY == "name":
                    person_value = ms["name"]
                elif PERSON_PROPERTY == "email":
                    person_value = ms["person"]["email"]
                elif PERSON_PROPERTY == "id":
                    person_value = ms["id"]
                elif PERSON_PROPERTY == "avatar":
                    person_value = ms["avatar_url"]
                else:
                    raise ValueError(f'Unknown person property "{PERSON_PROPERTY}". Valid values are: "name", "email", "id" and "avatar"')
                value.add(person_value)

            value = list(value)

        elif property_dict["type"] == "files":
            # https://developers.notion.com/reference/property-item-object#files-property-values
            value = set()

            for file_dict in property_dict["files"]:
                file_name = file_dict["name"]
                file_url = file_dict["file"]["url"]

                # https://stackoverflow.com/questions/22676/how-to-download-a-file-over-http
                #blob_str = requests.get(file_dict["file"]["url"]).text
                #blob_bin = requests.get(file_dict["file"]["url"]).content
                #local_blob_bin_path = urllib.request.urlretrieve(file_dict["file"]["url"])[0]   # return the local file path
                value.add(file_url)                     # TODO : download the file and provide the blob ?
            
            value = list(value)

        elif property_dict["type"] == "checkbox":
            # https://developers.notion.com/reference/property-item-object#checkbox-property-values
            value =  property_dict["checkbox"]

        elif property_dict["type"] == "url":
            # https://developers.notion.com/reference/property-item-object#url-property-values
            value =  property_dict["url"]

        else:
            raise Exception(f'Unknown property type "{property_dict["type"]}"')

        return value


    ###########################################################################
    # MAKE PAGES ##############################################################
    ###########################################################################

    def create_a_page(self, notion_db_id, properties, verbose=False):
        # https://developers.notion.com/reference/post-page

        data_dict = {
            "parent": {
                "database_id": notion_db_id
            },
            "properties": {}
        }

        for notion_property_name, notion_property_dict in properties.items():
            notion_property_type = notion_property_dict["type"]
            notion_property_value = notion_property_dict["value"]
            if notion_property_value is not None:
                data_dict["properties"][notion_property_name] = self.make_property(type=notion_property_type, value=notion_property_value)

        url = f"https://api.notion.com/v1/pages"

        resp = requests.post(url, headers=self.request_header, data=json.dumps(data_dict))

        if resp.status_code != 200:
            # C.f. https://developers.notion.com/reference/post-page#errors
            if resp.status_code == 404:
                raise Exception("The specified parent database or page does not exist, or if the integration does not have access to the parent")
            else:
                msg = os.linesep.join([
                    resp.reason,
                    "; ".join([f"{k}: {v}" for k, v in resp.json().items()]),
                    json.dumps(data_dict)
                ])
                raise Exception(msg)

        if verbose:
            print(json.dumps(resp.json(), sort_keys=False, indent=4))
        
        return resp.json()


    def update_a_page(self, notion_page_id, properties):
        # https://developers.notion.com/reference/patch-page

        data_dict = {
            "properties": {}
        }

        for notion_property_name, notion_property_dict in properties.items():
            notion_property_type = notion_property_dict["type"]
            notion_property_value = notion_property_dict["value"]
            if notion_property_value is not None:
                data_dict["properties"][notion_property_name] = self.make_property(type=notion_property_type, value=notion_property_value)

        url = f"https://api.notion.com/v1/pages/{notion_page_id}"

        resp = requests.patch(url, headers=self.request_header, data=json.dumps(data_dict))

        if resp.status_code != 200:
            # https://developers.notion.com/reference/patch-page#errors
            msg = os.linesep.join([
                    resp.reason,
                    "; ".join([f"{k}: {v}" for k, v in resp.json().items()]),
                    json.dumps(data_dict)
                ])
            raise Exception(msg)

        return resp.json()


    def check_value_type(self, value, expected_types):
        if not isinstance(value, expected_types):
            raise ValueError(f"Value {value} is not compatible with expected type {expected_types}")


    def make_property(self, type, value):

        property_dict = {}

        if type == "title":
            # https://developers.notion.com/reference/property-value-object#title-property-values
            self.check_value_type(value, str)
            property_dict["title"] = [{"text": {"content": value}}]   # TODO: multi lines ???

        elif type == "rich_text":
            # https://developers.notion.com/reference/property-value-object#rich-text-property-values
            property_dict["rich_text"] = []
            if isinstance(value, (list, tuple)):
                for line in value:
                    self.check_value_type(line, str)
                    property_dict["rich_text"].append({"text": {"content": line}})
            elif isinstance(value, str):
                property_dict["rich_text"] = [{"text": {"content": value}}]
            else:
                self.check_value_type(value, (list, tuple, str))

        elif type == "number":
            # https://developers.notion.com/reference/property-value-object#number-property-values
            self.check_value_type(value, (int, float))
            property_dict["number"] = value

        elif type == "select":
            # https://developers.notion.com/reference/property-value-object#select-property-values
            self.check_value_type(value, str)
            property_dict["select"] = {"name": value}

        elif type == "status":
            # https://developers.notion.com/reference/property-value-object#status-property-values
            self.check_value_type(value, str)
            property_dict["status"] = {"name": value}

        elif type == "multi_select":
            # https://developers.notion.com/reference/property-value-object#multi-select-property-values
            property_dict["multi_select"] = []
            for item in value:
                self.check_value_type(item, str)
                property_dict["multi_select"].append({"name": item})

        elif type == "date":
            # https://developers.notion.com/reference/property-value-object#date-property-values
            raise NotImplementedError()  # TODO !!!

        elif type == "formula":
            # https://developers.notion.com/reference/property-value-object#formula-property-values
            raise NotImplementedError()  # TODO !!!

        elif type == "relation":
            # https://developers.notion.com/reference/property-value-object#relation-property-values
            self.check_value_type(value, (str, list, tuple))
            if isinstance(value, str):
                property_dict["relation"] = [{"id": value}]
            elif isinstance(value, list, tuple):
                property_dict["relation"] = []
                for page_id in value:
                    property_dict["relation"].append({"id": page_id})

        elif type == "rollup":
            # https://developers.notion.com/reference/property-value-object#rollup-property-values
            raise NotImplementedError()  # TODO !!!

        elif type == "people":
            # https://developers.notion.com/reference/property-value-object#people-property-values
            raise NotImplementedError()  # TODO !!!

        elif type == "files":
            # https://developers.notion.com/reference/property-value-object#files-property-values
            raise NotImplementedError()  # TODO !!!

        elif type == "checkbox":
            # https://developers.notion.com/reference/property-value-object#checkbox-property-values
            self.check_value_type(value, bool)
            property_dict["checkbox"] = value

        elif type == "url":
            # https://developers.notion.com/reference/property-value-object#url-property-values
            self.check_value_type(value, str)
            property_dict["url"] = value

        else:
            raise ValueError(f'Unknown property type "{type}"')

        return property_dict