import subprocess
import os
import signal

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
            "-framerate", "60",
            "-video_size", "1280x720",
            "-i", self.device,
            "-c:v", "copy",
            "-movflags", "+faststart",
            self.output_file
        ]

        self.start_recording()

    def start_recording(self):
        print(f"Starting Video Recording: {self.output_file}")
        # stdin=subprocess.PIPE allows us to send 'q' to stop FFmpeg gracefully
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
                # Sending 'q' tells FFmpeg to finish the file header and exit
                self.process.communicate(input=b'q', timeout=5)
            except subprocess.TimeoutExpired:
                # If it hangs, force kill it
                self.process.kill()
                print("Video process forced to stop.")

            print("Video saved.")
