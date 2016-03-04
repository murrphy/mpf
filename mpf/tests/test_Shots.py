from mock import MagicMock
from mpf.tests.MpfTestCase import MpfTestCase

class TestShots(MpfTestCase):

    def getConfigFile(self):
        return 'test_shots.yaml'

    def getMachinePath(self):
        return 'tests/machine_files/shots/'

    def start_game(self):
        # shots only work in games so we have to do this a lot
        self.machine.events.post('game_start')
        self.advance_time_and_run()
        self.machine.game.balls_in_play = 1


    def test_loading_shots(self):
        # Make sure machine-wide shots load & mode-specific shots do not
        self.assertIn('shot_1', self.machine.shots)
        self.assertIn('shot_2', self.machine.shots)
        self.assertIn('shot_3', self.machine.shots)
        self.assertIn('shot_4', self.machine.shots)
        self.assertIn('led_1', self.machine.shots)
        self.assertIn('led_2', self.machine.shots)
        self.assertIn('led_3', self.machine.shots)
        self.assertIn('led_4', self.machine.shots)

        self.assertNotIn('mode1_shot_1', self.machine.shots)

        # Start the mode and make sure those shots load
        self.machine.modes.mode1.start()
        self.advance_time_and_run()
        self.assertIn('mode1_shot_1', self.machine.shots)

        self.assertIn('shot_1', self.machine.shots)
        self.assertIn('shot_2', self.machine.shots)
        self.assertIn('shot_3', self.machine.shots)
        self.assertIn('shot_4', self.machine.shots)
        self.assertIn('led_1', self.machine.shots)
        self.assertIn('led_2', self.machine.shots)
        self.assertIn('led_3', self.machine.shots)
        self.assertIn('led_4', self.machine.shots)

        # Stop the mode and make sure those shots go away
        self.machine.modes.mode1.stop()
        self.advance_time_and_run()
        self.assertNotIn('mode1_shot_1', self.machine.shots)

        self.assertIn('shot_1', self.machine.shots)
        self.assertIn('shot_2', self.machine.shots)
        self.assertIn('shot_3', self.machine.shots)
        self.assertIn('shot_4', self.machine.shots)
        self.assertIn('led_1', self.machine.shots)
        self.assertIn('led_2', self.machine.shots)
        self.assertIn('led_3', self.machine.shots)
        self.assertIn('led_4', self.machine.shots)

    def test_hits(self):
        self.shot_1_hit = MagicMock()
        self.shot_1_default_hit = MagicMock()
        self.shot_1_default_unlit_hit = MagicMock()
        self.mode1_shot_1_hit = MagicMock()
        self.machine.events.add_handler('shot_1_hit', self.shot_1_hit)
        self.machine.events.add_handler('shot_1_default_hit',
                                        self.shot_1_default_hit)
        self.machine.events.add_handler('shot_1_default_unlit_hit',
                                        self.shot_1_default_unlit_hit)
        self.machine.events.add_handler('mode1_shot_1_hit',
                                        self.mode1_shot_1_hit)

        # make sure shot does not work with no game in progress
        self.machine.switch_controller.process_switch('switch_1', 1)
        self.machine.switch_controller.process_switch('switch_1', 0)
        self.advance_time_and_run()
        self.shot_1_hit.assert_not_called()

        self.start_game()

        # hit shot_1, test all three event variations
        self.machine.switch_controller.process_switch('switch_1', 1)
        self.machine.switch_controller.process_switch('switch_1', 0)
        self.advance_time_and_run()

        self.shot_1_hit.assert_called_once_with(profile='default',
                                                state='unlit')
        self.shot_1_default_hit.assert_called_once_with(profile='default',
                                                state='unlit')
        self.shot_1_default_unlit_hit.assert_called_once_with(
                profile='default', state='unlit')

        # hit the mode shot and make sure it doesn't fire
        self.machine.switch_controller.process_switch('switch_3', 1)
        self.machine.switch_controller.process_switch('switch_3', 0)
        self.advance_time_and_run()
        self.mode1_shot_1_hit.assert_not_called()

        # Start the mode
        self.machine.modes.mode1.start()
        self.advance_time_and_run()

        # hit the mode shot and make sure it was called
        self.machine.switch_controller.process_switch('switch_3', 1)
        self.machine.switch_controller.process_switch('switch_3', 0)
        self.advance_time_and_run()
        self.mode1_shot_1_hit.assert_called_once_with(profile='default',
                                                      state='unlit')

        # stop the mode
        self.machine.modes.mode1.stop()
        self.advance_time_and_run()

        # hit the mode shot and make sure it was not called
        self.mode1_shot_1_hit = MagicMock()
        self.machine.switch_controller.process_switch('switch_3', 1)
        self.machine.switch_controller.process_switch('switch_3', 0)
        self.advance_time_and_run()
        self.mode1_shot_1_hit.assert_not_called()

    def test_show_in_profile_root(self):
        pass

    def test_show_in_step(self):
        pass

    def test_combined_show_in_profile_root_and_step(self):
        pass

    def test_multiple_switches(self):
        pass

    def test_switch_sequence(self):
        pass

        # include cancel switch, delay switch, time

    def test_control_events(self):
        pass

        # enable_events
        # disable_events
        # reset_events
        # hit_events
        # advance_events
        # remove_active_profile_events

        # shot groups
        # enable_events
        # disable_events
        # reset_events
        # rotate_left_events
        # rotate_right_events
        # enable_rotation_events
        # disable_rotation_events
        # advance_events
        # remove_active_profile_events

    def test_shot_profiles(self):
        pass
        # loop
        # state_names_to_rotate
        # state_names_to_not_rotate
        # rotation_pattern
        # player_variable
        # show_when_disabled
        # block
        # states (with various show params and tokens)