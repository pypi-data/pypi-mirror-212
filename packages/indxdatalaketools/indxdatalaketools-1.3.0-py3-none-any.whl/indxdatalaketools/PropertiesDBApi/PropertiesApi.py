#
#   Created by Ryan McDermott
#   Created on 7/7/2022
#

from indxdatalaketools.GoogleClientWrappers import SecretManager
from indxdatalaketools import Helpers

PROPERTIES_DB_URL = 'https://properties.indx.acuityeyegroup.dev/'
APPLICATION_JSON = "application/json"


class Client:
    '''
        Class that contains all the functionality make a call to Properties
        Database URL
    '''
    __project_id = ''
    __secret_id = ''
    __api_key = ''
    __properties_lists = {}

    def __init__(self):
        self.__project_id = 'indx-data-services'
        self.__secret_id = 'datalake-properties-db-api-key'
        self.__api_key = SecretManager.Wrapper().get_secret(
            self.__project_id, self.__secret_id)

    @Helpers.retry_decorator()
    def populate_modality_lists(self):
        '''
            populates the poperties lists dictionary
        '''
        lists = {}
        headers = {
            "Content-Type": APPLICATION_JSON,
            "x-api-key": self.__api_key
        }
        response = Helpers.create_get_request(PROPERTIES_DB_URL +
                                              "property-lists",
                                              headers=headers)
        property_lists = response['data']

        for property_list in property_lists:
            attributes = property_list['attributes']

            # do not need to include non enabled property lists
            if 'enabled' in attributes and attributes['enabled']:
                lists[attributes["list-name"]] = property_list["id"]

        #retry process here. empty list being returned from api,
        #raise exception
        if len(lists) == 0:
            raise Helpers.PropertiesTableException

        return lists

    def get_modalities(self):
        '''
            Function that returns a list of modlaites pulled from the properties database api
            Returns:
                - list: The list of modalities 
        '''
        if self.__properties_lists == {}:
            self.__properties_lists = self.populate_modality_lists()

        modalities = []
        headers = {
            "Content-Type": APPLICATION_JSON,
            "x-api-key": self.__api_key
        }
        modalties_id = self.__properties_lists['modalities']
        response = Helpers.create_get_request(PROPERTIES_DB_URL +
                                              "property-lists/" + modalties_id,
                                              headers=headers)
        modality_list = response['included']

        for property_value in modality_list:
            modality = property_value['attributes']["value"]
            modalities.append(modality)

        return modalities

    def get_race_codes(self):
        '''
            Function that returns the list of race codes pulled from the properties database api
            Returns:
                - list: The list of race codes
        '''
        if self.__properties_lists == {}:
            self.__properties_lists = self.populate_modality_lists()

        race_codes = []
        headers = {
            "Content-Type": APPLICATION_JSON,
            "x-api-key": self.__api_key
        }
        race_codes_id = self.__properties_lists['race-codes']
        response = Helpers.create_get_request(PROPERTIES_DB_URL +
                                              "property-lists/" + race_codes_id,
                                              headers=headers)
        modality_list = response['included']

        for property_value in modality_list:
            race_code = property_value['attributes']["value"]
            race_codes.append(race_code)

        return race_codes
