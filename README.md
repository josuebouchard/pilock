# PiLock

## Abstract

PiLock addresses a practical problem faced in shared workspaces: ensuring that valuable resources can be accessed quickly by trusted users while still maintaining accountability. By integrating an NFC reader, a simple servo-based lock, and a Raspberry Pi running a Python web application, the system provides a balance between accessibility and oversight. Key functions such as access control, logging, and return tracking are combined with a user-friendly web interface for managers, ensuring that the system is both functional and easy to administer.

While the current design emphasizes affordability and proof-of-concept implementation, PiLock demonstrates how relatively simple hardware and open-source software can replace manual supervision with an automated, reliable process. Future improvements could include support for more secure NFC standards, encrypted communication between modules, or offloading the computing side to the cloud for centralized monitoring.

## Report

The full final report can be [read here](/final_report.pdf).

## Running the code

In all cases it requires that you are placed on the corresponding folder.

### Controller software

```bash
uv run main.py
```

### Management web server

```bash
# Web Interface Server
uv run uvicorn app.main:app --host=0.0.0.0 --port=8080

# Controller API
uv run uvicorn app.controller_api:app --host=127.0.0.1 --port=3000
```