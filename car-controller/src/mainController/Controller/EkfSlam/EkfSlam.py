"""
Extended Kalman Filter SLAM example

author: Atsushi Sakai (@Atsushi_twi)
"""
import math
import numpy as np

# EKF state covariance
Cx = np.diag([0.5, 0.5, np.deg2rad(30.0)]) ** 2

M_DIST_TH = 0.2  # Threshold of Mahalanobis distance for data association.
STATE_SIZE = 3  # State size [x,y,yaw]
LM_SIZE = 2  # LM state size [x,y]

class EKFSlam():

    def __init__(self):
        self.reset()

    def reset(self):
        self.helpDataStructure = np.eye(3)
        self.positionState = np.zeros((3, 1))
        self.observationIDS = []

    def update(self, robotPositonUpdate, observaitons):
        self.positionState, self.helpDataStructure, self.observationIDS = ekf_slam(self.positionState, self.helpDataStructure, robotPositonUpdate, observaitons)

    def getRobotPosition (self):
        return self.positionState[0:3].reshape((3))

    def getLandmarkPositions(self):
        return self.positionState[3:].reshape((-1,2))

    def getOberservationIDs(self):
        return self.observationIDS

    def deleteNearestLandmark(self,x,y):
        landmarkID = self.getNearestLandmark(x,y)
        self.deleteLandmarkID(landmarkID)

    def getNearestLandmark(self, x, y):
        landmarkID = search_correspond_landmark_id(self.positionState, self.helpDataStructure, np.array([x,y]), False)
        return landmarkID

    def deleteLandmarkID(self, landmarkID):
        startIndex = STATE_SIZE+LM_SIZE*landmarkID
        endIndex = startIndex + LM_SIZE
        deleteRange = np.arange(startIndex,endIndex)


        self.positionState = np.delete(self.positionState, deleteRange, 0)
        self.helpDataStructure =  np.delete(self.helpDataStructure, deleteRange, 0)
        self.helpDataStructure =  np.delete(self.helpDataStructure, deleteRange, 1)

    def getCountOfLandmarks(self):
        return calc_n_lm(self.positionState)



def ekf_slam(positonEstablisched, helpDataStructure, robotPositonDelta, observation):

    # Predict
    S = STATE_SIZE
    positonEstablisched[0:S] = motion_model(positonEstablisched[0:S], robotPositonDelta)
    G, Fx = jacob_motion(positonEstablisched[0:S], robotPositonDelta)
    helpDataStructure[0:S, 0:S] = G.T @ helpDataStructure[0:S, 0:S] @ G + Fx.T @ Cx @ Fx
    initP = np.eye(2)
    landmarkIDs = []

    # Update
    for iz in range(observation.shape[0]):  # for each observation

        min_id = search_correspond_landmark_id(positonEstablisched, helpDataStructure, observation[iz, 0:2])
        landmarkIDs.append(min_id)

        nLM = calc_n_lm(positonEstablisched)
        if min_id == nLM:
            print("New LM")
            # Extend state and covariance matrix
            xAug = np.vstack((positonEstablisched, calc_landmark_position(positonEstablisched, observation[iz, 0:2])))
            PAug = np.vstack((np.hstack((helpDataStructure, np.zeros((len(positonEstablisched), LM_SIZE)))),
                              np.hstack((np.zeros((LM_SIZE, len(positonEstablisched))), initP))))
            positonEstablisched = xAug
            helpDataStructure = PAug
        lm = get_landmark_position_from_state(positonEstablisched, min_id)
        y, S, H = calc_innovation(lm, positonEstablisched, helpDataStructure, observation[iz, 0:2], min_id)

        K = (helpDataStructure @ H.T) @ np.linalg.inv(S)
        positonEstablisched = positonEstablisched + (K @ y)
        helpDataStructure = (np.eye(len(positonEstablisched)) - (K @ H)) @ helpDataStructure

    positonEstablisched[2] = pi_2_pi(positonEstablisched[2])

    return positonEstablisched, helpDataStructure, landmarkIDs


def motion_model(robotPosition, robotPositonDelta):
    F = np.eye(3)

    B = np.array([[math.cos(robotPosition[2, 0]), 0],
                  [math.sin(robotPosition[2, 0]), 0],
                  [0.0, 1]])

    newRobotPosition = (F @ robotPosition) + (B @ robotPositonDelta)
    return newRobotPosition


def calc_n_lm(x):
    n = int((len(x) - STATE_SIZE) / LM_SIZE)
    return n


def jacob_motion(robotPosition, robotPositonDelta):
    Fx = np.hstack((np.eye(STATE_SIZE), np.zeros((STATE_SIZE, LM_SIZE * calc_n_lm(robotPosition)))))

    jF = np.array([[0.0, 0.0, (-robotPositonDelta[0] * math.sin(robotPosition[2, 0]))[0]],
                   [0.0, 0.0, (robotPositonDelta[0] * math.cos(robotPosition[2, 0]))[0]],
                   [0.0, 0.0, 0.0]])

    G = np.eye(STATE_SIZE) + Fx.T @ jF @ Fx

    return G, Fx,


def calc_landmark_position(x, observation):
    zp = np.zeros((2, 1))

    zp[0, 0] = x[0, 0] + observation[0] * math.cos(x[2, 0] + observation[1])
    zp[1, 0] = x[1, 0] + observation[0] * math.sin(x[2, 0] + observation[1])

    return zp


def get_landmark_position_from_state(x, ind):
    lm = x[STATE_SIZE + LM_SIZE * ind: STATE_SIZE + LM_SIZE * (ind + 1), :]

    return lm


def search_correspond_landmark_id(xAug, PAug, zi, addMinDistance = True):
    """
    Landmark association with Mahalanobis distance
    """

    nLM = calc_n_lm(xAug)

    min_dist = []

    for i in range(nLM):
        lm = get_landmark_position_from_state(xAug, i)
        y, S, H = calc_innovation(lm, xAug, PAug, zi, i)
        min_dist.append(y.T @ np.linalg.inv(S) @ y)

    if addMinDistance:
        min_dist.append(M_DIST_TH)  # new landmark

    min_id =np.argmin(min_dist)

    return min_id


def calc_innovation(lm, positonEstablisched, helpDataStructure, observation, LMid):
    delta = lm - positonEstablisched[0:2]
    q = (delta.T @ delta)[0, 0]
    z_angle = math.atan2(delta[1, 0], delta[0, 0]) - positonEstablisched[2, 0]
    zp = np.array([[math.sqrt(q), pi_2_pi(z_angle)]])
    y = (observation - zp).T
    y[1] = pi_2_pi(y[1])
    H = jacob_h(q, delta, positonEstablisched, LMid + 1)
    S = H @ helpDataStructure @ H.T + Cx[0:2, 0:2]

    return y, S, H


def jacob_h(q, delta, x, i):
    sq = math.sqrt(q)
    G = np.array([[-sq * delta[0, 0], - sq * delta[1, 0], 0, sq * delta[0, 0], sq * delta[1, 0]],
                  [delta[1, 0], - delta[0, 0], - q, - delta[1, 0], delta[0, 0]]])

    G = G / q
    nLM = calc_n_lm(x)
    F1 = np.hstack((np.eye(3), np.zeros((3, 2 * nLM))))
    F2 = np.hstack((np.zeros((2, 3)), np.zeros((2, 2 * (i - 1))),
                    np.eye(2), np.zeros((2, 2 * nLM - 2 * i))))

    F = np.vstack((F1, F2))

    H = G @ F

    return H


def pi_2_pi(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi
