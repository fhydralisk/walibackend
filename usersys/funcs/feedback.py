from base.exceptions import default_exception, Error500, Error404
from utils.usersid import user_from_sid
from usersys.models import UserBase, UserFeedback


def calc_reward(user, content, wechat_id):
    # type: (UserBase, str, str) -> float

    # TODO: Calc the reward.
    return 0.0


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

    # TODO: Create UserFeedback Object

    # Calculate and return reward.

    return calc_reward(user, content, wechat_id)
