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
import getpass
import shlex
import shutil

import pyxb
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import printer

from hammr.utils import constants
from hammr.utils import hammr_utils
from hammr.utils import migration_utils
from ussclicore.utils import generics_utils

from uforge.objects import uforge

class Migration(Cmd, CoreGlobal):
    """List existing migrations, launch the migration of a live system, delete a complete migration."""

    cmd_name = "migration"

    def __init__(self):
        super(Migration, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                  description="Displays all the migrations for the user")
        return doParser

    def do_list(self, args):
        try:
            # call UForge API
            printer.out("Getting migrations for [" + self.login + "] ...")
            migrations = self.api.Users(self.login).Migrations.Getall()
            migrations = migrations.migrations.migration

            if len(migrations) == 0:
                printer.out("No migrations available")
                return
            print migration_utils.migration_table(migrations).draw() + "\n"

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return hammr_utils.handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_launch(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " launch", add_help=True,
                                  description="Launches a migration")
        mandatory = do_parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True,
                               help="yaml/json file providing the migration configuration")
        return do_parser

    def do_launch(self, args):
        try:
            # add arguments
            do_parser = self.arg_launch()
            do_args = do_parser.parse_args(shlex.split(args))

            # if the help command is called, parse_args returns None object
            if not do_args:
                return 2

            try:
                uforge_password = self.password
            except AttributeError:
                printer.out("Using API keys with command 'hammr migration launch' is not yet supported. Please use password.", printer.ERROR)
                return 2

            migration_config = migration_utils.retrieve_migration_configuration(do_args.file)
            target_format = migration_utils.retrieve_target_format(self.api, self.login, migration_config["target"]["builder"]["type"])
            image = migration_utils.retrieve_image(migration_config["target"]["builder"], target_format, self.api, self.login)
            if image is None:
                return 2
            cred_account = migration_utils.retrieve_account(self.api, self.login, migration_config["target"]["builder"]["account"]["name"])
            publish_image = migration_utils.build_publish_image(migration_config["target"]["builder"], target_format, cred_account)
            if publish_image is None:
                return 2

            migration = self.create_migration(migration_config["name"], migration_config["os"], target_format.name, image, publish_image)
            self.api.Users(self.login).Migrations.Create(body=migration, element_name="ns1:migration")

            local_uforge_migration_path = hammr_utils.download_binary_in_local_temp_dir(self.api, constants.TMP_WORKING_DIR, constants.URI_MIGRATION_BINARY, constants.MIGRATION_BINARY_NAME)

            self.upload_and_launch_migration_binary(self.login, uforge_password, migration_config, local_uforge_migration_path, self.api.getUrl())

            # delete temp dir
            shutil.rmtree(constants.TMP_WORKING_DIR)

            printer.out("Migration launched successfully, please go to the platform to follow steps of the migration.", printer.OK)

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_launch()
        except Exception as e:
            if hammr_utils.is_uforge_exception(e):
                return hammr_utils.handle_uforge_exception(e)
            printer.out(str(e), printer.ERROR)

        return 0

    def help_launch(self):
        do_parser = self.arg_launch()
        do_parser.print_help()

    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name + " delete", add_help=True,
                                  description="Deletes a complete migration")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True,
                               help="the ID of the migration to delete")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--no-confirm', dest='no_confirm', action='store_true', required=False,
                              help="do not ask before deleting the migration")

        return doParser

    def do_delete(self, args):
        try:
            doParser = self.arg_delete()
            doArgs = doParser.parse_args(shlex.split(args))

            if not doArgs:
                return 2

            # call UForge API
            printer.out("Retrieving migration with id [" + doArgs.id + "]...")

            migration = self.api.Users(self.login).Migrations(doArgs.id).Get()

            if migration is None:
                printer.out("No migration available with id " + doArgs.id)
                return 2

            print migration_utils.migration_table([migration]).draw() + "\n"

            if doArgs.no_confirm or generics_utils.query_yes_no(
                                    "Do you really want to delete migration with id " + doArgs.id + "?"):
                printer.out("Please wait...")
                self.api.Users(self.login).Migrations(doArgs.id).Delete()
                printer.out("Migration deleted", printer.OK)

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return hammr_utils.handle_uforge_exception(e)

    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()

    def upload_and_launch_migration_binary(self, uforge_login, uforge_password, migration_config, file_src_path,
                                           uforge_url):
        hostname = migration_config["source"]["host"]
        username = migration_config["source"]["user"]

        if not "password" in migration_config["source"]:
            password = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        else:
            password = migration_config["source"]["password"]

        if not "ssh-port" in migration_config["source"]:
            port = 22
        else:
            port = migration_config["source"]["ssh-port"]

        overlay = "-o "
        if "overlay" in migration_config["source"] and not migration_config["source"]["overlay"]:
            overlay = ""

        exclude = ""
        if "exclude" in migration_config["source"]:
            for ex in migration_config["source"]["exclude"]:
                exclude += "-e '" + ex + "' "

        dir = "/tmp"

        binary_path = dir + "/" + constants.MIGRATION_BINARY_NAME
        client = hammr_utils.upload_binary_to_client(hostname, port, username, password, file_src_path, binary_path, None)

        command_launch = 'chmod +x ' + dir + '/' + constants.MIGRATION_BINARY_NAME + '; nohup ' + dir + '/' + constants.MIGRATION_BINARY_NAME + ' -u ' + uforge_login + ' -p ' + uforge_password + ' -U ' + uforge_url + ' -n \'' + \
                         migration_config["name"] + '\' ' + overlay + exclude + ' >/dev/null 2>&1 &'
        hammr_utils.launch_binary(client, command_launch)
        client.close()

        return 0

    def create_migration(self, migration_name, migration_family, target_format_name, image, publish_image):
        migration_created = uforge.Migration()
        migration_created.name = migration_name

        migration_created.stages = pyxb.BIND()
        migration_created.stages._ExpandedName = pyxb.namespace.ExpandedName(uforge.Namespace, 'Stages')

        scan_stage = uforge.ScanStage()
        scan_stage.family = migration_family
        scan_stage.family._ExpandedName = pyxb.namespace.ExpandedName(uforge.Namespace, 'family')
        migration_created.stages.append(scan_stage)

        target_format = uforge.TargetFormat()
        target_format.name = target_format_name

        generation_stage = uforge.GenerationStage()
        image.targetFormat = target_format
        generation_stage.image = image
        migration_created.stages.append(generation_stage)

        publication_stage = uforge.PublicationStage()
        publish_image.targetFormat = target_format
        publication_stage.publishImage = publish_image
        migration_created.stages.append(publication_stage)

        return migration_created

