from unittest.mock import patch, MagicMock

import pytest

from operatorcert.entrypoints.update_cert_project_data import (
    update_cert_project_related_data,
)


@patch("operatorcert.entrypoints.update_cert_project_data.pyxis.patch")
@patch("operatorcert.entrypoints.update_cert_project_data.store_results")
def test_update_cert_project_data(
    mock_store: MagicMock,
    mock_patch: MagicMock,
) -> None:
    args = MagicMock()
    args.pyxis_url = "https://example.com"
    args.cert_project_id = "id1234"
    args.certification_date = "Started"
    mock_rsp = MagicMock()
    mock_rsp.json.return_value = {
        "org_id": 123,
        "container": {
            "isv_pid": "some_pid",
        },
        "certification_date": "2021-09-22T22:44:58.304Z",
        "certification_status": "Started",
    }
    mock_patch.return_value = mock_rsp

    update_cert_project_related_data(args)
    mock_store.assert_called_with(
        {
            "cert_project": {
                "org_id": 123,
                "container": {
                    "isv_pid": "some_pid",
                },
                "certification_date": "2021-09-22T22:44:58.304Z",
                "certification_status": "Started",
            }
        }
    )
