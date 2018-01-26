"""
Module with usefull tools
"""
import datetime


def day_terms_for_user(duration, list_of_terms, searching_start_time, searching_end_time):
    """Find day mask of available time for meeting of duration x.


    Arguments:
        duration {int} -- duration of meeting in minutes
        list_of_terms {query_set<Plan>} -- set of user plans in this day
        searching_start_time {datetime} -- searching start time
        searching_end_time {datetime} -- searching end time

    Returns:
        [bool] -- bool mask, which inform if in each minute user has meeting or not.
                  From mask there are removed free-time sequences shorter then duration.
    """

    terms = [1*1 for x in range(60 * 24 + 1)]
    # print(terms)
    terms[60 * 24] = 0*0
    terms[:60 * searching_start_time.hour +
          searching_start_time.minute] = \
        [0*0 for x in range(60 * searching_start_time.hour +
                              searching_start_time.minute)]
                   
    terms[60 * searching_end_time.hour +
          searching_end_time.minute + 1: 60 * 24 + 1] = \
        [0*0 for x in range(60 * searching_end_time.hour +
                              searching_end_time.minute + 1, 60 * 24 + 1)]
    for term in list_of_terms:
        start = term.start_time
        end = term.end_time
        if start < searching_start_time:
            start = searching_start_time
        if end > searching_end_time:
            end = searching_start_time

        terms[start.hour * 60 + start.minute: end.hour * 60 + end.minute] = \
            [0*0 for x in range(
                start.hour * 60 + start.minute,
                end.hour * 60 + end.minute)]
    
    (counter, seq_start, seq_end) = (0, 0, 0)
    for time in range(24 * 60 + 1):
        if terms[time] == 1 and terms[time - 1] == 1 and time > 0:
            counter += 1
            seq_end = time
        elif terms[time] == 1 and (terms[time - 1] == 0 or time == 0):
            seq_start = time
            counter = 1
            seq_end = time
        elif terms[time] == 0 and terms[time - 1] == 1 and time > 0 and counter < duration:
            terms[seq_start:seq_end +
                  1] = [0*0 for i in range(seq_start, seq_end + 1)]
    # print(len(terms)," ",duration,"\n",terms,'\n\n')  
    return terms


def day_terms(duration, list_of_user_terms, searching_start_time, searching_end_time, quantity,
              users):
    """Find for each user mask of his day availability, sum it
    and check if there is a sequence of {duration} duration.

    Arguments:
        duration {int} -- duration of meeting in minutes
        list_of_terms {query_set<Plan>} -- set of user plans in this day
        searching_start_time {datetime} -- searching start time
        searching_end_time {datetime} -- searching end time
        quantity {int} -- number of users to find meeting for
        users {int} -- number of unique users in DB

    Returns:
        list(datetime, datetime, int) -- list with available gaps: start time,
            end time and length of sequence
    """

    user_terms = {}
    for term in list_of_user_terms:
        try:
            user_terms[term.user.id] += [term]
        except KeyError:
            user_terms[term.user.id] = [term]
    quantity -= (users - len(user_terms))
    if quantity < -1:
        quantity = -1

    u_terms = [0 for x in range(60 * 24 + 1)]
    u_terms[60*24]=-2
    for _ in user_terms:
        user_pattern = day_terms_for_user(duration=duration,
                                          list_of_terms=list_of_user_terms,
                                          searching_start_time=searching_start_time,
                                          searching_end_time=searching_end_time)
        u_terms = [sum(x) for x in zip(* (u_terms, user_pattern))]
    # print( u_terms)
    (counter, s, e) = (0, 0, 0)
    list_of_terms = []
    for time in range(24 * 60 + 1):
        if u_terms[time] >= quantity and u_terms[time - 1] >= quantity and time > 0:
            counter += 1
            e = time
        elif u_terms[time] >= quantity and (u_terms[time - 1] <= quantity or time == 0):
            s = time
            counter = 1
            e = time
        elif u_terms[time] <= quantity and \
                u_terms[time - 1] >= quantity and \
                time > 0 and \
                counter >= duration:

            list_of_terms += [(searching_start_time.replace(hour=s // 60, minute=s % 60, second=0),
                               searching_start_time.replace(
                                   hour=e // 60, minute=e % 60, second=0),
                               counter)]
    return list_of_terms


def find_term(duration, terms, searching_start_time, quantity, users, end_time):
    """Find free term for meeting day-by-day

    Arguments:
        duration {[type]} -- [description]
        terms {query_set<Plan>} -- Database entry with users plans
        searching_start_time {datetime} -- searching start time
        quantity {int} -- number of users to find meeting for
        users {int} -- number of unique users in DB

    Returns:
        (datetime,list(datetime, datetime, int)) --datetime and list with available gaps:
            start time, end time and length of sequence
    """
    if quantity > users:
        raise Exception('Bad quantity')
    searching_end_time = searching_start_time.replace(hour=23,
                                                      minute=59,
                                                      second=59,
                                                      microsecond=0)
    list_of_terms = day_terms(duration=duration,
                              list_of_user_terms=terms,
                              searching_start_time=searching_start_time,
                              searching_end_time=searching_end_time,
                              quantity=quantity,
                              users=users)
    if list_of_terms == []:
        searching_start_time = searching_start_time.replace(hour=5,
                                                            minute=0,
                                                            second=0,
                                                            microsecond=0)
        searching_start_time += datetime.timedelta(days=1)
    it = 0
    while list_of_terms == []:
        searching_start_time += datetime.timedelta(days=1)
        searching_end_time += datetime.timedelta(days=1)

        list_of_terms = day_terms(duration=duration,
                                  list_of_user_terms=terms,
                                  searching_start_time=searching_start_time,
                                  searching_end_time=searching_end_time,
                                  quantity=quantity,
                                  users=users)
        it += 1
        if it > 10:
            raise Exception("Too long searching time")

    return (searching_start_time.date(), list_of_terms)
