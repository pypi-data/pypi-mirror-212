#
#   Created by Ryan McDermott
#   Created on  2/24/2022
#

import re
import cv2
import os

from indxdatalaketools.GoogleClients.GoogleClients import GcpClients

import numpy as np

from indxdatalaketools import Helpers
from indxdatalaketools.ClientTools.PatientsTable import Insert
from indxdatalaketools.ClientTools.Changelog import Insert as ChnglogInsert
from indxdatalaketools.DataStandardizer import PatientTable

from indxdatalaketools import DataLakeGlobals


class Client:
    '''
        Class that contains all the functionality to upload a file
        to a data lake
    '''

    client_uuid = ''
    text_file_list = [".txt", ".tsv", ".csv"]

    def __init__(self, client_uuid):
        '''
            Init function that sets up client credentials, uuid, 
            and google api clients used to upload files to a GCS bucket
            Args:
                google_clients          (ApiClients): object containing all Google Api Clients
                client_uuid             (string): The client's uuid
            Returns:
                None
        '''
        self.client_uuid = client_uuid
        self.__file_upload_logger = GcpClients.instance().get_logging_client(
        ).logger(client_uuid + '-file-logger')

    def upload_file_to_datalake(self, modality, mrn, metadata, file_path, 
                                patient_uuid=None):
        '''
            Uploads a file to the data lake and sets the metadata
            for that file
            Args:
                modality    (string): The file's modality
                mrn         (string): The mrn of the patient to who the files 
                    belongs to
                metadata    (string): The metadata that is associated with the
                    file
                file_path   (string): The path to the file we wish to upload 
                    to a datalake
                patient_uuid (string): If this optional argument is set, 
                    mrn is bypassed and this string is used as the hashed 
                    patient mrn
            Returns:
                boolean: True if the File was successfully uploaded, False if 
                    otherwise
                
        '''
        file_contents = self.__read_file_contents(file_path)
        file_extension = os.path.splitext(file_path)[1]

        DataLakeGlobals.SIZE_OF_FILES += len(file_contents) * .000001

        # convert bmp to png
        if '.bmp' == file_extension.lower():
            file_contents = self.__convert_bmp_to_png(file_contents)
            file_root = os.path.splitext(file_path)[0]
            file_path = file_root + '.png'

        stripped_mrn = self.__strip_leading_zeros(mrn)
        if patient_uuid is not None:
            hashed_patient_mrn = patient_uuid
        else:
            hashed_patient_mrn = Helpers.patient_hash(self.client_uuid, 
                                                      [stripped_mrn])[0]
        hashed_file_name = Helpers.hash_contents_to_file_name(
            file_path, file_contents)
        blob_name = modality + "/" + hashed_patient_mrn + "/" + hashed_file_name
        bucket = GcpClients.instance().get_storage_client().bucket(
            self.client_uuid)
        blob = bucket.blob(blob_name)

        if '.pdf' == file_extension.lower():
            blob.content_type = "application/pdf"

        if Helpers.try_blob_exists(blob):
            Helpers.print_error("File" + blob.name + " already exists")
            self.__file_upload_logger.log_text("File" + blob.name +
                                               " already exists",
                                               severity='INFO')
            return True

        if not self.__create_blob_with_metadata(blob, file_contents, metadata):
            Helpers.print_error("Could not upload file " + file_path +
                                " to datalake")
            return False

        if hashed_patient_mrn != 'UNKNOWN'and \
            not self.__insert_data_to_patients_table(stripped_mrn, hashed_patient_mrn):
            Helpers.print_error("Could not insert data to PATIENTS table")
            return False

        blob.metadata = metadata
        return ChnglogInsert.Client(self.client_uuid).insert_to_changelog_table(
            blob, 'CREATED')

    def __convert_bmp_to_png(self, file_bytes):
        '''
            Converts the BMP bytes string into a png bytes string
            Args:
                byte (string): The string of bytes we wish to convert
            Returns:
                string: The converted bytes in string format
        '''
        nparr = np.frombuffer(file_bytes, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        png_img = cv2.imencode('.png', img)[1]
        data_encode = np.array(png_img)
        byte_encode = data_encode.tobytes()

        return byte_encode

    def __strip_leading_zeros(self, string_to_strip):
        '''
            strips the leading '0' from a string
            Args:
                string_to_strip (string): Te string we wish to strip
            Returns:
                string: The string with leading '0' stripped
        '''
        stripped_string = re.sub("^0+", "", string_to_strip)

        return stripped_string

    def __insert_data_to_patients_table(self, mrn, hashed_patient_mrn):
        '''
            Inserts the file's patient to the patient table
            Args:
                mrn (string): the patients mrn
                hashed_patient_mrn (stirng): the patient id
        '''
        patient_data = {
            "MRN": mrn,
            "CLIENT_ID": self.client_uuid,
            "PATIENT_ID": hashed_patient_mrn
        }

        patient_data = PatientTable.Client().standardize(patient_data)

        if Insert.Client(
                self.client_uuid).insert_data_to_patients_table(patient_data):
            return True

        Helpers.print_error('Failed to upload ' + str(patient_data) +
                            ' to patients table')
        return False

    def __create_blob_with_metadata(self, blob, file_contents, metadata):
        '''
            Creates the blob in GCS and adds metadata to it
            Args:
                blob (google.cloud.storage.blob): The blob we want to upload
                file_contents (bytes): The bytes of the file we wish to upload
                metadata (dict): The files Metadata
            Returns:
                boolean: True if the operation was successful, False if otherwise
        '''
        # add metadata to blob and save in bucket
        blob.metadata = metadata

        if not self.__try_upload_blob(blob, file_contents):
            return False

        if Helpers.try_blob_exists(blob):
            print('successfully uploaded file to datalake')
            self.__file_upload_logger.log_text('successfully uploaded file ' +
                                               blob.name + ' to datalake',
                                               severity='INFO')
            if metadata['MODALITY'] != metadata['CLASSIFIED_MODALITY']:
                self.__file_upload_logger.log_text(
                    'Classified Modality for ' + blob.name + ' (' +
                    metadata['CLASSIFIED_MODALITY'] +
                    ') does not matched metadata supplied (' +
                    metadata['MODALITY'] + ')',
                    severity='WARNING')

            return True

        return False

    def __read_file_contents(self, file_path):
        """
            Reads file from the file path, has the capabilities to read from local file,
            network file, and url. The file will be decoded to UTF-8 and remove carraige returns
            "\r" to match LF encoding.

            Args:
                file_path: The local file path, server file path or url
            Returns:
                string: string representation of data found
        """

        extension = os.path.splitext(file_path)[1].lower()

        if "gs://" in file_path:
            # GCS BUCKET
            if extension in self.text_file_list:
                content = self.__read_gcs_blob(file_path)
                return content.replace(b'\r\n', b'\n')
            else:
                file_bytes = self.__read_gcs_blob(file_path)
                return file_bytes

        # LOCAL FILE
        if extension in self.text_file_list:
            content = open(file_path, 'rb').read()
            return content.replace(b'\r\n', b'\n')
        else:
            file_bytes = open(file_path, 'rb').read()
            return file_bytes

    def __read_gcs_blob(self, gcs_blob_path):
        '''
            Reads a blob from GCS and returns the bytes 
            Args:
                gcs_blob_path (string): The path to the blob
            Returns:
                bytes: contents of the gcs blob
        '''
        file_path = gcs_blob_path.replace("gs://", "")
        bucket_name = file_path.split("/")[0]
        source_blob_name = file_path.split("/", 1)[1]
        bucket = GcpClients.instance().get_storage_client().bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        content = blob.download_as_bytes()

        return content

    def __try_upload_blob(self, blob, contents):
        '''
            Tries to upload a blob to GCS with string contents
            Args:
                blob (google.cloud.storage.Blob): The blob we wish to upload to
                contents (string): The files contents
        '''
        try:

            blob.upload_from_string(contents, content_type=blob.content_type)
            return True
        except Exception as e:
            Helpers.print_error("Could not upload blob " + str(e))
            self.__file_upload_logger.log_text(
                'Failed To Upload Blob ' + blob.name + ' using GCS client: ' +
                str(e),
                severity='ERROR')
            return False
