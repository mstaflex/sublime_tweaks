import sublime
import sublime_plugin
import subprocess


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
