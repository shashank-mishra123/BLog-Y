from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from blogs.models import Category, Blog
from django.utils.text import slugify
import os
import urllib.request
import random


class Command(BaseCommand):
    help = 'Seed demo categories and blog posts with images (for development only)'

    def handle(self, *args, **options):
        # Ensure media demo path exists
        media_demo_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'demo')
        os.makedirs(media_demo_path, exist_ok=True)

        # Create demo user
        username = 'shashank'
        user, created = User.objects.get_or_create(username=username, defaults={
            'email': 'shashank@example.com'
        })
        if created:
            user.set_password('shashank')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))

        # Demo categories and image pools (Unsplash sample images)
        demo_categories = [
            ('Technology', [
                'https://images.unsplash.com/photo-1518779578993-ec3579fee39f',
                'https://images.unsplash.com/photo-1519389950473-47ba0277781c',
                'https://images.unsplash.com/photo-1498050108023-c5249f4df085'
            ]),
            ('Health', [
                'https://images.unsplash.com/photo-1532938911075-1b06ac7ceec7',
                'https://images.unsplash.com/photo-1496318447583-f524534e9ce1',
                'https://images.unsplash.com/photo-1516251193007-45ef944ab0c6'
            ]),
            ('Business', [
                'https://images.unsplash.com/photo-1454165205744-3b78555e5572',
                'https://images.unsplash.com/photo-1507679799987-c73779587ccf',
                'https://images.unsplash.com/photo-1542223616-56f6f5f7f7d4'
            ]),
            ('Lifestyle', [
                'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
                'https://images.unsplash.com/photo-1499955085172-a104c9463ece',
                'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb'
            ]),
            ('Travel', [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e',
                'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa',
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee'
            ]),
            ('Education', [
                'https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d',
                'https://images.unsplash.com/photo-1516979187457-637abb4f9353',
                'https://images.unsplash.com/photo-1523240795612-9a054b0db644'
            ])
        ]

        # Helper to download image bytes
        def download_image(url):
            try:
                # Append parameters to get reasonable size
                if '?' not in url:
                    url = url + '?auto=format&fit=crop&w=1200&q=80'
                resp = urllib.request.urlopen(url, timeout=20)
                return resp.read()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Failed to download {url}: {e}'))
                return None

        total_created = 0
        for cat_index, (cat_name, images) in enumerate(demo_categories, start=1):
            category, _ = Category.objects.get_or_create(category_name=cat_name)
            self.stdout.write(self.style.SUCCESS(f'Using category: {cat_name}'))

            # Create 10 posts per category
            for i in range(1, 11):
                title = f"{cat_name} Insights #{i}"
                slug = slugify(f"{title}-{cat_index}-{i}")
                # Ensure unique slug
                orig_slug = slug
                suffix = 1
                while Blog.objects.filter(slug=slug).exists():
                    slug = f"{orig_slug}-{suffix}"
                    suffix += 1

                short_description = f"An in-depth look at {cat_name.lower()} topic number {i}. Learn trends, best practices, and practical tips."
                blog_body = (
                    f"<p>{cat_name} post #{i} — This article explores the subject in detail. "
                    "It includes practical examples, case studies, and recommended next steps for practitioners and enthusiasts.</p>"
                    "<p>Continue reading for more insights and resources.</p>"
                )

                # Choose an image
                img_url = random.choice(images)
                img_bytes = download_image(img_url)

                blog = Blog(
                    title=title,
                    slug=slug,
                    category=category,
                    author=user,
                    short_description=short_description,
                    blog_body=blog_body,
                    status='Published',
                    is_featured=(i == 1)
                )

                if img_bytes:
                    filename = f"demo_{cat_name.lower()}_{i}.jpg"
                    # Save to ImageField
                    blog.featured_image.save(filename, ContentFile(img_bytes), save=False)
                else:
                    self.stdout.write(self.style.WARNING(f'Image not available for {title}, skipping image.'))

                blog.save()
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {total_created} demo posts.'))
        self.stdout.write(self.style.NOTICE('Run `python manage.py runserver` and visit the site.'))