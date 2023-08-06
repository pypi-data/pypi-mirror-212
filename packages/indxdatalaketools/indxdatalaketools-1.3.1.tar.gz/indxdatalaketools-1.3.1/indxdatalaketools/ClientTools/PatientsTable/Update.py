#
#   Created By Ryan McDermott
#   Created on 2/21/2022
#

import datetime
from indxdatalaketools import Helpers
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients
from indxdatalaketools.Helpers import print_error
from indxdatalaketools.GoogleClientWrappers import BigQuery
from indxdatalaketools.PatientsHoldingApi import HoldingTable


class Client:
    '''
        Class that handles all functionlaity to update a patient in the PATIENTS table
    '''
    client_uuid = ''
    dataset_id = ''
    patient_table_name = ''
    overwrite = False

    __patient_insert_logger = None
    __big_query_wrapper = None

    def __init__(self, client_uuid):
        '''
            Init function that sets up client credentials, uuid, 
            and google big query client used to insert items to the Patients table
            Args:
                google_clients          (ApiClients): object containing all Google Api Clients
                client_uuid             (string): The client's uuid
            Returns:
                None
        '''
        self.client_uuid = client_uuid
        self.dataset_id = "indx-data-services."+self.client_uuid.\
            replace("-", "_")
        self.patient_table_name = self.dataset_id + ".PATIENTS"
        logging_client = GcpClients.instance().get_logging_client()
        self.__patient_insert_logger = logging_client.logger(client_uuid +
                                                             '-patient-logger')

    def update_patient_in_patient_table(self,
                                        patient_data,
                                        patient_row,
                                        overwrite=False):
        '''
            function that checks to see if the patient in the table needs to get updated or not
            and then applies the update if applicable.
            Args:
                patient_data    (dict): The information for the patient
                patient_row     (row): The row that we wish to update in the Table
                overwrite       (boolean): Flag to indicate whether or not we can over 
                    write the patients data
            Returns:
                boolean: True if the update was successful or if the patient 
                    did not need to be updated, False if otherwise
        '''
        self.overwrite = overwrite
        if self.__compare_dict_to_table_row(patient_data, patient_row):
            # The Patient Data is updatable so update
            time_now = datetime.datetime.utcnow()
            patient_update_time = datetime.datetime.fromisoformat(
                str(patient_row.get("UPDATED_AT")))
            if time_now < patient_update_time + datetime.timedelta(minutes=90):

                patient_data['UPDATED_AT'] = None
                patient_data = Helpers.convert_keys_in_dictionary(patient_data)
                patient_data['action'] = "UPDATED"
                self.__patient_insert_logger.log_text(
                    'staging patient data ' + str(patient_data) + " for update",
                    severity='INFO')
                return HoldingTable.Client().insert_data_to_holding_table(
                    patient_data)

            return self.__update_patients_table_row_with_dml(
                patient_data, patient_row=patient_row)

        print("Nothing to Update for Patient " + patient_data["PATIENT_ID"])
        return True

    def __update_patients_table_row_with_dml(self,
                                             patient_data,
                                             patient_row=None):
        '''
            This function updates the row of a table with new data. CLIENT_ID, PATIENT_ID,
            and MRN cannot be updated. This function builds the DPL query based on what the client
            wishes to update. Only values that are null in the PATIENTS table will be updated. if 
            overwrite is False then patient row must be passed.
            Args:
                patient_data    (dict): The new data that needs to be updated
                patient_row     (row): The row found in the big query table
            Returns:
                Boolean: True if the operation was succesfull, false if otherwise
        '''
        dml_query = self.__create_dml_update_query(patient_data, patient_row)
        if BigQuery.Wrapper().perform_query(dml_query) is None:
            self.__patient_insert_logger.log_text(
                'could not update patient info ' + str(patient_data),
                severity='WARNING')
            return False

        self.__patient_insert_logger.log_text('updated patient info ' +
                                              str(patient_data),
                                              severity='INFO')
        return True

    def __create_dml_update_query(self, patient_data, patient_row=None):
        '''
            Creates the dlp query necessary to update a Patient in the PATIENTS table
            Args:
                patient_data    (dict): The new data that needs to be updated
                patient_row     (row): The row found in the big query table
                overwrite       (boolean): Flag to indicate whether or not we can over 
                    write the patients data
            Returns:
                string: The query we wish to run on the PATIENTS table
        '''
        table_name = "indx-data-services." + self.client_uuid.replace(
            '-', '_') + ".PATIENTS"
        dml_query = 'UPDATE `' + table_name + '` SET '

        for k in patient_data:
            dml_query += self.__populate_changed_keys_in_query(
                k, patient_row.get(k), patient_data[k])

        # remove last comma
        dml_query = dml_query[:-2] + ' '
        dml_query += 'WHERE PATIENT_ID = \'' + patient_data['PATIENT_ID'] + '\''
        return dml_query

    def __populate_changed_keys_in_query(self, key, patient_row_value,
                                         patient_data_value):
        '''
            Populates all keys that are to be updated for the patient
            Args:
                key                (string): The key we are using to compare the Patients
                    Data
                patient_row_value  (string): The value found in the patient row for a 
                    given key
                patient_data_value (stirng): The value passed in the json for a given
                    key
            Returns:
                string: The new string to append to the dlp query, empty if nothing needs 
                    to be added
        '''
        #Client ID, Patient ID, and MRN are immutable
        if key == "CLIENT_ID" or key == "MRN" or \
            key == "PATIENT_ID" or key == "PATIENT_PARTITION" or key == 'DATE_INSERTED':
            return ''

        if self.overwrite == False and patient_data_value is None:
            return ''

        # New information can always be added to a patient record
        if self.overwrite == False and patient_row_value is None:
            return key + ' = \'' + str(patient_data_value) + '\', '

        # Overwriting existing information requires a special command
        if self.overwrite == True and patient_data_value is not None:
            return key + ' = \'' + str(patient_data_value) + '\', '

        # overwriting existing
        if self.overwrite == True and patient_data_value is None:
            return key + ' = DEFAULT, '

        return ''

    def __compare_dict_to_table_row(self, patient_data, patient_row):
        '''
            Function that compares the client provided json data to the information
            contained in the PATIENTS table for a specific PATIENT_ID. If
            they are the same then we do not need to update. If the PATIENTS table
            contains more information we do not need to update.
            Args:
                patient_data    (dict): The dictionary containing the client provided patient
                    informations
                patient_row     (row): The information found in the PATIENTS table for a specific
                    PATIENT_ID
            Returns:
                True if a patient needs to be updated, false if otherwise.
        '''

        status = True

        if self.overwrite == True:
            return True

        if self.__compare_checksum(patient_data, patient_row):
            print("No Changes in Checksum")
            return False

        # compare, the changes in the two records
        for k in patient_data:
            if k == "CLIENT_ID" or k == "MRN" or k == "PATIENT_ID" \
            or k == "UPDATED_AT" or k == "CHECKSUM" or \
                k == "PATIENT_PARTITION" or k == 'DATE_INSERTED':
                continue

            elif not self.__is_updateable(patient_data[k], patient_row.get(k)):
                status = False

        return status

    def __compare_checksum(self, patient_data, patient_row):
        '''
            Function that compares the tnew value and old values checksum to see if 
            the values are the same or not.
            Args:
                patient_data    (dict): The dictionary containing the client provided patient
                    informations
                patient_row     (row): The information found in the PATIENTS table for a specific
                    PATIENT_ID
            Returns:
                boolean: True if the values are the same, False if they are different
        '''
        if patient_data['CHECKSUM'] == patient_row.get('CHECKSUM'):
            return True

        return False

    def __is_updateable(self, input_value, existing_value):
        '''
            Function that checks whether or not there is new data in the
            json passed for a patient. If the the values are the same True is returned. 
            Args:
                patient_json_value (string): The value of the patient json data passed in
                existing_value  (string): The value already existing in the PATIENTS table
            Returns:
                boolean: True if there is more data passed, False if not
        '''
        if input_value is None and existing_value is None:
            # no values, is updateable
            return True

        if input_value is None and existing_value is not None and self.overwrite == False:
            # no trying to replace value this none, not updateable
            return False

        if input_value is not None and existing_value is None:
            # can update the patient
            return True

        if input_value is not None and existing_value is not None and self.overwrite == False:
            if input_value == existing_value:
                # no change here
                return True
            print(input_value, existing_value)
            # different values cannot overwrite, not updateable
            print_error(
                "Cannot overide values in the PATIENT table using this command,"
                + " try patients-table update command instead.")
            return False

        # default changeable
        return True