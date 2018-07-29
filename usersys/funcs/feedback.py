from base.exceptions import default_exception, Error500, Error404
from utils.usersid import user_from_sid
from usersys.models import UserBase, UserFeedback
from datetime import datetime
import random


def calc_reward(user, content, wechat_id):
    # type: (UserBase, str, str) -> float
    if random.randint(1,100)<=95:
        return random.randrange(1000,2000)/100.0
    else:
        return random.randint(2000,10000)/100.0


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
    F,is_not_exited =  UserFeedback.objects.get_or_create(uid=user,wechat_id=wechat_id )
    F.content = content
    if not is_not_exited and F.feedback_date.date()==datetime.today().date():
        F.reward=0
        F.save()
    else:
        F.reward =calc_reward(user, content, wechat_id)
        F.save()
    return F.reward