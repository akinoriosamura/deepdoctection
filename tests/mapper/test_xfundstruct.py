# -*- coding: utf-8 -*-
# File: test_xfundstruct.py

# Copyright 2021 Dr. Janis Meyer. All rights reserved.
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

"""
Testing module mapper.xfundstruct
"""

from typing import Dict
from unittest.mock import MagicMock, patch

from pytest import mark

from deepdoctection.mapper.xfundstruct import xfund_to_image
from deepdoctection.utils.detection_types import JsonDict
from deepdoctection.utils.settings import CellType, TokenClasses, WordType

from .conftest import get_always_pubtabnet_white_image


@mark.basic
@patch(
    "deepdoctection.mapper.xfundstruct.load_image_from_file", MagicMock(side_effect=get_always_pubtabnet_white_image)
)
def test_xfund_to_image(
    datapoint_xfund: JsonDict, xfund_category_names: Dict[str, str], ner_token_to_id_mapping: JsonDict
) -> None:
    """
    testing xfund_to_image is mapping correctly
    """

    # Act
    xfund_to_image_func = xfund_to_image(False, False, xfund_category_names, ner_token_to_id_mapping)
    img = xfund_to_image_func(datapoint_xfund)

    # Assert
    assert img
    image_anns = img.get_annotation()
    words = [ann.get_sub_category(WordType.characters).value for ann in image_anns]  # type: ignore
    assert words == ["Akademisches", "Auslandsamt", "Bewerbungsformular"]

    sub_cats_category_names = [ann.get_sub_category(WordType.token_class).category_name for ann in image_anns]
    assert sub_cats_category_names == [TokenClasses.other, TokenClasses.other, CellType.header]

    sub_cats_ner_tags = [ann.get_sub_category(WordType.tag).category_name for ann in image_anns]
    assert sub_cats_ner_tags == ["O", "O", "B"]
