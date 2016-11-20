"""Controls a playfield magnet in a pinball machine."""
from mpf.core.delays import DelayManager

from mpf.core.device_monitor import DeviceMonitor
from mpf.core.system_wide_device import SystemWideDevice


@DeviceMonitor("_enabled", "_active", "_release_in_progress")
class Magnet(SystemWideDevice):

    """Controls a playfield magnet in a pinball machine."""

    config_section = 'magnets'
    collection = 'magnets'
    class_label = 'magnet'

    def __init__(self, machine, name):
        """Initialise magnet."""
        super().__init__(machine, name)
        self.delay = DelayManager(machine.delayRegistry)
        self._enabled = False
        self._active = False
        self._release_in_progress = False

    def enable(self, **kwargs):
        """Enable magnet."""
        del kwargs
        if self._enabled:
            return

        self.debug_log("Enabling Magnet")
        self._enabled = True

        if self.config['grab_switch']:
            self.config['grab_switch'].add_handler(self.grab_ball)

    def disable(self, **kwargs):
        """Disable magnet."""
        del kwargs
        if not self._enabled:
            return

        self.debug_log("Disabling Magnet")
        self._enabled = False

        if self.config['grab_switch']:
            self.config['grab_switch'].remove_handler(self.grab_ball)

    def reset(self, **kwargs):
        """Release ball and disable magnet."""
        del kwargs
        self.debug_log("Resetting Magnet")
        self.release_ball()
        self.disable()

    def grab_ball(self, **kwargs):
        """Grab a ball."""
        del kwargs
        if not self._enabled or self._active or self._release_in_progress:
            return
        self.debug_log("Grabbing a ball.")
        self._active = True
        self.config['magnet_coil'].enable()

        self.machine.events.post("magnet_{}_grabbing_ball".format(self.name))
        '''event: magnet_(name)_grabbing_ball

        desc: Will (try to) grab a ball.
        '''
        self.delay.add(self.config['grab_time'], self._grabbing_done)

    def _grabbing_done(self):
        self.machine.events.post("magnet_{}_grabbed_ball".format(self.name))
        '''event: magnet_(name)_grabbed_ball

        desc: Grabbed the ball (or hope to).
        '''

    def release_ball(self, **kwargs):
        """Release the grabbed ball."""
        del kwargs
        if not self._active or self._release_in_progress:
            return

        self._active = False
        self._release_in_progress = True
        self.debug_log("Releasing ball.")
        self.machine.events.post("magnet_{}_releasing_ball".format(self.name))
        '''event: magnet_(name)_releasing_ball

        desc: Releasing a ball.
        '''

        self.delay.add(self.config['release_time'], self._release_done)
        self.config['magnet_coil'].disable()

    def _release_done(self):
        self._release_in_progress = False
        self.machine.events.post("magnet_{}_released_ball".format(self.name))
        '''event: magnet_(name)_released_ball

        desc: Released a ball.
        '''

    def fling_ball(self, **kwargs):
        """Fling the grabbed ball."""
        del kwargs
        if not self._active or self._release_in_progress:
            return

        self._active = False
        self._release_in_progress = True
        self.debug_log("Flinging ball.")
        self.machine.events.post("magnet_{}_flinging_ball".format(self.name))
        '''event: magnet_(name)_flinging_ball

        desc: Flinging a ball by disabling and enabling the magnet again for a short time.
        '''

        self.delay.add(self.config['fling_drop_time'], self._fling_reenable)
        self.config['magnet_coil'].disable()

    def _fling_reenable(self):
        self.delay.add(self.config['fling_regrab_time'], self._fling_done)
        self.config['magnet_coil'].enable()

    def _fling_done(self):
        self._release_in_progress = False
        self.config['magnet_coil'].disable()
        self.machine.events.post("magnet_{}_flinged_ball".format(self.name))
        '''event: magnet_(name)_flinged_ball

        desc: Flinged a ball.
        '''
