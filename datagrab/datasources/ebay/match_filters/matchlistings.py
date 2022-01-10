from datagrab.datasources.ebay.match_filters.string_filters import split_words, remove_unicode


def match_search_strs(match_strings, listing_titles):
    """
    loop through a list of sets and check if for at least one set, every element of that set is present in the
    listing title
    :param match_strings: a list of sets each containing strings
    :param listing_titles:  a set containing each word in the listing title
    :return:
    """
    if any(all(data in listing_titles for data in search_str) for search_str in match_strings):
        return True
    else:
        return False


def match_storage_str(storage_str, listing):
    """
    :param storage_str: a string representing phone storage capacity i.e ("64gb", "128 gb")
    :param listing: a set containing each word in the listing title i.e {"Iphone", "128gb", "unlocked"}
    :return: True if the storage string (or all split elements of storage string) is/are in the listing title set
    """
    storage_strs = storage_str.split()
    if len(storage_strs) == 1:
        return storage_strs[0] in listing
    elif len(storage_strs) > 1:
        return all(strs in listing for strs in storage_strs)


def match_storage_size(match_data, listing_titles):
    """
    Check if the storage of the phone we are looking for matches the listing but not the other storage types
    :param match_data:a list representing phone storage capacity i.e (["64gb", "64 gb"])
    :param listing_titles: a set containing each word in the listing title i.e {"Iphone", "128gb", "unlocked"}
    :return:
    """
    if any(match_storage_str(storage_string, listing_titles) for storage_string in match_data['storage_strs']) and all(not match_storage_str(alt_storage, listing_titles)for alt_storage in match_data['alt_specs']):
        return True
    else:
        return False


def match_phone_listing(match_data, listing_title):
    """

        Matches a listing with the correct phone object by analyzing the listing title and comparing it with the name of the\
        Phone object
        :param listing_title: string of the listing name/title to be matched
        :param match_data: data (phone name, phone storage) representing the phone being matched to the listing
        :return:
        """
    is_a_match = False

    # remove unicodes in the listing title and split all the words
    listing_title = listing_title.lower()
    listing_title = remove_unicode(listing_title)
    listing_titles = split_words(listing_title)
    listing_titles = set(listing_titles)

    # each phone has a list of search strings that represent how they can be written "Samsung Galaxy S8 plus" and
    # "Samsung Galaxy S8+" for example represent the same phone. Split the words of each search string into sets and
    # add them to a list

    search_strs_list = []
    for search_strs in match_data['search_strs']:
        split_string = search_strs.lower().split()
        search_str_set = set(split_string)
        search_strs_list.append(search_str_set)

    # check if the phone has different storage sizes to check against that (make sure a 64gb phone isnt matched to
    # the same make but 128gb phone)
    if match_data['alt_specs']:
        is_a_match = match_search_strs(search_strs_list, listing_titles) and match_storage_size(match_data, listing_titles)
    else:
        is_a_match = match_search_strs(search_strs_list, listing_titles)

    return is_a_match
