"""
State machine utility


"""


class StateMachine(object):
    STATE_MACHINE_DEFINE = {}

    K_STATES = "states"
    K_ACTIONS = "actions"
    K_STATE_GRAPH = "state graph"
    K_TRANSITIONS = "transitions"
    K_NEXT_STATE = "next state"
    K_PRE_SE = "side effect pre"
    K_POST_SE = "side effect post"
    K_SE_CONTEXT = "side effect context"
    K_SE_EXCEPTION_HANDLER = "side effect exception handler"

    class StateDoesNotExist(Exception):
        pass

    class ActionError(Exception):
        pass

    @staticmethod
    def zip_ctx(list_se, ctx):
        return [(se, ctx) for se in list_se]

    def get_state_dict(self, state):
        try:
            return self.STATE_MACHINE_DEFINE[self.K_STATE_GRAPH][state]
        except KeyError:
            raise self.StateDoesNotExist

    def next_state_action(self, current_state, action):
        state_dict = self.get_state_dict(current_state)

        try:
            action = state_dict[self.K_TRANSITIONS][action]
        except KeyError:
            raise self.ActionError

        if self.K_NEXT_STATE not in action:
            raise KeyError

        return action

    def na_and_se(self, current_state, action):
        """

        :param current_state:
        :param action:
        :return:
        """

        action_dict = self.next_state_action(current_state, action)

        next_state = action_dict[self.K_NEXT_STATE]
        try:
            next_state_dict = self.get_state_dict(next_state)
        except self.StateDoesNotExist:
            next_state_dict = {}

        ctx_src = action_dict.get(self.K_SE_CONTEXT, None)
        ctx_dst = next_state_dict.get(self.K_SE_CONTEXT, None)
        ctx_sm = self.STATE_MACHINE_DEFINE.get(self.K_SE_CONTEXT, None)

        pre_se = (
                self.zip_ctx(self.STATE_MACHINE_DEFINE.get(self.K_PRE_SE, []), ctx_sm) +
                self.zip_ctx(action_dict.get(self.K_PRE_SE, []), ctx_src) +
                self.zip_ctx(next_state_dict.get(self.K_PRE_SE, []), ctx_dst)
        )

        post_se = (
                self.zip_ctx(next_state_dict.get(self.K_POST_SE, []), ctx_dst) +
                self.zip_ctx(action_dict.get(self.K_POST_SE, []), ctx_src) +
                self.zip_ctx(self.STATE_MACHINE_DEFINE.get(self.K_POST_SE, []), ctx_sm)
        )

        return (
            next_state,
            pre_se,
            post_se,
        )

    def _execute_transition(self, pre_se, post_se, state_dealer, current_state, state_next, action, extra_ctx):
        current_func = None
        try:
            for se, ctx in pre_se:
                current_func = se
                se(current_state=current_state, action=action, ctx=ctx, extra_ctx=extra_ctx)

            if state_dealer is not None:
                current_func = state_dealer
                state_dealer(current_state=current_state, state_next=state_next, action=action, extra_context=extra_ctx)

            for se, ctx in post_se:
                current_func = se
                se(current_state=current_state, action=action, ctx=ctx, extra_ctx=extra_ctx)

            return state_next
        except Exception as e:
            handler = self.STATE_MACHINE_DEFINE.get(self.K_SE_EXCEPTION_HANDLER, None)
            if handler is None:
                raise
            else:
                handler(
                    current_state=current_state,
                    state_next=state_next,
                    action=action,
                    extra_context=extra_ctx,
                    exc=e,
                    current_func=current_func
                )

    def execute_transition(self, current_state, action, extra_ctx, state_dealer=None):
        state_next, pre_se, post_se = self.na_and_se(current_state, action)
        self._execute_transition(pre_se, post_se, state_dealer, current_state, state_next, action, extra_ctx)

    def start_sm(self, init_state, extra_ctx, state_dealer=None):
        state_dict = self.get_state_dict(init_state)
        ctx = state_dict.get(self.K_SE_CONTEXT, None)
        ctx_sm = self.STATE_MACHINE_DEFINE.get(self.K_SE_CONTEXT, None)
        pre_se = (
                self.zip_ctx(self.STATE_MACHINE_DEFINE.get(self.K_PRE_SE, []), ctx_sm) +
                self.zip_ctx(state_dict.get(self.K_PRE_SE, []), ctx)
        )
        post_se = (
                self.zip_ctx(state_dict.get(self.K_POST_SE, []), ctx) +
                self.zip_ctx(self.STATE_MACHINE_DEFINE.get(self.K_POST_SE, []), ctx_sm)
        )
        self._execute_transition(pre_se, post_se, state_dealer, None, init_state, None, extra_ctx)
