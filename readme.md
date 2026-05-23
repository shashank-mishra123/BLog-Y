# Blogging System

A modern Django blog platform with dynamic articles, real image handling, searchable posts, authenticated commenting, and customizable social links.

## Project Flow

1. `blog_main/views.py` delivers the homepage with featured posts, latest published blog posts, and the about section.
2. `blogs/views.py` handles category filtering, individual blog pages, comment posting, and search results.
3. `blogs/context_processors.py` exposes categories and configured social links globally to templates.
4. `assignments/models.py` stores the About section and social media link records.
5. The frontend uses Bootstrap 5 and a custom `blog.css` stylesheet for a clean modern layout.

## Folder Structure

- `blog_main/` — project settings, main views, URLs, and static assets.
- `blogs/` — blog models, views, templates, category and post logic.
- `assignments/` — settings for About data and social media links.
- `dashboards/` — admin dashboard and content management pages.
- `templates/` — shared page templates and the overall site layout.
- `media/` — uploaded post images.

## Pages and Routes

- `/` — homepage with featured stories and latest articles.
- `/blogs/<slug>/` — individual blog post page with comments.
- `/category/<int:category_id>/` — category page showing posts in that section.
- `/search/` — search results for keywords in titles, summaries, and full post bodies.
- `/login/`, `/register/`, `/logout/` — authentication pages.
- `/dashboard/` — content management and admin dashboard.

## Social Links

Social media icons are now dynamic and only display links configured in the admin panel. Supported platforms include:

- GitHub
- LinkedIn
- Facebook
- Twitter
- Pinterest

Use Django admin to add `SocialLink` records; no placeholder or static footer links are shown.

## Frontend Improvements

- New modern hero section with featured post highlight.
- Latest articles grid showing up to 12 posts.
- Category page updated to a clean card grid for better readability.
- Dynamic social media footer and sidebar sections.
- Smooth reveal animations, hover effects, and a consistent visual style.

## Testing and Validation

Run the following commands in the project root:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver
```

For demo content:

```bash
python manage.py seed_demo_data
```

Then visit `http://127.0.0.1:8000/` to verify the homepage, category pages, social links, and blog details.

## Notes

- Add an `About` entry and `SocialLink` entries through Django admin to enable the about card and follow buttons.
- The site uses dynamic image URLs or uploaded media images for blog post previews.
- The search endpoint orders results by newest posts first.
