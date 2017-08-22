# Copyright 2007-2017 UShareSoft SAS, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from unittest import TestCase

from hammr.utils.generate_utils import *

class TestGenerateK5(TestCase):
    def test_generate_k5vmdk_should_return_uncompressed_image_given_compressed_image(self):
        # given
        image_given = CompressedImage()
        intall_profile_given = MockObject()

        # when
        image, install_profile = generate_k5vmdk(image_given, WhateverObject(), intall_profile_given, WhateverObject(), WhateverObject())

        # then
        self.assertFalse(image.compress)
        self.assertEquals(intall_profile_given, install_profile)


    def test_generate_k5vmdk_should_return_uncompressed_image_given_uncompressed_image(self):
        # given
        image_given = UncompressedImage()
        intall_profile_given = MockObject()

        # when
        image, install_profile = generate_k5vmdk(image_given, WhateverObject(), intall_profile_given,
                                                 WhateverObject(), WhateverObject())

        # then
        self.assertFalse(image.compress)
        self.assertEquals(intall_profile_given, install_profile)


class TestGeneratePXE(TestCase):
    def test_generate_pxe_should_return_uncompressed_image_given_compressed_image(self):
        # given
        image_given = CompressedImage()
        intall_profile_given = MockObject()

        # when
        image, install_profile = generate_pxe(image_given, WhateverObject(), intall_profile_given, None, None)

        # then
        self.assertFalse(image.compress)
        self.assertEquals(intall_profile_given, install_profile)


    def test_generate_pxe_should_return_uncompressed_image_given_uncompressed_image(self):
        # given
        image_given = UncompressedImage()
        intall_profile_given = MockObject()

        # when
        image, install_profile = generate_pxe(image_given, WhateverObject(), intall_profile_given,
                                                 None, None)

        # then
        self.assertFalse(image.compress)
        self.assertEquals(intall_profile_given, install_profile)

class CompressedImage:
    compress = True

class UncompressedImage:
    compress = False

class MockObject:
    first_attribute = "something"
    second_attribute = "something else"

class WhateverObject:
    whatever = "whatever"