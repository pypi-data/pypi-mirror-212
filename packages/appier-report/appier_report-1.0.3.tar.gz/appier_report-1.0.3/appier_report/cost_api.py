import time
import traceback
from datetime import datetime, timedelta

import requests

from appier_report.utils.date_utils import DateUtils


class Report:
    """
    This class is used to interact with the Appier Campaign Report API.
    """

    ENDPOINTS = {
        "campaign": "https://mmp.appier.org/campaign_report",
        "inventory": "https://mmp.appier.org/inventory_report",
    }

    def __init__(self, api_type: str = "campaign", access_token: str = ""):
        """
        Args:
            api_type: "campaign" or "inventory"
            access_token: The access token for the Appier API.
        Returns:
            Nothing

        Doc Author:
            minhpc@ikameglobal.com
        """
        self.access_token = access_token
        self.endpoint = Report.ENDPOINTS.get(api_type, None)

        if not self.endpoint:
            raise Exception(f"Invalid type: {api_type}")

    def _get_report(
        self,
        start_date: str = None,
        end_date: str = None,
        timezone: int = 0,
        max_retries: int = 3,
        retry_interval: int = 30,
        **kwargs,
    ) -> list[dict]:
        """
        Get campaign report data from Appier Cost API.

        Args:
            start_date: Format YYYY-MM-DD
            end_date: Format YYYY-MM-DD
            timezone: Timezone offset in hours.
            max_retries: Number of retries before giving up.
            retry_interval: Time to wait between retries.
            **kwargs: Other parameters

        Note:
            The **start_date** and **end_date** should be near each other (about 5 days apart),
            otherwise the request will fail.

        Returns:
            Report data in JSON format.
        Doc Author:
            minhpc@ikameglobal.com
        """
        params = {
            "access_token": self.access_token,
            "start_date": start_date,
            "end_date": end_date,
            "timezone": timezone,
            **kwargs,
        }

        for i in range(max_retries + 1):
            try:
                response = requests.get(url=self.endpoint, params=params)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Error: {e}")
                print('---------------------------------')
                print(traceback.format_exc())
                print('---------------------------------')
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
        raise Exception(f"Error: {response.status_code}")

    def get_report(
        self,
        start_date: str = None,
        end_date: str = None,
        date_interval: int = 5,
        timezone: int = 0,
        max_retries: int = 3,
        retry_interval: int = 30,
        **kwargs,
    ) -> list[dict]:
        """
        Wrapper for _get_report() to get report data from Appier Cost API.

        Args:
            start_date: Format YYYY-MM-DD
            end_date: Format YYYY-MM-DD
            date_interval: Number of days between each request.
            timezone: Timezone offset in hours.
            max_retries: Number of retries before giving up.
            retry_interval: Time to wait between retries.
            **kwargs: Other parameters

        Returns:
            Report data in JSON format.
        Doc Author:
            minhpc@ikameglobal.com
        """
        if not start_date or not end_date:
            start_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
            end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        date_ranges = DateUtils.get_date_ranges(start_date=start_date, end_date=end_date, date_interval=date_interval)

        result = []
        for start, end in date_ranges:
            result.extend(
                self._get_report(
                    start_date=start,
                    end_date=end,
                    timezone=timezone,
                    max_retries=max_retries,
                    retry_interval=retry_interval,
                    **kwargs,
                )
            )

        return result


if __name__ == '__main__':
    inventory_report = Report(access_token="52da5d8cd6a84a9dbef1fd7c55159193", api_type='inventory')
    report = inventory_report.get_report(start_date='2023-06-04', end_date='2023-06-04')
    print(report)
