# Marie Mellor
# CSCI 665
# hw2
# gymnast.py
import datetime
import sys

# time unit node to hold the unit of time the crack appears, a pointer that holds the sizes of cracks which appear at that time unit
# the next and previous nodes, how much water is added in total from that time unit and the number of cracks that
# are left from that time unit
class time_unit_node:
    def __init__(self, time, cracks_list=None):
        self.time_unit = time
        self.cracks = cracks_list
        self.next = None
        self.previous = None
        self.water_to_add_each_time = 0
        self.number_of_nodes = 0

# crack node to hold a linked list of cracks for a given time unit in order from largest to smallest which also points to
# next and previous cracks in the linked list
class crack_node:
    def __init__(self, crack_size, previous_value=None, next_value=None):
        self.crack = crack_size
        self.next = next_value
        self.previous = previous_value

# function to print linked lists
def print_linkedlist(sort_list):
    printing = True
    current_node = sort_list
    counter = 0
    while printing:
        time = current_node.time_unit
        cracks = current_node.cracks
        printing_cracks = True
        while printing_cracks:
            if cracks is not None:
                print("time:", time, "crack:", cracks.crack)
                counter += 1
                if cracks.next is None:
                    break
                else:
                    cracks = cracks.next
            else:
                break
        current_node = current_node.next
        if current_node is None:
            break
    print("printed: ", counter)


def create_nodes(cracks_list_strings):
    # initialize values to none
    master_list = None
    sort_list_cracks = None
    sort_nodes = None
    prev_time_at_crack = 0
    time_node = None
    # loop over the time units and their given crack sizes
    for i in range(len(cracks_list_strings)):
        t, c = cracks_list_strings[i].split()
        # conver to ints
        time_at_crack = int(t)
        crack_size = int(c)

        # create a crack node given the size of the crack
        current_crack_node = crack_node(crack_size)
        # if there is nothing in the master list
        if master_list is None:
            # create a time node using the current time and add it to the master list
            time_node = time_unit_node(time_at_crack)
            master_list = time_node
        else:
            # otherwise, check if the current time is not equal to the time node's time unit
            if time_at_crack != time_node.time_unit:
                # create a new time node with the current time
                new_time_node = time_unit_node(time_at_crack)
                # set the new node to the current node's next value
                time_node.next = new_time_node
                # set the new node's previous node to the current time node
                new_time_node.previous = time_node
                # the current time node is now the new time node
                time_node = new_time_node

        # calculate the water that must be added for each time interation
        # water that needs to be added is determined by the size of the crack for every time unit
        time_node.water_to_add_each_time = time_node.water_to_add_each_time + crack_size
        # number of nodes increase by 1
        time_node.number_of_nodes = time_node.number_of_nodes + 1
        crack_not_added = True
        # get the current list of cracks from the time node
        current_crack_list = time_node.cracks
        # while the crack hasnt been added
        while crack_not_added:
            # if the list is empty
            if current_crack_list is None:
                # set the time node's crack node to the current crack node
                time_node.cracks = current_crack_node
                break
            else:
                # otherwise, check if the largest crack in the current crack node is larger than
                # the largest crack in the list of cracks
                if current_crack_node.crack >= current_crack_list.crack:
                    # if it is, set it's next value to the list of cracks
                    current_crack_node.next = current_crack_list
                    # if it has no previous meaning its first in the list
                    if current_crack_list.previous is None:
                        # set the time node's cracks to the current crack node
                        time_node.cracks = current_crack_node
                    # current crack node is now previous
                    current_crack_list.previous = current_crack_node
                    break
                else:
                    # if there is no next value
                    if current_crack_list.next is None:
                        # set the list's next to the current crack node and crack node's previous to the list
                        current_crack_list.next = current_crack_node
                        current_crack_node.previous = current_crack_list
                        break
                    # if the crack lists largeat crack is bigger than the current crack node's largest
                    # and the next current crack list crack is less than or equal to the current crack node's largest crack
                    elif current_crack_list.crack > current_crack_node.crack and current_crack_list.next.crack <= current_crack_node.crack:
                        # insert the value into the proper spot in the linked list, shuffle pre-existing values in list appropriately
                        # set temp node to next value in crack list
                        temp_node = current_crack_list.next
                        # current crack node's previous becomes current crack list
                        current_crack_node.previous = current_crack_list
                        # current crack list's next value becomes the current crac node
                        current_crack_list.next = current_crack_node
                        # current crack node's next becomes the temp node
                        current_crack_node.next = temp_node
                        # temp node's previous becomes the current crack node
                        temp_node.previous = current_crack_node
                        break
                    else:
                        # current is now the next value in the linked list
                        current_crack_list = current_crack_list.next

    #print_linkedlist(master_list)
    # return linked list
    return master_list


def calculate_water_added_new(current_time_node, time):
    total_water_to_add = 0
    if current_time_node.time_unit <= time:
        # calculate the time multiplier as time - current_time_node.time_unit
        time_multiplier = (time - current_time_node.time_unit) * current_time_node.number_of_nodes
        total_water_to_add = time_multiplier + current_time_node.water_to_add_each_time

    # print("for time ", time, "add ", total_water_to_add)

    return total_water_to_add


