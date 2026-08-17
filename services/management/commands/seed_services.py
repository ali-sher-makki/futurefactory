from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import Service

SERVICES_DATA = [
    {'name': 'Website Development', 'icon': '💻', 'order': 1,
     'short_description': 'Full-stack custom websites and web applications.',
     'detail_description': 'Custom web applications, responsive websites, and robust full-stack solutions tailored to your business needs.',
     'features': 'Custom frontend & backend build\nReact, Next.js & Django applications\nAPI integration & databases\nScalable & secure architecture'},
    {'name': 'WordPress Development', 'icon': '🌐', 'order':2,
     'short_description': 'Custom WordPress sites built for speed and performance.',
     'detail_description': 'Custom WordPress themes, plugin integration, Elementor/Gutenberg builds, and performance optimization.',
     'features': 'Custom WordPress themes & plugins\nMobile-first & fast loading\nElementor & Gutenberg builds\nSecurity & speed optimization'},
  
    {'name': 'Lead Generation', 'icon': '🎯', 'order': 3,
     'short_description': 'Qualified prospects, delivered consistently.',
     'detail_description': 'We identify and deliver high-intent leads matched to your ideal customer profile, so your sales team spends time closing instead of searching.',
     'features': 'Ideal customer profile targeting\nVerified contact data\nWeekly delivery cadence\nCRM-ready lead lists'},
    {'name': 'LinkedIn Outreach', 'icon': '🔗', 'order': 4,
     'short_description': 'Connect with decision-makers at scale.',
     'detail_description': 'Personalized connection and messaging sequences that open conversations with the people who actually make buying decisions.',
     'features': 'Personalized message sequences\nDecision-maker targeting\nResponse tracking\nA/B tested messaging'},
    {'name': 'Cold Calling', 'icon': '📞', 'order': 5,
     'short_description': 'Trained callers booking real conversations.',
     'detail_description': 'Experienced callers who represent your brand professionally and turn cold lists into booked conversations.',
     'features': 'Script development\nObjection handling\nCall recording and QA\nDaily call reports'},
    {'name': 'Appointment Setting', 'icon': '📅', 'order': 6,
     'short_description': 'Your calendar, filled with warm meetings.',
     'detail_description': 'We qualify and schedule meetings directly onto your calendar, so you only show up for conversations worth having.',
     'features': 'Calendar integration\nLead qualification\nConfirmation follow-ups\nNo-show reduction'},
    {'name': 'Data Entry', 'icon': '🗂️', 'order': 7,
     'short_description': 'Accurate, structured data, on time.',
     'detail_description': 'Fast, accurate data entry so your systems stay clean and your team stays focused on higher-value work.',
     'features': 'CRM and spreadsheet entry\nQuality checks\nFast turnaround\nConfidential handling'},
    {'name': 'Data Scraping', 'icon': '🕸️', 'order': 8,
     'short_description': 'Clean, structured data, on demand.',
     'detail_description': 'Custom-built scraping pipelines that extract exactly the data you need from the web, formatted and ready to use.',
     'features': 'Custom scraping scripts\nStructured export formats\nScheduled refreshes\nData validation'},
    {'name': 'Email Marketing', 'icon': '📧', 'order': 9,
     'short_description': 'Campaigns that convert, not just send.',
     'detail_description': 'End-to-end email campaigns, from list building to copy to send, built to nurture leads into customers.',
     'features': 'Campaign strategy\nCopywriting and design\nList segmentation\nPerformance reporting'},
    {'name': 'Social Media Marketing', 'icon': '📱', 'order': 10,
     'short_description': 'Consistent presence, real engagement.',
     'detail_description': 'Content and posting strategy that builds your brand presence and keeps your audience engaged across platforms.',
     'features': 'Content calendar\nPlatform-specific strategy\nEngagement management\nMonthly analytics'},
    {'name': 'Meta Ads', 'icon': '📈', 'order': 11,
     'short_description': 'Paid campaigns managed for ROI.',
     'detail_description': 'Facebook and Instagram ad campaigns built, tested, and optimized to bring down cost per lead.',
     'features': 'Campaign setup and targeting\nCreative testing\nBudget optimization\nWeekly performance reports'},
    {'name': 'AI Automation', 'icon': '🤖', 'order': 12,
     'short_description': 'Workflows that run themselves.',
     'detail_description': 'We design automated workflows that connect your tools and handle repetitive tasks, so your team can focus on growth.',
     'features': 'Workflow mapping\nTool integrations\nAI-assisted processes\nOngoing optimization'},
]


class Command(BaseCommand):
    help = 'Seeds the database with Future Factory service offerings'

    def handle(self, *args, **options):
        created_count = 0
        for data in SERVICES_DATA:
            slug = slugify(data['name'])
            obj, created = Service.objects.update_or_create(
                slug=slug,
                defaults={**data, 'is_active': True},
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(SERVICES_DATA)} services ({created_count} created, '
            f'{len(SERVICES_DATA) - created_count} updated).'
        ))