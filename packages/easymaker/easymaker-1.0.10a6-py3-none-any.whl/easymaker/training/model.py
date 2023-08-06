import easymaker


class Model:
    def __init__(self):
        self.easymaker_api_sender = easymaker.easymaker_config.api_sender

    def create(self,
               model_name,
               training_id,
               model_description=None,
               tag_list=None,
               ):
        """
        Args:
            model_name (str): Experiment name
            training_id (str): Training Id
            model_description (str): Experiment description
            tag_list (list): tags
        Returns:
            model_id
        """
        response = self.easymaker_api_sender.create_model(model_name=model_name,
                                                          training_id=training_id,
                                                          model_description=model_description,
                                                          tag_list=tag_list)

        self.model_id = response['model']['modelId']
        print(f'[AI EasyMaker] Model create complete. Model Id : {self.model_id}')
        return self.model_id

    def create_by_model_uri(self,
                            model_name,
                            framework_code,
                            model_uri,
                            model_description=None,
                            tag_list=None,
                            ):
        """
        Args:
            model_name (str): Experiment name
            framework_code (str): easymaker.TENSORFLOW or easymaker.PYTORCH
            model_uri (str): model uri (NHN Cloud Object Storage or NAS)
            model_description (str): Experiment description
            tag_list (list): tags
        Returns:
            model_id
        """
        response = self.easymaker_api_sender.create_model(model_name=model_name,
                                                          framework_code=framework_code,
                                                          model_uri=model_uri,
                                                          model_description=model_description,
                                                          tag_list=tag_list)

        self.model_id = response['model']['modelId']
        print(f'[AI EasyMaker] Model create complete. Model Id : {self.model_id}')
        return self.model_id