def calculate_flooding(master_list, total_number_of_cracks, max_water_allowed_in_village, water_drain):
    # initialize values
    time = 0
    water_to_add = 0
    total_water_in_village = 0
    max_water_level_in_village = 0
    checking_water = True

    while checking_water is True:
        # initialize values
        current_node = master_list
        largest_time_node = None
        water_to_add = 0
        water_to_add_new = 0
        continue_searching_for_biggest_node = True
        while continue_searching_for_biggest_node:
            if current_node.time_unit > time:
                break
            if current_node.time_unit <= time:
                if largest_time_node is not None:
                    if largest_time_node.cracks is None:
                        largest_time_node = current_node
                    else:
                        # get the largest crack to be removed for each time node from [0, the current time]
                        if current_node.cracks is not None:
                            if (current_node.cracks.crack + (time - current_node.time_unit)) > \
                                    (largest_time_node.cracks.crack + (time - largest_time_node.time_unit)):
                                largest_time_node = current_node
                else:
                    largest_time_node = current_node

                # calculate how much water needs to be added from the current node
                temp = calculate_water_added_new(current_node, time)
                # add to overall water that needs to be added to village
                water_to_add = water_to_add + temp

                # set current node to next
                current_node = current_node.next
                # if there are no more nodes, break
                if current_node is None:
                    break

        largest_water_remove = 0
        # remove the largest crack
        if largest_time_node is not None:
            if largest_time_node.cracks is not None:
                # get the largest crack
                largest_crack = largest_time_node.cracks
                # set the next largest crack
                largest_time_node.cracks = largest_crack.next
                # remove the water that would have been added by the largest crack
                largest_water_remove = largest_crack.crack + (time - largest_time_node.time_unit)

                # now adjust the water to add each new iteration by removing the amount of water for
                # the removed node
                largest_time_node.water_to_add_each_time = \
                    largest_time_node.water_to_add_each_time - largest_crack.crack

                # decrement the number of cracks that remain for the time node
                largest_time_node.number_of_nodes = largest_time_node.number_of_nodes - 1

                # decrement how many cracks are left in total
                total_number_of_cracks -= 1

                if total_number_of_cracks > 0:
                    # if there are no cracks left in the node it can be removed
                    if largest_time_node.number_of_nodes == 0:
                        # get previous node and previous node
                        previous_node = largest_time_node.previous
                        next_node = largest_time_node.next

                        if previous_node is None:
                            # this is the first time node, simply reset the master list
                            master_list = next_node
                            next_node.previous = None
                        else:
                            previous_node.next = next_node
                            if next_node is not None:
                                next_node.previous = previous_node

        # calculate the water that will be added to the village
        # water that gets added to the village per time unit is:
        # the water to be added - the water that gets drained per time unit - the water that the largest crack would have added
        total_water_to_add_to_village = water_to_add - water_drain - (largest_water_remove)
        # calculate how much water is in the village
        total_water_in_village = total_water_to_add_to_village + total_water_in_village
        # water cannot be negative
        if total_water_in_village < 0:
            total_water_in_village = 0
        # print("total water:", total_water_in_village, "time:", time)

        # determine the max water level that was reached
        if max_water_level_in_village < total_water_in_village:
            max_water_level_in_village = total_water_in_village

        # check if the village flooded
        if total_water_in_village >= max_water_allowed_in_village:
            return total_water_in_village, time, "flooded"

        if total_number_of_cracks <= 0:
            return max_water_level_in_village, time, "safe"

        if master_list.time_unit > time:
            skip_time = master_list.time_unit - time
            # drain the village by skip_time * water_drain
            total_water_in_village = total_water_in_village - (skip_time * water_drain)
            if total_water_in_village < 0:
                total_water_in_village = 0

            time = master_list.time_unit
        else:
            time += 1


def main():

    # read input data and put into a list
    i = 0
    cracks_list_strings = []
    for line in sys.stdin:
        if i == 0:
            total_number_of_cracks = int(line.strip())
        if i == 1:
            max_water = int(line.strip())
        if i == 2:
            water_drained_per_time = int(line.strip())
        elif i > 2:
            crack = line.strip()
            cracks_list_strings.append(crack)
            '''if i == int(total_number_of_cracks) + 2:
                break'''
        i += 1

    '''print("total cracks:", total_number_of_cracks)
    print("max water:", max_water)
    print("water drained per time unit:", water_drained_per_time)'''
    # print("crack list as string: ", cracks_list_strings)

    # start_time = datetime.datetime.now()

    # create nodes
    master_list = create_nodes(cracks_list_strings)

    # end_time = datetime.datetime.now()
    # total_time = end_time - start_time
    # print("created nodes took :", total_time)

    # calculate the flooding in the village
    water, time, outcome = calculate_flooding(master_list, total_number_of_cracks, max_water, water_drained_per_time)

    # end_calculate = datetime.datetime.now()
    # print("finished running in: ", end_calculate - start_time)

    # format output
    if outcome == "flooded":
        print("FLOOD")
        print(time)
        print(water)
    else:
        print("SAFE")
        print(water)
main()

# scp flood.py mhm3244@glados.cs.rit.edu:~/Courses/cs665
