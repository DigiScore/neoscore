#!/usr/bin/env python

##############################################################################
### Incomplete and not in use - seems too bulky of a solution to warrant this.
### Leaving in case the code becomes useful at some point
##############################################################################
class AccidentalState:
    """
    A class containing the current accidental state of all pitch letters at a given point in a staff
    """
    def __init__(self, staff, position):
        """

        Args:
            staff (Staff): The staff in which the check is being made
            position (float): The horizontal position to check from

        """
        # TODO: Allow items in staff.contents to disrupt the accidental state, such as barlines and key signatures
        # Sort staff.contents by horizontal position
        staff_contents = sorted(staff.contents, key=lambda item: item.x_pos)
        # Iterate through staff_contents, modifying the state with each item as necessary
        # Break once we reach or go past position
        for item in staff_contents:
            # Use a round-about type check
            if type(item).__name__ == 'NoteColumn':
                pass
            if item.x_pos >= position:
                break
