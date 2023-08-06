# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Callable

import pytest

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType

MODULE_NAME = "CONN"


def create_connection(
    client: AtlanClient, name: str, connector_type: AtlanConnectorType
) -> Connection:
    admin_role_guid = str(RoleCache.get_id_for_name("$admin"))
    to_create = Connection.create(
        name=name, connector_type=connector_type, admin_roles=[admin_role_guid]
    )
    response = client.upsert(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    resolved = client.get_asset_by_guid(result.guid, asset_type=Connection)
    return resolved


def test_invalid_connection(client: AtlanClient, make_unique: Callable[[str], str]):
    with pytest.raises(
        ValueError, match="One of admin_user, admin_groups or admin_roles is required"
    ):
        Connection.create(
            name=make_unique(MODULE_NAME), connector_type=AtlanConnectorType.POSTGRES
        )


def test_invalid_connection_admin_role(
    client: AtlanClient,
    make_unique: Callable[[str], str],
):
    with pytest.raises(
        ValueError, match="Provided role ID abc123 was not found in Atlan."
    ):
        Connection.create(
            name=make_unique(MODULE_NAME),
            connector_type=AtlanConnectorType.SAPHANA,
            admin_roles=["abc123"],
        )


def test_invalid_connection_admin_group(
    client: AtlanClient,
    make_unique: Callable[[str], str],
):
    with pytest.raises(
        ValueError, match="Provided group name abc123 was not found in Atlan."
    ):
        Connection.create(
            name=make_unique(MODULE_NAME),
            connector_type=AtlanConnectorType.SAPHANA,
            admin_groups=["abc123"],
        )


def test_invalid_connection_admin_user(
    client: AtlanClient,
    make_unique: Callable[[str], str],
):
    with pytest.raises(
        ValueError, match="Provided username abc123 was not found in Atlan."
    ):
        Connection.create(
            name=make_unique(MODULE_NAME),
            connector_type=AtlanConnectorType.SAPHANA,
            admin_users=["abc123"],
        )
