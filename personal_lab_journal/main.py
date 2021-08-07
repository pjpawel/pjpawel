#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from gui import Ui_Widget, LoginDialog
import baza
from tabmodel import TabModel


class Zadania(QWidget, Ui_Widget):

    def __init__(self, parent=None):
        super(Zadania, self).__init__(parent)
        self.setupUi(self)

        self.logujBtn.clicked.connect(self.loguj)
        self.koniecBtn.clicked.connect(self.koniec)
        self.dodajBtn.clicked.connect(self.dodaj)
        self.zapiszBtn.clicked.connect(self.zapisz)

    def dodaj(self):
        #Dodawanie nowego zadania
        nazwa, ok = QInputDialog.getMultiLineText(self, 'Nowy eksperyment', 'Podaj nazwę związku')
        
        if not ok:
            return
        elif not nazwa.strip():
            QMessageBox.critical(self, 'Błąd', 'Nazwa nie może być pusta.', QMessageBox.Ok)
            return

        zadanie = baza.dodajZadanie(self.osoba, nazwa)
        model.tabela.append(nazwa)
        model.layoutChanged.emit()
        if len(model.tabela) == 1:
            self.odswiezWidok()

    def zapisz(self):
        baza.zapiszDane(model.tabela)
        model.layoutChanged.emit()

    def loguj(self):
        login, haslo, ok = LoginDialog.getLoginHaslo(self)
        if not ok:
            return

        if not login or not haslo:
            QMessageBox.warning(self, 'Błąd', 'Pusty login lub hasło!', QMessageBox.Ok)
            return

        self.osoba = baza.loguj(login, haslo)
        if self.osoba is None:
            QMessageBox.critical(self, 'Błąd', 
                                 'Błędne hasło!', QMessageBox.Ok)

        zadania = baza.czytajDane(self.osoba)
        model.aktualizuj(zadania)
        model.layoutChanged.emit()
        self.odswiezWidok()
        self.dodajBtn.setEnabled(True)
        self.zapiszBtn.setEnabled(True)

    def odswiezWidok(self):
        self.widok.setModel(model) #pezkazanie modelu do widoku
        self.widok.hideColumn(0) #ukrywanie kolumny id
        self.widok.horizontalHeader().setStretchLastSection(True)
        self.widok.resizeColumnsToContents()


    def koniec(self):
        self.close()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    baza.polacz()
    model = TabModel(baza.pola)
    okno = Zadania()
    okno.show()
    okno.move(350, 200)
    sys.exit(app.exec_())
