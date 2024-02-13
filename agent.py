from state import StateMachine, State
import j2l.pytactx.agent as pytactx
from getpass import getpass

class AgentState(State):
  icp = 0
  cp = [(5, 5), (5, 15), (15, 15), (15, 5)]

  def __init__(self, parentFSM: StateMachine, agent: pytactx.IAgent) -> None:
    super().__init__(parentFSM)
    self._agent = agent
    
  def do_action(self):
    self.on_do_action()

  def on_do_action(self):
    ...

  def to_move(self):
    xCp, yCp = AgentState.cp[AgentState.icp]
    if not (self._agent.x == xCp and self._agent.y == yCp):
      self._agent.moveTowards(xCp, yCp)
    else:
      AgentState.icp = (AgentState.icp + 1) % len(AgentState.cp)

  def __str__(self):
    return 'AgentState'


class AttackState(AgentState):

  def __init__(self, parentFSM: StateMachine, agent: pytactx.IAgent) -> None:
    super().__init__(parentFSM, agent)
    self.__parentFSM = parentFSM
    self.__xEnemy = 0
    self.__yEnemy = 0

  def on_do_action(self):
    if len(self._agent.range) > 0:
      for enemyName, enemyAttribute in self._agent.range.items():
        self.__xEnemy, self.__yEnemy = enemyAttribute["x"], enemyAttribute["y"]
        self._agent.fire(True)
        break
    if self._agent.x == self.__xEnemy and self._agent.y == self.__yEnemy:
      self._stateMachine.set_state(SearchState(self._stateMachine, self._agent))
      return
    self._agent.setColor(255, 0, 0)
    self._agent.moveTowards(self.__xEnemy, self.__yEnemy)
    self._agent.fire(True)
    

  def __str__(self):
    return 'AttackState'


class SearchState(AgentState):

  def __init__(self, parentFSM: StateMachine, agent: pytactx.IAgent) -> None:
    super().__init__(parentFSM, agent)
    self.icp = 0

  def on_do_action(self):
    if self._agent.distance > 0:
      self._stateMachine.set_state(AttackState(self._stateMachine, self._agent))
      return
    self._agent.fire(False)
    self.to_move()
    self._agent.setColor(0, 255, 0)

  def __str__(self):
    return 'SearchState'


class SpecialAgent(pytactx.Agent):

  def __init__(self, playerId="") -> None:
    super().__init__(playerId, arena="LaTerreDuMilieu", username="demo", password=getpass("🔑 password: "), server="mqtt.jusdeliens.com", verbosity=2)
    self.__fsm = StateMachine(None)
    self.__fsm.set_state(SearchState(self.__fsm, self))

  def on_update(self):
    self.update()
    self.__fsm.do_action()
