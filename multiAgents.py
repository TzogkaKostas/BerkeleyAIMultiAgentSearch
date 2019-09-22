# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys
from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"
		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		currPos = currentGameState.getPacmanPosition()
		currFood = currentGameState.getFood()
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		caps_score = 0
		for capsule in currentGameState.getCapsules(): 
			if capsule == newPos:
				caps_score = 10
		if not newFood.asList(): #this means win,so always go there
			return 100

		dist_list = []
		for agent in newGhostStates:
			ghost_pos = agent.getPosition()
			m_dist = abs(newPos[0] - ghost_pos[0]) + abs(newPos[1] - ghost_pos[1])
			dist_list.append(m_dist)
		avg = sum(dist_list)/float(len(dist_list))

		dist_list2 = []
		for food_pos in newFood.asList():
			m_dist2 = abs(newPos[0] - food_pos[0]) + abs(newPos[1] - food_pos[1])
			dist_list2.append(m_dist2)
		
		min_food_dist = -10*min(dist_list2)

		if currFood[newPos[0]][newPos[1]]:
			min_food_dist = 0

		
		return 0.1*min_food_dist + 0.9*avg + 1*caps_score
		"*** YOUR CODE HERE ***"
		return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluations function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""
	def minimax_decision(self,gameState,numAgents,depth):
		value_dic = dict()
		for a in gameState.getLegalActions(0):
			next_state = gameState.generateSuccessor(0,a)
			value_dic[a] = self.Min_Value(next_state,1,numAgents,depth)
		#print "dic:",value_dic

		min_val = max( value_dic.values() )
		for action,value in value_dic.items():
			if value == min_val:
				#print "action:",action
				return action

	def Max_Value(self,gameState,numAgents,depth):
		if gameState.isWin() or gameState.isLose() or depth == 0:
			return self.evaluationFunction(gameState)
		v = -sys.maxint-1
		for a in gameState.getLegalActions(0):
			next_state = gameState.generateSuccessor(0,a)
			v = max(v,self.Min_Value(next_state,1,numAgents,depth))
		return v

	def Min_Value(self,gameState,myid,numAgents,depth):
		if gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		v = sys.maxint
		for a in gameState.getLegalActions(myid):
			next_state = gameState.generateSuccessor(myid,a)
			if myid	== numAgents-1:
				v = min(v,self.Max_Value(next_state,numAgents,depth-1))
			else:
				v = min(v,self.Min_Value(next_state,myid+1,numAgents,depth))
		return v

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.
		  Here are some method calls that might be useful when implementing minimax.
		  #	Returns a list of legal actions for an agent
		  #agentIndex=0 means Pacman, ghosts are >= 1
		"""
		#actions = gameState.getLegalActions(j)
		#gameState.generateSuccessor(agentIndex, self,action):
		#Returns the successor game state after an agent takes an action

		numAgents = gameState.getNumAgents()
		return self.minimax_decision(gameState,numAgents,self.depth)
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""
	def alpha_beta(self,gameState,numAgents,depth):
		value_dic = dict()
		a = -sys.maxint-1
		b = sys.maxint
		for action in gameState.getLegalActions(0):
			next_state = gameState.generateSuccessor(0,action)
			v = self.Min_Value_ab(next_state,1,numAgents,depth,a,b)
			value_dic[action] = v
			if v > b:
				return v
			a = max(a,v)

		min_val = max( value_dic.values() )
		for action,value in value_dic.items():
			if value == min_val:
				return action

	def Max_Value_ab(self,gameState,numAgents,depth,a,b):
		if gameState.isWin() or gameState.isLose() or depth == 0:
			return self.evaluationFunction(gameState)
		v = -sys.maxint-1
		for action in gameState.getLegalActions(0):
			next_state = gameState.generateSuccessor(0,action)
			v = max(v,self.Min_Value_ab(next_state,1,numAgents,depth,a,b))
			if v > b:
				return v
			a = max(a,v)
		return v

	def Min_Value_ab(self,gameState,myid,numAgents,depth,a,b):
		if gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		v = sys.maxint
		for action in gameState.getLegalActions(myid):
			next_state = gameState.generateSuccessor(myid,action)
			if myid	== numAgents-1:
				v = min(v,self.Max_Value_ab(next_state,numAgents,depth-1,a,b))
			else:
				v = min(v,self.Min_Value_ab(next_state,myid+1,numAgents,depth,a,b))
			if v < a :
				return v
			b = min(b,v)
		return v

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		numAgents = gameState.getNumAgents()
		return self.alpha_beta(gameState,numAgents,self.depth) 
		util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""
	def expectimax(self,gameState,numAgents,depth):
		value_dic = dict()
		for a in gameState.getLegalActions(0):
			next_state = gameState.generateSuccessor(0,a)
			value_dic[a] = self.expecti_min_value(next_state,1,numAgents,depth)

		min_val = max( value_dic.values() )
		for action,value in value_dic.items():
			if value == min_val:
				return action

	def expecti_max_value(self,gameState,numAgents,depth):
		if gameState.isWin() or gameState.isLose() or depth == 0:
			return self.evaluationFunction(gameState)
		v = -sys.maxint-1
		for a in gameState.getLegalActions(0):
			next_state = gameState.generateSuccessor(0,a)
			v = max(v,self.expecti_min_value(next_state,1,numAgents,depth))
		return v

	def expecti_min_value(self,gameState,myid,numAgents,depth):
		if gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		v = 0
		legal_actions = gameState.getLegalActions(myid)
		p = 1.0/len(legal_actions)
		for a in legal_actions:
			next_state = gameState.generateSuccessor(myid,a)
			if myid	== numAgents-1:
				v = v + p*self.expecti_max_value(next_state,numAgents,depth-1)
			else:
				v = v + p*self.expecti_min_value(next_state,myid+1,numAgents,depth)
		return v

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		numAgents = gameState.getNumAgents()
		return self.expectimax(gameState,numAgents,self.depth)
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	currPos = currentGameState.getPacmanPosition()
	currFood = currentGameState.getFood()
	GhostStates = currentGameState.getGhostStates()	

	if currentGameState.isWin() == True:
		score = sys.maxint
	elif currentGameState.isLose() == True:
		score = -sys.maxint-1
	else:
		capsules_list = currentGameState.getCapsules()
		caps_dist_list = []
		caps_dist = 0
		for c in capsules_list:
			caps_dist_list.append(manhattanDistance(c,currPos))
		if len(capsules_list) != 0:
			caps_score = 1.0/(len(capsules_list))  #number of capsules
			caps_dist_score = 1.0/(sum(caps_dist_list)/float(len(capsules_list)))
		else:				#average distance from capsules
			caps_dist_score = 0
			caps_score = 0


		dist_list = []
		for agent in GhostStates:
			ghost_pos = agent.getPosition()
			m_dist = manhattanDistance(ghost_pos,currPos)
			dist_list.append(m_dist)
		avg_ghost_score = ( sum(dist_list)/float(len(dist_list)) )**2
									#average distance from ghost

		dist_list2 = []
		for food_pos in currFood.asList():
			m_dist2 = manhattanDistance(food_pos,currPos)
			dist_list2.append(m_dist2)


		if (len(dist_list2) != 0):
			min_food_dist = 1.0/(min(dist_list2)) #minimum distance from foods.
		else:
			min_food_dist = 0

		num_food_score =  1.0/(currentGameState.getNumFood()) #number of foods.

		score = 1000000.0*num_food_score + 1000.0*min_food_dist + 10000000.0*caps_score + 1*avg_ghost_score+1*caps_dist_score
	return score
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
