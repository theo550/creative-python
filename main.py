import os
import j2l.pytactx.agent as pytactx
from getpass import getpass
import event

agent = pytactx.Agent(playerId=os.getenv('ROBOT_ID'),
                      arena=os.getenv('ARENA'),
                      username="demo",
                      password=os.getenv('PASSWORD'),
                      server="mqtt.jusdeliens.com",
                      verbosity=2)
event.subscribe(agent)

def moveTo(agentToMove, x,y):
  while not (agentToMove.x == x and agentToMove.y == y):
    agentToMove.moveTowards(x, y)
    agentToMove.update()

state = 'search'
enemyPosition = None
icp = 0
cp = [(5,5), (5,15), (15,15), (15,5)]


def doSearch(bot):
  if bot.distance > 0:
    global state
    state = 'attack'
    return

  bot.fire(False)
  global icp
  xCp = cp[icp][0]
  yCp = cp[icp][1]
  if not (bot.x == xCp and bot.y == yCp):
    bot.moveTowards(xCp, yCp)
  else:
    icp = (icp + 1) % len(cp)

  bot.setColor(0,255,0)


def doAttack(bot):
  bot.setColor(255,0,0)
  if bot.distance == 0:
    global state
    state = 'search'
    return

  bot.fire(True)


while True:
  if state == 'attack':
    doAttack(agent)
  elif state == 'search':
    doSearch(agent)

  agent.update()