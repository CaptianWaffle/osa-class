#!/usr/bin/env python3
"""
Galton board
@author: Wolfgang Baldus
@version: 1
"""

import argparse
import random
import threading


class Board:
    """
    Class Board
    Contains multiple bins that collect beans
    Contains multiple levels of pegs
    """

    def __init__(self, bins: int):
        """Make a new board of the specified size"""
        self._bins = [0] * bins
        self._pegs = bins // 2

    def status(self):
        """Print status of the board in some meaningful format"""
        print(self._bins)

    def __len__(self):
        """Return the board size"""
        return len(self._bins)

    def __getitem__(self, idx: int):
        """Get number of beans in the specified bin"""
        return self._bins[idx]

    def __setitem__(self, idx: int, new_value: int):
        """Set number of beans in the specified bin"""
        self._bins[idx] = new_value

    @property
    def bins(self):
        """Return the bins"""
        return self._bins

    @property
    def pegs(self):
        """Return number of levels of pegs"""
        return self._pegs


class Bean(threading.Thread):
    """
    Class Bean
    Data members:
    - board: Board
    - current position: position of the bean on the board
    - probability: probability of a bean falling to the right on a peg
    - lock: lock
    """

    def __init__(self, board: object, start: int, prob: float, lock: object):
        """Make a new Bean"""
        super().__init__(group=None, target=self, args=(board, start, prob, lock))
        self._board = board
        self._pos = start
        self._prob = prob
        self._lock = lock
        
        self._board

    def move_left(self):
        """Move a bean left"""
        current_beans = self._board.__getitem__(self._pos)
        next_position_beans = self._board.__getitem__(self._pos - 1)
        self._board.__setitem__(self._pos, current_beans - 1)
        self._board.__setitem__(self._pos - 1, next_position_beans + 1)
        
        self._pos = self._pos - 1

    def move_right(self):
        """Move a bean right"""
        current_position_beans = self._board.__getitem__(self._pos)
        next_position_beans = self._board.__getitem__(self._pos + 1)
        self._board.__setitem__(self._pos, current_position_beans - 1)
        self._board.__setitem__(self._pos + 1, next_position_beans + 1)
        
        self._pos = self._pos + 1

    def run(self):
        """Run a bean through the pegs"""
        probability = self._prob * 100 
        for x in range(self._board.pegs):
                       
            direction1 = random.choices(['left', 'right'], weights=[100-probability, probability], k=1)
            direction2 = random.choices(['left', 'right'], weights=[100-probability, probability], k=1)
            #print(self._board.__len__())              
            if direction1 == direction2:
                if direction1 == ['left']:
                    if self._pos == 0:
                        continue
                        #print("Ran into left edge")
                    else:
                        self._lock.acquire()
                        self.move_left()
                        self._lock.release()
                else:
                    if self._pos == self._board.__len__() - 1:
                        continue
                        #print("Ran into right edge" + str(self._board.__len__()))
                    else:
                        self._lock.acquire()
                        self.move_right()
                        self._lock.release()                    
    
def main():
    """Main function"""
    # Parse command-line arguments.
    # Their short/long names are provided by you must complete the parsing section
    parser = argparse.ArgumentParser(description="Process the arguments.")
    parser.add_argument("-bb", "--beans",default=1000 ,type=int)
    parser.add_argument("-b", "--bins", default=11, type=int)
    parser.add_argument("-s", "--start", default=5, type=int)
    parser.add_argument("-p", "--prob", default=0.5, type=int)

    print("Start")
    args = parser.parse_args()
    print("Beans: " + str(args.beans) + ", bins: " + str(args.bins) + ", start: " + str(args.start) + ", prob: " + str(args.prob))
    # Create a list of jobs
    job_list = []
    # Create a shared lock
    my_lock = threading.Lock()
    # Create a board
    board = Board(args.bins)
    board.__setitem__(args.start, args.beans)
    # Create jobs (beans)
    for x in range(args.beans):
        job_list.append(Bean(board, args.start, args.prob, my_lock)) 
    
    print_list = []  
    for job in job_list:
        print_list.append(job.is_alive())
    print(print_list)
    # Print the board status
    board.status()
    # Start jobs
    for job in job_list:
        job.start()
    # Stop jobs
    #print("Active threading count: " + str(threading.active_count()))
    #for job in job_list:
        #print(job.is_alive())
        
    # Print the board status
    board.status()
    print("Done")


if __name__ == "__main__":
    main()