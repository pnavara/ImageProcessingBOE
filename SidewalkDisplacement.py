import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyrealsense2 as rs
import math
from Grabcut import Grabcut

def displacement(colorized_depth):
    img1 = cv2.imread('images/d435colored_4.png')
    img = cv2.imread('images/d435depth_4.png')

    loop = True
    while loop:

        obj = Grabcut()
        imageGC = obj.GC(img1)

        plt.imshow(imageGC[...,::-1])
        plt.show()

        x, y = input('Enter xy values: ').split()
        x1, y1 = input('Enter other xy values: ').split()
        depth = aligned_depth_frame.get_distance(int(x), int(y))
        dx, dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [int(x), int(y)], depth)
        depth1 = aligned_depth_frame.get_distance(int(x1), int(y1))
        dx1, dy1, dz1 = rs.rs2_deproject_pixel_to_point(color_intrin, [int(x1), int(y1)], depth1)
        # euclid = cv2.norm((dx, dy, dz), (dx1, dy1, dz1), cv2.NORM_L2) # another way to calculate displacement, should be the same result as the distance variable
        distance = math.sqrt(((dx1 - dx) ** 2) + ((dy1 - dy) ** 2) + ((dz1 - dz) ** 2))

        print('Displacement: ', distance, 'meters')
        print('Displacement: ', distance * 100, 'cm')

        again = input('Go again? (y or n)')
        if again == 'y':
            continue
        else:
            loop = False

# Setup:
pipe = rs.pipeline()
cfg = rs.config()
# cfg.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)  # unhide if you want to record a new bag file
# cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30) # unhide if you want to record a new bag file
# cfg.enable_record_to_file("images/test2.bag")                     # unhide if you want to record a new bag file

cfg.enable_device_from_file('images/test2.bag')                 # unhide if you want to read your saved bag file
profile = pipe.start(cfg)

align_to = rs.stream.color
align = rs.align(align_to)

take = True
counter = 0 # counter for waiting for auto exposure to adjust
try:
    while (take):
        # Store next frameset for later processing:
        frames = pipe.wait_for_frames()

        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
        depth_image = np.asanyarray(aligned_depth_frame.get_data())

        color_image = np.asanyarray(color_frame.get_data())

        colorizer = rs.colorizer()
        colorized_depth = np.asanyarray(
            colorizer.colorize(aligned_depth_frame).get_data())

        # Press esc or 'q' to close the image window
        # if key & 0xFF == ord('q') or key == 27: #unhide this if statement and its content if you want to record a new bag file
        #
        #     take = False
        #
        #     cv2.destroyAllWindows()

        if counter == 60: #unhide this if statement and its content if you want to read a saved bag file
            cv2.imwrite('images/d435colored_4.png', color_image)
            cv2.imwrite('images/d435depth_4.png', colorized_depth)
            take = False
            displacement(colorized_depth)
        else:
            counter = counter + 1

except Exception as e:
    print(e)
    pass

finally:
    pipe.stop()
