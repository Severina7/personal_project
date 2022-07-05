from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from mintapi import constants
import logging
import os
from mintapi.signIn import sign_in, _create_web_driver_at_mint_com

class MintException(Exception):
    pass

logger = logging.getLogger("mintapi")

ENDPOINTS = {
    constants.ACCOUNT_KEY: {
        "apiVersion": "pfm/v1",
        "endpoint": "accounts",
        "beginningDate": None,
        "endingDate": None,
        "includeCreatedDate": True,
    },
    constants.CATEGORY_KEY: {
        "apiVersion": "pfm/v1",
        "endpoint": "categories",
        "beginningDate": None,
        "endingDate": None,
        "includeCreatedDate": False,
    },
    constants.TRANSACTION_KEY: {
        "apiVersion": "pfm/v1",
        "endpoint": "transactions",
        "beginningDate": "fromDate",
        "endingDate": "toDate",
        "includeCreatedDate": False,
    },
}


def convert_mmddyy_to_datetime(date):
    try:
        newdate = datetime.strptime(date, "%m/%d/%y")
    except (TypeError, ValueError):
        newdate = None
    return newdate

class Mint(object):
    driver = None
    status_message = None

    def __init__(
        self,
        email=None,
        password=None,
        mfa_method=None,
        mfa_token=None,
        mfa_input_callback=None,
        intuit_account=None,
        headless=False,
        session_path=None,
        imap_account=None,
        imap_password=None,
        imap_server=None,
        imap_folder="INBOX",
        wait_for_sync=True,
        wait_for_sync_timeout=5 * 60,
        fail_if_stale=False,
        use_chromedriver_on_path=False,
        chromedriver_download_path=os.getcwd(),
        driver=None,
        beta=False,
    ):
        self.driver = None
        self.status_message = None

        if email and password:
            self.login_and_get_token(
                email,
                password,
                mfa_method=mfa_method,
                mfa_token=mfa_token,
                mfa_input_callback=mfa_input_callback,
                intuit_account=intuit_account,
                headless=headless,
                session_path=session_path,
                imap_account=imap_account,
                imap_password=imap_password,
                imap_server=imap_server,
                imap_folder=imap_folder,
                wait_for_sync=wait_for_sync,
                wait_for_sync_timeout=wait_for_sync_timeout,
                fail_if_stale=fail_if_stale,
                use_chromedriver_on_path=use_chromedriver_on_path,
                chromedriver_download_path=chromedriver_download_path,
                driver=driver,
                beta=beta,
            )

    def _get_api_key_header(self):
        key_var = "window.__shellInternal.appExperience.appApiKey"
        api_key = self.driver.execute_script("return " + key_var)
        auth = "Intuit_APIKey intuit_apikey=" + api_key
        auth += ", intuit_apikey_version=1.0"
        header = {"authorization": auth}
        header.update(constants.JSON_HEADER)
        return header

    def close(self):
        """Logs out and quits the current web driver/selenium session."""
        if not self.driver:
            return

        self.driver.quit()
        self.driver = None

    def get(self, url, **kwargs):
        return self.driver.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.driver.request("POST", url, **kwargs)

    def login_and_get_token(
        self,
        email,
        password,
        mfa_method=None,
        mfa_token=None,
        mfa_input_callback=None,
        intuit_account=None,
        headless=False,
        session_path=None,
        imap_account=None,
        imap_password=None,
        imap_server=None,
        imap_folder=None,
        wait_for_sync=True,
        wait_for_sync_timeout=5 * 60,
        fail_if_stale=False,
        use_chromedriver_on_path=False,
        chromedriver_download_path=os.getcwd(),
        driver=None,
        beta=False,
    ):

        self.driver = driver or _create_web_driver_at_mint_com(
            headless, session_path, use_chromedriver_on_path, chromedriver_download_path
        )

        try:
            self.status_message = sign_in(
                email,
                password,
                self.driver,
                mfa_method,
                mfa_token,
                mfa_input_callback,
                intuit_account,
                wait_for_sync,
                wait_for_sync_timeout,
                fail_if_stale,
                imap_account,
                imap_password,
                imap_server,
                imap_folder,
                beta,
            )
        except Exception as e:
            msg = f"Could not sign in to Mint. Current page: {self.driver.current_url}"
            logger.exception(e)
            self.driver.quit()
            self.driver = None
            raise Exception(msg) from e

    def get_attention(self):
        attention = None
        # noinspection PyBroadException
        try:
            if "complete" in self.status_message:
                attention = self.status_message.split(".")[1].strip()
            else:
                attention = self.status_message
        except Exception:
            pass
        return attention

    def get_bills(self):
        return self.get(
            "{}/bps/v2/payer/bills".format(constants.MINT_ROOT_URL),
            headers=self._get_api_key_header(),
        ).json()["bills"]

    def get_data(self, name, limit, id=None, start_date=None, end_date=None):
        endpoint = self.__find_endpoint(name)
        data = self.__call_mint_endpoint(endpoint, limit, id, start_date, end_date)
        if name in data.keys():
            for i in data[name]:
                if endpoint["includeCreatedDate"]:
                    i["createdDate"] = i["metaData"]["createdDate"]
                i["lastUpdatedDate"] = i["metaData"]["lastUpdatedDate"]
                i.pop("metaData", None)
        else:
            raise MintException(
                "Data from the {} endpoint did not containt the expected {} key.".format(
                    endpoint["endpoint"], name
                )
            )
        return data[name]

    def get_account_data(
        self,
        limit=5000,
    ):
        return self.get_data(constants.ACCOUNT_KEY, limit)

    def get_category_data(
        self,
        limit=5000,
    ):
        return self.get_data(constants.CATEGORY_KEY, limit)

    def get_budget_data(
        self,
        limit=5000,
    ):
        return self.get_data(
            constants.BUDGET_KEY,
            limit,
            None,
            start_date=self.__x_months_ago(11),
            end_date=self.__first_of_this_month(),
        )

    def get_investment_data(
        self,
        limit=5000,
    ):
        return self.get_data(
            constants.INVESTMENT_KEY,
            limit,
        )

    def get_transaction_data(
        self,
        limit=5000,
        include_investment=False,
        start_date=None,
        end_date=None,
        remove_pending=True,
        id=0,
    ):
        """
        Note: start_date and end_date must be in format mm/dd/yy.
        If pulls take too long, consider a narrower range of start and end
        date. See json explanation of include_investment.

        Also note: Mint includes pending transactions, however these sometimes
        change dates/amounts after the transactions post. They have been
        removed by default in this pull, but can be included by changing
        remove_pending to False
        """

        try:
            if include_investment:
                id = 0
            data = self.get_data(
                constants.TRANSACTION_KEY,
                limit,
                id,
                convert_mmddyy_to_datetime(start_date),
                convert_mmddyy_to_datetime(end_date),
            )
            if remove_pending:
                filtered = filter(
                    lambda transaction: transaction["isPending"] == False,
                    data,
                )
                data = list(filtered)
        except Exception:
            raise Exception
        return data

    def get_net_worth_data(self, account_data=None):
        if account_data is None:
            account_data = self.get_account_data()

        # account types in this list will be subtracted
        invert = set(["LoanAccount", "CreditAccount"])
        return sum(
            [
                -a["currentBalance"] if a["type"] in invert else a["currentBalance"]
                for a in account_data
                if a["isActive"] and "currentBalance" in a
            ]
        )

    def initiate_account_refresh(self):
        self.post(
            url="{}/refreshFILogins.xevent".format(constants.MINT_ROOT_URL),
            headers=constants.JSON_HEADER,
        )

    def __find_endpoint(self, name):
        return ENDPOINTS[name]

    def __call_mint_endpoint(
        self, endpoint, limit, id=None, start_date=None, end_date=None
    ):
        url = "{}/{}/{}?limit={}&".format(
            constants.MINT_ROOT_URL, endpoint["apiVersion"], endpoint["endpoint"], limit
        )
        if endpoint["beginningDate"] is not None and start_date is not None:
            url = url + "{}={}&".format(endpoint["beginningDate"], start_date)
        if endpoint["endingDate"] is not None and end_date is not None:
            url = url + "{}={}&".format(endpoint["endingDate"], end_date)
        if id is not None:
            url = url + "id={}&".format(id)
        response = self.get(
            url,
            headers=self._get_api_key_header(),
        )
        return response.json()

    def __first_of_this_month(self):
        return date.today().replace(day=1)

    def __x_months_ago(self, months=2):
        return (self.__first_of_this_month() - relativedelta(months=months)).replace(
            day=1
        )


def get_accounts(email, password, get_detail=False):
    mint = Mint(email, password)
    return mint.get_account_data(get_detail=get_detail)


def initiate_account_refresh(email, password):
    mint = Mint(email, password)
    return mint.initiate_account_refresh()