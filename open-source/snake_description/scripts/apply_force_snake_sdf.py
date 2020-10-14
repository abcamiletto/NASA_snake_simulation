import trollius
from trollius import From

import pygazebo
import pygazebo.msg.joint_cmd_pb2

@trollius.coroutine
def publish_loop():
    manager = yield From(pygazebo.connect())

    publisher = yield From(
        manager.advertise('/gazebo/default/model/joint_cmd',
                          'gazebo.msgs.JointCmd'))

    message = pygazebo.msg.joint_cmd_pb2.JointCmd()
    message.name = 'pexod::body_leg_0'
    message.axis = 2
    message.force = 20.0

    while True:
        print "Publishin message"
        yield From(publisher.publish(message))
        yield From(trollius.sleep(1.0))

loop = trollius.get_event_loop()
loop.run_until_complete(publish_loop())