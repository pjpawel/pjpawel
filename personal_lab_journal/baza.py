# -*- coding: utf-8 -*-

from peewee import *
from datetime import datetime

baza = SqliteDatabase('adresy.db')


class BazaModel(Model):  # klasa bazowa

    class Meta:
        database = baza


class Osoba(BazaModel):
    login = CharField(null=False, unique=True)
    haslo = CharField()

    class Meta:
        order_by = ('login',)


class Zadanie(BazaModel):
    nazwa = TextField(null=False)
    otrzymywanie = TextField(null=True)
    widmo = TextField(null=True)
    datad = DateTimeField(default=datetime.now)
    wykonane = BooleanField(default=False)
    osoba = ForeignKeyField(Osoba, related_name='zadania')

    class Meta:
        order_by = ('datad',)


def polacz():
    baza.connect()  # nawiązujemy połączenie z bazą
    baza.create_tables([Osoba, Zadanie], safe = True)  # tworzymy tabele
    ladujDane()  # wstawiamy początkowe dane
    return True


def loguj(login, haslo):
    try:
        osoba, created = Osoba.get_or_create(login=login, haslo=haslo)
        return osoba
    except IntegrityError:
        return None


def ladujDane():
    """ Przygotowanie początkowych danych testowych """
    if Osoba.select().count() > 0:
        return
    osoby = ('adam', 'ewa')
    nazwy = ('Anilina', 'p-nitrofenol', 'tlenek glinu')
    otrzymywanie = 'brak'
    widmo = 'brak'
    for login in osoby:
        o = Osoba(login=login, haslo='123')
        o.save()
        for tresc in nazwy:
            z = Zadanie(nazwa=tresc, osoba=o, otrzymywanie=otrzymywanie, widmo=widmo)
            z.save()
    baza.commit()
    baza.close()

def czytajDane(osoba):
    """ Pobranie zadań danego użytkownika z bazy """
    zadania = []  # lista zadań
    wpisy = Zadanie.select().where(Zadanie.osoba == osoba)
    for z in wpisy:
        zadania.append([
            z.id,  # identyfikator zadania
            z.nazwa, #nazwa (numer) otrzymywanego związku
            z.otrzymywanie,  #opis otrzymywania
            z.widmo, #widmo NMR
            '{0:%Y-%m-%d %H:%M:%S}'.format(z.datad),  # data dodania
            z.wykonane,  # bool: czy wykonane?
            False])  # bool: czy usunąć?
    return zadania

def dodajZadanie(osoba, nazwa, otrzymywanie):
    #Dodawanie nowego zadania
    zadanie = Zadanie(nazwa = nazwa, osoba = osoba, otrzymywanie = otrzymywanie, widmo = "brak")
    zadanie.save()
    return [
        zadanie.id,
        zadanie.nazwa,
        zadanie.otrzymywanie,
        zadanie.widmo,
        '{0:%Y-%m-%d %H:%M:%S}'.format(zadanie.datad),
        zadanie.wykonane,
        False]

def zapiszDane(zadania):
    #Zapisywanie zmian
    for i, z in enumerate(zadania):
        # utworzenie instancji zadania
        zadanie = Zadanie.select().where(Zadanie.id == z[0]).get()
        if z[6]:  # jeżeli zaznaczono zadanie do usunięcia
            zadanie.delete_instance()  # usunięcie zadania z bazy
            del zadania[i]  # usunięcie zadania z danych modelu
        else:
            zadanie.nazwa = z[1]
            zadanie.otrzymywanie = z[2]
            zadanie.widmo = z[3]
            zadanie.wykonane = z[5]
            zadanie.save()

pola = ['Id', 'Nazwa', 'Otrzymywanie', 'Widmo NMR', 'Dodano', 'Zrobione', 'Usuń']
