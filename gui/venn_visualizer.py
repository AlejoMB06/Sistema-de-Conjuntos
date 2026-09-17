# gui/venn_visualizer.py

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VennVisualizer:
    @staticmethod
    def generar_diagrama_venn(frame_destino, conjuntos_activos):
        # Limpiar gráfico anterior si existe
        for widget in frame_destino.winfo_children():
            widget.destroy()

        # Aumentamos un poco la altura para dar espacio a la leyenda de identificación
        fig, ax = plt.subplots(figsize=(6, 5.5))
        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        n = len(conjuntos_activos)

        if n == 2:
            c1, c2 = conjuntos_activos[0], conjuntos_activos[1]
            s1, s2 = c1.elementos, c2.elementos

            solo_1 = s1 - s2
            solo_2 = s2 - s1
            inter = s1 & s2

            # Colores asignados
            color1, color2 = '#3498db', '#e74c3c'

            elipses = [
                Ellipse((0.38, 0.58), 0.55, 0.75, angle=0, edgecolor=color1, facecolor=color1, alpha=0.25, linewidth=2),
                Ellipse((0.62, 0.58), 0.55, 0.75, angle=0, edgecolor=color2, facecolor=color2, alpha=0.25, linewidth=2)
            ]
            for el in elipses:
                ax.add_patch(el)

            # Textos y elementos
            ax.text(0.28, 0.58, "\n".join(str(x) for x in solo_1) if solo_1 else "(vacío)", color='white', fontsize=9, ha='center', va='center')
            ax.text(0.72, 0.58, "\n".join(str(x) for x in solo_2) if solo_2 else "(vacío)", color='white', fontsize=9, ha='center', va='center')
            ax.text(0.5, 0.58, "Intersección:\n" + ("\n".join(str(x) for x in inter) if inter else "(vacío)"), color='#f39c12', fontsize=9, ha='center', va='center', fontweight='bold')

            # Leyenda de identificación rápida
            ax.text(0.35, 0.12, f"● {c1.nombre}", color=color1, fontsize=10, ha='center', va='center', fontweight='bold')
            ax.text(0.65, 0.12, f"● {c2.nombre}", color=color2, fontsize=10, ha='center', va='center', fontweight='bold')

        elif n == 3:
            c1, c2, c3 = conjuntos_activos[0], conjuntos_activos[1], conjuntos_activos[2]
            s1, s2, s3 = c1.elementos, c2.elementos, c3.elementos

            e_100 = s1 - s2 - s3
            e_010 = s2 - s1 - s3
            e_001 = s3 - s1 - s2
            e_111 = s1 & s2 & s3

            color1, color2, color3 = '#3498db', '#e74c3c', '#2ecc71'

            elipses = [
                Ellipse((0.5, 0.68), 0.5, 0.65, angle=0, edgecolor=color1, facecolor=color1, alpha=0.2, linewidth=2),
                Ellipse((0.35, 0.42), 0.5, 0.65, angle=60, edgecolor=color2, facecolor=color2, alpha=0.2, linewidth=2),
                Ellipse((0.65, 0.42), 0.5, 0.65, angle=-60, edgecolor=color3, facecolor=color3, alpha=0.2, linewidth=2)
            ]
            for el in elipses:
                ax.add_patch(el)

            ax.text(0.5, 0.82, "\n".join(str(x) for x in e_100) if e_100 else "", color='white', fontsize=8, ha='center', va='center')
            ax.text(0.22, 0.28, "\n".join(str(x) for x in e_010) if e_010 else "", color='white', fontsize=8, ha='center', va='center')
            ax.text(0.78, 0.28, "\n".join(str(x) for x in e_001) if e_001 else "", color='white', fontsize=8, ha='center', va='center')
            ax.text(0.5, 0.50, "Global:\n" + ("\n".join(str(x) for x in e_111) if e_111 else ""), color='#f39c12', fontsize=8, ha='center', va='center', fontweight='bold')

            # Leyenda de identificación rápida
            ax.text(0.2, 0.08, f"● {c1.nombre}", color=color1, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.5, 0.08, f"● {c2.nombre}", color=color2, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.8, 0.08, f"● {c3.nombre}", color=color3, fontsize=9, ha='center', va='center', fontweight='bold')

        elif n >= 4:
            c1, c2, c3, c4 = conjuntos_activos[0], conjuntos_activos[1], conjuntos_activos[2], conjuntos_activos[3]
            s1, s2, s3, s4 = c1.elementos, c2.elementos, c3.elementos, c4.elementos

            color1, color2, color3, color4 = '#3498db', '#e74c3c', '#2ecc71', '#f1c40f'

            elipses = [
                Ellipse((0.35, 0.60), 0.5, 0.7, angle=45, edgecolor=color1, facecolor=color1, alpha=0.15, linewidth=2),
                Ellipse((0.65, 0.60), 0.5, 0.7, angle=-45, edgecolor=color2, facecolor=color2, alpha=0.15, linewidth=2),
                Ellipse((0.45, 0.45), 0.5, 0.7, angle=-45, edgecolor=color3, facecolor=color3, alpha=0.15, linewidth=2),
                Ellipse((0.55, 0.45), 0.5, 0.7, angle=45, edgecolor=color4, facecolor=color4, alpha=0.15, linewidth=2)
            ]
            for el in elipses:
                ax.add_patch(el)

            solo_c1 = s1 - s2 - s3 - s4
            solo_c2 = s2 - s1 - s3 - s4
            solo_c3 = s3 - s1 - s2 - s4
            solo_c4 = s4 - s1 - s2 - s3
            t_todos = s1 & s2 & s3 & s4

            ax.text(0.18, 0.82, "\n".join(str(x) for x in solo_c1) if solo_c1 else "", color='white', fontsize=7, ha='center', va='center')
            ax.text(0.82, 0.82, "\n".join(str(x) for x in solo_c2) if solo_c2 else "", color='white', fontsize=7, ha='center', va='center')
            ax.text(0.18, 0.25, "\n".join(str(x) for x in solo_c3) if solo_c3 else "", color='white', fontsize=7, ha='center', va='center')
            ax.text(0.82, 0.25, "\n".join(str(x) for x in solo_c4) if solo_c4 else "", color='white', fontsize=7, ha='center', va='center')
            
            ax.text(0.5, 0.52, "Los 4:\n" + ("\n".join(str(x) for x in t_todos) if t_todos else ""), color='#e67e22', fontsize=8, ha='center', va='center', fontweight='bold')

            # Leyenda de identificación rápida para los 4 conjuntos abajo en dos filas o una fila limpia
            ax.text(0.25, 0.08, f"● {c1.nombre}", color=color1, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.45, 0.08, f"● {c2.nombre}", color=color2, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.65, 0.08, f"● {c3.nombre}", color=color3, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.85, 0.08, f"● {c4.nombre}", color=color4, fontsize=9, ha='center', va='center', fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_destino)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)