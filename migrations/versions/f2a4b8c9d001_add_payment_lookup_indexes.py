"""Add payment lookup indexes

Revision ID: f2a4b8c9d001
Revises: e4f8a9b2c1d8
Create Date: 2026-06-03 09:05:00.000000

"""
from alembic import op


revision = "f2a4b8c9d001"
down_revision = "e4f8a9b2c1d8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_invoice_external_id", "invoice", ["external_id"])
    op.create_index("ix_invoice_status_created", "invoice", ["status", "created_at"])
    op.create_index("ix_invoice_address_addr", "invoice_address", ["addr"])
    op.create_index(
        "ix_transaction_callback_confirmations",
        "transaction",
        ["callback_confirmed", "need_more_confirmations", "created_at"],
    )
    op.create_index(
        "ix_unconfirmed_transaction_callback",
        "unconfirmed_transaction",
        ["callback_confirmed", "created_at"],
    )
    op.create_index(
        "ix_notification_callback_retry",
        "notification",
        ["callback_confirmed", "retries", "created_at"],
    )
    op.create_index("ix_payout_external_id_crypto", "payout", ["external_id", "crypto"])


def downgrade():
    op.drop_index("ix_payout_external_id_crypto", table_name="payout")
    op.drop_index("ix_notification_callback_retry", table_name="notification")
    op.drop_index("ix_unconfirmed_transaction_callback", table_name="unconfirmed_transaction")
    op.drop_index("ix_transaction_callback_confirmations", table_name="transaction")
    op.drop_index("ix_invoice_address_addr", table_name="invoice_address")
    op.drop_index("ix_invoice_status_created", table_name="invoice")
    op.drop_index("ix_invoice_external_id", table_name="invoice")
