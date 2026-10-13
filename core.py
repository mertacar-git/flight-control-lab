import math

def simulate(kp=1.0, ki=0.1, kd=1.5, target=20.0, duration=40.0, dt=0.02, gust=0.0):
    values = [kp, ki, kd, target, duration, dt, gust]
    if not all(math.isfinite(v) for v in values) or min(kp, ki, kd) < 0 or not 0 < dt <= 0.1 or not 0 < duration <= 120:
        raise ValueError('Invalid gains, timestep or duration.')
    altitude = velocity = integral = 0.0
    rows = []
    for i in range(int(duration/dt)+1):
        t = i*dt
        error = target-altitude
        requested = kp*error + ki*integral - kd*velocity
        command = max(-10.0, min(10.0, requested))
        rows.append(dict(time_s=t, altitude_m=altitude, velocity_ms=velocity, command_ms2=command, error_m=error))
        if abs(requested) <= 10 or error*requested < 0:
            integral += error*dt
        disturbance = gust if 10 <= t < 12 else 0.0
        velocity += (command-0.3*velocity+disturbance)*dt
        altitude += velocity*dt
    return rows
