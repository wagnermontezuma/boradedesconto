async with semaphore(3):
    retry(..., wait=exponential):
        get_offers(merchant)
