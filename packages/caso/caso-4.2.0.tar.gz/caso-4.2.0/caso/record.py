# -*- coding: utf-8 -*-

# Copyright 2014 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Module containing all the cloud accounting records."""

import abc
import datetime
import enum
import json
import typing
import uuid as m_uuid

# We are not parsing XML so this is safe
import xml.etree.ElementTree as ETree  # nosec

import pydantic

import caso
from oslo_log import log

LOG = log.getLogger(__name__)


class _BaseRecord(pydantic.BaseModel, abc.ABC):
    """This is the base cASO record object."""

    version: str = pydantic.Field(..., exclude=True)

    site_name: str
    cloud_type: str = caso.user_agent
    compute_service: str

    @abc.abstractmethod
    def ssm_message(self):
        """Render record as the expected SSM message."""
        raise NotImplementedError("Method not implemented")


class _ValidCloudStatus(str, enum.Enum):
    started = "started"
    completed = "completed"
    error = "error"
    paused = "paused"
    suspended = "suspended"
    stopped = "stopped"
    unknown = "unknown"


class CloudRecord(_BaseRecord):
    """The CloudRecord class holds information for each of the records.

    This class is versioned, following the Cloud Accounting Record versions.
    """

    version: str = pydantic.Field("0.4", exclude=True)

    uuid: m_uuid.UUID
    name: str

    user_id: str
    user_dn: typing.Optional[str]
    group_id: str
    fqan: str

    status: _ValidCloudStatus

    image_id: typing.Optional[str]

    public_ip_count = 0
    cpu_count: int
    memory: int
    disk: int

    start_time: datetime.datetime
    end_time: typing.Optional[datetime.datetime]

    # NOTE(aloga): due to the validation that we are doing below until
    # https://github.com/samuelcolvin/pydantic/issues/935
    # and
    # https://github.com/samuelcolvin/pydantic/pull/2625
    # are closed, we need to define the durations here, so do not move them
    # around, otherwise we cannot access the needed fields
    suspend_duration: typing.Optional[int]

    wall_duration: typing.Optional[int]
    cpu_duration: typing.Optional[int]

    benchmark_value: typing.Optional[float]
    benchmark_type: typing.Optional[str]

    @classmethod
    @pydantic.validator("wall_duration", always=True)
    def _validate_wall_duration(cls, value, values):
        duration = None
        if value is not None:
            duration = value
        elif values["end_time"]:
            duration = values["end_time"] - values["self.start_time"]
            duration = int(duration.total_seconds())
        return duration

    @classmethod
    @pydantic.validator("cpu_duration", always=True)
    def _validate_cpu_duration(cls, value, values):
        duration = None
        if value is not None:
            duration = value
        elif values["wall_duration"] is not None and values["cpu_count"]:
            duration = values["wall_duration"] * values["cpu_count"]
            duration = int(duration)
        return duration

    def set_cpu_duration(self, value: int):
        """Set the CPU duration for the record."""
        self._cpu_duration = value

    def ssm_message(self):
        """Render record as the expected SSM message."""
        opts = {
            "by_alias": True,
            "exclude_none": True,
        }
        # NOTE(aloga): do not iter over the dictionary returned by record.dict() as this
        # is just a dictionary representation of the object, where no serialization is
        # done. In order to get objects correctly serialized we need to convert to JSON,
        # then reload the model
        serialized_record = json.loads(self.json(**opts))
        aux = [f"{k}: {v}" for k, v in serialized_record.items()]
        aux.sort()
        return "\n".join(aux)

    class Config:
        """Config class for Pydantic."""

        @staticmethod
        def map_fields(value: str) -> str:
            """Map object fields to Cloud Accounting Record fields."""
            d = {
                "uuid": "VMUUID",
                "site_name": "SiteName",
                "name": "MachineName",
                "user_id": "LocalUserId",
                "group_id": "LocalGroupId",
                "fqan": "FQAN",
                "status": "Status",
                "start_time": "StartTime",
                "end_time": "EndTime",
                "suspend_duration": "SuspendDuration",
                "wall_duration": "WallDuration",
                "cpu_duration": "CpuDuration",
                "cpu_count": "CpuCount",
                "network_type": "NetworkType",
                "network_in": "NetworkInbound",
                "network_out": "NetworkOutbound",
                "memory": "Memory",
                "disk": "Disk",
                "storage_record_id": "StorageRecordId",
                "image_id": "ImageId",
                "cloud_type": "CloudType",
                "user_dn": "GlobalUserName",
                "public_ip_count": "PublicIPCount",
                "benchmark_value": "Benchmark",
                "benchmark_type": "BenchmarkType",
                "compute_service": "CloudComputeService",
            }
            return d.get(value, value)

        json_encoders = {datetime.datetime: lambda v: int(v.timestamp())}
        alias_generator = map_fields
        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        extra = "forbid"


class IPRecord(_BaseRecord):
    """The IPRecord class holds information for each of the records.

    This class is versioned, following the Public IP Usage Record versions.
    """

    version: str = pydantic.Field("0.2", exclude=True)

    uuid: m_uuid.UUID

    user_id: typing.Optional[str]
    user_dn: typing.Optional[str]
    group_id: str
    fqan: str

    measure_time: datetime.datetime

    ip_version: int
    public_ip_count: int

    def ssm_message(self):
        """Render record as the expected SSM message."""
        opts = {
            "by_alias": True,
            "exclude_none": True,
        }
        return self.json(**opts)

    class Config:
        """Config class for Pydantic."""

        @staticmethod
        def map_fields(field: str) -> str:
            """Map object fields to accounting Public IP Usage record fields."""
            d = {
                "measure_time": "MeasurementTime",
                "site_name": "SiteName",
                "cloud_type": "CloudType",
                "user_id": "LocalUser",
                "group_id": "LocalGroup",
                "fqan": "FQAN",
                "user_dn": "GlobalUserName",
                "ip_version": "IPVersion",
                "public_ip_count": "IPCount",
                "compute_service": "CloudComputeService",
            }
            return d.get(field, field)

        json_encoders = {datetime.datetime: lambda v: int(v.timestamp())}
        alias_generator = map_fields
        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        extra = "forbid"


