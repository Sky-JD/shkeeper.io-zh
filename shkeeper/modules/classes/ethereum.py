from abc import abstractmethod
from os import environ
import json
from shkeeper import requests
import datetime
from collections import namedtuple
from decimal import Decimal
from flask import current_app as app
from shkeeper.modules.classes.crypto import Crypto
from shkeeper.services.backend_balances import evm_accounts_balance


class Ethereum(Crypto):
    can_set_tx_fee = False
    network_currency = "ETH"

    def gethost(self):
        host = environ.get("ETHEREUM_API_SERVER_HOST", "ethereum-shkeeper")
        port = environ.get("ETHEREUM_SERVER_PORT", "6000")
        return f"{host}:{port}"

    def get_auth_creds(self):
        username = environ.get(f"ETH_USERNAME", "shkeeper")
        password = environ.get(f"ETH_PASSWORD", "shkeeper")
        return (username, password)

    def estimate_tx_fee(self, amount, **kwargs):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/calc-tx-fee/{amount}",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        return response

    @property
    def fee_deposit_account(self):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/fee-deposit-account",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)

        FeeDepositAccount = namedtuple("FeeDepositAccount", "addr balance")
        return FeeDepositAccount(response["account"], Decimal(response["balance"]))

    def balance(self):
        self._balance_error = None
        api_balance = None
        local_confirmed_balance = None
        try:
            response = requests.post(
                f"http://{self.gethost()}/{self.crypto}/balance",
                auth=self.get_auth_creds(),
            ).json(parse_float=Decimal)
            api_balance = Decimal(response["balance"])
        except Exception as e:
            self._balance_error = str(e)
            app.logger.warning("Wallet API balance error for %s: %s", self.crypto, e)

        if self.crypto != self.network_currency:
            local_confirmed_balance = self._local_confirmed_invoice_balance()
            aggregate_balance = evm_accounts_balance(self.network_currency, self.crypto)
            if aggregate_balance.error:
                self._balance_error = (
                    f"accounts_aggregate: {aggregate_balance.error}"
                )
            elif aggregate_balance.configured and aggregate_balance.amount is not None:
                self._balance_source = f"{self.network_currency.lower()}_accounts_aggregate"
                amount = aggregate_balance.amount
                if (
                    local_confirmed_balance is not None
                    and local_confirmed_balance > amount
                ):
                    app.logger.info(
                        "%s account aggregate %s is lower than local confirmed invoice balance %s",
                        self.crypto,
                        amount,
                        local_confirmed_balance,
                    )
                    self._balance_source = (
                        f"{self.network_currency.lower()}_accounts_aggregate_local_floor"
                    )
                    amount = local_confirmed_balance
                if api_balance is not None and aggregate_balance.amount != api_balance:
                    app.logger.info(
                        "%s wallet API balance %s differs from account aggregate %s",
                        self.crypto,
                        api_balance,
                        aggregate_balance.amount,
                    )
                return amount

            if (
                local_confirmed_balance is not None
                and api_balance is not None
                and local_confirmed_balance > api_balance
            ):
                app.logger.info(
                    "%s wallet API balance %s is lower than local confirmed invoice balance %s",
                    self.crypto,
                    api_balance,
                    local_confirmed_balance,
                )
                self._balance_source = (
                    f"{self.network_currency.lower()}_local_confirmed_floor"
                )
                return local_confirmed_balance

        self._balance_source = "wallet_api"
        return api_balance if api_balance is not None else Decimal("0")

    def _local_confirmed_invoice_balance(self):
        try:
            from sqlalchemy import func
            from shkeeper import db
            from shkeeper.models import Invoice, InvoiceStatus, Transaction

            value = (
                db.session.query(func.coalesce(func.sum(Transaction.amount_crypto), 0))
                .join(Invoice, Transaction.invoice_id == Invoice.id)
                .filter(Transaction.crypto == self.crypto)
                .filter(Transaction.need_more_confirmations == False)
                .filter(Invoice.status != InvoiceStatus.OUTGOING)
                .scalar()
            )
            return Decimal(str(value or 0))
        except Exception as e:
            app.logger.warning(
                "Local confirmed invoice balance query failed for %s: %s",
                self.crypto,
                e,
            )
            return None

    def get_confirmations_by_txid(self, txid):
        transactions = self.getaddrbytx(txid)
        _, _, confirmations, _ = transactions[0]
        return confirmations

    def get_task(self, id):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/task/{id}",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        return response

    def getstatus(self):
        try:
            response = requests.post(
                f"http://{self.gethost()}/{self.crypto}/status",
                auth=self.get_auth_creds(),
            ).json(parse_float=Decimal)

            block_ts = response["last_block_timestamp"]
            now_ts = int(datetime.datetime.now().timestamp())

            delta = abs(now_ts - block_ts)
            block_interval = 12
            if delta < block_interval * 10:
                return "Synced"
            else:
                return "Sync In Progress (%d blocks behind)" % (delta // block_interval)

        except Exception as e:
            return "Offline"

    def mkaddr(self, **kwargs):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/generate-address",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        addr = response["address"]
        return addr

    def getaddrbytx(self, tx):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/transaction/{tx}",
            auth=self.get_auth_creds(),
            timeout=60,
        ).json(parse_float=Decimal)
        if isinstance(response, dict):
            if response.get("status") == "error":
                raise Exception(
                    response.get("msg") or response.get("message") or str(response)
                )
            response = response.get("transactions") or response.get("result") or []
        result = []
        for item in response:
            if isinstance(item, dict):
                address = item.get("addr") or item.get("address")
                amount = item.get("amount") or item.get("amount_crypto")
                confirmations = item.get("confirmations", 1)
                category = item.get("category", "receive")
            elif len(item) == 3:
                address, amount, confirmations = item
                category = "receive"
            else:
                address, amount, confirmations, category = item
            result.append([address, Decimal(amount), confirmations, category])
        return result

    def dump_wallet(self):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/dump",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        now = datetime.datetime.now().strftime("%F_%T")
        filename = f"{now}_{self.crypto}_shkeeper_wallet.json"
        # content = json.dumps(response['accounts'], indent=4)
        content = json.dumps(response, indent=4)
        return filename, content

    def create_wallet(self, *args, **kwargs):
        return {"error": None}

    def mkpayout(self, destination, amount, fee, subtract_fee_from_amount=False):
        if self.crypto == self.network_currency and subtract_fee_from_amount:
            fee = Decimal(self.estimate_tx_fee(amount)["fee"])
            if fee >= amount:
                return f"Payout failed: not enought ETH to pay for transaction. Need {fee}, balance {amount}"
            else:
                amount -= fee
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/payout/{destination}/{amount}",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        return response

    def multipayout(self, payout_list):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/multipayout",
            auth=self.get_auth_creds(),
            json=payout_list,
        ).json(parse_float=Decimal)
        return response

    def metrics(self):
        host = str(self.gethost())
        host = host.split(":")[0].replace("-", "_")
        try:
            success_text = f"# HELP {host}_status Connection status to {host}\n# TYPE {host}_status gauge\n{host}_status 1.0\n"
            return (
                requests.get(
                    f"http://{self.gethost()}/metrics", auth=self.get_auth_creds()
                ).text
                + success_text
            )
        except Exception as e:
            error_text = f"# HELP {host}_status Connection status to {host}\n# TYPE {host}_status gauge\n{host}_status 0.0\n"
            return error_text

    def get_all_addresses(self):
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/get_all_addresses",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        return response
