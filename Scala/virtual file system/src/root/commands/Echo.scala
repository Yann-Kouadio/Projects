package root.commands
import root.files.{Directory, File}
import root.filesystem.State

import scala.annotation.tailrec

class Echo(args: Array[String]) extends Commands {

    def createContent(args: Array[String], topIndex: Int): String = {
        @tailrec
        def createContentHelper(i: Int, accumulator: String): String = {
            if (i >=  topIndex) accumulator
            else createContentHelper(i+1, accumulator + " " + args(i))
        }

        createContentHelper(0, "")
    }

    def getRootAfterEcho(currentDir: Directory, path: List[String], contents: String, append: Boolean): Directory = {
        if (path.isEmpty) currentDir
        else if (path.tail.isEmpty) {
            val dirEntry = currentDir.findEntry(path.head)

            if (dirEntry == null) currentDir.addEntry(new File(currentDir.path, path.head, contents))
            else if (dirEntry.isDirectory) currentDir
            else {
                if (append) currentDir.replaceEntry(path.head, dirEntry.asFile.appendContents(contents).asDirectory)
                else currentDir.replaceEntry(path.head, dirEntry.asFile.setContents(contents).asDirectory)
            }
        }
        else {
            val nextDir = currentDir.findEntry(path.head).asDirectory
            val newNextDir = getRootAfterEcho(nextDir, path.tail, contents, append)

            if (newNextDir == nextDir) currentDir
            else currentDir.replaceEntry(path.head, newNextDir)
        }

    }

    def doEcho(state: State, contents: String, filename: String, append: Boolean): State = {
        if(filename.contains(Directory.SEPARATOR)) state.setMessage("Echo: Filename must not contain separator")
        else {
            val newRoot: Directory = getRootAfterEcho(state.root, state.wd.getAllFoldersInPath :+ filename, contents, append)

            if (newRoot == state.root) state.setMessage(s"$filename : No such file")
            else State(newRoot, newRoot.findDescendant(state.wd.getAllFoldersInPath))
        }

    }

    override def apply(state: State): State = {
        if (args.isEmpty || args.length.equals(0)) state
        else if (args.length.equals(1)) state.setMessage(args.head)
        else {
            val operator = args(args.length - 2)
            val filename = args(args.length - 1)
            val contents = createContent(args, args.length - 2)

            if (operator == ">>") doEcho(state, contents, filename, true)
            else if (">".equals(operator)) doEcho(state, contents, filename, false)
            else state.setMessage(createContent(args, args.length))
        }

    }
}
