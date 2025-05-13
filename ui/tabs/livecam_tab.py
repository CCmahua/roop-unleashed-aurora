import gradio as gr
import roop.globals
import ui.globals


camera_frame = None

def livecam_tab():
    with gr.Tab("🎥 实时摄像头"):
        with gr.Row(variant='panel'):
            gr.Markdown("""
                        此功能允许您使用物理网络摄像头并将选定的面部应用到视频流中。
                        您还可以将视频流转发到虚拟摄像头，可用于视频通话或流媒体软件。<br />
                        支持的系统：v4l2loopback (Linux)、OBS虚拟摄像头 (macOS/Windows) 和 unitycapture (Windows)。<br />
                        **请注意：** 要更改面部或其他设置，您需要停止并重新启动正在运行的实时摄像头。
            """)

        with gr.Row(variant='panel'):
            with gr.Column():
                bt_start = gr.Button("▶ 开始", variant='primary')
            with gr.Column():
                bt_stop = gr.Button("⏹ 停止", variant='secondary', interactive=False)
            with gr.Column():
                camera_num = gr.Slider(0, 8, value=0, label="摄像头编号", step=1.0, interactive=True)
                cb_obs = gr.Checkbox(label="转发到虚拟摄像头", interactive=True)
            with gr.Column():
                dd_reso = gr.Dropdown(choices=["640x480","1280x720", "1920x1080"], value="1280x720", label="虚拟摄像头分辨率", interactive=True)
                cb_xseg = gr.Checkbox(label="使用DFL Xseg遮罩", interactive=True, value=True)
                cb_mouthrestore = gr.Checkbox(label="恢复原始嘴部区域", interactive=True, value=False)

        with gr.Row():
            fake_cam_image = gr.Image(label='虚拟摄像头输出', interactive=False, format="jpeg")

    start_event = bt_start.click(fn=start_cam,  inputs=[cb_obs, cb_xseg, cb_mouthrestore, camera_num, dd_reso, ui.globals.ui_selected_enhancer, ui.globals.ui_blend_ratio, ui.globals.ui_upscale],outputs=[bt_start, bt_stop,fake_cam_image])
    bt_stop.click(fn=stop_swap, cancels=[start_event], outputs=[bt_start, bt_stop], queue=False)


def start_cam(stream_to_obs, use_xseg, use_mouthrestore, cam, reso, enhancer, blend_ratio, upscale):
    from roop.virtualcam import start_virtual_cam
    from roop.utilities import convert_to_gradio

    roop.globals.selected_enhancer = enhancer
    roop.globals.blend_ratio = blend_ratio
    roop.globals.subsample_size = int(upscale[:3])
    start_virtual_cam(stream_to_obs, use_xseg, use_mouthrestore, cam, reso)
    while True:
        yield gr.Button(interactive=False), gr.Button(interactive=True), convert_to_gradio(ui.globals.ui_camera_frame)
        

def stop_swap():
    from roop.virtualcam import stop_virtual_cam
    stop_virtual_cam()
    return gr.Button(interactive=True), gr.Button(interactive=False)
    



