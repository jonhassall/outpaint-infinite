import gradio as gr
import subprocess
import shutil
import os
import random
import zipfile
from PIL import Image

# Ensure frames directory exists
os.makedirs("frames", exist_ok=True)

def generate_step(source_path, direction, prompt):
    """Runs the Krea2 script for a single step and returns a 1024x1024 cropped PIL Image"""
    out_path = "temp_out.png"
    
    # Map directions to canvas size, generation bounding box, and the final crop box
    if direction == "right":
        width, height, bbox = 1536, 1024, ["0", "0", "1024", "1024"]
        crop_box = (512, 0, 1536, 1024)
    elif direction == "left":
        width, height, bbox = 1536, 1024, ["512", "0", "1536", "1024"]
        crop_box = (0, 0, 1024, 1024)
    elif direction == "down":
        width, height, bbox = 1024, 1536, ["0", "0", "1024", "1024"]
        crop_box = (0, 512, 1024, 1536)
    elif direction == "up":
        width, height, bbox = 1024, 1536, ["0", "512", "1024", "1536"]
        crop_box = (0, 0, 1024, 1024)

    # Call Krea2 model
    cmd = [
        "python", "example.py",
        "--source", source_path,
        "--output", out_path,
        "--width", str(width),
        "--height", str(height),
        "--bbox", *bbox,
        "--prompt", prompt
    ]
    subprocess.run(cmd, check=True)
    
    # Crop the image back to 1024x1024 to create the moving window
    img = Image.open(out_path)
    return img.crop(crop_box)

def infinite_journey(start_image, prompt, history):
    """Generator function that continuously yields new images to the UI"""
    if start_image is None:
        raise gr.Error("Please upload a starting image!")
    
    # Reset or initialize state
    step = len(history) if history else 0
    current_image_path = "temp_in.png"
    
    if step == 0:
        shutil.copy(start_image, current_image_path)
        # Save frame 0
        frame_path = f"frames/step_{step:04d}.png"
        shutil.copy(start_image, frame_path)
        history = [frame_path]
        yield frame_path, history
    else:
        # Resume from the last frame if we are continuing
        shutil.copy(history[-1], current_image_path)
        
    while True:
        step += 1
        direction = random.choice(["up", "down", "left", "right"])
        print(f"Generating step {step} moving {direction}...")
        
        cropped_img = generate_step(current_image_path, direction, prompt)
        
        # Save the new frame
        frame_path = f"frames/step_{step:04d}.png"
        cropped_img.save(frame_path)
        cropped_img.save(current_image_path) # Update temp input for next loop
        
        history.append(frame_path)
        
        # Yielding updates the Gradio UI instantly
        yield frame_path, history

def pack_zip(history):
    """Packages all frames currently in history into a ZIP file"""
    if not history:
        return None
        
    zip_path = "infinite_journey.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in history:
            # Write file to zip, keeping only the filename, not the folder path
            zipf.write(file_path, os.path.basename(file_path))
    
    return zip_path

# --- Gradio UI Layout ---
with gr.Blocks() as demo:
    gr.Markdown("# 🌌 Infinite Outpaint Explorer")
    
    # Hidden state to keep track of all generated image paths
    history_state = gr.State([])
    
    with gr.Row():
        with gr.Column(scale=1):
            src_img = gr.Image(type="filepath", label="Starting Image (1024x1024)")
            prompt = gr.Textbox(value="a beautiful fantasy landscape, masterpiece, 8k", label="Prompt")
            
            with gr.Row():
                start_btn = gr.Button("🚀 Start Journey", variant="primary")
                stop_btn = gr.Button("🛑 Stop")
            
            gr.Markdown("---")
            zip_btn = gr.Button("📦 Prepare ZIP Download")
            zip_out = gr.File(label="Download frames")
            
        with gr.Column(scale=2):
            live_view = gr.Image(type="filepath", label="Live View", interactive=False)

    # 1. Clicking Start triggers the generator.
    # We save this event to the `run_event` variable so we can cancel it later.
    run_event = start_btn.click(
        fn=infinite_journey, 
        inputs=[src_img, prompt, history_state], 
        outputs=[live_view, history_state]
    )
    
    # 2. Clicking Stop cancels the generator loop safely.
    stop_btn.click(fn=None, cancels=[run_event])
    
    # 3. Clicking Zip triggers the packing function using the current state
    zip_btn.click(
        fn=pack_zip,
        inputs=[history_state],
        outputs=[zip_out]
    )

if __name__ == "__main__":
    app_port = int(os.getenv("APP_PORT", "7860"))
    demo.launch(server_name="0.0.0.0", server_port=app_port, theme=gr.themes.Monochrome())
