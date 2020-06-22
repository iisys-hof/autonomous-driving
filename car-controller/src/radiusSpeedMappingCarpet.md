# Radius Speed Mapping

I have the problem that the curve driving is not like expected.
For that i want do do a view measurements to get a better approximation on gerarate/speed and radius form the car.

The idea is, the inside wheel drives every time with a commanded value form 20.
Then i measure the radius, time for different outside wheel speeds.

I am not able to drive very big circles , so i measure with a fix distance and use the delta x.


Floor: carpet

Inner Wheel(cmd) | Outer Wheel(cmd) | Duration(s) |  Staus | deltaX (cm) |deltaY (cm) | calculated Duration(s) | calculated Diameter(cm)
--- | --- | --- | --- | --- | ---  | ---  | --- 
30 | 30 |  15,6 | radius extrapolation | 0 | 356 | infinity | infinity
29 | 30 | 15,9 | radius extrapolation  | 15 | 356 | 1186 | 88464
28 | 30 | 16,5 |radius extrapolation  | 52 | 356 | 357 | 2490
27 | 30 | 17,0 |radius extrapolation  | 85 | 356 | 228 | 1576
26 | 30 | 17,9 |radius extrapolation  | 99 | 356 | 207 | 1380
25 | 30 | 19,5 |radius extrapolation  | 132 | 356 | 173 | 1092
24 | 30 | 23,5 |radius extrapolation  | 240 | 356 | 124 | 768
23 | 30 | 22,3 |radius extrapolation  |318 | 257 | 80 | 526
22 | 30 | 21,8 |radius extrapolation   | 318 |  278 | 80 | 480
21 | 30 | 22 |radius extrapolation | 217 | 217 | 80 | 434

For the callaction of the table above i Used:
alpha = arctan(deltaX/delatY)*2
r = deltaY/sin(alpha)
durationComplete = 2*PI/alpha*duration

Inner Wheel(cmd) | Outer Wheel(cmd) | Duration(s) |  Diameter(cm) | Staus
--- | --- | --- | --- | ---
20 | 30 | 76,8 | 384 | standing
20 | 35 | 50,8 | 272 | standing
20 | 40 | 36,4 | 234 | standing
20 | 45 | 26,8 | 206 | standing
20 | 50 | 18,4 | 132 | standing 
20 | 60 | 13,5 | 110 | standing
20 | 70 | 10,5  | 96 | standing
20 | 80 |  8,4 | 85 | standing
20 | 90 |  7,1 | 78 | standing
20 | 100 | 6,4  | 73 | standing
15 | 100 | 6,0 | 70 | standing
12 | 100 | 5,3 | 21 | standing
10 | 100 | 5,5 | 17  | standing
12 | 100 | 5,3 | 66 | moving
10 | 100 | 5,3 | 66| moving