# USB Rocket Launcher with Webcam

- https://www.jeffgeerling.com/blog/2016/good-use-raspberry-pi-missile-control
- https://www.amctrl.com/rocketlauncher.html
- https://github.com/pwicks86/usb_missile_control
 
## Webcam Streamer

- https://github.com/pikvm/ustreamer

```bash
# Install
sudo apt install ustreamer
# Test
sudo ustreamer --device=/dev/video0 --host=131.220.157.234 --port=80
# Systemd service
sudo nano /etc/systemd/system/ustreamer.service
## Insert
[Unit]
Description=uStreamer Service
After=network.target

[Service]
ExecStart=/usr/bin/ustreamer --device=/dev/video0 --host=131.220.157.234 --port=80
Restart=always
User=root
Group=root

# Optional: increase security slightly (still runs as root)
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
####
sudo systemctl daemon-reload
sudo systemctl enable ustreamer
sudo systemctl start ustreamer
sudo systemctl status ustreamer
```
