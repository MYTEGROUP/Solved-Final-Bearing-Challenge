import math
"""

challenge Author: @TimelessP (on X)
Challenge Date: 2024-09-19 22:07:32
Challenge Description: (see the prompt example below)
Gist URL: https://gist.github.com/TimelessP/f1124f7c1556d0b614c4871757287885

---

Solution Metadata
Solution Author: Ahmed Mekallach
Solution Date: [2024-10-24]
Solution Version: [v1.0]

---

Prompt Example:

A starting prompt to explain the goal, but, most importantly, a solution function must pass the given unit tests:
Okay, let's step it up. I need a python function written as per the following requirements: 
A function that takes parameters start_lat_deg, start_lon_deg (as floats), start_bearing_deg, and the final parameter is a fraction of 1.0, 
where 1.0 is the full distance around the great circle of a sphere to travel. 
So, 0.25 takes you a quarter of the way around the great circle.  
The function will calculate the bearing at the destination as you've travelled in that direction around the great circle. 
The end_bearing, end_lat, end_lon will be returned. 
Assume it's a perfect sphere, and polar north and magnetic north are in the same position 
(i.e. we want a simple sphere model here to find the final bearing at the destination).


"""



def great_circle_navigation_perfect(start_lat_deg, start_lon_deg, start_bearing_deg, fraction):
    """
    Computes the final latitude, longitude, and bearing after traveling a certain fraction
    around a great circle of a perfect sphere from a starting point with a given initial bearing.

    Parameters:
    start_lat_deg (float): Starting latitude in degrees (-90.0 to 90.0), positive north.
    start_lon_deg (float): Starting longitude in degrees (-180.0 to 180.0), positive east.
    start_bearing_deg (float): Initial bearing in degrees (0.0 to 360.0), measured clockwise from north.
    fraction (float): Fraction of the great circle to travel (from 0.0 to 1.0).
                      A fraction of 1.0 corresponds to a full circumnavigation.

    Returns:
    (float, float, float): Tuple containing the final latitude, longitude, and bearing in degrees.
                           The latitude is between -90.0 and 90.0 degrees.
                           The longitude is between -180.0 and 180.0 degrees.
                           The bearing is between 0.0 and 360.0 degrees.
    """

    # Convert input degrees to radians
    lat1 = math.radians(start_lat_deg)
    lon1 = math.radians(start_lon_deg)
    bearing1 = math.radians(start_bearing_deg)

    # Calculate angular distance
    angular_distance = fraction * 2 * math.pi
    delta = angular_distance % (2 * math.pi)  # Normalize angular distance

    # Precompute trigonometric functions
    sin_lat1 = math.sin(lat1)
    cos_lat1 = math.cos(lat1)
    sin_angular_distance = math.sin(angular_distance)
    cos_angular_distance = math.cos(angular_distance)
    sin_bearing1 = math.sin(bearing1)
    cos_bearing1 = math.cos(bearing1)

    # Compute destination latitude
    sin_lat2 = sin_lat1 * cos_angular_distance + cos_lat1 * sin_angular_distance * cos_bearing1
    lat2 = math.asin(sin_lat2)

    # Compute destination longitude
    y = sin_bearing1 * sin_angular_distance * cos_lat1
    x = cos_angular_distance - sin_lat1 * sin_lat2
    lon2 = lon1 + math.atan2(y, x)
    # Normalize longitude to be between -π and +π radians
    lon2 = (lon2 + math.pi) % (2 * math.pi) - math.pi

    # Convert latitude and longitude back to degrees
    end_lat_deg = math.degrees(lat2)
    end_lon_deg = math.degrees(lon2)

    # Compute the back azimuth (bearing from destination to start)
    back_azimuth = math.atan2(y, x)
    end_bearing_deg = (math.degrees(back_azimuth) + 360) % 360

    # Adjust the final bearing based on angular distance
    if math.isclose(delta, 0.0, abs_tol=1e-12) or math.isclose(delta, 2 * math.pi, abs_tol=1e-12):
        # No movement or full circumnavigation: bearing remains the same
        arrival_bearing_deg = start_bearing_deg % 360
    elif math.isclose(delta, math.pi, abs_tol=1e-12):
        # Halfway around the circle: bearing is perpendicular to the initial bearing
        arrival_bearing_deg = (start_bearing_deg + 90) % 360
    elif delta > math.pi:
        # More than halfway: bearing is opposite to the back azimuth
        arrival_bearing_deg = (end_bearing_deg + 180) % 360
    else:
        # Less than halfway: bearing is the back azimuth
        arrival_bearing_deg = end_bearing_deg

    return end_lat_deg, end_lon_deg, arrival_bearing_deg


def test_great_circle_navigation():
    """
    Unit tests to check if the function is performing as expected.
    """

    # Helper function for almost equal comparison.
    def almost_equal(val1, val2, tol=1e-4):
        return math.isclose(val1, val2, abs_tol=tol)

    # Test Case 1: Start at 0, 0 with a bearing of 0, travelling 25% around the circle.
    result1 = great_circle_navigation_perfect(0, 0, 0, 0.25)
    print(f"1. expected (90, 0, 0), actual {result1=}")
    assert almost_equal(result1[0], 90.0) and almost_equal(result1[1], 0.0) and almost_equal(result1[2],
                                                                                             0.0), "Test Case 1 Failed"

    # Test Case 2: Start at 0, 0 with a bearing of 45, travelling 25% around the circle.
    result2 = great_circle_navigation_perfect(0, 0, 45.0, 0.25)
    print(f"2. expected (45, 90, 90), actual {result2=}")
    assert almost_equal(result2[0], 45.0) and almost_equal(result2[1], 90.0) and almost_equal(result2[2],
                                                                                              90.0), "Test Case 2 Failed"

    # Test Case 3: Start at 0, 0 with a bearing of 45, travelling 75% around the circle.
    result3 = great_circle_navigation_perfect(0, 0, 45.0, 0.7500001)
    print(f"3. expected (-45, -90, 90), actual {result3=}")
    assert almost_equal(result3[0], -45.0) and almost_equal(result3[1], -90.0) and almost_equal(result3[2],
                                                                                                90.0), "Test Case 3 Failed"

    # Test Case 4: Start at 0, 0 with a bearing of 45, travelling halfway around the circle.
    expected_bearing = (45 + 90) % 360  # Final bearing should be 45 + 90 = 135 degrees
    result4 = great_circle_navigation_perfect(0, 0, 45.0, 0.5)
    print(f"4. expected (0, 180, 135), actual {result4=}")
    assert almost_equal(result4[0], 0.0) and (
                almost_equal(result4[1], 180.0) or almost_equal(result4[1], -180.0)) and almost_equal(result4[2],
                                                                                                      expected_bearing), "Test Case 4 Failed"

    # Test Case 5: Start at 0, 0 with a bearing of 45, travelling all the way around the circle.
    result5 = great_circle_navigation_perfect(0, 0, 45.0, 1.0)
    print(f"5. expected (0, 0, 45), actual {result5=}")
    assert almost_equal(result5[0], 0.0) and almost_equal(result5[1], 0.0) and almost_equal(result5[2],
                                                                                            45.0), "Test Case 5 Failed"

    print("All test cases passed! Please double check that the unit tests were not modified in the process.")

if __name__ == "__main__":
    # Run the tests

    test_great_circle_navigation()

    #testing other values? Are they right?
    end_lat_deg, end_lon_deg, arrival_bearing_deg = great_circle_navigation_perfect(0, 0, 60, 0.10)
    print(f"{end_lat_deg}, {end_lon_deg}, {arrival_bearing_deg}")