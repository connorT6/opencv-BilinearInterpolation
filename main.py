import cv2 as cv
import numpy as np

im = cv.imread("samples/image.png", cv.IMREAD_GRAYSCALE)
scale = 4
numOfRowsOnOriginal = int(im.shape[0])
numOfColsOnOriginal = int(im.shape[1])
numOfRowsOnZoomed = int(scale * numOfRowsOnOriginal) - (scale - 1)
numOfColsOnZoomed = int(scale * numOfColsOnOriginal) - (scale - 1)

zoomed = np.zeros((numOfRowsOnZoomed, numOfColsOnZoomed), dtype=im.dtype)

for i in range(0, numOfRowsOnZoomed):
    for j in range(0, numOfColsOnZoomed):
        color1 = None
        color2 = None
        color3 = None
        color4 = None
        rowOnOriginal = int(i / scale)
        colOnOriginal = int(j / scale)

        if rowOnOriginal != (numOfRowsOnOriginal - 1) and colOnOriginal != (numOfColsOnOriginal - 1):
            rowIndex = rowOnOriginal * scale
            rowIndex1 = (rowOnOriginal + 1) * scale

            colIndex = colOnOriginal * scale
            colIndex1 = (colOnOriginal + 1) * scale

            verticalColor1 = None
            verticalColor2 = None

            if i == rowIndex and j == colIndex:
                verticalColor1 = im[rowOnOriginal, colOnOriginal]
                verticalColor2 = -1
            else:
                if j == colIndex: #if the pixel we are processing is on a major column. we don't need 2 horizontal colors which calculated vertically
                    color1 = im[rowOnOriginal, colOnOriginal]
                    color3 = im[rowOnOriginal + 1, colOnOriginal]
                    verticalDif1 = i - rowOnOriginal * scale
                    verticalDif2 = (rowOnOriginal + 1) * scale - i
                    verticalColor1 = ((color1 * verticalDif2) / (verticalDif1 + verticalDif2)) + (
                            (color3 * verticalDif1) / (verticalDif1 + verticalDif2))
                    verticalColor2 = -1
                else:
                    color1 = im[rowOnOriginal, colOnOriginal]
                    color2 = im[rowOnOriginal, colOnOriginal + 1]
                    color3 = im[rowOnOriginal + 1, colOnOriginal]
                    color4 = im[rowOnOriginal + 1, colOnOriginal + 1]
                    verticalDif1 = i - rowOnOriginal * scale
                    verticalDif2 = (rowOnOriginal + 1) * scale - i
                    verticalColor1 = ((color1 * verticalDif2) / (verticalDif1 + verticalDif2)) + (
                            (color3 * verticalDif1) / (verticalDif1 + verticalDif2))
                    verticalColor2 = ((color2 * verticalDif2) / (verticalDif1 + verticalDif2)) + (
                            (color4 * verticalDif1) / (verticalDif1 + verticalDif2))

            if verticalColor2 == -1:#if the pixel is on a intersection of a row and colmn
                zoomed[i, j] = verticalColor1
            else:
                horizontalDif1 = j - colOnOriginal * scale
                horizontalDif2 = (colOnOriginal + 1) * scale - j
                tempColor = ((verticalColor1 * horizontalDif2) / (horizontalDif1 + horizontalDif2)) + (
                        (verticalColor2 * horizontalDif1) / (horizontalDif1 + horizontalDif2))
                zoomed[i, j] = tempColor

cv.namedWindow('Original', cv.WINDOW_AUTOSIZE)
cv.imshow('Original', im)
cv.waitKey(0)
cv.destroyAllWindows()
cv.namedWindow('Zoomed by Bilinear Interpolation', cv.WINDOW_AUTOSIZE)
cv.imshow('Zoomed by Bilinear Interpolation', zoomed)
cv.waitKey(0)
cv.destroyAllWindows()
