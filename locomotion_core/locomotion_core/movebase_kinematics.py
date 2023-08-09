import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist

global lx, az, u_du1, u_du2
lx = 0.0; az = 0.0; u_du1 = 0; u_du2 = 0

class get_move_cmds(Node):

    def __init__(self):
        super().__init__('movebase_kinematics')
        self.subscription = self.create_subscription(
            Twist,
            'r4/core_cmdvel',
            self.move_cmd_callback,
            5)
        self.subscription  # prevent unused variable warning

        self.pub_du1 = self.create_publisher(Int16, 'r4/du1/pwr', 5)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.du1_callback)
        self.i = 0

        self.pub_du2 = self.create_publisher(Int16, 'r4/du2/pwr', 5)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.du2_callback)
        self.i = 0

    def move_cmd_callback(self, msg):
        global lx, az, u_du1, u_du2
        lx = msg.linear.x
        az = msg.angular.z

        u_du1 = int(400 * (lx - az) )
        u_du2 = int(400 * (lx + az))
        #print(lx)

    def du1_callback(self):
        global u_du1
        msg = Int16()
        msg.data = u_du1
        self.pub_du1.publish(msg)
        self.i += 1

    def du2_callback(self):
        global u_du2
        msg = Int16()
        msg.data = u_du2
        self.pub_du2.publish(msg)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sub_move_cmds = get_move_cmds()

    rclpy.spin(sub_move_cmds)

    sub_move_cmds.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()