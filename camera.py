import subprocess
import os

class Camera:
    def __init__(self, device="/dev/video0", output_file="output.mp4"):
        self.device = device
        self.output_file = output_file
        self.process = None

        # 1. Setup Camera hardware settings
        try:
            subprocess.run([
                "v4l2-ctl", "-d", self.device,
                "--set-fmt-video=width=1280,height=720,pixelformat=MJPG",
                "--set-parm=60"
            ], check=True)
        except Exception as e:
            print(f"Camera Hardware Setup Error: {e}")

        # 2. Prepare FFmpeg command
        self.cmd = [
            "ffmpeg", "-y",
            "-f", "v4l2",
            "-input_format", "mjpeg",
            "-framerate", "30",
            "-video_size", "1280x720",
            "-i", self.device,
            "-c:v", "copy",
            "-movflags", "+frag_keyframe+empty_moov+default_base_moof",
            self.output_file
        ]

        self.start_recording()

    def start_recording(self):
        print(f"Starting Video Recording: {self.output_file}")
        self.process = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

    def release(self):
        """Safely stops the FFmpeg process to finalize the MP4 file."""
        if self.process and self.process.poll() is None:
            print("Finalizing video file...")
            try:
                self.process.communicate(input=b'q', timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("Video process forced to stop.")

            print("Video saved.")
