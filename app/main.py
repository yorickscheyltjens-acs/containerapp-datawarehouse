import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging

from config import Config
from syncs import AdminpulseDocumentsSync

SYNC_MAPPINGS = {
    "AdminpulseDocuments": AdminpulseDocumentsSync
}


async def main():
    Config.check_environment_variables()

    sync = Config.SYNC
    if sync not in SYNC_MAPPINGS:
        raise Exception(f'Invalid SYNC value: {sync}')
    
    sync_instance = SYNC_MAPPINGS[sync]()
    await sync_instance.main()

    pass


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        force=True
    )
    asyncio.run(main())
