package root.files

import root.filesystem.FilesystemException

import scala.annotation.tailrec

class Directory(override val parentPath: String, override val name: String, val contents: List[DirEntry]) extends DirEntry(parentPath, name) {

    def getAllFoldersInPath: List[String] = {
        // /a/b/b => List[a, b, c]
        path.substring(1).split(Directory.SEPARATOR).toList.filter(x => !x.isEmpty)
    }

    def findEntry(entryName: String): DirEntry = {
        @tailrec
        def findEntryHelper(name: String, contentList: List[DirEntry]): DirEntry = {
            if (contentList.isEmpty) null
            else if (contentList.head.name.equals(name)) contentList.head
            else findEntryHelper(name, contentList.tail)
        }

        findEntryHelper(entryName, contents)
    }

    def hasEntry(name: String): Boolean = findEntry(name) != null

    def addEntry(newEntry: DirEntry): Directory = {
        new Directory(parentPath, name, contents :+ newEntry)
    }

    def replaceEntry(entryName: String, newEntry: Directory): Directory = {
        new Directory(parentPath, name, contents.filter(e => !e.name.equals(entryName)) :+ newEntry )
    }

    def removeDir(entryName: String): Directory = {
        if (!hasEntry(entryName)) this
        else new Directory(parentPath, name, contents.filter(x => !x.name.equals(entryName)))
    }

    def findDescendant(path: List[String]): Directory = {
        if (path.isEmpty) this
        else findEntry(path.head).asDirectory.findDescendant(path.tail)
    }

    def findDescendant(path: String): Directory = {
        if (path.isEmpty) this
        else findDescendant(path.split(Directory.SEPARATOR).toList)
    }

    def isRoot: Boolean = parentPath.isEmpty

    override def isDirectory: Boolean = true

    override def isFile: Boolean = false

    override def asDirectory: Directory = this

    override def asFile: File = throw new FilesystemException("A directory cannot be transformed as file")

    override def getType: String = "Directory"
}

object Directory {
    val SEPARATOR = "/"
    val ROOT_PATH = "/"

    def empty(parentPath: String, name: String): Directory = {
        new Directory(parentPath, name, List())
    }

    def ROOT: Directory = Directory.empty("", "")
}
