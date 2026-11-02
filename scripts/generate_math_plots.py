import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Style configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern LaTeX style
plt.rcParams['axes.unicode_minus'] = False

IMG_DIR = os.path.join('projects', 'math_assets')
os.makedirs(IMG_DIR, exist_ok=True)

def generate_quadratic_plot():
    fig, ax = plt.subplots(figsize=(6, 4.2), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(-4, 4, 300)
    a, p, q = 1, 1, -2  # f(x) = (x-1)^2 - 2
    y = a * (x - p)**2 + q
    
    ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = (x - 1)^2 - 2$')
    ax.plot([p], [q], marker='o', markersize=8, color='#f43f5e', label=r'$\mathrm{Vertex:}\ (1, -2)$')
    ax.axvline(p, color='#fbbf24', ls='--', lw=1.5, alpha=0.8, label=r'$\mathrm{Axis:}\ x = 1$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 6)
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$f(x) = a(x - p)^2 + q \quad (a=1, p=1, q=-2)$', color='#f8fafc', fontsize=12, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=9, loc='upper left')
    
    path = os.path.join(IMG_DIR, 'graph_quadratic.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

def generate_trig_plot():
    fig, ax = plt.subplots(figsize=(6, 4.2), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(-2*np.pi, 2*np.pi, 400)
    y1 = np.sin(x)
    y2 = 2 * np.sin(2 * x)
    
    ax.plot(x, y1, color='#94a3b8', lw=1.8, ls='--', alpha=0.7, label=r'$y = \sin(x)\ (T=2\pi, A=1)$')
    ax.plot(x, y2, color='#38bdf8', lw=2.8, label=r'$y = 2\sin(2x)\ (T=\pi, A=2)$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    ax.set_xlim(-2*np.pi, 2*np.pi)
    ax.set_ylim(-2.8, 2.8)
    ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
    ax.set_xticklabels([r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$'])
    
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$y = A\sin(Bx) \quad (\mathrm{Amplitude}=|A|,\ \mathrm{Period}=\frac{2\pi}{|B|})$', color='#f8fafc', fontsize=11, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=9, loc='upper right')
    
    path = os.path.join(IMG_DIR, 'graph_trig.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

def generate_calculus_derivative_plot():
    fig, ax = plt.subplots(figsize=(6, 4.2), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(-1, 3.5, 300)
    def f(t): return 0.4 * t**3 - 1.2 * t**2 + t + 1
    def df(t): return 1.2 * t**2 - 2.4 * t + 1
    
    y = f(x)
    a = 2.0
    fa = f(a)
    slope = df(a)
    tangent_y = fa + slope * (x - a)
    
    ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = 0.4x^3 - 1.2x^2 + x + 1$')
    ax.plot(x, tangent_y, color='#fbbf24', lw=2.2, ls='-', label=rf'$\mathrm{{Tangent\ at\ }} x=2: m = {slope:.2f}$')
    ax.plot([a], [fa], marker='o', markersize=8, color='#f43f5e', label=rf'$P({a:.1f}, {fa:.1f})$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    ax.set_xlim(-0.5, 3.2)
    ax.set_ylim(-1, 4.5)
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$f^\prime(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$', color='#f8fafc', fontsize=12, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=9, loc='upper left')
    
    path = os.path.join(IMG_DIR, 'graph_derivative.png')
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")
    return path

def generate_calculus_integral_plot():
    fig, ax = plt.subplots(figsize=(6, 4.2), dpi=200, facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    x = np.linspace(0, 4, 300)
    def f(t): return -0.5 * (t - 2)**2 + 3
    y = f(x)
    
    ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = -0.5(x-2)^2 + 3$')
    
    # Riemann boxes
    a, b, n = 0.5, 3.5, 8
    dx = (b - a) / n
    for i in range(n):
        xi = a + i * dx
        yi = f(xi + dx/2)
        ax.bar(xi + dx/2, yi, width=dx, alpha=0.35, color='#fbbf24', edgecolor='#f59e0b', align='center')
        
    # Shaded exact area
    x_fill = np.linspace(a, b, 200)
    y_fill = f(x_fill)
    ax.fill_between(x_fill, 0, y_fill, color='#38bdf8', alpha=0.2, label=r'$\mathrm{Area:}\ S = \int_{0.5}^{3.5} f(x)\,dx$')
    
    ax.axhline(0, color='#64748b', lw=1.2)
    ax.axvline(0, color='#64748b', lw=1.2)
    
    ax.set_xlim(0, 4)
    ax.set_ylim(-0.5, 3.6)
    ax.grid(True, color='#334155', ls=':', lw=0.8)
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
        
    ax.set_title(r'$\int_a^b f(x)\,dx = \lim_{n \to \infty} \sum_{k=1}^n f(x_k^*)\Delta x$', color='#f8fafc', fontsize=12, pad=10)
    ax.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='#e2e8f0', fontsize=9, loc='upper right')
    
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

