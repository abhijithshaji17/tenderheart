import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parametric heart shape
t = np.linspace(0, 2 * np.pi, 1000)
x_heart = 16 * np.sin(t)**3
y_heart = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

# Setup figure
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect('equal')
ax.axis('off')

# Main elements
glow_line, = ax.plot([], [], color='magenta', linewidth=15, alpha=0.05)
heart_line, = ax.plot([], [], color='deeppink', linewidth=2.5)
heart_fill = ax.fill([], [], color='hotpink', alpha=0.4)[0]

# Generate random sparkles inside the heart shape
num_sparkles = 80
sparkle_x = []
sparkle_y = []

while len(sparkle_x) < num_sparkles:
    x_try = np.random.uniform(-16, 16)
    y_try = np.random.uniform(-17, 13)
    # Heart shape inequality (inside region)
    if (x_try**2 + (5*y_try/13 - np.sqrt(abs(x_try)))**2) < 256:
        sparkle_x.append(x_try)
        sparkle_y.append(y_try)

# Create sparkle scatter plot
sparkle_plot = ax.scatter(sparkle_x, sparkle_y, s=15, color='white', alpha=0)

# Frame count
draw_frames = len(t)
pulse_frames = 200
total_frames = draw_frames + pulse_frames

# Update function
def update(frame):
    if frame < draw_frames:
        xi = x_heart[:frame]
        yi = y_heart[:frame]
        heart_line.set_data(xi, yi)
        glow_line.set_data(xi, yi)
        if frame > 3:
            heart_fill.set_xy(np.column_stack([xi, yi]))
            sparkle_plot.set_alpha(0)  # Hide sparkles during draw
    else:
        # Pulsing
        pulse_frame = frame - draw_frames
        pulse = 0.4 + 0.2 * np.sin(pulse_frame * 0.2)
        heart_fill.set_alpha(pulse)
        glow_line.set_alpha(0.05 + 0.05 * np.sin(pulse_frame * 0.2))

        # Sparkle twinkling (random alpha variation)
        sparkle_alpha = 0.3 + 0.7 * np.abs(np.sin(pulse_frame * 0.3 + np.linspace(0, 6, num_sparkles)))
        sparkle_plot.set_alpha(sparkle_alpha)

    return heart_line, glow_line, heart_fill, sparkle_plot

# Animate
ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=10, blit=True)

# Show
plt.show()
