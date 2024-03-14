import time

def getLogComment(status,statusType):
    
    if(statusType == 'detectorStatus'):
        if(status == -2):
            return "No lines were detected in the image!"

        if(status == -1):
            return "Unable to read given image!"

        elif(status == 0):
            return "Image preprocessing failed!"

        elif(status == 1):
            return "HoughLines function raised an error!"

        elif(status == 2):
            return "Contour detection failed!"

        elif(status == 3):
            return "Something went wrong during the piece identification proccess!"
        elif(status == 4):
            return "Pieces's colors were successfully detected!"
        else:
            return "Unkown status was given"

    elif(statusType == 'playerMoveStatus'):
        if(status[0] == -1):
            return f"The move {status[1]} made by the player is illegal!"

        elif(status[0] == 1):
            return "The move {status[1]} was made by the player"
        
        else:
            return "Unkown status was given"
    
    elif(statusType == 'botMoveStatus'):
        return f"The move {status} was made by the AI!"

    elif(statusType == 'endgameStatus'):
        if(status == 2):
            return "The player wins!"

        elif(status == 1):
            return "The AI wins!"

        elif(status == 0):
            return "It's a draw!"

        else:
            return "Unkown status was given"

    elif(statusType == 'bootStatus'):
        return "System startup was completed successfully!"

    else:
        pass