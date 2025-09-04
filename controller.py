import logging

log = logging.getLogger("rocket")

class DryRunController:
    def up(self): log.info("[DRY] up")
    def down(self): log.info("[DRY] down")
    def left(self): log.info("[DRY] left")
    def right(self): log.info("[DRY] right")
    def stop(self): log.info("[DRY] stop")
    def fire(self): log.info("[DRY] fire")

def get_controller():
    try:
        import usb_missile_control as umc
        log.info("usb_missile_control imported")

        launcher = umc.Launcher() if hasattr(umc, "Launcher") else umc.USBMissileDevice()

        class RealController:
            def up(self): launcher.up()
            def down(self): launcher.down()
            def left(self): launcher.left()
            def right(self): launcher.right()
            def stop(self):
                if hasattr(launcher, "stop"): launcher.stop()
                elif hasattr(launcher, "halt"): launcher.halt()
            def fire(self):
                for name in ["fire", "shoot", "launch"]:
                    if hasattr(launcher, name):
                        return getattr(launcher, name)()

        return RealController()
    except Exception as e:
        log.warning("Falling back to dry-run controller: %s", e)
        return DryRunController()

