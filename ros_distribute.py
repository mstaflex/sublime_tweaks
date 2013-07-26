import sublime
import sublime_plugin
import subprocess

ROS_PATH_KEY = "distribute_target_ros_path.settings"
MESSAGE_NO_KEY = "There is no API key set yet. Enter a valid key now. You can register for a key under http://words.bighugelabs.com/getkey.php for free."


def save_ros_target_path(path):
    #settings = sublime.Settings()
    ros_path_settings = sublime.load_settings(ROS_PATH_KEY)
    ros_path_settings.set("path", path)
    sublime.save_settings(ROS_PATH_KEY)


def get_target_ros_path(user_query=True):
    ros_path_settings = sublime.load_settings(ROS_PATH_KEY)
    path = ros_path_settings.get("path", "")
    if path == "" and user_query:
        sublime.message_dialog(MESSAGE_NO_KEY)
        sublime.active_window().show_input_panel("Target ROS path:", "", save_ros_target_path, None, None)
    return path


class ChangeRosPath(sublime_plugin.TextCommand):
    def run(self, edit):
        current_path = get_target_ros_path(user_query=False)
        sublime.active_window().show_input_panel("New ROS target path:", current_path, save_ros_target_path, None, None)



def distribute(params):
    result = subprocess.call(params.split(' '))
    if result == 0:
        sublime.status_message("File distribution successfull")
    else:
        sublime.message_dialog("File distribution failed! (Errno:%d)" % (result))


class RosDistributeFileCommand(sublime_plugin.TextCommand):
    def distributeCB(self, command):
        command = command.split(' ')
        distribute(*command)

    def botSelectedCB(self, bot_nr):
        user_ros_path = "cps_ros"
        fname = self.view.file_name()
        # get the path within the ros folder to this file
        path = fname[fname.index(user_ros_path) + len(user_ros_path):]

        bot = self.getBotName(nr=bot_nr)

        command = "rcp %s %s:/home/tbot/ros%s" % (fname, bot, path)

        sublime.active_window().show_input_panel(
            "distribute command: ", command, distribute, None, None)

    def getBotName(self, nr=None):
        bot_names = ['tbot_unit%02d' % (bot) for bot in range(1, 8)]
        if nr == None:
            return bot_names
        else:
            return bot_names[nr]

    def run(self, edit):
        fname = self.view.file_name()

        if not 'cps_ros' in fname:
            sublime.message_dialog("You need to call this command from within the user ros folder (cps_ros)")
            return

        bot_names = self.getBotName()

        sublime.active_window().show_quick_panel(bot_names, self.botSelectedCB, sublime.MONOSPACE_FONT)
