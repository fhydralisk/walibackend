from base.exceptions import default_exception, Error500, Error404
from utils.usersid import user_from_sid
from usersys.models import UserBase, UserFeedback
from datetime import datetime
import random


def calc_reward(user, content, wechat_id):
    # type: (UserBase, str, str) -> float
    f_last = user.feedback.order_by('feedback_date').last()  # type: UserFeedback
    if f_last is not None and f_last.feedback_date.date() >= datetime.today().date():
        return 0.0
    
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
    new_f = UserFeedback.objects.create(
        uid=user,
        wechat_id=wechat_id,
        content=content,
        reward=calc_reward(user, content, wechat_id)
    )
    return new_f.reward
