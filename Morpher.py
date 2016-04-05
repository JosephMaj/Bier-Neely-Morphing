
_author__ = 'root'
import math
import Image

import FeatureDetector  # SOMEHOW MAGIC HAPPENS AND IT RUNS. I DON'T THINK PYTHON IS SUPPOSED TO WORK LIKE THAT

# get hash map
Line_Map = FeatureDetector.get_map()
Seed_Image_array = FeatureDetector.get_images()

# check it worked
# Note the map is the Line segment, the start or end point, the x or y
for key in Line_Map:
    print(Line_Map[key])
print("\n\n")

# Make Array of base images

Morphed_Images_Array = [Seed_Image_array[0], Seed_Image_array[1]]

# TODO HARDCODED ARRAY

def make_warp_coordiantes(line_map, source_img, dest_img):
    print(dest_img.shape)
    print(dest_img[100][120])
    print("\n\n\n")

    # Useful variables

    dest_im_hash = hash(dest_img.tostring())
    source_im_hash = hash(source_img.tostring())

    warp = []

    for y in range(0, len(dest_img)):  # 25):
        warp.append([])
        for x in range(0, len(dest_img[y])):  # 25)

            DSUM =[0,0]
            Weight_sum = 0.0
            z = 0

            lt=len(line_map[dest_im_hash])

            for z in range(0, lt):
                # u=( (X-P) * (Q-P) ) / ||Q-P||^2
                p = line_map[dest_im_hash][z][0]

                q=line_map[dest_im_hash][z][1]

                x_minus_p = (x - p[0], y - p[1])

                q_minus_p = (q[0] - p[0],
                             q[1] - p[1])

                dot_product = x_minus_p[0] * q_minus_p[0] + x_minus_p[1] * q_minus_p[1]

                magnitude_of_line = (math.sqrt(q_minus_p[0] * q_minus_p[0] + q_minus_p[1] * q_minus_p[1]))

                u = dot_product / (magnitude_of_line ** 2)

                # v = ( x_minus_p * Perp(Q-P) ) / || Q - P ||

                perpendicular = (-q_minus_p[1], q_minus_p[0])

                dot_product_of_perp_and_x_minus_p = x_minus_p[0] * perpendicular[0] + x_minus_p[1] * perpendicular[1]

                v = dot_product_of_perp_and_x_minus_p / magnitude_of_line

                # Co-ordinate in source image
                # X' = P' + u * (Q'-P') +  ((v * Perp( Q' - P' ) ) / ||Q'-P'||)

                p_prime = line_map[source_im_hash][z][0]

                q_prime = line_map[source_im_hash][z][1]

                q_prime_minus_p_prime = (q_prime[0] - p_prime[0], q_prime[1] - p_prime[1])

                perpendicular_of_source = (-q_prime_minus_p_prime[1], q_prime_minus_p_prime[0])

                magnitude_prime = (math.sqrt(
                    q_prime_minus_p_prime[0]**2 + q_prime_minus_p_prime[1]**2))

                source_coordinate_pre_weighting = (
                    (p_prime[0] + u * q_prime_minus_p_prime[0] + ((v * perpendicular_of_source[0]) / magnitude_prime)),
                    (p_prime[1] + u * q_prime_minus_p_prime[1] + ((v * perpendicular_of_source[1]) / magnitude_prime)))

                displacement = (source_coordinate_pre_weighting[0] - x, source_coordinate_pre_weighting[1] - y)


                #sketchy
                dist = float(math.fabs(float((q[1]-p[1])* float(x) - (q[0]-p[0])*float(y) + q[0]*p[1] - q[1]*p[0])) / float(magnitude_of_line))

                #boring weight


                #print(magnitude_of_line)
                #print(dist)

                weight= (float(magnitude_of_line)**0.0 / (dist+.001))**1.0


                DSUM[0] = DSUM[0] + weight * displacement[0]
                DSUM[1] = DSUM[1] + weight * displacement[1]
                Weight_sum =Weight_sum +weight

                #warp[y].append(source_coordinate_pre_weighting)


            #maybe?
            source_coordinate_weighted = ((x + DSUM[0]/ Weight_sum ), (y+ DSUM[1]/Weight_sum))

            warp[y].append(source_coordinate_weighted)

            #print("Original: " + str(x) + "," + str(y))
            #print ("u " + str(u))
            #print "v: " + str(v)
            #print("Warp: " + str(source_coordinate_weighted[0]), str(source_coordinate_weighted[1]))
    return warp


def make_wrapped_image(warped_coordinates, source_weight, dest_weight):
    img = Image.new('RGB', (256, 256), "white")  # create a new black image
    pixels = img.load()  # create the pixel map

    for i in range(0, 256):  # for every pixel:
        for j in range(0, 256):

            # TODO FIND BEST LINE TO WARP FROM

            if warped_coordinates[i][j][0] >= 0 and warped_coordinates[i][j][1] >= 0 and warped_coordinates[i][j][0] < 256 and warped_coordinates[i][j][1] < 256:

                source_pixel = tuple(
                    Morphed_Images_Array[0][int(warped_coordinates[i][j][0])][int(warped_coordinates[i][j][1])])

                # print Morphed_Images_Array[1][i][j][0]
                blend_x = int(((source_pixel[2]) * source_weight + (Morphed_Images_Array[1][j][i][2]) * dest_weight))
                blend_y = int(((source_pixel[1]) * source_weight + (Morphed_Images_Array[1][j][i][1]) * dest_weight))
                blend_z = int(((source_pixel[0]) * source_weight + (Morphed_Images_Array[1][j][i][0]) * dest_weight))
                #print(blend_x, blend_y, blend_z)
                pixels[i, j] = (blend_x, blend_y, blend_z)

                # tuple( Morphed_Images_Array[0][int(warped_coordinates[i][j][0])][int(warped_coordinates[i][j][1])])

            else:
                pixels[i, j] = (Morphed_Images_Array[1][j][i][2], Morphed_Images_Array[1][j][i][1], Morphed_Images_Array[1][j][i][0])

    img.save("S:" + str(source_weight) + "D:" + str(dest_weight) + ".png")
    img.show()

    return pixels


warp_map = make_warp_coordiantes(Line_Map, Morphed_Images_Array[0], Morphed_Images_Array[1])

# for x in range(0, 11):
make_wrapped_image(warp_map, source_weight=(0.5), dest_weight=(0.5))