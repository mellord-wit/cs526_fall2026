# The Gale-SHapley Marriage Problem

# First line of input is total n men and women
# Each line after is first n men and with preference,
# and then n women and their preference.
# Each name is separated by spaces.
# First half is men second half is women.

import sys

def main():
    if len(sys.argv) != 2:
        exit(1)
    try:
        with open(sys.argv[1], 'r') as f:
            n = int(f.readline())
            people = []*n
            if not n:
                exit(1)
            for line in f:
                names = line.split()
                people.append(names)
    except ValueError:
        exit(1)
    f.close()

    mPref = []*n
    wPref = []*n
    for i in range(0,n):
        mPref.append(people[i])
    for i in range(n,n*2):
        wPref.append(people[i])

    menList = []*n
    menPrefrences = dict()
    unengagedMen = []*n
    menProposeOffset = dict()
    womenList = []*n
    womenPrefrences = dict()
    womenEngagement = dict()
    womenProposals = dict()

    for j in range(0,n):
        curMan = mPref[j].pop(0)
        menPrefrences[curMan] = mPref[j]
        menList.append(curMan)
        unengagedMen.append(curMan)
        menProposeOffset[curMan] = -1

        curWoman = wPref[j].pop(0)
        womenPrefrences[curWoman] = wPref[j]
        womenList.append(curWoman)
        womenEngagement[curWoman] = "none"
        womenProposals[curWoman] = []


    while len(unengagedMen) > 0:
        propose(unengagedMen, menPrefrences, menProposeOffset, womenProposals)
        print('***********************')
        for women in womenEngagement:
            print(womenEngagement[women], women)
        print('***********************')
        print()
        accpetProposal(womenProposals, womenPrefrences, womenEngagement, n, unengagedMen)

        print('***********************')
        for women in womenEngagement:
            print(womenEngagement[women], women)
        print('***********************')
        print()


        # Invariant:      the size of unengagedMen > 0
        #
        # Initialization: the size of unengagedMen starts off as n
        #                 since there are n number of unengaged men
        #                 in the first iteration of the loop
        # Maintenance:    after running through the functions propose and
        #                 accpetProposal, the size of the list unengagedMen
        #                 decreases with every man that finds a partner. Because
        #                 of this, the loop invariant is preserveed
        # Termination:    the loop terminates once len(unengagedMen) == 0
        #                 indicating all of the men have proposed and have been
        #                 accepted by a woman

    for women in womenEngagement:
        print(womenEngagement[women], women)

def propose(unengagedMen, menPrefrences, menProposeOffset, womenProposals):
    for curMan in unengagedMen:
        curPref = menPrefrences.get(curMan)
        curIndex = menProposeOffset.get(curMan)
        curIndex += 1
        menProposeOffset[curMan] = curIndex
        curProposal = curPref[curIndex]
        womenProposals.get(curProposal).append(curMan)

    # Invariant:      the index of curMan within the size of unengagedMen
    #
    # Initialization: curMan starts off as the first man in the list of unengagedMen
    #                 We then start getting the preferences from
    #                 the men and and indexing through the current mans
    #                 prefrences so that he may propose to his most prefered
    #                 woman
    # Maintenance:    We loop through all the unengagedMen up to the
    #                 length of that list each time, and add them
    #                 to the dictionary womanProposals, this changes until
    #                 we reach the end of unengagedMen
    # Termination:    Once we have finsihed looping through all of the current
    #                 unengagedMen  we exit the function, we move on from this
    #                 unction and the loop terminates

def accpetProposal(womenProposals, womenPrefrences, womenEngagement, n, unengagedMen):
    for curWoman in womenProposals:
        curProposals = womenProposals.get(curWoman)
        curPref = womenPrefrences.get(curWoman)
        curEngagement = womenEngagement.get(curWoman)
        curEngagementOffset = n + 1
        if curEngagement != "none":
            curEngagementOffset = curPref.index(curEngagement)
        originalEngagementOffset = curEngagementOffset
        for curProposal in curProposals:
            curOffset = curPref.index(curProposal)
            if curOffset < curEngagementOffset:
                curEngagementOffset = curOffset
        if curEngagementOffset != originalEngagementOffset:
            newFiance = curPref[curEngagementOffset]
            womenEngagement[curWoman] = newFiance
            unengagedMen.remove(newFiance)
            if originalEngagementOffset != (n + 1):
                curFiance = curPref[originalEngagementOffset]
                unengagedMen.append(curFiance)


        # Invariant:      the inner for loop;
        #                 the index of curProposal < curProposals length
        #
        # Initialization: curProposal at posiiton 0 because we start
        #                 from 0 and go for the size of curProposals
        #                 to loop through all the possible proposals
        #                 and compare them with the womens ranking
        # Maintenance:    We loop through each proposal and take its
        #                 index off set and compare it with the engagment off set.
        #                 if the curOffset is less than the engagement we make the
        #                 curEngagementOffset the new curOffset so that the offset
        #                 is the highest ranked choice on the women's list
        #                 of men that have proposed to her thus far
        # Termination:    Once we've looped through all of the proposals in
        #                 curProposals and all the women have accepted a proposal
        #                 based on their ranking, the loop terminates

    # Invariant:      The outer for loop;
    #                 the index of curWoman < womenProposals length
    #
    # Initialization: curWoman at position 0 indicating the first woman in the
    #                 list since we are going through all of the women regardless
    #                 if they have been proposed to or not. We initialize
    #                 the dictinoary curProposals for the curWoman as well as the
    #                 curPref for the curWoman and the curEngagement
    # Maintenance:    We loop through all of the n number of women in the list
    #                 and initialize all their prefrences as well as who has proposed
    #                 to them thus far. If there are no curEngagements for the
    #                 curWoman we make sure to set the curEngagementOffset to
    #                 the index of the curPref at curEngagement. The curEngagement
    #                 then compared to the previous engagements and a fiance is
    #                 determined based on the woman's ranking of the curProposal.
    # Termination:    Once we've looped through all the women in the list and
    #                 their preferences are initialized and compared to the
    #                 curProposals, the loop terminates.

main()
