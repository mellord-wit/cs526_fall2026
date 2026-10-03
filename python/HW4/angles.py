# Marie Mellor
# CSCI 665 hw3
# angles.py

import sys
import math
import datetime

class tree_node:
    def __init__(self, input_polar_angle):
        self.polar_angle = input_polar_angle
        self.right = None
        self.left = None

    def add_node(self, input_polar_angle):
        if input_polar_angle <= self.polar_angle:
            if self.left is None:
                new_node = tree_node(input_polar_angle)
                self.left = new_node
                return
            else:
                return self.left.add_node(input_polar_angle)
        else:
            if self.right is None:
                new_node = tree_node(input_polar_angle)
                self.right = new_node
                return
            else:
                return self.right.add_node(input_polar_angle)

    '''def find_node(self, input_polar_angle):
        round_factor = 4
        #margin_of_error = 0.00000000000001
        margin_of_error = 0.00015
        rounded_input = round(input_polar_angle, round_factor)
        rounded_base_value = round(self.polar_angle, round_factor)

        #if input_polar_angle >= (self.polar_angle - margin_of_error) and input_polar_angle <= (self.polar_angle + margin_of_error):
        if rounded_input >= (rounded_base_value - margin_of_error) and rounded_input <= (rounded_base_value + margin_of_error):
            return input_polar_angle
        else:
            if input_polar_angle <= self.polar_angle:
                if self.left is None:
                    return None
                else:
                    return self.left.find_node(input_polar_angle)
            else:
                if self.right is None:
                    return None
                else:
                    return self.right.find_node(input_polar_angle)'''

    def find_node(self, input_polar_angle):
        round_factor = 4
        #margin_of_error = 0.00000000000001
        margin_of_error  = 0.00015

        rounded_input = round(input_polar_angle, round_factor)
        rounded_base_value = round(self.polar_angle, round_factor)

        rounded_input = round(rounded_input + margin_of_error, round_factor)
        rounded_base_value = round(rounded_base_value + margin_of_error, round_factor)

        if rounded_input >= (rounded_base_value - margin_of_error) and rounded_input <= (rounded_base_value + margin_of_error):
            return input_polar_angle
        else:
            if input_polar_angle <= self.polar_angle:
                if self.left is None:
                    return None
                else:
                    return self.left.find_node(input_polar_angle)
            else:
                if self.right is None:
                    return None
                else:
                    return self.right.find_node(input_polar_angle)

def test_binary_tree():
    test_array = [10,44,1,25,6,78,32,66]
    tree = None
    for i in test_array:
        if tree is None:
            tree = tree_node(i)
        else:
            tree.add_node(i)

    print("input array", test_array)

    test_array = [10,44,1,50,6,78,8,66]
    print("find array", test_array)

    for i in test_array:
        found = tree.find_node(i)
        if found is None:
            print(i, "not in list")
        else:
            print(i, "in list")


def compute_polar_angle(point):
    if point[0] == 0:
        return 90.0
    else:
        return round(math.degrees(math.atan((point[1]/point[0]))),10)
        #return math.degrees((math.atan2(point[1], point[0])))

def compute_1_over_tan(point):
    if point[0] == 0:
        return 90.0
    else:
        cosine = math.cos(point[0])
        sine = math.sin(point[0])
        cotangent = 1/(sine/cosine)
        return round(math.degrees(cotangent), 10)

def test_polar_angle():
    points = [[2,5], [9,1], [2,2], [4,7], [0,0], [0,8], [8,0]]
    for point in points:
        print(point, "polar angle=", compute_polar_angle(point))
        print(point, "1/tan angle=",compute_1_over_tan(point))


def determine_right_triangle(points_list):
    first_point_counter = 1
    total_triangles = 0
    for i in range(len(points_list)):
        first_point = points_list[i]
        '''shift_x = 0 - first_point[0]
        shift_y = 0 - first_point[1]'''
        tree = None
        for j in range(len(points_list)):
            if i != j:
                second_point = points_list[j]
                new_x = second_point[0] - first_point[0]
                new_y = second_point[1] - first_point[1]
                new_point = [new_x, new_y]
                second_polar_angle = compute_polar_angle(new_point)
                if tree is None:
                    tree = tree_node(second_polar_angle)
                else:
                    tree.add_node(second_polar_angle)

        # find right triangle
        for j in range(len(points_list)):
            if i != j:
                second_point = points_list[j]
                new_x = second_point[0] - first_point[0]
                new_y = second_point[1] - first_point[1]
                new_point = [new_x, new_y]
                second_polar_angle = compute_polar_angle(new_point)

                if second_polar_angle >= 90:
                    angle_to_find = second_polar_angle - 90.0
                    found_angle = tree.find_node(angle_to_find)
                    if found_angle is not None:
                        total_triangles += 1

                if second_polar_angle < 90:
                    angle_to_find = 90.0 + second_polar_angle
                    found_angle = tree.find_node(angle_to_find)
                    if found_angle is not None:
                        total_triangles += 1

    return total_triangles

def main():
    # read input data and put into a list
    input_list = []
    i = 0
    for line in sys.stdin:
        if i == 0:
            n = int(line.strip())
        elif i == n+1:
            break
        else:
            input_list.append(line.split())
        i += 1

    # convert to ints
    points_list = []
    for points in input_list:
        current_x = int(points[0])
        current_y = int(points[1])
        current_point = [current_x, current_y]
        points_list.append(current_point)


    start = datetime.datetime.now()

    right_triangle_count = determine_right_triangle(points_list)

    end = datetime.datetime.now()

    print(right_triangle_count)
    #print("time: ", end-start)

    #test_polar_angle()

main()


