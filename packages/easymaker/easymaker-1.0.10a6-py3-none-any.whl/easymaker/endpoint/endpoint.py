import requests
import time
from datetime import timedelta
import easymaker
from easymaker.common import exceptions
from easymaker.common import utils
from easymaker.common.utils import status_code_utils
from easymaker.common import constants


class Endpoint:
    def __init__(self, endpoint_id=None):
        """
        Args:
            endpoint_id (str): Endpoint Id
        """
        self.easymaker_api_sender = easymaker.easymaker_config.api_sender
        if endpoint_id is not None:
            self.endpoint_id = endpoint_id
        self.default_endpoint_stage_info = None

    def create(self,
               model_id,
               endpoint_name,
               endpoint_instance_name,
               apigw_resource_uri,
               endpoint_instance_count=1,
               endpoint_description=None,
               tag_list=None,
               use_log=False,
               wait=True,
               # autoscaler_enable=False,
               # autoscaler_min_node_count=1,
               # autoscaler_max_node_count=10,
               # autoscaler_scale_down_enable=True,
               # autoscaler_scale_down_util_threshold=50,
               # autoscaler_scale_down_unneeded_time=10,
               # autoscaler_scale_down_delay_after_add=10,
               ):
        """
        Returns:
            endpoint_id(str)
        """

        self.instance_list = self.easymaker_api_sender.get_instance_list()
        response = self.easymaker_api_sender.create_endpoint(endpoint_name=endpoint_name,
                                                             endpoint_description=endpoint_description,
                                                             flavor_id=utils.from_name_to_id(self.instance_list, endpoint_instance_name),
                                                             model_id=model_id,
                                                             apigw_resource_uri=apigw_resource_uri,
                                                             node_count=endpoint_instance_count,
                                                             tag_list=tag_list,
                                                             use_log=use_log,
                                                             # ca_enable=autoscaler_enable,
                                                             # ca_min_node_count=autoscaler_min_node_count,
                                                             # ca_max_node_count=autoscaler_max_node_count,
                                                             # ca_scale_down_enable=autoscaler_scale_down_enable,
                                                             # ca_scale_down_util_thresh=autoscaler_scale_down_util_threshold,
                                                             # ca_scale_down_unneeded_time=autoscaler_scale_down_unneeded_time,
                                                             # ca_scale_down_delay_after_add=autoscaler_scale_down_delay_after_add,
                                                             )

        self.endpoint_id = response['endpoint']['endpointId']
        if wait:
            waiting_time_seconds = 0
            endpoint_status = status_code_utils.replace_status_code(response['endpoint']['endpointStatusCode'])
            while endpoint_status != 'ACTIVE':
                print(f'[AI EasyMaker] Endpoint create status : {endpoint_status} ({timedelta(seconds=waiting_time_seconds)}) Please wait...')
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                endpoint = self.easymaker_api_sender.get_endpoint_by_id(self.endpoint_id)
                endpoint_status = status_code_utils.replace_status_code(endpoint['endpoint']['endpointStatusCode'])
                if 'FAILED' in endpoint_status:
                    endpoint['endpoint']['endpointStatusCode'] = endpoint_status
                    raise exceptions.EasyMakerError(endpoint)

            endpoint_model_status = 'CREATE_REQUESTED'
            while endpoint_model_status != 'ACTIVE':
                print(f'[AI EasyMaker] Endpoint stage create status : {endpoint_model_status} ({timedelta(seconds=waiting_time_seconds)}) Please wait...')
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                self.get_endpoint_stage_info_list()
                endpoint_model_status = self.default_endpoint_stage_info['endpoint_status_code']
                if 'FAILED' in endpoint_model_status:
                    raise exceptions.EasyMakerError('FAILED_TO_DEPLOY_MODEL')
            print(f'[AI EasyMaker] Endpoint create complete. Endpoint Id : {self.endpoint_id}, Default Stage Id : {self.default_endpoint_stage_info["endpoint_stage_id"]}')
        else:
            print(f'[AI EasyMaker] Endpoint create request complete. Endpoint Id : {self.endpoint_id}')
        return self.endpoint_id

    def create_stage(self,
                     model_id,
                     stage_name,
                     endpoint_instance_name,
                     endpoint_instance_count=1,
                     stage_description=None,
                     tag_list=None,
                     use_log=False,
                     wait=True,
                     # autoscaler_enable=False,
                     # autoscaler_min_node_count=1,
                     # autoscaler_max_node_count=10,
                     # autoscaler_scale_down_enable=True,
                     # autoscaler_scale_down_util_threshold=50,
                     # autoscaler_scale_down_unneeded_time=10,
                     # autoscaler_scale_down_delay_after_add=10,
                     ):
        """
        Returns:
            stage_id(str)
        """

        self.instance_list = self.easymaker_api_sender.get_instance_list()
        response = self.easymaker_api_sender.create_stage(endpoint_id=self.endpoint_id,
                                                          stage_name=stage_name,
                                                          stage_description=stage_description,
                                                          flavor_id=utils.from_name_to_id(self.instance_list, endpoint_instance_name),
                                                          model_id=model_id,
                                                          apigw_resource_uri=self._get_apigw_resource_uri(),
                                                          node_count=endpoint_instance_count,
                                                          tag_list=tag_list,
                                                          use_log=use_log,
                                                          # ca_enable=autoscaler_enable,
                                                          # ca_min_node_count=autoscaler_min_node_count,
                                                          # ca_max_node_count=autoscaler_max_node_count,
                                                          # ca_scale_down_enable=autoscaler_scale_down_enable,
                                                          # ca_scale_down_util_thresh=autoscaler_scale_down_util_threshold,
                                                          # ca_scale_down_unneeded_time=autoscaler_scale_down_unneeded_time,
                                                          # ca_scale_down_delay_after_add=autoscaler_scale_down_delay_after_add,
                                                          )
        stage_id = ''
        if wait:
            waiting_time_seconds = 0
            endpoint_model_status = 'CREATE_REQUESTED'
            while endpoint_model_status != 'ACTIVE':
                print(f'[AI EasyMaker] Endpoint stage create status : {endpoint_model_status} ({timedelta(seconds=waiting_time_seconds)}) Please wait...')
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                endpoint_stage_info_list = self.get_endpoint_stage_info_list()
                for endpoint_stage_info in endpoint_stage_info_list:
                    if endpoint_stage_info['stage_name'] == stage_name:
                        endpoint_model_status = endpoint_stage_info['endpoint_status_code']
                        stage_id = endpoint_stage_info['endpoint_stage_id']
                if 'FAILED' in endpoint_model_status:
                    raise exceptions.EasyMakerError('FAILED_TO_DEPLOY_MODEL')
            print(f'[AI EasyMaker] Stage create complete. Stage Id : {stage_id}')
        else:
            print(f'[AI EasyMaker] Stage create request complete.')
        return stage_id

    def _get_apigw_resource_uri(self):
        return self.get_endpoint_model_list()['endpointModelList'][0]['apigwResourceUri']

    def get_endpoint_list(self):
        return self.easymaker_api_sender.get_endpoint_list()

    def get_endpoint_by_id(self):
        return self.easymaker_api_sender.get_endpoint_by_id(self.endpoint_id)

    def get_endpoint_model_list(self):
        return self.easymaker_api_sender.get_endpoint_model_list(self.endpoint_id)

    def get_endpoint_stage_list(self):
        return self.easymaker_api_sender.get_endpoint_stage_list(self.endpoint_id)

    def get_endpoint_stage_info_list(self):
        response = self.get_endpoint_stage_list()
        endpoint_stage_list = response['endpointStageList']
        endpoint_stage_info_list = []
        for endpoint_stage in endpoint_stage_list:
            endpoint_model_list = endpoint_stage['endpointModelList']
            for endpoint_model in endpoint_model_list:
                if 'apigwStageName' in endpoint_stage:
                    stage_name = endpoint_stage['apigwStageName']
                elif endpoint_stage['defaultStage']:
                    stage_name = 'default'
                else:
                    stage_name = ''

                endpoint_stage_info = {
                    'endpoint_stage_id': endpoint_stage['endpointStageId'],
                    'stage_name': stage_name,
                    'default_stage': endpoint_stage['defaultStage'],
                    'endpoint_status_code': status_code_utils.replace_status_code(endpoint_model['endpointModelStatusCode']),
                }

                if endpoint_model['endpointModelStatusCode'] != 'ACTIVE':
                    endpoint_stage_info['endpoint_url'] = ''
                else:
                    endpoint_stage_info['endpoint_url'] = 'https://' + endpoint_stage['apigwStageUrl'] + endpoint_model['apigwResourceUri']

                endpoint_stage_info_list.append(endpoint_stage_info)
            if endpoint_stage['defaultStage']:
                self.default_endpoint_stage_info = endpoint_stage_info

        return endpoint_stage_info_list

    def predict(self, endpoint_stage_info=None, json=None, files=None, data=None, headers=None):
        if endpoint_stage_info is None:
            if self.default_endpoint_stage_info is None:
                self.get_endpoint_stage_info_list()
            endpoint_stage_info = self.default_endpoint_stage_info

        response = requests.post(endpoint_stage_info['endpoint_url'], json=json, files=files, data=data, headers=headers).json()
        return response
