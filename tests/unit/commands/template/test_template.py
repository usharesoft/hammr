# -*- coding: utf-8 -*-
# Copyright 2007-2016 UShareSoft SAS, All rights reserved
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

from uforge.objects.uforge import *
from hammr.commands.template import template
from mock import MagicMock


class TestTemplate(TestCase):
    def test_do_clone_should_split_parameters_even_with_spaces(self):
        # given
        t = template.Template()
        name = "my new name wit spaces"
        args = "--id 42 --name '%s' --version 1.0" % name
        t.clone_appliance = MagicMock(return_value=appliance())

        # when
        t.do_clone(args)

        # then
        self.assertEqual(t.clone_appliance.call_count, 1)
        self.assertEqual(t.clone_appliance.call_args[0][1].name, name)