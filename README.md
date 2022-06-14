# Py_Evolution

## Controls:
__Q:__ Quit  
__D:__ Show Debug Info  
__Space:__ Pause/Unpause Game  
__Up Arrow:__ Increase Food spawn rate  
__Down Arrow:__ Decrease Food spawn rate  

Click on Creature to show its properties, press __E__ to hide the information panel

## Neural Network inputs:
1. Distance to food, if any is in view
2. Angle of velocity to food if any is within view
3. Is the creature within the boundaries (only matters if hard boundary is applied)
4. Energy of creature
5. Age of creature
6. Velocity x
7. Velocity y
8. Constant (always 1)

## Neural Network outputs:
1. Force x that is applied to creature
2. Force y that is applied to creature
3. Should the creature reproduce (> 0 –> yes; < 0 –> no)
4. Creature colour r
5. Creature colour g
6. Creature colour b

