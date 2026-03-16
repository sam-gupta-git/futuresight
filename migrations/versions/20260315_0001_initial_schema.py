"""initial schema"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260315_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("market_prices", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("symbol", sa.Text(), nullable=False), sa.Column("price", sa.Float(), nullable=False), sa.Column("volume", sa.Float(), nullable=False), sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_market_prices_symbol", "market_prices", ["symbol"], unique=False)
    op.create_index("ix_market_prices_timestamp", "market_prices", ["timestamp"], unique=False)

    op.create_table("options_chain", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("symbol", sa.Text(), nullable=False), sa.Column("strike", sa.Float(), nullable=False), sa.Column("expiration", sa.Date(), nullable=False), sa.Column("iv", sa.Float(), nullable=False), sa.Column("delta", sa.Float(), nullable=False), sa.Column("gamma", sa.Float(), nullable=False), sa.Column("volume", sa.Integer(), nullable=False), sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_options_chain_symbol", "options_chain", ["symbol"], unique=False)
    op.create_index("ix_options_chain_timestamp", "options_chain", ["timestamp"], unique=False)

    op.create_table("futures_quotes", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("contract", sa.Text(), nullable=False), sa.Column("price", sa.Float(), nullable=False), sa.Column("volume", sa.Float(), nullable=False), sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_futures_quotes_timestamp", "futures_quotes", ["timestamp"], unique=False)

    op.create_table("signals", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("symbol", sa.Text(), nullable=False), sa.Column("signal_type", sa.Text(), nullable=False), sa.Column("price", sa.Float(), nullable=False), sa.Column("confidence", sa.Float(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_signals_symbol", "signals", ["symbol"], unique=False)
    op.create_index("ix_signals_signal_type", "signals", ["signal_type"], unique=False)
    op.create_index("ix_signals_created_at", "signals", ["created_at"], unique=False)

    op.create_table("trades", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("symbol", sa.Text(), nullable=False), sa.Column("instrument_type", sa.Text(), nullable=False), sa.Column("entry_price", sa.Float(), nullable=False), sa.Column("exit_price", sa.Float(), nullable=True), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("entry_time", sa.DateTime(timezone=True), nullable=False), sa.Column("exit_time", sa.DateTime(timezone=True), nullable=True), sa.Column("strategy", sa.Text(), nullable=False), sa.Column("pnl", sa.Float(), nullable=False), sa.Column("r_multiple", sa.Float(), nullable=False), sa.Column("notes", sa.Text(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_trades_symbol", "trades", ["symbol"], unique=False)
    op.create_index("ix_trades_entry_time", "trades", ["entry_time"], unique=False)

    op.create_table("alerts", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("symbol", sa.Text(), nullable=False), sa.Column("alert_type", sa.Text(), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_alerts_symbol", "alerts", ["symbol"], unique=False)
    op.create_index("ix_alerts_timestamp", "alerts", ["timestamp"], unique=False)

    op.create_table("analytics", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("metric", sa.Text(), nullable=False), sa.Column("value", sa.Float(), nullable=False), sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_analytics_timestamp", "analytics", ["timestamp"], unique=False)


def downgrade() -> None:
    op.drop_table("analytics")
    op.drop_table("alerts")
    op.drop_table("trades")
    op.drop_table("signals")
    op.drop_table("futures_quotes")
    op.drop_table("options_chain")
    op.drop_table("market_prices")
