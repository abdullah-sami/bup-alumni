from django.core.management.base import BaseCommand
from student.models import Batch

class Command(BaseCommand):
    help = 'Setup initial batches and programs'

    def handle(self, *args, **kwargs):
        
        # Create Sample Batches
        batches_data = [
            {'title': 'BBA 1', 'session': '2009-10'},
            {'title': 'BBA 2', 'session': '2010-11'},
            {'title': 'BBA 3', 'session': '2011-12'},
            {'title': 'BBA 4', 'session': '2012-13'},
            {'title': 'BBA 5', 'session': '2013-14'},
            {'title': 'BBA 6', 'session': '2014-15'},
            {'title': 'BBA 7', 'session': '2015-16'},
            {'title': 'BBA 8', 'session': '2016-17'},
            {'title': 'BBA 9', 'session': '2017-18'},
            {'title': 'BBA 10', 'session': '2018-19'},
            {'title': 'BBA 11', 'session': '2019-20'},
            {'title': 'BBA 12', 'session': '2020-21'},
            {'title': 'BBA 13', 'session': '2021-22'},
            {'title': 'BBA 14', 'session': '2022-23'},
            {'title': 'BBA 15', 'session': '2023-24'},
            {'title': 'BBA 16', 'session': '2024-25'},
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