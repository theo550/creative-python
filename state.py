
class IState:

  def do_action(self):
    ...

  def __str__(self) -> str:
    return 'IState'


class StateMachine:

  def __init__(self, initialState: IState) -> None:
    self.__state = initialState

  def set_state(self, State: IState):
    print('New State:', State)
    self.__state = State

  def do_action(self):
    if self.__state != None:
      self.__state.do_action()


class State(IState):

  def __init__(self, parentFSM: StateMachine) -> None:
    self._stateMachine = parentFSM

  def on_do_action(self):
    ...

  def do_action(self):
    self.on_do_action()

  def __str__(self):
    return "State"



