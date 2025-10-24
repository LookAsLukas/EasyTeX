import flet as ft
import matplotlib.pyplot as plt
import io
import base64
plt.rcParams['text.usetex'] = True


def cook_input(s: str) -> str:
    if not s.strip():
        return ""

    s = '\n'.join(map(lambda x: '\\[' + x + '\\]', s.split('\n')))
    return s


def main(page: ft.Page):
    # Start with empty image
    image_component = ft.Image(src_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")

    def textbox_change(e):
        # Create image in memory
        fig = plt.figure()
        fig.text(
            x=0.5, y=0.5,
            s=cook_input(e.control.value),
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=25,
        )
        plt.axis('off')
        
        # Save to memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="svg", bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        
        # Convert to base64
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        image_component.src_base64 = img_data
        page.update()

    page.bgcolor = "#FFFFFF"
    
    text_input = ft.TextField(
        on_change=textbox_change,
        color="#000000",
        hint_text="Enter LaTeX formula (e.g., \\int x^2 dx)",
        border_color="#000000",
        multiline=True,
        min_lines=1,
        max_lines=None,
    )
    
    page.add(
        ft.Column(
            [
                # Image container takes 70% of space
                ft.Container(
                    content=image_component,
                    expand=7,  # 7 parts = 70%
                ),
                # Text input takes 30% of space
                ft.Container(
                    content=text_input,
                    expand=3,  # 3 parts = 30%
                ),
            ],
            expand=True,
        )
    )


ft.app(main)
