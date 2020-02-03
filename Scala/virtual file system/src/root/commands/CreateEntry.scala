package root.commands

import root.files.{DirEntry, Directory}
import root.filesystem.State

abstract class CreateEntry(name: String) extends Commands {

    override def apply(state: State): State = {
        val wd = state.wd

        if (wd.hasEntry(name)) state.setMessage(s"Entry $name already exist")
        else if (name.contains(Directory.SEPARATOR)) state.setMessage(s"$name must not contain separators")
        else if (checkIllegal(name)) state.setMessage(s"$name : illegal entry")
        else doCreateEntry(state, name)
    }

    def checkIllegal(name: String): Boolean = name.contains(".")



    def doCreateEntry(state: State, name: String): State = {
        def updateStructure(currentDir: Directory, path: List[String], newEntry: DirEntry): Directory = {
            if (path.isEmpty) currentDir.addEntry(newEntry)
            else {
                val oldEntry = currentDir.findEntry(path.head).asDirectory
                currentDir.replaceEntry(oldEntry.name, updateStructure(oldEntry, path.tail, newEntry))
            }
        }

        val wd = state.wd

        // 1. all the directories in the full path
        val allDirsInPath = wd.getAllFoldersInPath

        // 2. create new dir in the th wd
//        val newDir = Directory.empty(wd.path, name)
        val newEntry: DirEntry = createSpecificEntry(state)

        // 3. update the all directory structures starting for the root
        val newRoot = updateStructure(state.root, allDirsInPath, newEntry)

        // 4. find new working directory given wd's full path, in the new wd dir
        val newWd = newRoot.findDescendant(allDirsInPath)

        State(newRoot, newWd)
    }

    def createSpecificEntry(state: State): DirEntry

}
