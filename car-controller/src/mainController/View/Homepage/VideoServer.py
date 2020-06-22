# Copyright 2020 @PascalPuchtler

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from flask import (Flask, Response, jsonify, make_response, render_template,request)
from CrossCutting.IterableQueue.IterableQueue import IterableQueue

import cv2


class VideoServer:
    def __init__(self, videoQueue, movementQueue, moveControllerCommandQueue, trajectoryPlanningCommandQueue ):
        self.app = Flask(__name__)
        self.videoQueue = videoQueue
        self.movementQueue = movementQueue
        self.moveControllerCommandQueue = moveControllerCommandQueue
        self.trajectoryPlanningCommandQueue = trajectoryPlanningCommandQueue

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/autonomous_driving')
        def autonomous_driving():
            if not moveControllerCommandQueue.full():
                moveControllerCommandQueue.put('autonomous_driving')
            res = make_response(jsonify({"message": "OK"}), 200)
            return res

        @self.app.route('/curve_test_mode')
        def curve_test_mode():
            if not moveControllerCommandQueue.full():
                moveControllerCommandQueue.put('curve_test_mode')
            res = make_response(jsonify({"message": "OK"}), 200)
            return res

        @self.app.route('/manuel_driving')
        def manuel_driving():
            if not moveControllerCommandQueue.full():
                moveControllerCommandQueue.put('manuel_driving')
            res = make_response(jsonify({"message": "OK"}), 200)
            return res

        @self.app.route('/reset_map')
        def reset_map():
            if not trajectoryPlanningCommandQueue.full():
                trajectoryPlanningCommandQueue.put('reset_map')
            res = make_response(jsonify({"message": "OK"}), 200)
            return res
        

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.gen(),  mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/move_command', methods=['POST'])
        def move_command():
            movements = request.get_json()
            #FIXME here we have the problem, that it could be that stop commands are ignored
            if not movementQueue.full():
                movementQueue.put(movements)
            res = make_response(jsonify({"message": "OK"}), 200)
            return res

        @self.app.route('/shutdown', methods=['POST', 'GET'])
        def shutdown():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
            return 'Server shutting down...'

    def gen(self):
        for frame in IterableQueue(self.videoQueue):
            _, frame = cv2.imencode('.jpg', frame)
            frame = frame.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def run(self):
        self.app.run(host='0.0.0.0', debug=True, use_reloader=False)
