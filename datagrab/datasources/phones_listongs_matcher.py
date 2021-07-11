import re


def match_phone_listing(search_data, listing):
    """

    :param search_data:
    :param listing:
    :return:
    """
    match = False

    listing_titles = listing["title"].lower()
    try:
        listing_titles = re.split(r',|_|-|!|\\| |\(|\)|/|\[|\]|\|', listing_titles)
    except:
        listing_titles = re.split(', |_|-|!| ', listing_titles)

    listing_titles = set(listing_titles)

    search_str_set = list()
    for search_str in search_data['search_strs']:
        search_str_set.append(search_str.lower().split())

    if len(search_data['alt_specs']) > 0:
        if any(all(data in listing_titles for data in search_str) for search_str in search_str_set) and (f'{search_data["specs"]}'.replace(" ", "").lower() in listing_titles) and (all(f'{x}'.replace(" ", "").lower() not in listing_titles for x in search_data['alt_specs'])):
            match = True
        else:
            match = False
    else:
        if any(all(data in listing_titles for data in search_str) for search_str in search_str_set):
            match = True
        else:
            match = False
    return match