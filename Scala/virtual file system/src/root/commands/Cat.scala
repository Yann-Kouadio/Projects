package root.commands
import root.filesystem.State

class Cat(filename: String) extends Commands {
    override def apply(state: State): State = {
        val wd = state.wd

        val dirEntry = wd.findEntry(filename)

        if (dirEntry == null || !dirEntry.isFile) state.setMessage(s"$filename : no such file")
        else state.setMessage(dirEntry.asFile.contents)
    }
}
