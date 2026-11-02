import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Style configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['axes.unicode_minus'] = False

IMG_DIR = os.path.join('projects', 'math_assets')
os.makedirs(IMG_DIR, exist_ok=True)

def annotate_badge(ax, x, y, label, color='#38bdf8', offset=(10, 10), show_proj=True):
    ax.plot([x], [y], marker='o', markersize=6.5, color=color, zorder=6)
    if show_proj:
        ax.plot([x, x], [0, y], color=color, ls=':', lw=1.1, alpha=0.6, zorder=4)
        ax.plot([0, x], [y, y], color=color, ls=':', lw=1.1, alpha=0.6, zorder=4)
    bbox = dict(boxstyle='round,pad=0.25', facecolor='#0f172a', edgecolor=color, alpha=0.9, lw=1.1)
    ax.annotate(
        label,
        xy=(x, y),
        xytext=offset,
        textcoords='offset points',
        color='#f8fafc',
        fontsize=8,
        fontweight='bold',
        bbox=bbox,
        zorder=7,
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.08', color=color, lw=0.9, alpha=0.8)
    )

def generate_quadratic_plot():
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(-3.5, 4.5, 300)
    a, p, q = 1, 1, -2  # f(x) = (x-1)^2 - 2
    y = a * (x - p)**2 + q
    
    ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = (x - 1)^2 - 2$')
    ax.axvline(p, color='#fbbf24', ls='--', lw=1.3, alpha=0.75, label=r'$\mathrm{Axis:}\ x = 1$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    annotate_badge(ax, 1, -2, 'Vertex V(1, -2)', color='#f43f5e', offset=(14, -18))
    
    # 2. y-intercept (0, -1)
    annotate_badge(ax, 0, -1, 'y-int (0, -1)', color='#a855f7', offset=(-75, 10))
    
    # 3. x-intercepts (1 ± sqrt(2), 0) => -0.41, 2.41
    r1 = 1 - np.sqrt(2)
    r2 = 1 + np.sqrt(2)
    annotate_badge(ax, r1, 0, f'x1({r1:.2f}, 0)', color='#10b981', offset=(-68, 14), show_proj=False)
    annotate_badge(ax, r2, 0, f'x2({r2:.2f}, 0)', color='#10b981', offset=(10, 14), show_proj=False)
    
    ax.set_xlim(-3, 4.5)
    ax.set_ylim(-3.5, 5.5)
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$f(x) = x^2 - 2x - 1$' + '  [Vertex, x/y-Intercepts]', color='#f8fafc', fontsize=11, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=8.5, loc='upper left')
    
    path = os.path.join(IMG_DIR, 'graph_quadratic.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

def generate_trig_plot():
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(-2*np.pi, 2*np.pi, 400)
    y2 = 2 * np.sin(2 * x)
    
    ax.plot(x, y2, color='#38bdf8', lw=2.8, label=r'$y = 2\sin(2x)\ (T=\pi,\ A=2)$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    # 1. Extrema / Peaks & Troughs
    annotate_badge(ax, np.pi/4, 2.0, r'Peak $(\frac{\pi}{4}, 2)$', color='#fbbf24', offset=(8, 12))
    annotate_badge(ax, 3*np.pi/4, -2.0, r'Trough $(\frac{3\pi}{4}, -2)$', color='#fbbf24', offset=(-50, -22))
    
    # 2. Intersections with x-axis
    annotate_badge(ax, 0, 0, '(0, 0)', color='#a855f7', offset=(-45, 12), show_proj=False)
    annotate_badge(ax, np.pi/2, 0, r'$(\frac{\pi}{2}, 0)$', color='#10b981', offset=(8, -20), show_proj=False)
    annotate_badge(ax, np.pi, 0, r'$(\pi, 0)$', color='#10b981', offset=(8, -20), show_proj=False)
    
    ax.set_xlim(-0.5, 2*np.pi + 0.5)
    ax.set_ylim(-2.8, 2.8)
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels([r'$0$', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
    
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$y = 2\sin(2x)$' + '  [Peaks, Troughs & Zero Crossings]', color='#f8fafc', fontsize=11, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=8.5, loc='upper right')
    
    path = os.path.join(IMG_DIR, 'graph_trig.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

def generate_calculus_derivative_plot():
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(-1.5, 3.2, 350)
    def f(t): return 0.5 * t**3 - 1.5 * t + 1
    def df(t): return 1.5 * t**2 - 1.5
    
    y = f(x)
    x0 = 1.6
    y0 = f(x0)
    slope = df(x0)
    tangent_y = y0 + slope * (x - x0)
    
    ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = 0.5x^3 - 1.5x + 1$')
    ax.plot(x, tangent_y, color='#fbbf24', lw=2.2, ls='-', label=rf'$\mathrm{{Tangent:}}\ m = {slope:.2f}$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    # 1. Moving Tangent Point P(x0, y0)
    annotate_badge(ax, x0, y0, f'P({x0:.1f}, {y0:.2f})', color='#f43f5e', offset=(12, -22))
    
    # 2. Curve y-intercept (0, 1)
    annotate_badge(ax, 0, 1.0, 'y-int (0, 1)', color='#a855f7', offset=(-65, 12))
    
    # 3. Tangent y-intercept (0, y0 - slope*x0)
    y_tan_int = y0 - slope * x0
    annotate_badge(ax, 0, y_tan_int, f'Tan y0(0, {y_tan_int:.2f})', color='#eab308', offset=(-85, -18))
    
    # 4. Second intersection Q: for 0.5*x^3, sum of roots = 0 => x_Q = -2*x0
    x_q = -2 * x0
    y_q = f(x_q)
    if -1.4 <= x_q <= 3.0:
        annotate_badge(ax, x_q, y_q, f'Int Q({x_q:.1f}, {y_q:.2f})', color='#38bdf8', offset=(10, 12))
        
    ax.set_xlim(-1.4, 3.0)
    ax.set_ylim(-3.5, 4.5)
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$f(x) = 0.5x^3 - 1.5x + 1$' + '  [Tangent P, Intercepts & Q]', color='#f8fafc', fontsize=11, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=8.5, loc='upper left')
    
    path = os.path.join(IMG_DIR, 'graph_derivative.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

def generate_calculus_integral_plot():
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(0, 4.2, 300)
    def f(t): return -0.5 * (t - 2)**2 + 3
    y = f(x)
    
    ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = -0.5(x-2)^2 + 3$')
    
    # Riemann boxes
    a, b, n = 0.6, 3.4, 7
    dx = (b - a) / n
    for i in range(n):
        xi = a + i * dx
        yi = f(xi + dx/2)
        ax.bar(xi + dx/2, yi, width=dx, alpha=0.35, color='#fbbf24', edgecolor='#f59e0b', align='center')
        
    # Shaded exact area
    x_fill = np.linspace(a, b, 200)
    y_fill = f(x_fill)
    ax.fill_between(x_fill, 0, y_fill, color='#38bdf8', alpha=0.2, label=r'$\mathrm{Area:}\ S = \int_{0.6}^{3.4} f(x)\,dx$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    # 1. Integration Boundary Points
    annotate_badge(ax, a, f(a), f'A({a:.1f}, {f(a):.2f})', color='#38bdf8', offset=(-60, 12))
    annotate_badge(ax, b, f(b), f'B({b:.1f}, {f(b):.2f})', color='#f43f5e', offset=(10, 12))
    
    # 2. Maximum / Vertex
    annotate_badge(ax, 2.0, 3.0, 'Max (2, 3)', color='#fbbf24', offset=(-35, 14))
    
    # 3. y-intercept (0, 1)
    annotate_badge(ax, 0, 1.0, 'y-int (0, 1)', color='#a855f7', offset=(10, -16))
    
    ax.set_xlim(0, 4.2)
    ax.set_ylim(-0.5, 3.8)
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$\int_a^b f(x)\,dx$' + '  [Boundaries A, B, Vertex & y-int]', color='#f8fafc', fontsize=11, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=8.5, loc='upper right')
    
    path = os.path.join(IMG_DIR, 'graph_integral.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

if __name__ == '__main__':
    generate_quadratic_plot()
    generate_trig_plot()
    generate_calculus_derivative_plot()
    generate_calculus_integral_plot()
