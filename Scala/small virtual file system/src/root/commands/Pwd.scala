package root.commands

import root.filesystem.State

class Pwd extends Commands {
    override def apply(state: State): State = state.setMessage(state.wd.path)

}
