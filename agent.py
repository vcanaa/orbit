class Agent(object):
  def __init__(self, dt):
    self.dt = dt
    self.total = 0

  def update(self, state):
    self.total += self.dt

    if self.total < 0.5:
      return [1, 0.4]
    elif self.total < 1.0:
      return [1, -0.32]
    elif self.total < 1.8:
      return [1, 0]
    elif self.total < 4:
      return [0, 0]
    elif self.total < 5:
      return [0.2, 0]
    else:
    	return [0, 0]