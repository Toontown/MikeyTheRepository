acceptErrorDialog = 0
doneEvent = 'game Done'
colorRed = (1, 0, 0, 1)
colorBlue = (0, 0, 1, 1)
colorGreen = (0, 1, 0, 1)
colorGhostRed = (1, 0, 0, 0.5)
colorGhostGreen = (0, 1, 0, 0.5)
colorWhite = (1, 1, 1, 1)
colorBlack = (0.5, 0.5, 0.5, 1.0)
colorShadow = (0, 0, 0, 0.5)
running = 0
maxX = 0.46999999999999997
minX = -0.46999999999999997
maxZ = 0.75000000000000002
minZ = -0.00000000000000001
newBallX = 0.0
newBallZ = 0.69999999999999998
rangeX = (maxX - minX)
rangeZ = (maxZ - minZ)
size = 0.085000000000000006
sizeZ = (size * 0.80000000000000004)
gX = int((rangeX / size))
gZ = int((rangeZ / sizeZ))
maxX = (minX + (gX * size))
maxZ = (minZ + (gZ * sizeZ))
controlOffsetX = 0.0
controlOffsetZ = 0.0
queExtent = 3
gridDimX = gX
gridDimZ = gZ
gridBrick = False
newBallTime = 1.0
newBallCountUp = 0.0
cogX = 0
cogZ = 0
controlSprite = None