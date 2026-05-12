"""
Site Bot - Simulează un vizitator care stă pe site între 6 și 18 ore,
reintrand pe site o dată la random(1–6) minute.

Utilizare:
    python site_bot.py --url https://site-ul-tau.ro
    python site_bot.py --url https://site-ul-tau.ro --min-hours 6 --max-hours 18
"""

import time
import random
import argparse
import logging
from datetime import datetime, timedelta
import urllib.request
import urllib.error

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("site-bot")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",
]


def ping(url: str, ua: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            log.info("✅  HTTP %s  ←  %s", resp.status, url)
            return True
    except urllib.error.HTTPError as e:
        log.warning("⚠️  HTTP %s", e.code)
    except urllib.error.URLError as e:
        log.error("❌  Eroare: %s", e.reason)
    except Exception as e:
        log.error("❌  %s", e)
    return False


def run_bot(url: str, min_hours: float, max_hours: float):
    total_seconds = random.uniform(min_hours * 3600, max_hours * 3600)
    end_time      = datetime.now() + timedelta(seconds=total_seconds)

    log.info("🤖  Bot pornit | durată: %.1f ore | până la: %s",
             total_seconds / 3600, end_time.strftime("%H:%M:%S"))

    ping_count = 0

    while datetime.now() < end_time:
        ua = random.choice(USER_AGENTS)
        ping(url, ua)
        ping_count += 1

        # Pauză random între 1 și 6 minute
        pause = random.uniform(60, 360)
        next_ping = datetime.now() + timedelta(seconds=pause)

        if next_ping >= end_time:
            log.info("🏁  Timp expirat, opresc.")
            break

        remaining = (end_time - datetime.now()).total_seconds()
        log.info("💤  Pauză: %.0f sec  |  Timp rămas: %s  |  Ping-uri: %d",
                 pause,
                 str(timedelta(seconds=int(remaining))),
                 ping_count)
        time.sleep(pause)

    log.info("✔️   Terminat după %d ping-uri.", ping_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--min-hours", type=float, default=6.0)
    parser.add_argument("--max-hours", type=float, default=18.0)
    args = parser.parse_args()

    run_bot(url=args.url, min_hours=args.min_hours, max_hours=args.max_hours)
