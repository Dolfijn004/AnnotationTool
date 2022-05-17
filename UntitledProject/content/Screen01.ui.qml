/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import UntitledProject

Rectangle {
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 270
        height: 1080
        color: "#ff0000"

        Button {
            id: button
            x: 85
            y: 76
            width: 100
            height: 79
            text: qsTr("knop 1")
        }

        Button {
            id: button1
            x: 85
            y: 170
            width: 100
            height: 82
            text: qsTr("knop 2")
        }

        Button {
            id: button2
            x: 85
            y: 267
            width: 100
            height: 80
            text: qsTr("knop 3")
        }
    }

    Rectangle {
        id: rectangle1
        x: 270
        y: 904
        width: 1228
        height: 176
        color: "#ff0000"

        Button {
            id: button3
            x: 74
            y: 44
            width: 100
            height: 92
            text: qsTr("knop 4")
        }

        Button {
            id: button4
            x: 248
            y: 44
            width: 100
            height: 92
            text: qsTr("knop 5")
        }

        Button {
            id: button5
            x: 429
            y: 44
            width: 100
            height: 92
            text: qsTr("knop 6")
        }
    }

    Rectangle {
        id: rectangle2
        x: 1498
        y: 0
        width: 422
        height: 1080
        color: "#ff0000"

        ScrollView {
            id: scrollView
            x: 43
            y: 134
            width: 348
            height: 307
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            ScrollBar.vertical.policy: ScrollBar.AlwaysOn
            ListView {
                x: 1979
                y: 579
                model: 20
                delegate: ItemDelegate {
                    text: "item" + index
                }
            }
        }

        ScrollView {
            id: scrollView1
            x: 43
            y: 591
            width: 348
            height: 307
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            ScrollBar.vertical.policy: ScrollBar.AlwaysOn
            ListView {
                x: 1979
                y: 579
                model: 20
                delegate: ItemDelegate {
                    text: "item" + index
                }
            }
        }
    }
}


