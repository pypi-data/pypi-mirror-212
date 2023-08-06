from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.exceptions import (
    InvalidSortBy,
    InvalidSortOrder,
    NotNumericLimit,
    NotNumericOffset,
    ResourceNotFound,
)
from odoo_somconnexio_python_client.resources.contract import (
    Contract,
)


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the API-KEY request header with "DUMMY" in cassettes
        "filter_headers": [("API-KEY", "DUMMY")],
    }


class ContractTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(
            ResourceNotFound, Contract.get_by_phone_number, phone_number="9999"
        )

    @pytest.mark.vcr()
    def test_get_contract_by_phone_number(self):
        contracts = Contract.get_by_phone_number(phone_number="616904164")
        contract = contracts[0]

        assert contract.code == "33062"
        assert contract.customer_vat == "ES30282588Y"
        assert contract.phone_number == "616904164"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_T_UNL_5120"

    @pytest.mark.vcr()
    def test_get_contract_by_code(self):
        contracts = Contract.get_by_code(code="33057")
        contract = contracts[0]

        assert contract.code == "33057"
        assert contract.customer_vat == "ES30282588Y"
        assert contract.phone_number == "-"
        assert contract.current_tariff_product == "SE_SC_REC_BA_F_300_SF"

    @pytest.mark.vcr()
    def test_search_paginated_contracts_by_customer_ref(self):
        paging_contracts = Contract.search_by_customer_ref(
            customer_ref="27550",
            limit=5,
            offset=0,
            sortBy="code",
            sortOrder="DESCENDENT",
        )
        contract = paging_contracts.contracts[1]
        paging = paging_contracts.paging

        assert contract.customer_ref == "27550"
        assert contract.customer_vat == "ES30282588Y"
        assert contract.phone_number == "717260966"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_PACK_UNL_20480"
        assert paging.limit == 5
        assert paging.totalNumberOfRecords == 8
        assert paging.offset == 0
        assert paging.sortBy == "code"
        assert paging.sortOrder == "DESCENDENT"

    @pytest.mark.vcr()
    def test_search_paginated_contracts_by_vat(self):
        paging_contracts = Contract.search_by_customer_vat(
            vat="ES30282588Y",
            limit=5,
            offset=0,
            sortBy="code",
            sortOrder="DESCENDENT",
        )
        paging = paging_contracts.paging
        first_contract = paging_contracts.contracts[0]
        second_contract = paging_contracts.contracts[1]

        assert first_contract.code == "33066"
        assert first_contract.customer_vat == "ES30282588Y"
        assert first_contract.phone_number == "784203016"
        assert first_contract.current_tariff_product == "SE_SC_REC_MOBILE_T_150_1024"

        assert second_contract.code == "33064"
        assert second_contract.customer_vat == "ES30282588Y"
        assert second_contract.phone_number == "717260966"
        assert (
            second_contract.current_tariff_product == "SE_SC_REC_MOBILE_PACK_UNL_20480"
        )

        assert paging.limit == 5
        assert paging.totalNumberOfRecords == 8
        assert paging.offset == 0
        assert paging.sortBy == "code"
        assert paging.sortOrder == "DESCENDENT"

    @pytest.mark.vcr()
    def test_search_contract_by_customer_ref_with_pagination_bad_limit(self):
        self.assertRaises(
            NotNumericLimit,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit="XXX",
        )

    @pytest.mark.vcr()
    def test_search_contract_by_customer_ref_with_pagination_bad_offset(self):
        self.assertRaises(
            NotNumericOffset,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit=5,
            offset="XXX",
        )

    @pytest.mark.vcr()
    def test_search_contract_by_customer_ref_with_pagination_bad_sort_order(self):
        self.assertRaises(
            InvalidSortOrder,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit=5,
            offset=0,
            sortBy="date_start",
            sortOrder="XXX",
        )

    @pytest.mark.vcr()
    def test_search_contract_by_customer_ref_with_pagination_bad_sort_by(self):
        self.assertRaises(
            InvalidSortBy,
            Contract.search_by_customer_ref,
            customer_ref="123",
            limit=5,
            offset=0,
            sortBy="XXX",
            sortOrder="DESCENDENT",
        )
