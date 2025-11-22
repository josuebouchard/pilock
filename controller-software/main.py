import time
from servo_lock import ServoLock
from pirc522 import RFID
import httpx
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
log = structlog.stdlib.get_logger()

http_client = httpx.Client(base_url="http://127.0.0.1:3000")

lock = ServoLock()
rdr = RFID(pin_irq=None)  # pyright: ignore[reportArgumentType]

# NFC Debounce logic
DEBOUNCE_SECONDS = 1.0  # Time to ignore the same card
last_seen: dict[str, float] = {}  # Track when each card was last seen


# NFC events
def on_NFC_tag_detected(hex_string_uid: str):
    nfc_log = log.bind(nfc_tag_uid=hex_string_uid)

    try:
        req = http_client.get(
            "/access/check",
            params={"tag_uid": hex_string_uid},
            timeout=2.0,  # Slow server cannot block system
        )
    except httpx.RequestError as exc:
        nfc_log.error(
            "HTTP request failed",
            error=str(exc),
        )
        return

    if req.is_error:
        nfc_log.error(
            "HTTP validation request error",
            status_code=req.status_code,
        )
        return

    response = req.json()

    nfc_log = nfc_log.bind(remote_access_log=response)

    if response.get("access_was_granted", False):
        lock.toggle()
        time.sleep(0.5)
        lock.detach()
        nfc_log.info("access granted", lock_state=lock.is_locked)
    else:
        nfc_log.info("access rejected", lock_state=lock.is_locked)


def main():
    log.info("system start-up")
    try:
        # Poll the NFC sensor
        while True:
            # rdr.wait_for_tag() # Optional, waits for interrupt trigger to continue
            (error, _tag_type) = rdr.request()
            if error:
                # No card is present
                continue

            # Try to get the UID
            (error, uid) = rdr.anticoll()
            if error:
                log.error("NFC anticollission error")
                continue

            # Convert UID to hex string
            hex_uid = bytearray(uid).hex()

            # Time based debouncing
            now = time.monotonic()
            if (now - last_seen.get(hex_uid, 0)) >= DEBOUNCE_SECONDS:
                # Action:
                on_NFC_tag_detected(hex_uid)
            last_seen[hex_uid] = now

            time.sleep(0.05)  # Prevent 100% CPU usage

    except KeyboardInterrupt:
        rdr.cleanup()
        log.info("system stop")


if __name__ == "__main__":
    main()
