from datetime import datetime
from mintapi import constants, exceptions
import email
import email.header
import imaplib
# import io
import logging
import os
import time

def sign_in(
    email,
    password,
    driver,
    mfa_method=None,
    mfa_token=None,
    mfa_input_callback=None,
    intuit_account=None,
    wait_for_sync=True,
    wait_for_sync_timeout=5 * 60,
    fail_if_stale=False,
    imap_account=None,
    imap_password=None,
    imap_server=None,
    imap_folder="INBOX",
    beta=False,
):
    if beta:
        url = constants.MINT_BETA_ROOT_URL
    else:
        url = constants.MINT_ROOT_URL
    """
    Takes in a web driver and gets it through the Mint sign in process
    """
    driver.implicitly_wait(20)  # seconds
    driver.get(url)
    if not beta:
        # Add 1 second delay otherwise an issue occurs when trying to click the sign in button on home page
        time.sleep(1)
        home_page(driver)