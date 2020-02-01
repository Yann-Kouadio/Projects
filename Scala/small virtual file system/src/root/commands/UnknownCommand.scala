package root.commands

import root.filesystem.State

class UnknownCommand extends Commands {
    override def apply(state: State): State = state.setMessage("Command not found")
}
