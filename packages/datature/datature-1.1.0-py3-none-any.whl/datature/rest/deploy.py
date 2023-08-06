#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   Deploy.py
@Author  :   Raighne.Weng
@Version :   1.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Deploy API
'''

from datature.http.resource import RESTResource
from datature.rest.types import DeploymentMetadata


class Deploy(RESTResource):
    """Datature Deploy API Resource."""

    @classmethod
    def list(cls) -> dict:
        """Lists all deployments in a project.

        :return: A list of dictionaries containing deployment metadata with the following structure:

                .. code-block:: json
                        [
                            {
                                "id": "deploy_30922d5e-b2f6-43dc-b7b4-e29e2c30fb45",
                                "object": "deploy",
                                "project_id": "proj_cd067221d5a6e4007ccbb4afb5966535",
                                "model_id": "model_5cbcf0fb9f692621f9cfc1ea8f1d68c7",
                                "scaling": {
                                    "mode": "fixed",
                                    "num_instances": 1
                                },
                                "status": {
                                    "overview": "AVAILABLE",
                                    "message": "Created service successfully",
                                    "status_date": 1673936127872
                                },
                                "create_date": 1673935589700,
                                "last_modified_date": 1673936127872,
                                "locked": false,
                                "url": "http://34.149.13.97/neural/3092245/predict"
                            }
                        ]

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Deploy.list()
        """
        return cls.request("GET", "/deploy/list")

    @classmethod
    def retrieve(cls, deploy_id: str) -> dict:
        """Retrieves a specific deployment using the deployment ID.

        :param deploy_id: The ID of the deployment as a string.
        :return: A dictionary containing the specific deployment metadata with the following structure:

                .. code-block:: json
                            {
                                "id": "deploy_30922d5e-b2f6-43dc-b7b4-e29e2c30fb45",
                                "object": "deploy",
                                "project_id": "proj_cd067221d5a6e4007ccbb4afb5966535",
                                "model_id": "model_5cbcf0fb9f692621f9cfc1ea8f1d68c7",
                                "scaling": {
                                    "mode": "fixed",
                                    "num_instances": 1
                                },
                                "status": {
                                    "overview": "AVAILABLE",
                                    "message": "Created service successfully",
                                    "status_date": 1673936127872
                                },
                                "create_date": 1673935589700,
                                "last_modified_date": 1673936127872,
                                "locked": false,
                                "url": "http://34.149.13.97/neural/3092245/predict"
                            }

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Deploy.retrieve("deploy_30922d5e-b2f6-43dc-b7b4-e29e2c30fb45")
        """
        return cls.request("GET", f"/deploy/{deploy_id}")

    @classmethod
    def delete(cls, deploy_id: str) -> dict:
        """Deletes a specific deployment from the project.

        :param deploy_id: The id of the deployment.
        :return: A dictionary containing the deleted deployment ID and the deletion status with the following structure:

                .. code-block:: json
                            {
                                "id": "deploy_30922d5e-b2f6-43dc-b7b4-e29e2c30fb45",
                                "deleted": true
                            }

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Deploy.delete("deploy_30922d5e-b2f6-43dc-b7b4-e29e2c30fb45")
        """
        return cls.request("DELETE", f"/deploy/{deploy_id}")

    @classmethod
    def create(cls, deployment: DeploymentMetadata) -> dict:
        """Creates a deployment for a specific model using the model ID.

        :param deployment: The configuration metadata of the deployment.
        :return: A dictionary containing the created deployment metadata with the following structure:

                .. code-block:: json
                        {
                            "id": "op_508fc5d1-e908-486d-9e7b-1dca99b80024",
                            "object": "operation",
                            "op_link": "users/api|affaf/proje-1dca99b80024",
                            "status": {
                                "overview": "Queued",
                                "message": "Operation queued",
                                "time_updated": 1676621361765,
                                "time_scheduled": 1676621361765,
                                "progress": {
                                    "unit": "whole operation",
                                    "with_status": {
                                        "queued": 1,
                                        "running": 0,
                                        "finished": 0,
                                        "cancelled": 0,
                                        "errored": 0
                                    }
                                }
                            }
                        }

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"

                        datature.deploy.create({
                            "name": "My First API",
                            "model_id": "model_5cbcf0fb9f692621f9cfc1ea8f1d68c7",
                            "num_of_instances": 1,
                        })
        """
        return cls.request("POST",
                           "/deploy",
                           request_body={
                               "name": deployment.get("name"),
                               "modelId": deployment.get("model_id"),
                               "numInstances":
                               deployment.get("num_of_instances"),
                           })
