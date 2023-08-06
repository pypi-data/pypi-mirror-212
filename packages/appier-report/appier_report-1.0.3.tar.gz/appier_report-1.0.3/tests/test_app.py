#!/usr/bin/env python
"""Tests for `appier_report` package."""
# pylint: disable=redefined-outer-name
import os
import pytest

from datetime import datetime, timedelta

from appier_report import Report


@pytest.fixture
def access_token():
    access_token = os.environ.get("APPIER_ACCESS_TOKEN", None)
    assert access_token is not None
    return access_token


def test_campaign_report(access_token):
    campaign_report = Report(access_token=access_token, api_type="campaign")
    assert campaign_report is not None

    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    report = campaign_report.get_report(start_date=start_date, end_date=end_date)
    assert len(report) > 0


def test_inventory_report(access_token):
    inventory_report = Report(access_token=access_token, api_type="inventory")
    assert inventory_report is not None

    start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    report = inventory_report.get_report(start_date=start_date, end_date=end_date)
    assert len(report) > 0
