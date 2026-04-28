"""
Stock/ETF provider — yfinance library (Yahoo Finance, free, no key required).
https://pypi.org/project/yfinance/
"""

import logging
from datetime import datetime, timezone

from .config import ETFS

logger = logging.getLogger(__name__)

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


def get_stocks() -> str:
    """Fetch ETF quotes using yfinance and return HTML table rows."""
    if not HAS_YFINANCE:
        logger.warning("yfinance not installed, using fallback")
        return _stock_fallback()

    rows = []
    try:
        tickers = yf.Tickers(" ".join(ETFS))
        for symbol in ETFS:
            try:
                ticker = tickers.tickers[symbol]
                info = ticker.fast_info
                price = info.last_price
                prev = info.previous_close
                if price and prev:
                    change = price - prev
                    pct = (change / prev) * 100
                    arrow = "🟢" if change >= 0 else "🔴"
                    change_str = f"+{change:.2f}" if change >= 0 else f"{change:.2f}"
                    pct_str = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"
                else:
                    arrow, change_str, pct_str = "⚪", "N/A", "N/A"
                    price = "N/A"
                try:
                    trade_ts = info.regularMarketTime
                    if trade_ts is not None:
                        if isinstance(trade_ts, datetime):
                            trade_dt = trade_ts.astimezone(timezone.utc)
                        else:
                            trade_dt = datetime.fromtimestamp(float(trade_ts), tz=timezone.utc)
                        as_of = trade_dt.strftime('%d %b %Y, %H:%M UTC')
                    else:
                        as_of = datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
                except Exception:
                    as_of = datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
                rows.append(
                    f"<tr>"
                    f"<td><b>{symbol}</b></td>"
                    f"<td>{price if isinstance(price, str) else f'{price:.2f}'}</td>"
                    f"<td>{arrow} {change_str}</td>"
                    f"<td>{pct_str}</td>"
                    f"<td>{as_of}</td>"
                    f"</tr>"
                )
            except Exception as exc:
                logger.warning("Failed to fetch %s: %s", symbol, exc)
                rows.append(
                    f"<tr>"
                    f"<td><b>{symbol}</b></td>"
                    f"<td colspan='4'>Data unavailable</td>"
                    f"</tr>"
                )
    except Exception as exc:
        logger.error("Failed to fetch stock data: %s", exc)
        return _stock_fallback()
    return "\n".join(rows) if rows else _stock_fallback()


def _stock_fallback() -> str:
    """Return one fallback <tr> row per ETF when stock APIs are unavailable."""
    rows = []
    for ticker in ETFS:
        rows.append(
            f"<tr>"
            f"<td><b>{ticker}</b></td>"
            f"<td colspan='4'>Market data temporarily unavailable</td>"
            f"</tr>"
        )
    return "\n".join(rows)
