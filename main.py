from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.fast_replyer import (keep_online, load_photos_dict, tg_app,
                              update_photos)

if __name__ == "__main__":
    load_photos_dict()
    scheduler = AsyncIOScheduler()

    # uncomment this in first start of program
    # scheduler.add_job(send_photos_to_fav, "interval", seconds=20)

    scheduler.add_job(update_photos, "interval", seconds=50)
    scheduler.add_job(keep_online, "interval", seconds=60*2)

    scheduler.start()
    tg_app.run()
