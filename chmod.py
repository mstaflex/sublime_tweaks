import sublime, sublime_plugin, subprocess

def chmod(v, e, permissions):
    subprocess.call( [ "chmod", permissions, v.file_name() ] )

def stat(filename):
    proc = subprocess.Popen( [ "stat", "-c", '%a', filename ], stdout=subprocess.PIPE )
    return str(proc.communicate()[0]).strip()

class ChangeModeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if sublime.platform() == 'windows':
            return

        fname = self.view.file_name()

        if fname == None:
            sublime.message_dialog("You need to save this buffer first!")
            return

        perms = stat(fname)

        def doneCB(permissions):
            chmod(self.view, edit, permissions)

        sublime.active_window().show_input_panel(
            "permissions to apply to the file " + fname + ": ", perms, doneCB, None, None)