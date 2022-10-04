from django.core.management.base import BaseCommand, CommandError
import csv
from train.models import State, City, Train
from pathlib import Path


class Command(BaseCommand):
    help = 'Store data in the Data Base.'

    def add_arguments(self, parser):
        parser.add_argument('--states', action='store_true', help='Store states in DB.')
        parser.add_argument('--cities', action='store_true', help='Store cities and states in DB.')
        parser.add_argument('--trains', action='store_true', help='Store trains data in DB.')

    def handle(self, *args, **options):
        if not options['cities'] and not options['states'] and not options['trains']:
            self.stdout.write(self.style.ERROR('Please specify either --cities or --states.'))
        if options['states']:
            if Path('data/states.csv').exists():
                with open('data/states.csv') as file:
                    csvfile = csv.reader(file)
                    print("Adding States objects.....")
                    for lines in csvfile:
                        State.objects.create(name=lines[0])
                    print("Finished states...")
            else:
                raise CommandError('No file is found with "states.csv" in data folder.')

        if options['cities']:
            if Path('data/city_states.csv').exists():
                with open('data/city_states.csv') as file:
                    for lines in csv.DictReader(file):
                        print(lines)
                        City.objects.create(name=lines['city'], state=State.objects.get(name=lines['state']))
                    print("Finished cities...")
            else:
                raise CommandError('No file is found with "city_states.csv" in data folder.')

        if options['trains']:
            if Path('data/trains.csv').exists():
                bulk_list = []
                with open('data/trains.csv') as file:
                    for lines in csv.DictReader(file):
                        bulk_list.append(Train(**lines))
                Train.objects.bulk_create(bulk_list)
            else:
                raise CommandError('No file is found with "trains.csv" in data folder.')


