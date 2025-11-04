from django.core.management.base import BaseCommand
from student.models import Batch, Program


class Command(BaseCommand):
    help = 'Setup initial batches and programs'

    def handle(self, *args, **kwargs):
        # Create Programs
        programs_data = [
            {'name': 'bba'},
            {'name': 'mba'},
        ]
        
        for program_data in programs_data:
            program, created = Program.objects.get_or_create(**program_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created program: {program.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Program already exists: {program.name}')
                )

        # Create Sample Batches
        batches_data = [
            {'title': 'GEN1', 'session': '2009-10'},
            {'title': 'GEN2', 'session': '2010-11'},
            {'title': 'GEN3', 'session': '2011-12'},
            {'title': 'GEN4', 'session': '2012-13'},
            {'title': 'GEN5', 'session': '2013-14'},
            {'title': 'GEN6', 'session': '2014-15'},
            {'title': 'GEN7', 'session': '2015-16'},
            {'title': 'GEN8', 'session': '2016-17'},
            {'title': 'GEN9', 'session': '2017-18'},
            {'title': 'GEN10', 'session': '2018-19'},
            {'title': 'GEN11', 'session': '2019-20'},
            {'title': 'GEN12', 'session': '2020-21'},
            {'title': 'GEN13', 'session': '2021-22'},
            {'title': 'GEN14', 'session': '2022-23'},
            {'title': 'GEN15', 'session': '2023-24'},
            {'title': 'GEN16', 'session': '2024-25'},
        ]
        
        for batch_data in batches_data:
            batch, created = Batch.objects.get_or_create(**batch_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created batch: {batch.title} ({batch.session})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Batch already exists: {batch.title} ({batch.session})')
                )

        self.stdout.write(
            self.style.SUCCESS('\nSetup completed successfully!')
        )