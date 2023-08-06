import contextlib
import dataclasses
import logging
import pathlib
import tempfile
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
import torch.nn
import transformers
import irisml.core
from irisml.tasks.make_image_text_contrastive_model import ImageTextContrastiveModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a model using transformers library.

    Currently only CLIPModel is supported.
    """
    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Config:
        name: str
        pretrained: bool = False
        azure_blob_container_url: Optional[str] = None
        azure_blob_path_prefix: Optional[str] = None

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        return self.Outputs(self._create_model(self.config.name, self.config.pretrained, self.config.azure_blob_container_url, self.config.azure_blob_path_prefix))

    def dry_run(self, inputs):
        return self.Outputs(self._create_model(self.config.name, False, None, None))

    @staticmethod
    def _create_model(name, pretrained, azure_blob_container_url, azure_blob_path_prefix):
        if not name:
            raise ValueError("name is required")

        if pretrained and azure_blob_container_url:
            raise ValueError("pretrained and azure_blob_container_url are mutually exclusive")

        if not azure_blob_container_url and azure_blob_path_prefix:
            raise ValueError("azure_blob_path_prefix requires azure_blob_container_url")

        if azure_blob_container_url:
            prefix = name if not azure_blob_path_prefix else f'{azure_blob_path_prefix}/{name}'
            with with_azure_directory(azure_blob_container_url, prefix) as temp_dir:
                transformers_model = transformers.AutoModel.from_pretrained(temp_dir)
        elif pretrained:
            transformers_model = transformers.AutoModel.from_pretrained(name)
        else:
            transformers_config = transformers.AutoConfig.from_pretrained(name)
            transformers_model = transformers.AutoModel.from_config(transformers_config)

        if isinstance(transformers_model, transformers.CLIPModel):
            model = ImageTextContrastiveModel(PoolerOutputExtractor(transformers_model.vision_model), PoolerOutputExtractor(transformers_model.text_model),
                                              transformers_model.visual_projection, transformers_model.text_projection,
                                              'clip', float(transformers_model.logit_scale))
        else:
            raise RuntimeError(f"The model type {type(transformers_model)} is not supported. Please submit a pull request.")

        return model


@contextlib.contextmanager
def with_azure_directory(blob_container_url, blob_prefix):
    container_client = ContainerClient.from_container_url(blob_container_url, credential=DefaultAzureCredential())
    blob_names = list(container_client.list_blob_names(name_starts_with=blob_prefix))
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        for blob_name in blob_names:
            filepath = temp_dir / blob_name[len(blob_prefix) + 1:]
            blob_client = container_client.get_blob_client(blob_name)
            logger.info(f"Downloading {blob_name} to {filepath}")
            filepath.write_bytes(blob_client.download_blob().readall())

        yield temp_dir


class PoolerOutputExtractor(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self._model = model

    def forward(self, inputs):
        result = self._model(inputs)
        return result.pooler_output

    def state_dict(self):
        return self._model.state_dict()

    def load_state_dict(self, *args, **kwargs):
        return self._model.load_state_dict(*args, **kwargs)
