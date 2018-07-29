from django.db.models import QuerySet

from base.exceptions import default_exception, Error500, Error404
from utils.usersid import user_from_sid
from usersys.models import UserBase, UserFeedback
from datetime import datetime
import random


def calc_reward(user, content, wechat_id):
    # type: (UserBase, str, str) -> float
    f_set = UserFeedback.objects.filter(uid=user, wechat_id=wechat_id)  # type: QuerySet[UserFeedback]
    date_list = list(f_set.values_list("feedback_date", flat=True))
    for i in date_list:
        if i.date() == datetime.today().date():
            return 0
    if random.randint(1, 100) <= 95:
        return random.randrange(1000, 2000)/100.0
    else:
        return random.randint(2000, 10000)/100.0


@default_exception(Error500)
@user_from_sid(Error404)
def post_feedback(user, content, wechat_id):
    # type: (UserBase, str, str) -> float
    """

    :param user: The UserBase Object
    :param content: Feedback content
    :param wechat_id: Wechat id
    :return: Reward
    """
    new_f = UserFeedback.objects.create(uid=user, wechat_id=wechat_id, content=content)
    new_f.reward = calc_reward(user, content, wechat_id)
    new_f.save()
    return new_f.reward
