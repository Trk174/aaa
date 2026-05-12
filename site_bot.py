"""
Site Bot - Simulează un vizitator care stă pe site între 6 și 18 ore.
Trimite request-uri periodice pentru a menține "prezența" activă.

Utilizare locală:
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

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("site-bot")

# ── User-agents realistici ──────────────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
]


def ping(url: str, ua: str) -> bool:
    """Trimite un GET request la URL și returnează True dacă reușește."""
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            log.info("✅  %s  →  HTTP %s", url, resp.status)
            return True
    except urllib.error.HTTPError as e:
        log.warning("⚠️  HTTP %s la %s", e.code, url)
    except urllib.error.URLError as e:
        log.error("❌  Eroare rețea: %s", e.reason)
    except Exception as e:
        log.error("❌  Eroare neașteptată: %s", e)
    return False


def human_pause() -> float:
    """
    Pauză realistă între ping-uri: între 45 sec și 8 minute,
    cu o distribuție mai naturală (nu uniform).
    """
    base = random.gauss(mu=150, sigma=60)   # medie ~2.5 min
    return max(45, min(480, base))          # clamp 45s – 8min


def run_bot(url: str, min_hours: float, max_hours: float):
    total_seconds = random.uniform(min_hours * 3600, max_hours * 3600)
    end_time      = datetime.now() + timedelta(seconds=total_seconds)
    ua            = random.choice(USER_AGENTS)

    log.info("🤖  Bot pornit pentru URL: %s", url)
    log.info("⏱️   Durată aleasă: %.1f ore  (până la %s)",
             total_seconds / 3600, end_time.strftime("%H:%M:%S"))
    log.info("🖥️   User-Agent: %s", ua[:60] + "…")

    ping_count = 0

    while datetime.now() < end_time:
        remaining = (end_time - datetime.now()).total_seconds()
        log.info("⏳  Timp rămas: %s", str(timedelta(seconds=int(remaining))))

        ping(url, ua)
        ping_count += 1

        # Schimbă user-agent din când în când
        if random.random() < 0.1:
            ua = random.choice(USER_AGENTS)
            log.info("🔄  User-Agent schimbat")

        pause = human_pause()
        next_ping = datetime.now() + timedelta(seconds=pause)

        if next_ping >= end_time:
            log.info("🏁  Aproape de final, opresc.")
            break

        log.info("💤  Pauză: %.0f sec  (next ping ~%s)",
                 pause, next_ping.strftime("%H:%M:%S"))
        time.sleep(pause)

    log.info("✔️   Bot terminat după %d ping-uri.", ping_count)


# ── CLI ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bot care stă pe un site un timp random."
    )
    parser.add_argument(
        "--url", required=True,
        help="URL-ul site-ului (ex: https://example.com)"
    )
    parser.add_argument(
        "--min-hours", type=float, default=6.0,
        help="Minim ore de stat pe site (default: 6)"
    )
    parser.add_argument(
        "--max-hours", type=float, default=18.0,
        help="Maxim ore de stat pe site (default: 18)"
    )
    args = parser.parse_args()

    run_bot(url=args.url, min_hours=args.min_hours, max_hours=args.max_hours)
