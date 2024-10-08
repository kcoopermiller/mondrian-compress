# Copyright 2024 The Scenic Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Base config for CLIP w/ linear + BERT."""

import ml_collections
from scenic.projects.lang4video.configs import base_clip
from scenic.projects.lang4video.configs import base_clip_bert


def get_config(run_local: str = '') -> ml_collections.ConfigDict:
  """Returns the experiment configuration."""
  config = base_clip_bert.get_config(run_local)

  config.experiment_name = 'clip_linear_bert'

  del config.model.image_encoder.config_name

  config.model.image_encoder_name = 'sequential'
  config.model.image_encoder.encoders = ml_collections.ConfigDict()
  config.model.image_encoder.encoders.a = ml_collections.ConfigDict()
  config.model.image_encoder.encoders.a.encoder_name = 'clip'
  config.model.image_encoder.encoders.a.encoder = ml_collections.ConfigDict()
  config.model.image_encoder.encoders.a.encoder.config_name = 'vit_b32'
  config.model.image_encoder.encoders.a.encoder.normalize = False
  config.model.image_encoder.encoders.b = ml_collections.ConfigDict()
  config.model.image_encoder.encoders.b.encoder_name = 'mlp'
  config.model.image_encoder.encoders.b.encoder = ml_collections.ConfigDict()
  config.model.image_encoder.encoders.b.encoder.num_layers = 0
  config.model.image_encoder.encoders.b.encoder.embedding_size = 768
  config.model.image_encoder.encoders.b.encoder.skip_connection = False

  # The following configurations are meant to be used by DMVR datasets but also
  # as input to other parts of the config.

  config.dataset_configs.min_resize = base_clip.get_clip_image_size(
      config.model.image_encoder.encoders.a.encoder.config_name)
  config.dataset_configs.crop_size = base_clip.get_clip_image_size(
      config.model.image_encoder.encoders.a.encoder.config_name)

  return config
