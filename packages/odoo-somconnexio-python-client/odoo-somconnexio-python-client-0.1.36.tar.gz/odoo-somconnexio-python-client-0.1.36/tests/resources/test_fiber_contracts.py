import pytest
import unittest2 as unittest
from odoo_somconnexio_python_client.exceptions import ResourceNotFound

from odoo_somconnexio_python_client.resources.fiber_contracts import (
    FiberContractsToPack,
)


def assert_model(contracts):
    contract = contracts[0]

    assert contract.code == "33055"
    assert contract.customer_vat == "ES30282588Y"
    assert contract.phone_number == "939591019"
    assert contract.current_tariff_product == "SE_SC_REC_BA_F_600"


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the API-KEY request header with "DUMMY" in cassettes
        "filter_headers": [("API-KEY", "DUMMY")],
    }


class FiberContractsToPackTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_by_partner_ref(self):
        assert_model(FiberContractsToPack.search_by_partner_ref(partner_ref=27550))

    @pytest.mark.vcr()
    def test_search_by_partner_ref_and_mobiles_sharing_data(self):
        assert_model(
            FiberContractsToPack.search_by_partner_ref(
                partner_ref=27550, mobiles_sharing_data=True
            )
        )

    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(
            ResourceNotFound,
            FiberContractsToPack.search_by_partner_ref,
            partner_ref="xxx",
        )