class AcceleratorRecord(_BaseRecord):
    """The AcceleratorRecord class holds information for each of the records.

    This class is versioned, following the Accelerator Usage Record versions

    """

    version: str = pydantic.Field("0.1", exclude=True)

    uuid: m_uuid.UUID

    user_dn: typing.Optional[str]
    fqan: str

    count: int
    available_duration: int
    _active_duration: typing.Optional[int]

    measurement_month: int
    measurement_year: int

    associated_record_type: str = "cloud"

    accelerator_type: str
    cores: typing.Optional[int]
    model: str

    benchmark_value: typing.Optional[float]
    benchmark_type: typing.Optional[str]

    @property
    def active_duration(self) -> int:
        """Get the active duration for the record (property)."""
        if self._active_duration is not None:
            return self._active_duration
        return self.available_duration

    def set_active_duration(self, value: int):
        """Set the active duration for the record."""
        self._active_duration = value

    def ssm_message(self):
        """Render record as the expected SSM message."""
        opts = {
            "by_alias": True,
            "exclude_none": True,
        }
        return self.json(**opts)

    class Config:
        """Config class for Pydantic."""

        @staticmethod
        def map_fields(field: str) -> str:
            """Map object fields to accounting Accelerator Usage Record fields."""
            d = {
                "measurement_month": "MeasurementMonth",
                "measurement_year": "MeasurementYear",
                "associated_record_type": "AssociatedRecordType",
                "uuid": "AccUUID",
                "user_dn": "GlobalUserName",
                "fqan": "FQAN",
                "site_name": "SiteName",
                "count": "Count",
                "cores": "Cores",
                "active_duration": "ActiveDuration",
                "available_duration": "AvailableDuration",
                "benchmark_type": "BenchmarkType",
                "benchmark": "Benchmark",
                "accelerator_type": "Type",
                "model": "Model",
                "cloud_type": "CloudType",
                "compute_service": "CloudComputeService",
            }
            return d.get(field, field)

        json_encoders = {datetime.datetime: lambda v: int(v.timestamp())}
        alias_generator = map_fields
        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        extra = "forbid"


class StorageRecord(_BaseRecord):
    """The StorageRecord class holds information for each of the records.

    This class is versioned, following the Storage Accounting Definition on
    EMI StAR
    """

    version: str = pydantic.Field("0.1", exclude=True)

    uuid: m_uuid.UUID
    name: str

    user_id: str
    user_dn: typing.Optional[str]
    group_id: str
    fqan: str

    active_duration: int
    attached_duration: typing.Optional[float]
    attached_to: typing.Optional[str]
    measure_time: datetime.datetime
    start_time: datetime.datetime

    storage_type: typing.Optional[str] = "Block Storage (cinder)"

    status: str
    capacity: int

    # (aidaph) Fix the return to something different to 0
    @classmethod
    @pydantic.validator("attached_duration", always=True)
    def _validate_attached_duration(cls, value):
        if value is not None:
            return value
        return 0

    def ssm_message(self):
        """Render record as the expected SSM message."""
        ns = {"xmlns:sr": "http://eu-emi.eu/namespaces/2011/02/storagerecord"}
        sr = ETree.Element("sr:StorageUsageRecord", attrib=ns)
        ETree.SubElement(
            sr,
            "sr:RecordIdentity",
            attrib={
                "sr:createTime": self.measure_time.isoformat(),
                "sr:recordId": str(self.uuid),
            },
        )
        ETree.SubElement(sr, "sr:StorageSystem").text = self.compute_service
        ETree.SubElement(sr, "sr:Site").text = self.site_name
        subject = ETree.SubElement(sr, "sr:SubjectIdentity")
        ETree.SubElement(subject, "sr:LocalUser").text = self.user_id
        ETree.SubElement(subject, "sr:LocalGroup").text = self.group_id
        if self.user_dn:
            ETree.SubElement(subject, "sr:UserIdentity").text = self.user_dn
        if self.fqan:
            ETree.SubElement(subject, "sr:Group").text = self.fqan
        ETree.SubElement(sr, "sr:StartTime").text = self.start_time.isoformat()
        ETree.SubElement(sr, "sr:EndTime").text = self.measure_time.isoformat()
        capacity = str(int(self.capacity * 1073741824))  # 1 GiB = 2^30
        ETree.SubElement(sr, "sr:ResourceCapacityUsed").text = capacity
        return ETree.tostring(sr)

    class Config:
        """Config class for Pydantic."""

        @staticmethod
        def map_fields(field: str) -> str:
            """Map object fields to accounting EMI StAR record values."""
            d = {
                "measure_time": "CreateTime",
                "uuid": "VolumeUUID",
                "name": "RecordName",
                "user_id": "LocalUser",
                "user_dn": "GlobalUserName",
                "group_id": "LocalGroup",
                "fqan": "FQAN",
                "site_name": "SiteName",
                "capacity": "Capacity",
                "active_duration": "ActiveDuration",
                "start_time": "StartTime",
                "storage_type": "Type",
                "status": "Status",
                "attached_to": "AttachedTo",
                "attached_duration": "AttachedDuration",
                "cloud_type": "CloudType",
                "compute_service": "CloudComputeService",
            }
            return d.get(field, field)

        alias_generator = map_fields
        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        extra = "forbid"
