package root.commands
import root.files.Directory
import root.filesystem.State

class Rm(name: String) extends Commands {
    override def apply(state: State): State = {
        // get the wd
        val wd = state.wd

        // Absolute Path
        val absolutePath =
            if(name.startsWith(Directory.SEPARATOR)) name
            else if (wd.isRoot) wd.path + name
            else wd.path + Directory.SEPARATOR + name

        // Dp some check
        if (Directory.ROOT_PATH.equals(absolutePath)) state.setMessage("Nuclear war not supported yet")
        else doRM(state, absolutePath)
    }

    def doRM(state: State, path: String): State = {

        def rmHelper(currentDir: Directory, path: List[String]): Directory = {
            if (path.isEmpty) currentDir
            else if (path.tail.isEmpty) currentDir.removeDir(path.head)
            else {
                val nextDir = currentDir.findEntry(path.head)

                if (!nextDir.isDirectory) currentDir
                else {
                    val newNextDirectory = rmHelper(nextDir.asDirectory, path.tail)

                    if(newNextDirectory == nextDir) currentDir
                    else currentDir.replaceEntry(path.head, newNextDirectory)
                }

            }
        }

        val tokens = path.substring(1).split(Directory.SEPARATOR).toList
        val newRoot: Directory = rmHelper(state.root, tokens)

        if (newRoot == state.root) state.setMessage(s"$path : no such file or directory")
        else {
            State(newRoot, newRoot.findDescendant(state.wd.path.substring(1)))
        }
        // Find the entry

    }
}
