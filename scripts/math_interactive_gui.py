import os
import sys
import tempfile
import glob

# Ensure writable matplotlib config directory
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.widgets import Slider, Button, RadioButtons

# 1. Unbind default Matplotlib keymaps that hijack arrow keys
for k in ['keymap.back', 'keymap.forward', 'keymap.pan', 'keymap.zoom', 'keymap.home']:
    plt.rcParams[k] = ''

# 2. Register Paperlogy Fonts from project folder & system fonts
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
font_dirs = [
    os.path.join(base_dir, 'Paperlogy'),
    os.path.join(base_dir, 'projects', 'math_assets', 'fonts'),
    os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'),
    r'C:\Windows\Fonts',
]

paper_registered = False
for d in font_dirs:
    if os.path.exists(d):
        for font_file in glob.glob(os.path.join(d, 'Paperlogy*.ttf')):
            try:
                fm.fontManager.addfont(font_file)
                paper_registered = True
            except Exception:
                pass

FONT_FAMILY = 'Paperlogy' if paper_registered else 'Malgun Gothic'
plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['font.sans-serif'] = [FONT_FAMILY, 'Malgun Gothic', '맑은 고딕', 'sans-serif']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['axes.unicode_minus'] = False


class MathInteractiveApp:
    def __init__(self):
        self.fig = plt.figure(figsize=(11.5, 7.2), facecolor='#0f172a')
        self.fig.canvas.manager.set_window_title("수학교사용 인터랙티브 시뮬레이터 (Paperlogy Font + LaTeX + Dynamic GUI)")
        
        self.mode = 0
        self.active_slider_idx = 0
        self.sliders = []
        
        # Main axes
        self.ax = self.fig.add_axes([0.08, 0.28, 0.62, 0.64], facecolor='#1e293b')
        self.setup_ui()
        self.update_plot()
        
        # Connect keyboard events
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def setup_ui(self):
        # 1. Mode Selection Radio Buttons
        ax_radio = self.fig.add_axes([0.74, 0.65, 0.23, 0.25], facecolor='#1e293b')
        self.radio = RadioButtons(
            ax_radio, 
            ('1. 이차함수 (Quadratic)', '2. 삼각함수 (Trig Wave)', '3. 미분 접선 (Tangent)', '4. 정적분 리만합 (Integral)'),
            activecolor='#38bdf8'
        )
        for label in self.radio.labels:
            label.set_color('#f8fafc')
            label.set_fontsize(10)
            label.set_fontfamily(FONT_FAMILY)
        self.radio.on_clicked(self.on_mode_change)

        # 2. Information Display Text Box
        self.ax_info = self.fig.add_axes([0.74, 0.28, 0.23, 0.32], facecolor='#1e293b')
        self.ax_info.axis('off')
        self.info_text = self.ax_info.text(
            0.05, 0.95, "", 
            color='#e2e8f0', fontsize=9.5, va='top', fontfamily=FONT_FAMILY,
            transform=self.ax_info.transAxes
        )

        # 3. Sliders Area with [-] and [+] step buttons
        slider_y = [0.16, 0.10, 0.04]
        self.ax_s1 = self.fig.add_axes([0.15, slider_y[0], 0.44, 0.035], facecolor='#334155')
        self.ax_s2 = self.fig.add_axes([0.15, slider_y[1], 0.44, 0.035], facecolor='#334155')
        self.ax_s3 = self.fig.add_axes([0.15, slider_y[2], 0.44, 0.035], facecolor='#334155')

        self.s1 = Slider(self.ax_s1, 'a: ', -3.0, 3.0, valinit=1.0, valstep=0.05, color='#38bdf8')
        self.s2 = Slider(self.ax_s2, 'b: ', -5.0, 5.0, valinit=-2.0, valstep=0.05, color='#fbbf24')
        self.s3 = Slider(self.ax_s3, 'c: ', -5.0, 5.0, valinit=0.0, valstep=0.05, color='#34d399')
        self.sliders = [self.s1, self.s2, self.s3]

        for s in self.sliders:
            s.label.set_color('#f8fafc')
            s.label.set_fontfamily(FONT_FAMILY)
            s.valtext.set_color('#38bdf8')
            s.valtext.set_fontfamily(FONT_FAMILY)
            s.on_changed(lambda val: self.update_plot())

        # Clickable Step Buttons [-] and [+] for each slider
        self.step_btns = []
        for i, y in enumerate(slider_y):
            ax_minus = self.fig.add_axes([0.60, y, 0.03, 0.035], facecolor='#334155')
            ax_plus = self.fig.add_axes([0.64, y, 0.03, 0.035], facecolor='#334155')
            
            b_minus = Button(ax_minus, '-', color='#334155', hovercolor='#475569')
            b_plus = Button(ax_plus, '+', color='#334155', hovercolor='#475569')
            
            b_minus.label.set_color('#f8fafc')
            b_minus.label.set_fontsize(11)
            b_minus.label.set_fontfamily(FONT_FAMILY)
            b_plus.label.set_color('#f8fafc')
            b_plus.label.set_fontsize(11)
            b_plus.label.set_fontfamily(FONT_FAMILY)
            
            idx = i
            b_minus.on_clicked(lambda event, s_idx=idx: self.step_slider(s_idx, -0.1))
            b_plus.on_clicked(lambda event, s_idx=idx: self.step_slider(s_idx, 0.1))
            self.step_btns.extend([b_minus, b_plus])

        # 4. Reset Button
        ax_reset = self.fig.add_axes([0.74, 0.08, 0.23, 0.06], facecolor='#334155')
        self.btn_reset = Button(ax_reset, '초기화 (Reset: R)', color='#334155', hovercolor='#475569')
        self.btn_reset.label.set_color('#f8fafc')
        self.btn_reset.label.set_fontsize(10)
        self.btn_reset.label.set_fontfamily(FONT_FAMILY)
        self.btn_reset.on_clicked(self.reset_values)

        # Bottom shortcut help text
        self.fig.text(
            0.08, 0.008, 
            "조작 방법: [마우스 클릭/드래그] 슬라이더 or [-][+] 버튼 | [키보드 1~4] 모드 전환 | [↑/↓] 계수 선택 | [←/→] 수치 조절 | [R] 초기화",
            color='#94a3b8', fontsize=9, fontfamily=FONT_FAMILY
        )

    def step_slider(self, s_idx, delta):
        s = self.sliders[s_idx]
        new_val = np.clip(s.val + delta, s.valmin, s.valmax)
        s.set_val(new_val)
        self.active_slider_idx = s_idx
        self.highlight_active_slider()

    def on_mode_change(self, label):
        if '이차함수' in label:
            self.mode = 0
            self.s1.label.set_text('a: ')
            self.s2.label.set_text('b: ')
            self.s3.label.set_text('c: ')
            self.s1.valmin, self.s1.valmax = -3.0, 3.0
            self.s2.valmin, self.s2.valmax = -5.0, 5.0
            self.s3.valmin, self.s3.valmax = -5.0, 5.0
            self.s1.set_val(1.0)
            self.s2.set_val(-2.0)
            self.s3.set_val(0.0)
        elif '삼각함수' in label:
            self.mode = 1
            self.s1.label.set_text('A (진폭): ')
            self.s2.label.set_text('B (주기): ')
            self.s3.label.set_text('C (위상): ')
            self.s1.valmin, self.s1.valmax = 0.2, 3.0
            self.s2.valmin, self.s2.valmax = 0.5, 4.0
            self.s3.valmin, self.s3.valmax = -np.pi, np.pi
            self.s1.set_val(1.5)
            self.s2.set_val(2.0)
            self.s3.set_val(0.0)
        elif '미분' in label:
            self.mode = 2
            self.s1.label.set_text('접점 x0: ')
            self.s2.label.set_text('곡선 a: ')
            self.s3.label.set_text('곡선 c: ')
            self.s1.valmin, self.s1.valmax = -2.5, 2.5
            self.s2.valmin, self.s2.valmax = 0.2, 2.0
            self.s3.valmin, self.s3.valmax = -3.0, 3.0
            self.s1.set_val(1.0)
            self.s2.set_val(0.5)
            self.s3.set_val(0.0)
        elif '정적분' in label:
            self.mode = 3
            self.s1.label.set_text('분할 n: ')
            self.s2.label.set_text('구간 a: ')
            self.s3.label.set_text('구간 b: ')
            self.s1.valmin, self.s1.valmax = 2, 50
            self.s2.valmin, self.s2.valmax = 0.0, 2.0
            self.s3.valmin, self.s3.valmax = 2.1, 4.5
            self.s1.set_val(8)
            self.s2.set_val(0.5)
            self.s3.set_val(3.5)
            
        for s in self.sliders:
            s.label.set_fontfamily(FONT_FAMILY)
        self.update_plot()

    def plot_point_badge(self, x, y, label, color='#38bdf8', offset=(10, 10), show_proj=True, marker='o', size=7):
        """Helper to plot a mathematical point with coordinates and dashed projections to axes"""
        self.ax.plot([x], [y], marker=marker, color=color, markersize=size, zorder=6)
        if show_proj:
            self.ax.plot([x, x], [0, y], color=color, ls=':', lw=1.1, alpha=0.6, zorder=4)
            self.ax.plot([0, x], [y, y], color=color, ls=':', lw=1.1, alpha=0.6, zorder=4)
        bbox = dict(boxstyle='round,pad=0.28', facecolor='#0f172a', edgecolor=color, alpha=0.9, lw=1.2)
        self.ax.annotate(
            label,
            xy=(x, y),
            xytext=offset,
            textcoords='offset points',
            color='#f8fafc',
            fontsize=8.5,
            fontfamily=FONT_FAMILY,
            fontweight='bold',
            bbox=bbox,
            zorder=7,
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.08', color=color, lw=1.0, alpha=0.8)
        )

    def update_plot(self):
        self.ax.clear()
        self.ax.set_facecolor('#1e293b')
        self.ax.grid(True, color='#334155', ls=':', lw=0.8)
        self.ax.axhline(0, color='#64748b', lw=1.2)
        self.ax.axvline(0, color='#64748b', lw=1.2)
        self.ax.tick_params(colors='#94a3b8', labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color('#475569')

        val1 = self.s1.val
        val2 = self.s2.val
        val3 = self.s3.val

        if self.mode == 0:
            a, b, c = val1, val2, val3
            x = np.linspace(-5, 5, 400)
            y = a * x**2 + b * x + c
            self.ax.plot(x, y, color='#38bdf8', lw=2.8, label=r'$f(x) = ax^2 + bx + c$')

            # 1. 꼭짓점 (Vertex)
            if abs(a) > 1e-5:
                vx = -b / (2 * a)
                vy = a * vx**2 + b * vx + c
                self.ax.axvline(vx, color='#fbbf24', ls='--', lw=1.2, alpha=0.7)
                self.plot_point_badge(vx, vy, f"꼭짓점 V({vx:.2f}, {vy:.2f})", color='#f43f5e', offset=(15, 12 if a > 0 else -25))
                vertex_str = f"({vx:.2f}, {vy:.2f})"
            else:
                vertex_str = "N/A (직선)"

            # 2. y-절편 (0, c)
            if -6 <= c <= 8:
                self.plot_point_badge(0, c, f"y절편 (0, {c:.2f})", color='#a855f7', offset=(-85, 10))

            # 3. x-절편 (근 / x축과의 교점)
            D = b**2 - 4 * a * c
            d_desc = "서로 다른 두 실근" if D > 0 else ("중근 (접함)" if abs(D) < 1e-4 else "서로 다른 두 허근")
            if abs(a) > 1e-5:
                if D > 1e-5:
                    r1 = (-b - np.sqrt(D)) / (2 * a)
                    r2 = (-b + np.sqrt(D)) / (2 * a)
                    if -5 <= r1 <= 5:
                        self.plot_point_badge(r1, 0, f"x절편 ({r1:.2f}, 0)", color='#10b981', offset=(-60, -22), show_proj=False)
                    if -5 <= r2 <= 5:
                        self.plot_point_badge(r2, 0, f"x절편 ({r2:.2f}, 0)", color='#10b981', offset=(10, -22), show_proj=False)
                elif abs(D) <= 1e-5:
                    r = -b / (2 * a)
                    if -5 <= r <= 5:
                        self.plot_point_badge(r, 0, f"중근 ({r:.2f}, 0)", color='#10b981', offset=(12, -22), show_proj=False)

            self.ax.set_xlim(-5, 5)
            self.ax.set_ylim(-6, 8)
            self.ax.set_title(rf'$f(x) = {a:.2f}x^2 + ({b:.2f})x + ({c:.2f})$', color='#f8fafc', fontsize=12, pad=10)
            
            info = f"■ 이차함수 분석\n" \
                   f"----------------------\n" \
                   f"• 최고차항 a: {a:.2f}\n" \
                   f"• 대칭축 x : {vertex_str.split(',')[0].replace('(', '')}\n" \
                   f"• 꼭짓점   : {vertex_str}\n" \
                   f"• y-절편   : (0, {c:.2f})\n" \
                   f"• 판별식 D : {D:.2f}\n" \
                   f"• x-절편   : {d_desc}"
            self.info_text.set_text(info)

        elif self.mode == 1:
            A, B, C = val1, val2, val3
            x = np.linspace(-2*np.pi, 2*np.pi, 500)
            y = A * np.sin(B * x - C)
            self.ax.plot(x, y, color='#38bdf8', lw=2.8)

            # 1. y-절편
            y_int = A * np.sin(-C)
            self.plot_point_badge(0, y_int, f"y절편 (0, {y_int:.2f})", color='#a855f7', offset=(-85, 12))

            # 2. x-절편 (x축과의 교점들)
            if abs(B) > 1e-4:
                # B*x - C = k*pi  =>  x = (C + k*pi)/B
                k_vals = range(-8, 9)
                for k in k_vals:
                    xk = (C + k * np.pi) / B
                    if -2*np.pi <= xk <= 2*np.pi and abs(xk) > 0.15:
                        self.ax.plot([xk], [0], marker='o', color='#10b981', markersize=5, zorder=5)
                # Mark main visible x-intercept near origin
                xk_main = (C + round(-C / np.pi) * np.pi) / B
                if -2*np.pi <= xk_main <= 2*np.pi:
                    self.plot_point_badge(xk_main, 0, f"교점 ({xk_main:.2f}, 0)", color='#10b981', offset=(8, -20), show_proj=False)

            # 3. 최댓값 극점
            if abs(B) > 1e-4:
                x_peak = (C + np.pi / 2) / B
                while x_peak < -2*np.pi: x_peak += 2*np.pi/abs(B)
                while x_peak > 2*np.pi: x_peak -= 2*np.pi/abs(B)
                if -2*np.pi <= x_peak <= 2*np.pi:
                    y_peak = A * np.sin(B * x_peak - C)
                    self.plot_point_badge(x_peak, y_peak, f"극값 ({x_peak:.2f}, {y_peak:.2f})", color='#fbbf24', offset=(10, 12 if y_peak > 0 else -22))

            T = (2 * np.pi) / abs(B) if abs(B) > 1e-4 else np.inf
            self.ax.set_xlim(-2*np.pi, 2*np.pi)
            self.ax.set_ylim(-3.5, 3.5)
            self.ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
            self.ax.set_xticklabels([r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$'])
            self.ax.set_title(rf'$y = {A:.2f}\sin({B:.2f}x - ({C:.2f}))$', color='#f8fafc', fontsize=12, pad=10)

            info = f"■ 삼각함수 파동 분석\n" \
                   f"----------------------\n" \
                   f"• 진폭 |A|  : {abs(A):.2f}\n" \
                   f"• 주기 T    : {T:.2f} ({T/np.pi:.2f} rad)\n" \
                   f"• 위상 이동 : {C/B if abs(B)>1e-4 else 0:.2f}\n" \
                   f"• y-절편    : (0, {y_int:.2f})\n" \
                   f"• 최댓값    : {abs(A):.2f}\n" \
                   f"• 최솟값    : {-abs(A):.2f}"
            self.info_text.set_text(info)

        elif self.mode == 2:
            x0, a, c = val1, val2, val3
            x = np.linspace(-3, 3, 400)
            def f(t): return a * t**3 - t + c
            def df(t): return 3 * a * t**2 - 1

            y = f(x)
            self.ax.plot(x, y, color='#38bdf8', lw=2.8)

            y0 = f(x0)
            slope = df(x0)
            tangent_line = y0 + slope * (x - x0)
            self.ax.plot(x, tangent_line, color='#fbbf24', lw=2.2, ls='-')

            # 1. 움직이는 접점 P(x0, y0)
            self.plot_point_badge(x0, y0, f"접점 P({x0:.2f}, {y0:.2f})\n[기울기 m={slope:.2f}]", color='#f43f5e', offset=(15, 15))

            # 2. 곡선 f(x)의 y-절편 (0, c)
            if -4 <= c <= 4:
                self.plot_point_badge(0, c, f"f y절편 (0, {c:.2f})", color='#a855f7', offset=(-80, 10))

            # 3. 접선의 y-절편 (0, y0 - slope * x0)
            y_tan_int = y0 - slope * x0
            if -4 <= y_tan_int <= 4:
                self.plot_point_badge(0, y_tan_int, f"접선 y절편 (0, {y_tan_int:.2f})", color='#eab308', offset=(-85, -20))

            # 4. 접선과 3차곡선의 제2 교점 Q (-2*x0, f(-2*x0))
            if abs(a) > 1e-4:
                x_q = -2 * x0
                y_q = f(x_q)
                if -2.5 <= x_q <= 2.5 and -4 <= y_q <= 4 and abs(x_q - x0) > 0.15:
                    self.plot_point_badge(x_q, y_q, f"교점 Q({x_q:.2f}, {y_q:.2f})", color='#38bdf8', offset=(-75 if x_q > 0 else 15, -20 if y_q > 0 else 15))

            self.ax.set_xlim(-2.5, 2.5)
            self.ax.set_ylim(-4, 4)
            self.ax.set_title(rf'$f(x) = {a:.2f}x^3 - x + {c:.2f} \quad \Rightarrow \quad f^\prime({x0:.2f}) = {slope:.2f}$', color='#f8fafc', fontsize=12, pad=10)

            info = f"■ 미분계수(접선) 분석\n" \
                   f"----------------------\n" \
                   f"• 접점 P(x0): ({x0:.2f}, {y0:.2f})\n" \
                   f"• 순간변화율: m = {slope:.2f}\n" \
                   f"• 접선 식   :\n" \
                   f"  y = {slope:.2f}x + {y_tan_int:.2f}\n" \
                   f"• 곡선 y절편: (0, {c:.2f})\n" \
                   f"• 제2 교점 Q: ({(-2*x0):.2f}, {f(-2*x0):.2f})"
            self.info_text.set_text(info)

        elif self.mode == 3:
            n, a_val, b_val = int(val1), val2, val3
            if b_val <= a_val: b_val = a_val + 0.5
            x = np.linspace(0, 5, 400)
            def f(t): return -0.4 * (t - 2)**2 + 3
            y = f(x)
            self.ax.plot(x, y, color='#38bdf8', lw=2.8)

            dx = (b_val - a_val) / n
            riemann_sum = 0
            for i in range(n):
                xi = a_val + i * dx
                yi = max(0, f(xi + dx/2))
                riemann_sum += yi * dx
                self.ax.bar(xi + dx/2, yi, width=dx, alpha=0.35, color='#fbbf24', edgecolor='#f59e0b', align='center')

            x_int = np.linspace(a_val, b_val, 1000)
            exact_val = np.trapezoid(f(x_int), x_int)
            error = abs(riemann_sum - exact_val)

            # 1. 적분 경계점 A(a, f(a)), B(b, f(b))
            self.plot_point_badge(a_val, f(a_val), f"A({a_val:.1f}, {f(a_val):.2f})", color='#38bdf8', offset=(-60, 12))
            self.plot_point_badge(b_val, f(b_val), f"B({b_val:.1f}, {f(b_val):.2f})", color='#f43f5e', offset=(10, 12))

            # 2. 극댓값 / 꼭짓점 (2, 3)
            self.plot_point_badge(2.0, 3.0, "극댓값 (2.00, 3.00)", color='#fbbf24', offset=(-45, 14))

            # 3. y-절편 (0, 1.4)
            self.plot_point_badge(0, f(0), f"y절편 (0, {f(0):.2f})", color='#a855f7', offset=(10, -18))

            self.ax.set_xlim(0, 5)
            self.ax.set_ylim(-0.5, 3.8)
            self.ax.set_title(rf'$\int_{{{a_val:.1f}}}^{{{b_val:.1f}}} f(x)\,dx \approx {riemann_sum:.3f} \quad (n={n})$', color='#f8fafc', fontsize=12, pad=10)

            info = f"■ 정적분 리만합 분석\n" \
                   f"----------------------\n" \
                   f"• 적분 구간 : [{a_val:.1f}, {b_val:.1f}]\n" \
                   f"• 점 A 좌표 : ({a_val:.1f}, {f(a_val):.2f})\n" \
                   f"• 점 B 좌표 : ({b_val:.1f}, {f(b_val):.2f})\n" \
                   f"• 분할 수 n : {n}\n" \
                   f"• 리만합 근사: {riemann_sum:.4f}\n" \
                   f"• 정적분 참값: {exact_val:.4f}\n" \
                   f"• 오차 (Error): {error:.4f}"
            self.info_text.set_text(info)

        self.fig.canvas.draw_idle()

    def on_key_press(self, event):
        k = str(event.key).lower()
        if k in ['1', '2', '3', '4']:
            idx = int(k) - 1
            self.radio.set_active(idx)
        elif k in ['up', 'down']:
            step = -1 if k == 'up' else 1
            self.active_slider_idx = (self.active_slider_idx + step) % len(self.sliders)
            self.highlight_active_slider()
        elif k in ['left', 'right']:
            step = 0.05 if k == 'right' else -0.05
            self.step_slider(self.active_slider_idx, step)
        elif k in ['r']:
            self.reset_values(None)

    def highlight_active_slider(self):
        for i, s in enumerate(self.sliders):
            if i == self.active_slider_idx:
                s.label.set_color('#38bdf8')
                s.label.set_weight('bold')
            else:
                s.label.set_color('#f8fafc')
                s.label.set_weight('normal')
        self.fig.canvas.draw_idle()

    def reset_values(self, event):
        self.s1.reset()
        self.s2.reset()
        self.s3.reset()

def run():
    app = MathInteractiveApp()
    plt.show()

if __name__ == '__main__':
    run()
