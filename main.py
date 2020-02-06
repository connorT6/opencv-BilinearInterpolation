import cv2 as cv
import numpy as np

im = cv.imread("samples/image.png", cv.IMREAD_REDUCED_GRAYSCALE_2)
scale = 4
originalRows = int(im.shape[0])
originalCols = int(im.shape[1])
rows = int(scale * originalRows) - (scale - 1)
cols = int(scale * originalCols) - (scale - 1)

zoomed = np.zeros((rows, cols), dtype=im.dtype)

for i in range(0, rows):
    for j in range(0, cols):
        color1 = None
        color2 = None
        color3 = None
        color4 = None
        tmpRow = int(i / scale)
        tmpCol = int(j / scale)

        if tmpRow != (originalRows - 1) and tmpCol != (originalCols - 1):
            rowIndex = tmpRow * scale
            rowIndex1 = (tmpRow + 1) * scale

            colIndex = tmpCol * scale
            colIndex1 = (tmpCol + 1) * scale

            verticalColor1 = None
            verticalColor2 = None

            if i == rowIndex and j == colIndex:
                verticalColor1 = im[tmpRow, tmpCol]
                verticalColor2 = -1
            else:
                if i == colIndex:
                    color1 = im[tmpRow, tmpCol]
                    color3 = im[tmpRow + 1, tmpCol]
                    verticalDif1 = i - tmpRow * scale
                    verticalDif2 = (tmpRow + 1) * scale - i
                    verticalColor1 = ((color1 * verticalDif2) / (verticalDif1 + verticalDif2)) + (
                            (color3 * verticalDif1) / (verticalDif1 + verticalDif2))
                    verticalColor2 = -1
                else:
                    color1 = im[tmpRow, tmpCol]
                    color2 = im[tmpRow, tmpCol + 1]
                    color3 = im[tmpRow + 1, tmpCol]
                    color4 = im[tmpRow + 1, tmpCol + 1]
                    verticalDif1 = i - tmpRow * scale
                    verticalDif2 = (tmpRow + 1) * scale - i
                    verticalColor1 = ((color1 * verticalDif2) / (verticalDif1 + verticalDif2)) + (
                            (color3 * verticalDif1) / (verticalDif1 + verticalDif2))
                    verticalColor2 = ((color2 * verticalDif2) / (verticalDif1 + verticalDif2)) + (
                            (color4 * verticalDif1) / (verticalDif1 + verticalDif2))

            if verticalColor2 == -1:
                zoomed[i, j] = verticalColor1
            else:
                horizontalDif1 = j - tmpCol * scale
                horizontalDif2 = (tmpCol + 1) * scale - j
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
