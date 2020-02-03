package root.commands

import root.files.{DirEntry, File}
import root.filesystem.State

class Touch(name: String) extends CreateEntry (name) {
    override def createSpecificEntry(state: State): DirEntry = File.empty(state.wd.path, name)
}
