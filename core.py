import math

def simulate(kp=1.0, ki=0.1, kd=1.5, target=20.0, duration=40.0, dt=0.02, gust=0.0):
    values = [kp, ki, kd, target, duration, dt, gust]
    if not all(math.isfinite(v) for v in values) or min(kp, ki, kd) < 0 or not 0.001 <= dt <= 0.1 or not dt <= duration <= 120 or target < 0:
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

def metrics(rows, target):
    errors = [r['error_m'] for r in rows]
    tolerance = max(abs(target)*0.02, 0.01)
    outside = [i for i, error in enumerate(errors) if abs(error) > tolerance]
    index = outside[-1]+1 if outside else 0
    settling = rows[index]['time_s'] if index < len(rows) else None
    rising = [r['time_s'] for r in rows if target > 0 and r['altitude_m'] >= 0.9*target]
    integral_error = sum((abs(a['error_m'])+abs(b['error_m']))*0.5*(b['time_s']-a['time_s']) for a,b in zip(rows,rows[1:]))
    return dict(overshoot_m=max(0, max(r['altitude_m'] for r in rows)-target),
                final_error_m=errors[-1], settling_time_s=settling,
                rise_time_90_s=rising[0] if rising else None,
                integral_absolute_error_ms=integral_error,
                saturation_pct=100*sum(abs(r['command_ms2']) >= 10 for r in rows)/len(rows))
