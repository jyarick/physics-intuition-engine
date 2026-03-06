EXAMPLES = {
    "Undamped oscillator": "m*diff(x(t), t, 2) + k*x(t) = 0",
    "Damped oscillator": "m*diff(x(t), t, 2) + b*diff(x(t), t) + k*x(t) = 0",
    "Driven damped oscillator": "m*diff(x(t), t, 2) + b*diff(x(t), t) + k*x(t) = F0*cos(omega*t)",
    "Constant forcing": "m*diff(x(t), t, 2) + b*diff(x(t), t) + k*x(t) = F0",
    "Critical damping example": "diff(x(t), t, 2) + 4*diff(x(t), t) + 4*x(t) = 0",
}