# Copyright (c) 2007-2018 UShareSoft, All rights reserved
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

# When anonymous type are used inside uforge.xsd, anonymous type such as "CTD_ANON_238" will be created inside uforge.py.
# We can't use directly these types in unit test for mocking otherwise unit tests may failed each time the uforge.xsd
# is slightly modified.
# So to avoid that, the type to used is retrieved dynamically using the PyXB internal attributes.
# This method returns the type of the element in a list attributes
# Example of use:
#   regionType = get_pyXB_anon_type_for_list(regions.regionEntities)
#   region = regionType()
#   regions.regionEntities.append(region)
def get_pyXB_anon_type_for_list_attrb(list_attrb):
    return list_attrb._PluralBinding__elementBinding._element__typeDefinition

# When anonymous type are used inside uforge.xsd, anonymous type such as "CTD_ANON_238" will be created inside uforge.py.
# We can't use directly these types in unit test for mocking otherwise unit tests may failed each time the uforge.xsd
# is slightly modified.
# So to avoid that, the type to used is retrieved dynamically using the PyXB internal attributes.
# This method returns the type of the attribute "attrb_name" in the "attrb_holder" object
# Example of use:
#   flavorType = get_pyXB_anon_type_for_list(flavors.flavor)
#   flavor = flavorType()
#   flavors.flavor.append(flavor)
def get_pyXB_anon_type_for_simple_attrb(attrb_holder, attrb_name):
    return getattr(attrb_holder, "_" + type(
        attrb_holder).__name__ + "__" + attrb_name)._ElementDeclaration__elementBinding._element__typeDefinition