import time, random, argparse, logging, json, os
from datetime import datetime, timedelta
import urllib.request, urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger("site-bot")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",
]

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"history": []}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

def ping(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            log.info("✅  HTTP %s  ←  %s", resp.status, url)
            return True
    except Exception as e:
        log.error("❌  %s", e)
        return False

def run_bot(url, min_hours, max_hours):
    stats = load_stats()
    total_seconds = random.uniform(min_hours * 3600, max_hours * 3600)
    end_time = datetime.utcnow() + timedelta(seconds=total_seconds)
    start_time = datetime.utcnow()
    ping_count = 0
    pauses = []

    log.info("🤖  Bot pornit | durată: %.1f ore", total_seconds / 3600)

    # Marchează ca activ
    stats["status"] = "active"
    stats["last_start"] = start_time.isoformat() + "Z"
    stats["url"] = url
    stats["duration_hours"] = round(total_seconds / 3600, 2)
    stats["min_interval_sec"] = 60
    stats["max_interval_sec"] = 360
    save_stats(stats)

    while datetime.utcnow() < end_time:
        ua = random.choice(USER_AGENTS)
        success = ping(url, ua)
        if success:
            ping_count += 1

        pause = random.uniform(60, 360)
        pauses.append(round(pause))
        next_ping = datetime.utcnow() + timedelta(seconds=pause)

        if next_ping >= end_time:
            break

        remaining = (end_time - datetime.utcnow()).total_seconds()
        log.info("💤  Pauză: %.0f sec | Rămas: %s | Vizite: %d",
                 pause, str(timedelta(seconds=int(remaining))), ping_count)
        time.sleep(pause)

    # Salvează run-ul în history
    run_entry = {
        "date": start_time.strftime("%Y-%m-%d"),
        "start": start_time.isoformat() + "Z",
        "end": datetime.utcnow().isoformat() + "Z",
        "duration_hours": round(total_seconds / 3600, 2),
        "visits": ping_count,
        "avg_interval_sec": round(sum(pauses) / len(pauses)) if pauses else 0,
    }

    stats["status"] = "inactive"
    stats["last_end"] = datetime.utcnow().isoformat() + "Z"
    stats["last_visits"] = ping_count
    stats["history"] = [run_entry] + stats.get("history", [])
    stats["history"] = stats["history"][:30]  # păstrează ultimele 30 zile
    save_stats(stats)

    log.info("✔️   Terminat după %d vizite.", ping_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--min-hours", type=float, default=6.0)
    parser.add_argument("--max-hours", type=float, default=18.0)
    args = parser.parse_args()
    run_bot(url=args.url, min_hours=args.min_hours, max_hours=args.max_hours)
