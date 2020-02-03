package root.commands

import root.files.DirEntry
import root.filesystem.State

class Ls extends Commands {
    override def apply(state: State): State = {
        val contents = state.wd.contents
        val niceOutput = createNiceOutput(contents)
        state.setMessage(niceOutput)
    }

    def createNiceOutput(contents: List[DirEntry]): String = {
        if (contents.isEmpty) ""
        else {
            val entry = contents.head
            entry.name + "[" + entry.getType + "] \n" + createNiceOutput(contents.tail)
        }
    }
}
