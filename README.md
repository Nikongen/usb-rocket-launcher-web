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
## Access rights
create a user rocket with access to specific devices

```bash
# Create group and add user
sudo addgroup rocket
sudo usermod -aG rocket nikolas

# Allow access to device for this group
sudo nano /etc/udev/rules.d/rocket
## add line
https://github.com/pyusb/pyusb/blob/master/docs/faq.rst#how-to-practically-deal-with-permission-issues-on-linux
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0x2123", ATTRS{idProduct}=="0x2123", GROUP="rocket", MODE="0660"

# Reload rules
sudo udevadm control --reload-rules
sudo udevadm trigger

```

## Packages

```bash
sudo apt install python3-usb python3-pyaudi python3-flask python3-gunicorn pipx

```

## Python & flask

```bash
sudo apt install python3-virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r req.txt
```
