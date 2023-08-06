import copy
import csv
import json
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Optional

from dateutil.parser import ParserError, parse

# Database manager.
from dls_normsql.databases import Databases

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.require import require

# Base class for generic things.
from dls_utilpack.thing import Thing

# Database constants.
from soakdb3_api.databases.constants import PinBarcodeErrors, Tablenames
from soakdb3_api.databases.database_definition import DatabaseDefinition

# Version for health response.
from soakdb3_lib.version import version as soakdb3_lib_version

logger = logging.getLogger(__name__)

thing_type = "soakdb3_lib.datafaces.aiosqlite"


class Normsql(Thing):
    """
    Implementation of dataface on top of underlying database API provider presumed to be sqlite.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification=None):
        Thing.__init__(self, thing_type, specification)

        # Barcodes filename is not type specific.
        self.__puck_barcodes_filename = require(
            f"{callsign(self)} specification",
            self.specification(),
            "puck_barcodes_filename",
        )

        self.__type_specific = require(
            f"{callsign(self)} specification",
            self.specification(),
            "type_specific_tbd",
        )

        self.__dbspec = require(
            f"{callsign(self)} specification",
            self.__type_specific,
            "database",
        )

        self.__visitid_mappings = require(
            f"{callsign(self)} specification",
            self.__type_specific,
            "visitid_mappings",
        )

        self.__database_definition_object = DatabaseDefinition()

        # Cache of database objects we have created.
        self.__cache = {}
        self.__cache_cvs_directories = {}

    # ----------------------------------------------------------------------------------------
    async def start(self):
        # There is no visitid known at start of the server.
        # They are built up as requested by clients.

        pass

    # ----------------------------------------------------------------------------------------
    async def disconnect(self):
        visitids = list(self.__cache.keys())
        for visitid in visitids:
            database = self.__cache.pop(visitid)
            await database.disconnect()
            database = None

    # ----------------------------------------------------------------------------------------
    async def establish_database_connection(self, visitid):

        database = self.__cache.get(visitid)
        if database is None:

            # Get path from visitid.
            visitid_path = self.__visitid2path(visitid)

            logger.debug(f"visitid {visitid} is for path {visitid_path}")

            if not os.path.isdir(visitid_path):
                raise RuntimeError(f"{visitid_path} is not a directory")

            # Get copy of specification template.
            dbspec = copy.deepcopy(self.__dbspec)

            dbspec["filename"] = f"{visitid_path}/database/soakDBDataFile.sqlite"
            dbspec["backup_directory"] = f"{visitid_path}/database/DataFileBackups"

            self.__cache_cvs_directories[visitid] = f"{visitid_path}/lab36"

            database = Databases().build_object(
                dbspec, self.__database_definition_object
            )
            await database.connect()

            # Cache database connections by visitid.
            self.__cache[visitid] = database

        return database

    # ----------------------------------------------------------------------------------------
    def __visitid2path(self, visitid: str) -> str:
        """
        Give back a file path given the visitid.

        Args:
            visitid (str): visitid
                At the current time, excel gives the visitid as windows-type path with leading drive letter.

        Returns:
            str: Linux filesystem path root of the database, backup and csv files.

        """

        # Go through all the mappings defined in the specification.
        for visitid_mapping in self.__visitid_mappings:
            # This mapping calls for regex replacement?
            if visitid_mapping["action"] == "regex_replace":
                pattern = visitid_mapping["pattern"]
                replace = visitid_mapping["replace"]

                # The visitid matches this mapping?
                match = re.search(pattern, visitid)
                if match is not None:
                    # Replace with the substitution.
                    path = re.sub(pattern, replace, visitid)
                    return path

        return visitid

    # # ----------------------------------------------------------------------------------------
    # async def reinstance(self):
    #     """"""

    #     # TODO: Consider if reinstance is a necessary method.
    #     if self.__database is None:
    #         return

    #     self.__database = self.__database.reinstance()

    # ----------------------------------------------------------------------------------------
    async def backup(self, visitid):
        """"""
        database = await self.establish_database_connection(visitid)

        return await database.backup()

    # ----------------------------------------------------------------------------------------
    async def restore(self, visitid, nth):
        """"""
        database = await self.establish_database_connection(visitid)

        return await database.restore(nth)

    # ----------------------------------------------------------------------------------------
    async def query_for_dictionary(self, visitid, sql, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        records = await database.query(sql, subs=subs, why=why)

        return records

    # ----------------------------------------------------------------------------------------
    async def query(self, visitid, sql, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        records = await database.query(sql, subs=subs, why=why)

        # Make a VBA collection with the first record giving the field names.
        collection = []
        for index, record in enumerate(records):
            if index == 0:
                collection.append(list(record.keys()))
            collection.append(list(record.values()))

        return collection

    # ----------------------------------------------------------------------------------------
    async def execute(self, visitid, sql, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        return await database.execute(sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def insert(self, visitid, table_name, records, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        if why is None:
            why = f"insert {len(records)} {table_name} records"

        await database.insert(table_name, records)

    # ----------------------------------------------------------------------------------------
    async def update(self, visitid, table_name, record, where, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        if why is None:
            why = f"update {table_name} record"

        await database.update(table_name, record, where, why=why)

    # ----------------------------------------------------------------------------------------
    async def update_body_fields(self, visitid, fields):
        """
        Handle update request from a soakdb range change.
        """
        database = await self.establish_database_connection(visitid)

        table_name = Tablenames.BODY

        maximum_id = None
        # Group the updates to rows by their id.
        rows = {}
        new_ids = {}
        for field in fields:
            id = str(field["id"])
            # This is a new row created from within the client?
            if id[0] == "-":
                # We haven't assigned this record to a real database id yet?
                if id not in new_ids:
                    # We don't know the maximum id in the database yet?
                    if maximum_id is None:
                        maximum_id = await self.query_for_dictionary(
                            visitid, f"SELECT MAX(ID) AS MAX_ID FROM {table_name}"
                        )
                        maximum_id = maximum_id[0]["MAX_ID"]
                    if maximum_id is None:
                        maximum_id = 0
                    maximum_id += 1
                    new_ids[id] = str(maximum_id)
                # Translate the negative id to a new id in the database.
                id = new_ids[id]

            row = rows.get(id)
            if row is None:
                row = []
                rows[id] = row

            # VBA doesn't put a Nothing value in the dictionary, so treat missing value as None.
            value = field.get("value")
            row.append({"field": field["field"], "value": value})

        # Get list of existing ids for those we want to update.
        id_csv = ", ".join(rows.keys())
        existing_rows = await self.query_for_dictionary(
            visitid, f"SELECT ID FROM {table_name} WHERE ID IN ({id_csv})"
        )
        existing_ids = []
        for existing_row in existing_rows:
            existing_ids.append(str(existing_row["ID"]))

        new_rows = []
        for updated_id in rows.keys():
            if updated_id not in existing_ids:
                new_rows.append({"ID": updated_id})

        logger.debug(
            f"inserting {len(new_rows)} new rows"
            f" and updating {len(rows.keys())} rows"
        )

        await database.begin()

        try:
            # Do the inserts at the start of the transaction.
            await database.insert(
                Tablenames.BODY,
                new_rows,
            )

            # Perform the updates on each row.
            for id, row in rows.items():
                sets = []
                subs = []
                for k in row:
                    field = k["field"]
                    value = k["value"]
                    sets.append(f"`{field}` = ?")
                    subs.append(value)
                subs.append(id)

                sets = ", ".join(sets)
                sql = f"UPDATE {table_name} SET {sets} WHERE ID = ?"

                # Add the update to the transaction.
                await database.execute(
                    sql,
                    subs=subs,
                )

            # Commit all the updates.
            logger.debug(
                f"committing {len(new_rows)} new rows"
                f" and updating {len(rows.keys())} rows"
            )
            await database.commit()

        except Exception:
            # Don't keep any partial operation.
            database.rollback()
            raise

    # ----------------------------------------------------------------------------------------
    async def update_head_fields(self, visitid, fields):
        """
        Handle update request from a soakdb range change.
        """

        table_name = Tablenames.HEAD

        # Perform the updates on the only row row.
        sets = []
        subs = []
        for k in fields:
            field = k["field"]
            value = k["value"]
            sets.append(f"`{field}` = ?")
            subs.append(value)

        sets = ", ".join(sets)
        sql = f"UPDATE {table_name} SET {sets}"

        await self.execute(visitid, sql, subs=subs, why="update head table")

    # ----------------------------------------------------------------------------------------
    def __check_mounted_vs_scanned(
        self,
        puck_scanned_at: str,
        crystal_mounted_at: str,
    ) -> Optional[str]:
        """
        Assign barcodes for pin positions to rows which don't have them yet.
        """

        if puck_scanned_at is None:
            return "no puck scan date"

        if crystal_mounted_at is None:
            return "no crystal MountedTimestamp"

        try:
            # If there is a hyphen in the date string, assume it is ISO, otherwise assume it's dd/mm/yyyy.
            dayfirst = "-" not in puck_scanned_at
            puck_scanned_datetime = parse(puck_scanned_at, dayfirst=dayfirst)
        except ParserError as exception:
            return f"invalid puck scan date: {str(exception)}"

        try:
            # If there is a hyphen in the date string, assume it is ISO, otherwise assume it's dd/mm/yyyy.
            dayfirst = "-" not in crystal_mounted_at
            crystal_mounted_datetime = parse(crystal_mounted_at, dayfirst=dayfirst)
        except ParserError as exception:
            return f"invalid crystal MountedTimestamp: {str(exception)}"

        #  From the VBA: if we are within 36 hours (1.5 days) of the mounted time, but we must have mounted before scanning.
        #  If scannedDate - mountedDate < 1.5 And scannedDate - mountedDate > 0 Then it's recent, add it.

        time_difference = (
            puck_scanned_datetime - crystal_mounted_datetime
        ).total_seconds()

        logger.debug(
            f"puck_scanned_datetime is {puck_scanned_datetime.isoformat()},"
            f" crystal_mounted_datetime is {crystal_mounted_datetime.isoformat()},"
            f" difference is {'%0.3f' % time_difference} seconds,"
            f" which is {'%0.3f' % (time_difference/3600)} hours"
        )

        if time_difference < 0:
            return "puck scan date is before crystal MountedTimestamp"

        elif time_difference > 36 * 3600:
            return f"puck scan date is {'%0.3f' % (time_difference/3600)} hours after crystal MountedTimestamp (36 hours is the max)"

        else:
            return None

    # ----------------------------------------------------------------------------------------
    async def assign_pin_barcodes(self, visitid):
        """
        Assign barcodes for pin positions to rows which don't have them yet.
        """

        # Get all the rows which have pin positions but no barcodes yet.
        crystal_rows = await self.query_for_dictionary(
            visitid,
            (
                "SELECT ID, Puck, PuckPosition, MountedTimestamp"
                f" FROM {Tablenames.BODY} WHERE (COALESCE(PuckPosition, '') != '') AND (COALESCE(PinBarcode, '') = '')"
            ),
        )

        # Nothing to do?
        if len(crystal_rows) == 0:
            return

        # Load the file consisting of the recent barcode scans.
        # This has to be reloaded every time because its contents changes asynchronously.
        # For example \\dc.diamond.ac.uk\dls\science\groups\i04-1\software\barcode-store\store\store.csv.
        pucks = {}
        with open(self.__puck_barcodes_filename, "r") as stream:
            reader = csv.reader(stream)
            for puck_row in reader:
                puck = {}
                puck["scanned_at"] = puck_row[1]
                puck["pin_barcodes"] = puck_row[3:]

                # Make a dictionary keyed by puck barcode.
                pucks[puck_row[2]] = puck

        fields = []
        # Traverse the crystal rows that need pin barcodes.
        for crystal_row in crystal_rows:
            anomaly = {
                "visitid": visitid,
                "puck_barcodes_filename": self.__puck_barcodes_filename,
                "crystal_row": {
                    "ID": crystal_row["ID"],
                    "Puck": crystal_row["Puck"],
                    "PuckPosition": crystal_row["PuckPosition"],
                    "MountedTimestamp": crystal_row["MountedTimestamp"],
                },
            }

            # Get puck row as keyed by the puck barcode.
            puck = pucks.get(crystal_row["Puck"])

            # No puck barcode assigned to this crystal?
            # Shouldn't really happen!
            if puck is None:
                pin_barcode = PinBarcodeErrors.NO_PUCK
                logger.warning(
                    f"[ANOMALY] crystal row has a puck barcode not found in store.csv\n{json.dumps(anomaly, indent=4)}"
                )
            else:
                puck_scanned_at = puck["scanned_at"]
                crystal_mounted_at = crystal_row["MountedTimestamp"]

                reason_why_not = self.__check_mounted_vs_scanned(
                    puck_scanned_at,
                    crystal_mounted_at,
                )

                if reason_why_not is not None:
                    pin_barcode = PinBarcodeErrors.BAD_DATE
                    anomaly["puck_scanned_at"] = puck_scanned_at
                    logger.warning(
                        f"[ANOMALY] {reason_why_not}\n{json.dumps(anomaly, indent=4)}"
                    )

                else:
                    # Pin position is not an integer?
                    # Shouldn't really happen!
                    try:
                        pin_position = int(crystal_row["PuckPosition"])

                        # Pin position exceeds number of pins scanned for the puck?
                        # Shouldn't really happen!
                        if pin_position < 1 or pin_position > len(puck["pin_barcodes"]):
                            pin_barcode = PinBarcodeErrors.BAD_PIN
                            anomaly["pin_barcodes_count"] = len(puck["pin_barcodes"])
                            logger.warning(
                                f"[ANOMALY] crystal row has a PuckPosition less than 0 or more than the tokens on the puck row in store.csv\n{json.dumps(anomaly, indent=4)}"
                            )
                        else:
                            pin_barcode = puck["pin_barcodes"][pin_position - 1]

                    except ValueError:
                        pin_barcode = PinBarcodeErrors.BAD_INT
                        logger.warning(
                            f"[ANOMALY] crystal row has a PuckPosition that is not an integer\n{json.dumps(anomaly, indent=4)}"
                        )

            # Make an update field.
            # TODO: Consider a transaction encapsulating the query needing barcodes and their assignment.
            field = {
                "id": crystal_row["ID"],
                "field": "PinBarcode",
                "value": pin_barcode,
            }
            fields.append(field)

        # Anything to do?
        if len(fields) > 0:
            # Update the pin barcodes in the database.
            await self.update_body_fields(visitid, fields)

    # ----------------------------------------------------------------------------------------
    async def write_csv(self, visitid, rows, filename):
        """
        Handle request to write rows as csv file.

        The rows are assumed fully prepared ahead of time.

        The filename's path should be a subdirectory (no leading slash).
        """

        # We don't really need the database itself, since all the data rows are provided as arguments.
        # However, this sets up the csv_directory for this visit.
        await self.establish_database_connection(visitid)

        # Get the csv directory from the specification.
        csv_directory = self.__cache_cvs_directories.get(visitid)
        if csv_directory is None:
            raise RuntimeError(
                f"no database connection has yet been made for visitid {visitid}"
            )

        filename = f"{csv_directory}/{filename}"
        await self.__create_directory(filename)

        with open(filename, "w") as stream:

            # Create the csv writer.
            writer = csv.writer(stream)

            # Write all rows to the csv file.
            writer.writerows(rows)

    # ----------------------------------------------------------------------------------------
    async def move_to_done(
        self,
        visitid: str,
        csv_file: str,
        transfer_type: str,
    ) -> None:
        """
        Handle request to move a csv file to the done subdirectory.

        Args:
            visitid (str): full path to visit, including /processing
            csv_file (str): name of csv file with (no directory part included)
            transfer_type (str): either "soak", "cryo" or "shifter"
        """

        # Get the csv directory from the specification.
        # This is an absolute filename ending in /lab36.
        csv_directory = self.__cache_cvs_directories.get(visitid)

        if csv_directory is None:
            raise RuntimeError(
                f"no database connection has yet been made for visitid {visitid}"
            )

        if transfer_type in ["soak", "cryo"]:
            tranfer_subdirectory = "echo"
        else:
            tranfer_subdirectory = transfer_type

        # We expect the source path to exist in the given transfer type.
        source_path = Path(csv_directory) / tranfer_subdirectory / csv_file

        if source_path.is_file():
            # Target file has the same name as the source, but in the done subdirectory.
            target_path = Path(csv_directory) / tranfer_subdirectory / "done" / csv_file
            await self.__create_directory(target_path)
            shutil.move(source_path, target_path)
        else:
            logger.warning(
                f"[UNEXPECTED] cannot move to done because file doesn't exist: {source_path}"
            )

    # ----------------------------------------------------------------------------------------
    async def __create_directory(self, filename):

        directory, filename = os.path.split(filename)

        if not os.path.exists(directory):
            # Make sure that parent directories which get created will have public permission.
            umask = os.umask(0)
            os.umask(umask & ~0o0777)
            os.makedirs(directory)
            os.umask(umask)

    # ----------------------------------------------------------------------------------------
    async def report_health(self):
        """"""

        report = {}

        report["alive"] = True
        report["version"] = soakdb3_lib_version()

        return report

    # ----------------------------------------------------------------------------------------
    async def open_client_session(self):
        """"""
        # Connect to the database to create the schemas if they don't exist already.
        await self.establish_database_connection()

    # ----------------------------------------------------------------------------------------
    async def close_client_session(self):
        """"""
        await self.disconnect()
