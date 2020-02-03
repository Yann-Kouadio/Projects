package root.commands

import root.files.{DirEntry, Directory}
import root.filesystem.State

import scala.annotation.tailrec

class Cd(dir: String) extends Commands {
    override def apply(state: State): State = {
        // 1. Find the root
        val root = state.root
        val wd = state.wd

        // 2. find the absolute path
        val absolutePath = {
            if (dir.startsWith(Directory.SEPARATOR)) dir
            else if (wd.isRoot) wd.path + dir
            else wd.path + Directory.SEPARATOR + dir
        }

        // 3. find the dir to cd to
        val destinationDir = doFindEntry(root, absolutePath)

        // 4. Change the state given the new directory
        if (destinationDir == null || !destinationDir.isDirectory) state.setMessage(s"$dir : no such directory")
        else State(root, destinationDir.asDirectory)
    }

    def doFindEntry(root: Directory, path: String): DirEntry = {
        @tailrec
        def findEntryHelper(currentDir: Directory, path: List[String]): DirEntry = {
            if (path.isEmpty || path.head.isEmpty) currentDir
            else if (path.tail.isEmpty) currentDir.findEntry(path.head)
            else {
                val nextDir = currentDir.findEntry(path.head)

                if (nextDir == null || !nextDir.isDirectory) null
                else findEntryHelper(nextDir.asDirectory, path.tail)
            }
        }

        @tailrec
        def collapseRelativeToken(path: List[String], result: List[String]): List[String] = {
            if (path.isEmpty) result
            else if (".".equals(path.head)) collapseRelativeToken(path.tail, result)
            else if("..".equals(path.head)) {
                if (result.isEmpty) null
                else collapseRelativeToken(path.tail, result.init)
            }
            else collapseRelativeToken(path.tail, result :+ path.head)
        }



        // 1. tokens
        val tokens: List[String] = path.substring(1).split(Directory.SEPARATOR).toList

        // 1.5 Eliminate or collapse relative token

        /*
        ["a", "."] => ["a"]
        ["a", "."]
        */

        val newTokens = collapseRelativeToken(tokens, List())

        // 2. navigate to the correct entry
        if (newTokens == null) null
        else
        findEntryHelper(root, newTokens)
    }

}
