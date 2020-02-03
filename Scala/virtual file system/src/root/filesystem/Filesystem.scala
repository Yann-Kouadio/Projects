package root.filesystem

import java.util.Scanner

import root.commands.Commands
import root.files.Directory

object Filesystem extends App {
    val root = Directory.ROOT
    var state = State(root, root)
    val scanner = new Scanner(System.in)

    while(true) {
        state.show
        val input = scanner.nextLine()
        state = Commands.from(input).apply(state)
    }
}
