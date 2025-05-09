
import os

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from singletons import settings, LocalizedStrings, loadManager
from actions.links import linkGameObject

import trimesh

from pprint import pprint # DEBUG

class Window(QWidget):

    def __init__(self, data):
        super().__init__()

        pprint(data) # DEBUG
        # Quest title vs challenge title
        title = LocalizedStrings[data.get('localizedTextIdTitle')] or LocalizedStrings[data.get('localizedTextIdName')]

        self.setWindowTitle(title)

        layout = QVBoxLayout(self)
        # Add content
        for stringData in self.createStringList():

            text = LocalizedStrings[data.get(stringData)]

            if text:
                # Create hyperlinks
                if text and '$' in text:
                    text = linkGameObject(text)

                label = QLabel(f'<div>{text}</div>', objectName=stringData)
                label.setWordWrap(True)
                # Handle links
                label.setOpenExternalLinks(False)
                label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                label.linkActivated.connect(self.popup)

                label.setFixedHeight(label.sizeHint().height())

                layout.addWidget(label)

        self.setFixedWidth(400)

        screen = QGuiApplication.primaryScreen().availableGeometry()
        screenCenter = screen.center()

        windowGeo = self.frameGeometry()
        windowGeo.moveCenter(screenCenter)

        self.move(windowGeo.topLeft())

    def popup(self, link):

        modelId = eval(link)['creature2ModelInfoId']
        modelPath = loadManager['Creature2ModelInfo'][modelId]['assetPath'].replace('.m3', '')
        modelName = modelPath.split('\\')[-1]

        scene = trimesh.load(f'{os.path.abspath(os.curdir)}/{settings['gameFiles']}/{modelPath}/{modelName}.gltf'.replace('\\', '/'))
        scene.show()

    def createStringList(self):
        # Datacube
        # [data['localizedTextIdText0%i' % textId] for textId in range(6) if data['localizedTextIdText0' + str(textId)]]

        # Quests
        stringList = ['localizedTextIdText', 'localizedTextIdGiverTextUnknown']

        for i in range(5):
            stringList.append(f'localizedTextIdMoreInfoSay0{i}')
            stringList.append(f'localizedTextIdMoreInfoText0{i}')

        stringList.append('localizedTextIdCompletedSummary')
        # Add objectives
        # for objective in range(6)
        #     ['objective%i' % objective]['localizedTextIdFull']

        # Event
        stringList.append('localizedTextIdEnd')
        # Add objectives
        # 'PublicEventObjective', 'localizedTextId'

        # Challenge
        stringList.append('localizedTextIdAreaRestriction')
        stringList.append('localizedTextIdProgress')

        return stringList
