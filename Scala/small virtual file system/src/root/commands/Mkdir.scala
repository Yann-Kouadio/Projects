package root.commands

import root.files.{DirEntry, Directory}
import root.filesystem.State

class Mkdir(name: String) extends CreateEntry(name) {
    override def createSpecificEntry(state: State): DirEntry = Directory.empty(state.wd.path, name)
}
