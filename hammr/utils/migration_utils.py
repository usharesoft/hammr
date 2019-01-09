# Copyright (c) 2007-2019 UShareSoft, All rights reserved
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

from texttable import Texttable
from ussclicore.utils import generics_utils

from hammr.utils import hammr_utils, generate_utils, account_utils
from hammr.utils import publish_builders

from uforge.objects import uforge

def migration_table(migrations):
    table = Texttable(800)
    table.set_cols_dtype(["t", "t", "t"])
    table.set_cols_align(["c", "l", "c"])
    table.header(["Id", "Name", "Status"])

    for migration in migrations:
        status = migration.status.message + " (" + str(migration.status.percentage) + "%)"
        if migration.status.complete or migration.status.error or migration.status.cancelled:
            status = migration.status.message
        table.add_row([migration.dbId, migration.name, status])

    return table


def retrieve_migration_configuration(args_file):
    file = generics_utils.get_file(args_file)
    if file is None:
        raise Exception("No such file or directory: " + args_file)
    data = hammr_utils.load_data(file)

    if "migration" in data:
        migration_config = data["migration"]
        check_mandatory_migrate(migration_config)
        return migration_config
    else:
        raise Exception("no migration section found")


def check_mandatory_migrate(migration):
    if not "name" in migration:
        raise Exception("check yours parameters in file, no attribute [name] for [migration]")
    if not "os" in migration:
        raise Exception("check yours parameters in file, no attribute [os] for [migration]")
    elif migration["os"] != "linux":
        raise Exception("check yours parameters in file, attribute [os] for [migration] is not correct. Only 'linux' is supported")
    if "source" in migration:
        check_mandatory_source(migration["source"])
    else:
        raise Exception("check yours parameters in file, no attribute [source] for [migration]")
    if "target" in migration:
        check_mandatory_target(migration["target"])
    else:
        raise Exception("check yours parameters in file, no attribute [target] for [migration]")


def check_mandatory_source(source):
    if not "host" in source:
        raise Exception("check yours parameters in file, no attribute [host] for [migration][source]")
    if not "user" in source:
        raise Exception("check yours parameters in file, no attribute [user] for [migration][source]")


def check_mandatory_target(target):
    if "builder" in target:
        check_mandatory_builder(target["builder"])
    else:
        raise Exception("check yours parameters in file, no attribute [builder] for [migration][target]")


def check_mandatory_builder(builder):
    if not "type" in builder:
        raise Exception("check yours parameters in file, no attribute [type] for [migration][target][builder]")
    if "account" in builder:
        check_mandatory_account(builder["account"])
    else:
        raise Exception("check yours parameters in file, no attribute [account] for [migration][target][builder]")


def check_mandatory_account(account):
    if not "name" in account:
        raise Exception("check yours parameters in file, no attribute [name] for [migration][target][builder][account]")


def retrieve_target_format(api, login, target_format_name):
    target_format = generate_utils.get_target_format_object(api, login, target_format_name)
    if target_format is None:
        raise Exception("TargetFormat type unknown: " + target_format_name)
    return target_format

def retrieve_image(builder, target_format, api, login):
    image_format_name = target_format.format.name
    check_mandatory_installation(image_format_name, builder)
    create_image_method = getattr(generate_utils, "generate_" + generics_utils.remove_special_chars(image_format_name), None)
    if create_image_method:
        install_profile = uforge.installProfile()
        install_profile.diskSize = 0
        image, install_profile = create_image_method(uforge.Image(), builder, install_profile, api, login)
        install_profile = set_install_profile_disk_size(install_profile, builder, image_format_name)
        image.installProfile = install_profile
        return image

    raise Exception("TargetFormat type is unsupported: " + target_format.format.name)

def check_mandatory_installation(image_format_name, builder):
    if image_format_name == "aws" or image_format_name == "outscale":
        if not "installation" in builder:
            raise Exception("check yours parameters in file, no attribute [installation] for [migration][target][builder], mandatory to migrate to [" + builder["type"] +"]")

def set_install_profile_disk_size(install_profile, builder, image_format_name):
    if image_format_name == "aws" or image_format_name == "outscale" or image_format_name == "gce":
        if "installation" in builder:
            if "diskSize" in builder["installation"]:
                install_profile.diskSize = builder["installation"]["diskSize"]
            else:
                raise Exception("check yours parameters in file, no attribute [disksize] for [migration][target][builder][installation], mandatory to migrate to [" + builder["type"] +"]")
    return install_profile

def build_publish_image(builder, target_format, cred_account):
    create_publish_image_method = getattr(publish_builders, "publish_" + generics_utils.remove_special_chars(target_format.format.name), None)
    if create_publish_image_method:
        publish_image = create_publish_image_method(builder, cred_account)
        publish_image.credAccount = cred_account
        return publish_image

    raise Exception("TargetFormat type is unsupported: " + target_format.format.name)

def retrieve_account(api, login, account_name):
    cred_accounts = api.Users(login).Accounts.Getall()
    if not cred_accounts:
        raise Exception("No CredAccounts available.\n You can use the command 'hammr account create' to create an account.")

    cred_accounts = cred_accounts.credAccounts.credAccount
    if cred_accounts is None or len(cred_accounts) == 0:
        raise Exception("No CredAccounts available.\n You can use the command 'hammr account create' to create an account.")

    account_retrieved = None
    for cred_account in cred_accounts:
        if cred_account.name == account_name:
            account_retrieved = cred_account
            break
    if not account_retrieved:
        raise Exception("CredAccount unknown: " + account_name + "\n You can use the command 'hammr account create' to create an account.")

    create_account_method = getattr(account_utils, generics_utils.remove_special_chars(cred_account.targetPlatform.type), None)
    cred_account = create_account_method()
    cred_account.name = account_name
    cred_account.uri = account_retrieved.uri
    return cred_account
